import subprocess
import os

path = r'D:\edge下载\chrome-win64\chrome-win64\\'  # 注意 r'' 避免转义
CHROME_PATH = os.path.join(path, 'chrome.exe')
USER_DATA_DIR = r"C:\selenium\chrome_user_data"


def myluanch(DEBUG_PORT, url):
    cmd = [
        CHROME_PATH,
        f'--remote-debugging-port={DEBUG_PORT}',
        f'--user-data-dir={USER_DATA_DIR}',
        url
    ]

    try:
        # 返回进程对象
        proc = subprocess.Popen(cmd)
        print(f"已启动 Chrome，调试端口：{DEBUG_PORT}")
        return proc
    except FileNotFoundError:
        print("找不到 chrome.exe，请检查路径或系统环境变量。")
        return None


# 启动示例
if __name__ == '__main__':
    port = 8016
    proc = myluanch(port, 'https://chatgpt.com/')

    # 稍后可以用 proc.terminate() 或 proc.kill() 关闭
    import time

    time.sleep(10)  # 等待 10 秒
    if proc:
        proc.terminate()  # 或 proc.kill()
        print("已关闭 Chrome")
