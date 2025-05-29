from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from launch import myluanch
import json

title = '“端午不补阳，全年都白忙”！3种“暖阳菜“这样吃，吃对营养又养人 ，越吃越健康'

port = 8016
myluanch(port, 'https://chatgpt.com/')

chrome_driver_path = r'C:\Users\Administrator\Downloads\chrome-win64\chrome-win64\chromedriver.exe'
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 连接已经打开的浏览器
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

wait = WebDriverWait(driver, 20)
text_area = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]')))
text_area.send_keys("这是一篇热门文章的标题，你需要根据这个标题生成文章。现在你需要生成大纲，确定每部分的内容，要求只能有一级标题：" + title + "。请你以纯 JSON 格式输出，不要加任何解释或标注。")

time.sleep(1)
input_value = text_area.text
print(f"输入框中的内容是: {input_value}")
send_button = wait.until(EC.element_to_be_clickable((By.ID, "composer-submit-button")))
send_button.click()
print("发送按钮已点击")

last_answer = ""
timeout = 60  # 最多等待 30 秒
start_time = time.time()

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

while True:
    # 获取所有回答
    answers = driver.find_elements(By.CSS_SELECTOR, 'div[data-message-author-role="assistant"]')
    if answers:
        # 取最后一条
        new_answer = answers[-1].text.strip()
        if new_answer != last_answer and new_answer != "":
            print(new_answer)
            new_answer = new_answer[new_answer.find('{')]
            with open('data.json','a+', encoding='utf-8') as f:
                f.write(new_answer)
            # print(parse_gpt_json(new_answer))
            last_answer = new_answer
            start_time = time.time()

    if time.time() - start_time > timeout:
        print("⏰ 超时退出监听")
        break

    time.sleep(1)  # 每秒检查一次

