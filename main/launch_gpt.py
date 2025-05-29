import subprocess
import os

# 配置参数
CHROME_PATH = r'C:\Users\Administrator\Downloads\chrome-win64\chrome-win64\chrome.exe'
USER_DATA_DIR = r"C:\selenium\chrome_user_data"
DEBUG_PORT = 9654

# 构建启动命令
cmd = [
    CHROME_PATH,
    f"--remote-debugging-port={DEBUG_PORT}",
    f"--user-data-dir={USER_DATA_DIR}",
    "https://www.newrank.cn/hotInfo?platform=GZH"
]

# 启动 Chrome（不会一闪而过）
try:
    subprocess.Popen(cmd)
    print(f"已启动 Chrome，调试端口：{DEBUG_PORT}")
except FileNotFoundError:
    print("找不到 chrome.exe，请检查路径或系统环境变量。")
