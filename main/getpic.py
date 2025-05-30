from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
from launch import myluanch, path
import json
import os
import requests

def download_pic(key, download=8222):
    port = 8222
    proc = myluanch(port, 'https://image.baidu.com/search/index?word='+key)

    chrome_driver_path = path + r'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 连接已经打开的浏览器
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

    save_dir = "images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    time.sleep(5)
    images = driver.find_elements(By.TAG_NAME, "img")
    img_urls = []

    for img in images:
        src = img.get_attribute('src')
        if src and src.startswith('http'):  # 确保是有效链接
            img_urls.append(src)

    print(f"共找到 {len(img_urls)} 张图片，开始下载...")

    for i, url in enumerate(img_urls):
        if i<3:
            continue
        if i > 22:
            break
        try:
            response = requests.get(url, timeout=10)
            with open(os.path.join(save_dir, f"image_{i+1}.jpg"), 'wb') as f:
                f.write(response.content)
            print(f"已保存: image_{i+1}.jpg")
        except Exception as e:
            print(f"下载失败: {url}，错误: {e}")

    print("全部下载完成！")
    proc.terminate()