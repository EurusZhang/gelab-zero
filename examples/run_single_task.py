import os
import sys
import time
if "." not in sys.path:
    sys.path.append(".")
import subprocess
import yaml
from copilot_agent_client.pu_client import evaluate_task_on_device
from copilot_front_end.mobile_action_helper import list_devices, get_device_wm_size
from copilot_agent_server.local_server import LocalServer
from copilot_front_end.hidden_surface_control_utils import vdu


config_file = f"{os.getcwd()}//config.yaml"
with open(config_file, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

log_folder = vdu.update_log_folder()
tmp_server_config = {
    "log_dir": f"{log_folder}/traces",
    "image_dir": f"{log_folder}/images",
    "debug": False
}

local_model_config = config["rollout_config"]
local_model_config["task_type"] = "parser_0922_summary"

# ===== 新增：用于记录每步耗时 =====
_step_times = []


# ===== 新增：包装 automate_step 方法 =====
def wrap_automate_step_with_timing(server_instance):
    original_method = server_instance.automate_step

    def timed_automate_step(payload):
        step_start = time.time()
        try:
            result = original_method(payload)
        finally:
            duration = time.time() - step_start
            _step_times.append(duration)
            print(f"[GELab-Zero] Step {len(_step_times)} took: {duration:.2f} seconds")
        return result

    # 替换实例方法
    server_instance.automate_step = timed_automate_step

if __name__ == "__main__":

     # task = "打开微信，给柏茗，发helloworld"
    # task = "打开 给到 app，在主页，下滑寻找，员工权益-奋斗食代，帮我领劵。如果不能领取就退出。"
    # task = "open wechat to send a message 'helloworld' to 'TKJ'"
    #task = "去淘宝帮我买本书"
    # if len(sys.argv) < 2:
    #     print("❌ 错误：未传入任务参数！")
    #     print("📝 使用方法：")
    #     print(f"   python {sys.argv[0]} \"你的任务描述\"")
    #     print("   示例1：python script.py \"去淘宝帮我买本书\"")
    #     print("   示例2：python script.py \"打开微信，给柏茗发helloworld\"")
    #     sys.exit(1)  
    # task = ' '.join(sys.argv[1:])

    # task = "登录我的抖音账号。选择手机验证码的方式登录，在手机区号选择里划动选择中国大陆+86，然后输入手机号17717016819，再等待用户输入验证码，再登录。"
    # task = "打开淘宝，搜索苹果手机iphone14，并选择256g，加入购物车"
    task = "打开大众点评，找到长泰广场的牛new寿喜烧，发布一条评论说“上个月来吃了一会，感觉非常好，会再来"

    # The device ID you want to use
    device_id = list_devices()[0]
    device_wm_size = get_device_wm_size(device_id)
    device_info = {
        "device_id": device_id,
        "device_wm_size": device_wm_size
    }

    # root device
    subprocess.check_output(f"adb -s {device_id} root")

    tmp_rollout_config = local_model_config
    l2_server = LocalServer(tmp_server_config)

    # 注入计时逻辑
    wrap_automate_step_with_timing(l2_server)
    # 执行任务并计总时间
    total_start = time.time()
    # Disable auto reply
    evaluate_task_on_device(l2_server, device_info, task, tmp_rollout_config, reflush_app=True)
    # Enable auto reply
    # evaluate_task_on_device(l2_server, device_info, task, tmp_rollout_config, reflush_app=True, auto_reply=True)
    total_time = time.time() - total_start

    # 在最后加一行总时间
    print(f"[GELab-Zero] Total execution time is {total_time} s")
