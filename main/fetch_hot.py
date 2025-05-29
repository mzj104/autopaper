from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import time
from launch import myluanch

port = 9654
myluanch(port, 'https://www.newrank.cn/hotInfo?platform=GZH')
save_title = 'hot.txt'
time.sleep(5)
chrome_driver_path = r'C:\Users\Administrator\Downloads\chrome-win64\chrome-win64\chromedriver.exe'  # 用 r'' 表示原始字符串
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 连接已经打开的浏览器
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

elements = driver.find_elements(By.CSS_SELECTOR, "span.text-mul-wrap[title]")
titles = [e.get_attribute("title") for e in elements]
print(f"找到{len(titles)}条热门标题")
print(f'已保存到{save_title}')
print("-----------------------------------")
with open(save_title,'a+', encoding='utf-8') as f:
    f.write('\n'.join(titles))

if len(titles) > 0:
    pass