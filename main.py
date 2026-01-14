import os
import datetime
import subprocess
from uuid import uuid4

def main():
    print("Hello from hellogelab-zero!")


if __name__ == "__main__":
    main()
    # print(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f"))

    # adb_command = "adb shell"
    # tmp_file_dir = r"C:\PathLink-Eurus\APT\AIOR\Temp"
    # screen_shot_pic_name = f"uuid_{uuid4()}.png"
    # screen_shot_pic_path = os.path.join(tmp_file_dir, screen_shot_pic_name)
    # print_command = True
    # screenshot_folder = "/data/user/0/com.qualcomm.mobile.virtualdisplaydemo/cache/"
    # # Modify screenshot name
    # command = f"adb shell ls {screenshot_folder}"
    # if print_command:
    #     print(f"Executing command: {command}")
    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # if result.returncode == 0:
    #     files = result.stdout.strip().split('\n')
    #     old_name = files[0]
    #     new_name = screen_shot_pic_name
    #     old_path = screenshot_folder + old_name
    #     new_path = screenshot_folder + new_name
    #     rename_command = f"{adb_command} mv {old_path} {new_path}"
    #     if print_command:
    #         print(f"Executing command: {rename_command}")
    #     rename_result = subprocess.run(rename_command, shell=True, capture_output=True, text=True)
    #     if rename_result.returncode == 0:
    #         print(f"Success to rename screenshot: {old_name} -> {new_name}")
    #     else:
    #         print(f"Fail to rename screenshot: {rename_result.stderr}")
    # else:
    #     print(f"Fail to get screenshot name: {result.stderr}")

    print(os.getcwd())