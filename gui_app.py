import sys
import os
import threading
import queue
import time
import yaml
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from pathlib import Path

# Add current directory to path
if "." not in sys.path:
    sys.path.append(".")

from copilot_agent_client.pu_client import evaluate_task_on_device
from copilot_front_end.mobile_action_helper import list_devices, get_device_wm_size
from copilot_agent_server.local_server import LocalServer
from copilot_front_end.hidden_surface_control_utils import log_folder
import subprocess

# Global stop flag
stop_flag = threading.Event()

class TextRedirector:
    """Redirect stdout/stderr to GUI text widget"""
    def __init__(self, text_widget, log_queue):
        self.text_widget = text_widget
        self.log_queue = log_queue
        
    def write(self, string):
        # Don't strip - preserve all whitespace including newlines
        if string:
            self.log_queue.put(string)
    
    def flush(self):
        pass

class InputRedirector:
    """Redirect stdin to GUI text widget for input() support"""
    def __init__(self, text_widget, log_queue):
        self.text_widget = text_widget
        self.log_queue = log_queue
        self.input_queue = queue.Queue()
        self.waiting_for_input = False
        
    def readline(self):
        """Read a line of input from the GUI"""
        self.waiting_for_input = True
        # Signal the GUI that we need input
        self.log_queue.put(("INPUT_REQUEST", None))
        # Wait for user input
        result = self.input_queue.get()
        self.waiting_for_input = False
        return result + '\n'
    
    def read(self, size=-1):
        """Read input (delegates to readline)"""
        return self.readline()
    
    def write(self, string):
        """Dummy write method for compatibility"""
        pass
    
    def flush(self):
        """Dummy flush method for compatibility"""
        pass
    
    def isatty(self):
        """Return True to indicate this is a terminal-like interface"""
        return True
    
    def readable(self):
        """Return True to indicate this stream is readable"""
        return True
    
    def writable(self):
        """Return False to indicate this stream is not writable"""
        return False

