# encoding=utf-8
"""
@File    :   hidden_surface_control_utils.py
@Time    :   2026/01/13 15:56:56
@Author  :   Ran Zhang
@Email   :   ranzhang@qti.qualcomm.com
"""

import os
import sys
sys.path.append("\\".join(os.path.abspath(__file__).split("\\")[:-2]))
import subprocess
import re
import shutil
import pygetwindow as gw
import win32gui
import win32con
import datetime
import yaml
import threading
from pathlib import Path
from dotenv import load_dotenv
from time import sleep

load_dotenv()
SCRCPY_PATH = os.getenv("SCRCPY_PATH")
VIRTUAL_DISPLAY_NAME = "HiddenSurfaceControl"

class VirtualDisplayUtils:
    def __init__(self):
        self.log_folder = ""
        # adb logcat
        self.adb_log_process = None
        self.adb_log_thread = False
        self.logcat_file = None

    def update_log_folder(self):
        self.log_folder = f"running_log/server_log/os-copilot-local-eval-logs/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")}"
        return self.log_folder

    def start_adb_log(self, device_id=None):
        """
        cmd:
            'adb -s 11111 shell "logcat -b all"'
            'adb -s 11111 shell "logcat | grep -E \'WeatherDS|NavigationDomainService|music_debug_tag|PluginManager|Qaior\'"'
        """
        self.adb_log_thread = False
        def _log_thread():
            try:
                self.adb_log_process = subprocess.Popen(f'adb -s {device_id} shell "logcat -b all"', stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
                timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                self.logcat_file = Path(self.log_folder) / f"logcat_{timestamp}.log"
                with open(self.logcat_file, "w", encoding="utf-8") as file:
                    while not self.adb_log_thread:
                        line_bytes = self.adb_log_process.stdout.readline()
                        if not line_bytes:
                            continue
                        try:
                            line = line_bytes.decode("utf-8")
                        except UnicodeDecodeError:
                            try:
                                line = line_bytes.decode()
                            except UnicodeDecodeError:
                                continue
                        file.write(line.rstrip("\n"))
                print(f"Started adb logcat to: {self.logcat_file}")
            except Exception:
                print(f"Exception in: {sys._getframe().f_code.co_name}")
            finally:
                pass

        self.log_thread = threading.Thread(target=_log_thread)
        self.log_thread.start()

    def stop_adb_log(self):
        try:
            self.adb_log_thread = True
            self.adb_log_process.terminate()
            self.adb_log_process.wait()
            self.adb_log_process = None
            self.log_thread.join()  # Wait for the logging thread to finish
            sleep(3)  # Ensure the recording process has completely stopped
            print(f"Stopped adb logcat to: {self.logcat_file}")
        except Exception:
            print(f"Exception in: {sys._getframe().f_code.co_name}")
        finally:
            pass

    def start_hidden_app(self, device_id=None, name=""):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_APP_LAUNCH --es target_component \"{name}\""
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def start_mirror_activity(self, device_id=None):
        cmd = f"adb -s {device_id} shell am start -n com.qualcomm.mobile.virtualdisplaydemo/.MirrorActivity"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def take_screenshot(self, device_id=None):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_CAPTURE"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def touch_hidden_app(self, device_id=None, x=None, y=None):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_TOUCH --es coordinates {int(x)}:{int(y)}"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def android_shell_quote(self, s: str) -> str:
        return "'" + s.replace("'", "'\"'\"'") + "'"

    def text_hidden_app(self, device_id=None, text=""):
        quoted = self.android_shell_quote(text)
        cmd = [
            "adb", "-s", device_id, "shell", "am", "start-foreground-service",
            "-a", "qualcomm.intent.action.VIRTUAL_DISPLAY_TEXT_INPUT",
            "--es", "text", quoted
        ]
        subprocess.run(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def scroll_hidden_app(self, device_id=None, startX=None, startY=None, endX=None, endY=None, steps=None, delayMs=None):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_SCROLL --es scroll {int(startX)}:{int(startY)}:{int(endX)}:{int(endY)}:{int(steps)}:{int(delayMs)}"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def send_back_key(self, device_id=None):
        subprocess.check_output(f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_KEY_EVENT --es key_event back", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

    def send_home_key(self, device_id=None):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_KEY_EVENT --es key_event back_to_home"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def stop_virtual_display_service(self, device_id=None):
        cmd = f"adb -s {device_id} shell am start-foreground-service -a qualcomm.intent.action.VIRTUAL_DISPLAY_EXIT"
        subprocess.check_output(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return cmd

    def open_physical_display(self, device_id=None, log_folder="."):
        """
        screen_record_folder example: C:\\PathLink-Eurus\\APT\\AIOR\\Temp\\virtual.mp4
        """
        subprocess.Popen(
            [
                SCRCPY_PATH,
                f"--serial={device_id}",
                "--display-id=0",
                "--window-x=100",
                "--window-y=80",
                "--window-title=Projection for Physical Display",
                "--no-clipboard-autosync",
                f"--record={log_folder}\\physical_display.mp4",
                "--record-format=mp4",
            ]
        )

    def open_virtual_display(self, device_id=None, log_folder="."):
        # Get the virtual display ID by parsing dumpsys display output
        """
        screen_record_folder example: C:\\PathLink-Eurus\\APT\\AIOR\\Temp\\virtual.mp4
        """
        try:
            # Get display info from adb
            result = subprocess.check_output(f"adb -s {device_id} shell dumpsys display", shell=True, text=True, encoding="utf-8", creationflags=subprocess.CREATE_NO_WINDOW)
            pattern = re.compile(r'DisplayInfo\{"([^"]+)"[^}]*displayId\s*=?\s*(\d+)')
            found = False
            for name, did in pattern.findall(result):
                if name == VIRTUAL_DISPLAY_NAME:
                    virtual_display_id = did
                    print(f"[HiddenSurfaceControl] Virtual Display ID: {did}")
                    found = True
                    # Launch scrcpy with the virtual display ID
                    subprocess.Popen(
                        [
                            SCRCPY_PATH,
                            f"--serial={device_id}",
                            f"--display-id={virtual_display_id}",
                            "--window-x=1000",
                            "--window-y=80",
                            "--window-title=Projection for Virtual Display",
                            "--no-clipboard-autosync",
                            f"--record={log_folder}\\virtual_display.mp4",
                            "--record-format=mp4",
                        ]
                    )
                    return True
            if not found:
                print(f"[HiddenSurfaceControl] No display found with name {VIRTUAL_DISPLAY_NAME}")
                return False
        except Exception as e:
            print(f"[HiddenSurfaceControl] Error opening virtual display: {e}")
            return False

    def taskkill_consoles(self, console_name="Projection for Virtual Display"):
        try:
            while True:
                windows = gw.getAllTitles()
                target_windows = [title for title in windows if title.startswith(console_name)]

                if target_windows:
                    print(f"[HiddenSurfaceControl] Detected {len(target_windows)} target window(s), attempting to close them...")
                    for title in target_windows:
                        def enum_callback(hwnd, _):
                            if win32gui.IsWindowVisible(hwnd):
                                window_title = win32gui.GetWindowText(hwnd)
                                if window_title.startswith(console_name):
                                    try:
                                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                                        print(f"[HiddenSurfaceControl] Sent WM_CLOSE to window: {window_title}")
                                    except Exception as e:
                                        print(f"[HiddenSurfaceControl] Failed to close window '{window_title}': {e}")
                        win32gui.EnumWindows(enum_callback, None)
                else:
                    print("[HiddenSurfaceControl] Target consoles are all killed!")
                    break
                sleep(1)
        except Exception:
            print(f"[HiddenSurfaceControl] Exception in: {sys._getframe().f_code.co_name}")
        finally:
            return

vdu = VirtualDisplayUtils()

config_file = f"{os.getcwd()}//config.yaml"
with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

mirror_display_switch = config.get("mirror_display_switch", False)

if __name__ == "__main__":
    adb_id="9deb5ba5"
    log_path = f"{os.path.dirname(os.path.abspath(__file__))}\\tmp"
    if os.path.exists(log_path):
        shutil.rmtree(log_path)
    os.makedirs(log_path)

    virtual_app = "com.taobao.taobao/com.taobao.tao.welcome.Welcome"
    # physical_app = "com.android.launcher3/com.android.launcher3.uioverrides.QuickstepLauncher"
    subprocess.check_output(f"adb -s {adb_id} root", creationflags=subprocess.CREATE_NO_WINDOW)
    subprocess.check_output(f"adb -s {adb_id} shell rm -f /data/user/0/com.qualcomm.mobile.virtualdisplaydemo/cache/snapshot*.png", creationflags=subprocess.CREATE_NO_WINDOW)

    # stop virtual display service additionally in cases of last failure abort
    vdu.stop_virtual_display_service(device_id=adb_id)

    # # launch physical app
    # subprocess.check_output(f"adb -s {adb_id} shell am start --display 0 -n {physical_app}")
    # sleep(3)
    # # scrcpy physical display
    # vdu.open_physical_display(device_id=adb_id, log_folder=log_path)
    # sleep(3)

    # launch virtual app
    vdu.start_hidden_app(device_id=adb_id, name=virtual_app)
    sleep(3)
    # scrcpy virtual display
    vdu.open_virtual_display(device_id=adb_id, log_folder=log_path)
    sleep(3)

    # mirror virtual display to physical screen
    vdu.start_mirror_activity(device_id=adb_id)
    sleep(3)

    while True:
        cmd = input("Wait for your command: ")
        if cmd == "y":
            # screenshot for virtual display
            vdu.take_screenshot(device_id=adb_id)
            sleep(3)
            # pull virtual display screenshots to local path
            subprocess.check_output(f"adb -s {adb_id} pull /data/user/0/com.qualcomm.mobile.virtualdisplaydemo/cache {log_path}", creationflags=subprocess.CREATE_NO_WINDOW)
        elif cmd == "n":
            break

    # stop virtual display service
    vdu.stop_virtual_display_service(device_id=adb_id)
    # stop app on physical display
    subprocess.check_output(f"adb -s {adb_id} shell am force-stop {virtual_app}", creationflags=subprocess.CREATE_NO_WINDOW)
