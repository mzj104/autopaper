from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from launch import myluanch,path
import json
from getpic import download_pic


def gen_dirs(title):
    download_pic(title)

    port = 8016
    proc = myluanch(port, 'https://chatgpt.com/')


    chrome_driver_path = path + r'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 连接已经打开的浏览器
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    wait = WebDriverWait(driver, 20)
    text_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]')))

    prompt ='你是一个结构化内容生成助手，需要根据用户提供的主题，生成内容大纲,最多分为4节。确保内容为 JSON 串，且内容符合以下结构：{"大纲": {"<用户输入的主题>": [{"标题": "引言", "内容": "<需填充>"}, {"标题": "<需填充>", "内容": "<需填充>"}, {"标题": "<需填充>", "内容": "<需填充>"}, {"标题": "<需填充>", "内容": "<需填充>"}, {"标题": "结语", "内容": "<需填充>"}]}}    请将 `<用户输入的主题>` 替换为用户提供的实际主题，将`<需填充>` 替换为合适的大纲。确保输出严格符合此格式，且为单行 JSON 字符串，不要包含其他任何文字或解释。'

    text_area.send_keys(prompt + title)

    time.sleep(1)
    input_value = text_area.text
    print(f"输入框中的内容是: {input_value}")
    send_button = wait.until(EC.element_to_be_clickable((By.ID, "composer-submit-button")))
    send_button.click()
    print("发送按钮已点击")


    import re

    def parse_gpt_json(text: str):
        # 移除 Markdown 代码块符号（如果有）
        text = re.sub(r"^```(json)?", "", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"```$", "", text.strip())

        try:
            data = json.loads(text)
            return data
        except json.JSONDecodeError as e:
            print("❌ JSON 解析失败:", e)
            print("原始内容:", text[:300])
            return None


    last_answer = ""
    timeout = 5 # 最多等待 30 秒
    start_time = time.time()

    while True:
        answers = driver.find_elements(By.CSS_SELECTOR, 'div[data-message-author-role="assistant"]')
        if answers:
            new_answer = answers[-1].text.strip()
            if new_answer != last_answer and new_answer != "":
                with open('data.json','w', encoding='utf-8') as f:
                    f.write(new_answer[new_answer.find('{'):])
                last_answer = new_answer
                start_time = time.time()

        if time.time() - start_time > timeout:
            print("⏰ 超时退出监听")
            break

        time.sleep(1)  # 每秒检查一次

    proc.terminate()
