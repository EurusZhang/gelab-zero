#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: How to call and control GelabZeroTaskRunner from Python

This script provides a simple API to control the GUI application through file-based IPC.
"""

import subprocess
import time
import json
from pathlib import Path


class GUIController:
    """Simple file-based controller for GUI application"""
    
    def __init__(self):
        self.control_dir = Path("tmp_gui_control")
        self.control_dir.mkdir(exist_ok=True)
        
        self.command_file = self.control_dir / "command.json"
        self.response_file = self.control_dir / "response.json"
        self.log_file = self.control_dir / "current_log.txt"
        
    def send_command(self, command, params=None, timeout=5):
        """Send a command to the GUI application"""
        if self.response_file.exists():
            self.response_file.unlink()
        
        cmd_data = {
            "command": command,
            "params": params or {},
            "timestamp": time.time()
        }
        
        with open(self.command_file, 'w', encoding='utf-8') as f:
            json.dump(cmd_data, f)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.response_file.exists():
                try:
                    with open(self.response_file, 'r', encoding='utf-8') as f:
                        response = json.load(f)
                    print(f"Response: {response}")
                    self.response_file.unlink()
                    return response
                except:
                    pass
            time.sleep(0.1)
        
        return None
    
    def set_task(self, task):
        """Set the task in the task entry field"""
        return self.send_command("set_task", {"task": task})
    
    def start_task(self, task=None):
        """Start task execution"""
        params = {"task": task} if task else {}
        return self.send_command("start", params)
    
    def stop_task(self):
        """Stop the currently running task"""
        return self.send_command("stop")
    
    def clear_logs(self):
        """Clear the log display"""
        return self.send_command("clear_logs")
    
    def save_logs(self, filepath=None):
        """Save logs to a file"""
        params = {"filepath": filepath} if filepath else {}
        return self.send_command("save_logs", params)
    
    def get_logs(self):
        """Get current log content"""
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def close_window(self):
        """Close the GUI window"""
        return self.send_command("close")
    
    def cleanup(self):
        """Clean up control files"""
        for f in [self.command_file, self.response_file, self.log_file]:
            if f.exists():
                f.unlink()


def main():
    """Usage example"""
    exe_path = Path("dist/GelabZeroTaskRunner.exe")
    cmd = [str(exe_path)]
    
    print("=== Gelab Zero Task Runner Controller ===")

    while True:
        user_input = input("Enter your command: ")
        if user_input == "launch_gui":
            # Launch GUI
            print("Launching GUI...")
            process = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(3)
            # Create controller
            controller = GUIController()
        elif user_input == "set_task":
            # Set task
            print("Setting task...")
            task = input("Input your task: ")
            controller.set_task(task)
            time.sleep(1)
        elif user_input == "start_task":
            # Start task
            print("Starting task...")
            controller.start_task()
            time.sleep(5)
        elif user_input == "stop_task":
            # Stop task
            print("Stopping task...")
            controller.stop_task()
            time.sleep(2)
        elif user_input == "set_start_task":
            # Set and Start task
            print("Setting and Starting task...")
            task = input("Input your task: ")
            controller.start_task(task=task)
            time.sleep(5)
        elif user_input == "clear_log":
            # Clear logs
            print("Clearing logs...")
            controller.clear_logs()
            time.sleep(1)
        elif user_input == "save_log":
            # Save logs
            print("Saving logs...")
            controller.save_logs(filepath="gui_logs.txt")
            time.sleep(1)
        elif user_input == "close_gui":
            # Close gui
            print("Closing gui...")
            controller.close_window()
            process.wait(timeout=10)
        elif user_input == "clean_up":
            # Cleanup
            controller.cleanup()
            print("Done!")
        elif user_input == "exit":
            break

if __name__ == "__main__":
    main()
