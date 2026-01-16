# Features

- Full mobile UI agent capabilities powered by GELab‑Zero
- Integrated Hidden Surface Control functionality
- Standalone GUI tool: GelabZeroTaskRunner.exe for user‑friendly operation
- Python integration via gui_control.py to control GelabZeroTaskRunner.exe from your project
- Configurable parameters through config.yaml
- Support for ADB logcat logging and screen recording

# Setup

- Install HiddenSurfaceControl APK
  - `adb root`
  - `adb remount`
  - `adb push HiddenSurfaceControl.apk /vendor/app`
  - `adb reboot`
- Add the path to scrcpy.exe to your PC’s System Variables (without quotes) and name the variable SCRCPY_PATH.
- Add ADB tool path into system variable "Path".
- How to enable typing on device
  - `adb push yadb /data/local/tmp/`
  - `adb install -r ADBKeyboard.apk`
  - Enable adbkeyboard in device Setting
  - `adb reboot`

# Attentions

- If `mirror_display_switch` is set to True, do NOT open the same app on the physical display while it is running on the virtual display. Doing so will cause the app to switch repeatedly between the physical and virtual displays, disrupting the agent’s workflow.

# Known Issues

- Currently supported only on Kaanapali 1.0 META devices with root access. Support for Kaanapali 2.0 may be added in the future.
- When the virtual display is mirrored to the physical screen, do NOT tap HOME, BACK, or MULTI‑TASK buttons. Due to a known issue in the HiddenSurfaceControl APK, this may cause the virtual display service to exit unexpectedly.
- Taobao
  - Fails to slide the verification slider.
  - Fails to enter (via paste) the verification code.
- Jingdong (JD)
  - Login requires face recognition, blocking automated login.
  - The agent repeatedly taps the phone number input box.
