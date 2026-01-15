#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: How to call GelabZeroTaskRunner.exe from Python

This script demonstrates GUI auto-start mode:
GUI Auto Mode - Pass task parameter, automatically start and execute, then auto-close when complete
"""

import subprocess
from pathlib import Path

def call_exe_gui_auto_mode(exe_path, task):
    """
    Call exe in GUI auto-start mode
    Pass task parameter, GUI interface automatically starts and executes task, then auto-closes when complete
    
    Args:
        exe_path: Path to the exe file
        task: Task description string
    
    Returns:
        subprocess.Popen object for monitoring process status
    """
    print(f"Starting GUI auto mode, task: {task}")
    try:
        process = subprocess.Popen([exe_path, task, "--gui-auto"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True,
                                 creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"GUI auto mode process started, PID: {process.pid}")
        print("GUI interface opened, task will start automatically...")
        print("Window will auto-close when task completes")
        return process
    except Exception as e:
        print(f"Failed to start GUI auto mode: {e}")
        return None

def main():
    """Usage example"""
    # exe file path
    exe_path = Path("dist/GelabZeroTaskRunner.exe")
    
    if not exe_path.exists():
        print(f"Error: Cannot find exe file {exe_path}")
        print("Please ensure you have successfully packaged with PyInstaller")
        return
    
    print("=== Gelab Zero Task Runner Call Example ===\n")
    
    # GUI auto mode example
    print("GUI Auto Mode Example:")
    task = "Open Notepad"
    process = call_exe_gui_auto_mode(str(exe_path), task)
    if process:
        print("GUI auto mode started, you can continue executing other code...")
        print("If you need to wait for task completion, use: process.wait()")
        
        # Example: Wait for task completion
        # process.wait()
        # print("Task execution completed")

if __name__ == "__main__":
    main()
