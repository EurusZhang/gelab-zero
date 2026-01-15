# Setup
- Install HiddenSurfaceControl APK
  - `adb root`
  - `adb remount`
  - `adb push HiddenSurfaceControl.apk /vendor/app`
  - `adb reboot`
  - Add scrcpy.exe path without any quotes into PC "System variables" as "SCRCPY_PATH"
- Install ADBKeyboard by `adb install` and reboot to take effective

# Attentions
- If set "mirror_display_switch" as False, DO NOT open same app on physical display while that app is running on virtual display. Otherwise it will disrupt agent workflow on virtual display because same app will toggle back and forth between physical and virtual displays

# Known Issues
- For now, it is only available for Kaanapali 1.0 META and device can be rooted. Kaanapali 2.0 can be available in the future.
- When virtual display is mirrored to physical screen, DO NOT try to click HOME or BACK or MULTI-TASK BUTTON in case of unexpected virtual display service exit, which is a known issue of HiddenSurfaceControl apk for now
- Taobao
  - Successful to slide and choose country code
  - Successful to type (actually paste) phone number
  - Fail to slide the slider to verify
  - Fail to type (actually paste) verification code
- Jingdong
  - Need face recognization to log in
  - It keeps clicking phone number input box because no keyboard shows out so it thinks that it's not able to type

# TODO
- [X] Formatted trace jsonl file
- [X] Support config.yaml file
  - [X] system prompts
  - [X] model_config.yaml info
  - [X] mirror display switch
- [ ] Export to .exe
  - [ ] support GUI with double clicks or running in console witout paras input
  - [ ] support running in console with task para input