class GelabZeroGUI:
    def __init__(self, root, auto_start_task=None):
        self.root = root
        self.root.title("Gelab Zero Task Runner")
        self.root.geometry("1200x800")
        
        # Auto-start configuration
        self.auto_start_task = auto_start_task
        self.auto_close_on_completion = auto_start_task is not None
        
        # Config file path
        self.config_file = f"{os.getcwd()}//config.yaml"
        
        # Load config from file
        self.config = self.load_config()
        
        # Log queue for thread-safe logging
        self.log_queue = queue.Queue()
        
        # Task execution thread
        self.task_thread = None
        self.is_running = False
        
        # Input handling
        self.input_redirector = None
        self.waiting_for_input = False
        self.input_start_pos = None
        
        # Setup UI
        self.setup_ui()
        
        # Start log update loop
        self.update_logs()
        
        # Auto-start task if provided
        if self.auto_start_task:
            self.root.after(1000, self.auto_start)  # Start after 1 second to allow UI to initialize
    
    def load_config(self):
        """Load configuration from config.yaml file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config:
                        return config
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to load config.yaml: {e}")
        
        return {}
    
    def setup_ui(self):
        """Setup the GUI layout"""
        # Top frame for task input
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)
        
        # Task prompt label and entry
        ttk.Label(top_frame, text="Task Prompt:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.task_entry = ttk.Entry(top_frame, width=60, font=("Arial", 10))
        self.task_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.task_entry.insert(0, "打开淘宝，搜索苹果手机，加入购物车。")

        # Buttons
        self.start_button = tk.Button(top_frame, text="Start", bg="#4CAF50", fg="white", 
                                      font=("Arial", 10, "bold"), width=10, command=self.start_task)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(top_frame, text="Stop", bg="#f44336", fg="white",
                                     font=("Arial", 10, "bold"), width=10, command=self.stop_task,
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Logs frame
        logs_frame = ttk.Frame(self.root)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Log text area - white background, read-only by default
        self.log_text = scrolledtext.ScrolledText(logs_frame, wrap=tk.WORD, 
                                                   font=("Consolas", 9), bg="white", fg="black",
                                                   state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind keys for input handling
        self.log_text.bind("<Return>", self.on_enter_key)
        self.log_text.bind("<Key>", self.on_key_press)
        
        # Bottom frame for log controls
        log_control_frame = ttk.Frame(logs_frame)
        log_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(log_control_frame, text="Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(log_control_frame, text="Save Logs", command=self.save_logs).pack(side=tk.LEFT, padx=5)
        
        # Enable temporarily to insert initial text
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, "=== Gelab Zero Task Runner ===\n")
        self.log_text.insert(tk.END, "Ready to execute tasks.\n\n")
        self.log_text.config(state=tk.DISABLED)
    
    def log(self, message):
        """Add message to log queue"""
        self.log_queue.put(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
    
    def update_logs(self):
        """Update log text widget from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                
                # Handle special input request message
                if isinstance(message, tuple) and message[0] == "INPUT_REQUEST":
                    self.waiting_for_input = True
                    # Enable text widget for input
                    self.log_text.config(state=tk.NORMAL)
                    # Mark the start position for input
                    self.input_start_pos = self.log_text.index(tk.END + "-1c")
                    # Focus on the text widget
                    self.log_text.focus_set()
                    continue
                
                # Handle normal log messages
                # Enable text widget temporarily to insert message
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, message)
                self.log_text.see(tk.END)
                
                # Disable text widget if not waiting for input
                if not self.waiting_for_input:
                    self.log_text.config(state=tk.DISABLED)
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.update_logs)
    
    def clear_logs(self):
        """Clear the log text area"""
        # Enable temporarily to clear and add message
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("Logs cleared.")
    
    def save_logs(self):
        """Save logs to a file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"gelab_zero_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Logs saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save logs: {e}")
    
    def on_key_press(self, event):
        """Handle key press events in log window"""
        # Allow input only when waiting for input
        if not self.waiting_for_input:
            # Block all editing keys except copy operations
            if event.keysym in ('c', 'C') and (event.state & 0x4):  # Ctrl+C
                return  # Allow copy
            return "break"  # Block all other keys
        
        # When waiting for input, restrict editing to only the input line
        current_pos = self.log_text.index(tk.INSERT)
        
        # For navigation keys, restrict cursor movement
        if event.keysym in ('Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Prior', 'Next'):
            # For Left arrow and Home, don't allow moving before input start
            if event.keysym in ('Left', 'Home', 'Up', 'Prior'):
                if self.log_text.compare(current_pos, "<=", self.input_start_pos):
                    return "break"  # Block movement before input start
            return None  # Allow other navigation
        
        # For backspace/delete operations
        if event.keysym in ('BackSpace', 'Delete'):
            # Block deletion if cursor is at or before input start position
            if self.log_text.compare(current_pos, "<=", self.input_start_pos):
                return "break"  # Block deletion of existing content
        
        # For typing and other keys
        else:
            # Only allow operations if cursor is at or after input start position
            if self.log_text.compare(current_pos, "<", self.input_start_pos):
                # Move cursor to input start position
                self.log_text.mark_set(tk.INSERT, self.input_start_pos)
        
        # Allow the key press
        return None
    
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not self.waiting_for_input:
            return "break"  # Block Enter when not waiting for input
        
        # Get the input text from input_start_pos to end
        user_input = self.log_text.get(self.input_start_pos, tk.END).strip()
        
        # Send input to the input redirector
        if self.input_redirector:
            self.input_redirector.input_queue.put(user_input)
        
        # Add newline to log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, "\n")
        self.log_text.config(state=tk.DISABLED)
        
        # Reset input state
        self.waiting_for_input = False
        self.input_start_pos = None
        
        return "break"  # Prevent default Enter behavior
    
    def start_task(self):
        """Start task execution"""
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task prompt!")
            return
        
        if self.is_running:
            messagebox.showwarning("Warning", "A task is already running!")
            return
        
        # Reset stop flag
        stop_flag.clear()
        
        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.is_running = True
        
        # Start task in separate thread
        self.task_thread = threading.Thread(target=self.run_task, args=(task,), daemon=True)
        self.task_thread.start()
    
    def stop_task(self):
        """Stop task execution"""
        if messagebox.askyesno("Confirm", "Are you sure you want to stop the task?"):
            stop_flag.set()
            self.log("Stop signal sent. Waiting for agent to finish current step...")
            self.stop_button.config(state=tk.DISABLED)
    
    def run_task(self, task):
        """Run the task (executed in separate thread)"""
        try:
            self.log(f"Starting task: {task}")
            self.log("=" * 60)
            
            # Get device info
            devices = list_devices()
            if not devices:
                self.log("ERROR: No devices found! Please connect an Android device.")
                return
            
            device_id = devices[0]
            self.log(f"Using device: {device_id}")
            
            device_wm_size = get_device_wm_size(device_id)
            device_info = {
                "device_id": device_id,
                "device_wm_size": device_wm_size
            }
            
            # Root device
            try:
                subprocess.check_output(f"adb -s {device_id} root", shell=True, 
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                self.log("Device rooted successfully")
            except Exception as e:
                self.log(f"Warning: Failed to root device: {e}")
            
            # Setup server config
            tmp_server_config = {
                "log_dir": f"{log_folder}/traces",
                "image_dir": f"{log_folder}/images",
                "debug": False
            }

            # Setup rollout config from config.yaml
            tmp_rollout_config = self.config["rollout_config"]
            tmp_rollout_config["task_type"] = "parser_0922_summary"

            # Create server
            l2_server = LocalServer(tmp_server_config)
            
            # Wrap automate_step to check stop flag
            original_automate_step = l2_server.automate_step
            
            def wrapped_automate_step(payload):
                if stop_flag.is_set():
                    self.log("Stop flag detected, returning STOP action")
                    return {
                        "action": {
                            "action_type": "ABORT",
                            "value": "User requested stop"
                        },
                        "current_step": payload.get("current_step", 0)
                    }
                return original_automate_step(payload)
            
            l2_server.automate_step = wrapped_automate_step
            
            # Execute task
            start_time = time.time()
            
            # Redirect stdout, stderr and stdin
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            old_stdin = sys.stdin
            
            # Create redirectors
            text_redirector = TextRedirector(self.log_text, self.log_queue)
            sys.stdout = text_redirector
            sys.stderr = text_redirector  # Also redirect stderr to prevent "lost sys.stderr" error
            
            # Create input redirector
            self.input_redirector = InputRedirector(self.log_text, self.log_queue)
            sys.stdin = self.input_redirector
            
            try:
                result = evaluate_task_on_device(
                    l2_server, device_info, task, tmp_rollout_config, 
                    reflush_app=True, auto_reply=False
                )
                
                total_time = time.time() - start_time
                
                self.log("=" * 60)
                self.log(f"Task completed in {total_time:.2f} seconds")
                self.log(f"Stop reason: {result.get('stop_reason', 'UNKNOWN')}")
                self.log(f"Total steps: {result.get('stop_steps', 0)}")
                
            finally:
                # Restore original streams
                sys.stdout = old_stdout
                sys.stderr = old_stderr
                sys.stdin = old_stdin
                self.input_redirector = None
            
        except Exception as e:
            self.log(f"ERROR: {str(e)}")
            import traceback
            self.log(traceback.format_exc())
        
        finally:
            # Update UI
            self.root.after(0, self.task_finished)
    
    def auto_start(self):
        """Auto-start the task if provided"""
        if self.auto_start_task:
            # Set the task in the entry field
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, self.auto_start_task)
            self.log(f"Auto-starting task: {self.auto_start_task}")
            # Start the task
            self.start_task()
    
    def task_finished(self):
        """Called when task finishes"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Ready for next task.")
        
        # Auto-close if this was an auto-started task
        if self.auto_close_on_completion:
            self.log("Task completed. Auto-closing in 3 seconds...")
            self.root.after(3000, self.auto_close)  # Close after 3 seconds
    
    def auto_close(self):
        """Auto-close the application"""
        self.log("Auto-closing application...")
        self.root.quit()
        self.root.destroy()

def main():
    # Check if task is provided as command-line argument
    if len(sys.argv) > 1:
        # Check for GUI mode with auto-start
        if len(sys.argv) > 2 and sys.argv[2] == "--gui-auto":
            # GUI mode with auto-start
            task = sys.argv[1]
            root = tk.Tk()
            app = GelabZeroGUI(root, auto_start_task=task)
            root.mainloop()
        else:
            # Invalid usage - only support GUI modes
            print("Error: Only GUI modes are supported.")
            print("Usage:")
            print("  python gui_app.py                    # GUI mode")
            print("  python gui_app.py <task> --gui-auto  # GUI auto-start mode")
            sys.exit(1)
    else:
        # GUI mode
        root = tk.Tk()
        app = GelabZeroGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main()
