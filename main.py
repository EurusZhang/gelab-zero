import os
import json
import datetime
import subprocess
import json
from uuid import uuid4
from tools.ask_llm_v2 import ask_llm_anything


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

# print(os.getcwd())


# messages_to_ask = [
#     {
#         "role": "user",
#         "content": [
#             {
#                 "type": "text",
#                 "text": "Who are you?"
#             },
#             # {
#             #     'type': "image_url",
#             #     'image_url': {
#             #         'url': current_image_url
#             #     }
#             # },
#         ]
#     }
# ]
# response = ask_llm_anything(
#     model_provider="vllm",
#     model_name="gelab-zero-4b-preview",
#     messages=messages_to_ask,
#     args={
#         "max_tokens": 1024,
#         "temperature": 0.5,
#         "top_p": 1.0,
#         "frequency_penalty": 0.0,
#     }
# )
# print(response)




# def format_jsonl_to_pretty_json(input_file, output_file):
#     """
#     将JSONL文件转换为带有换行格式的JSON文件
    
#     Args:
#         input_file: 输入的JSONL文件路径
#         output_file: 输出的格式化JSON文件路径
#     """
#     data_list = []
    
#     # 读取JSONL文件
#     with open(input_file, 'r', encoding='utf-8') as f:
#         for line in f:
#             if line.strip():  # 跳过空行
#                 data_list.append(json.loads(line))
    
#     # 写入格式化的JSON文件
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(data_list, f, ensure_ascii=False, indent=2)
    
#     print(f"转换完成！共处理 {len(data_list)} 条记录")
#     print(f"输出文件: {output_file}")


# input_file = r"C:\PathLink-Eurus\APT\Workspace\python\gelab-zero\running_log\server_log\os-copilot-local-eval-logs\2026-01-15_17-02-13-374621\traces\b9fe5223-1fd4-467b-ac56-64b6a4bd36ac.jsonl"  # 你的输入文件名
# output_file = r"C:\PathLink-Eurus\APT\Workspace\python\gelab-zero\running_log\server_log\os-copilot-local-eval-logs\2026-01-15_17-02-13-374621\traces\output.jsonl"  # 输出文件名

# format_jsonl_to_pretty_json(input_file, output_file)


print(f"{'*'*10}\naaaa\n{'*'*10}")