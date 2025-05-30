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
from launch import path,myluanch
from selenium.webdriver.common.action_chains import ActionChains
import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

def find(temp):
    screenshot = ImageGrab.grab()
    screenshot.save("screen.jpg")
    scene = cv2.imread('screen.jpg', cv2.IMREAD_COLOR)
    template = cv2.imread(temp, cv2.IMREAD_COLOR)
    scales = np.linspace(0.5, 2.0, 5)  # 20个缩放级别
    best_val = -np.inf
    best_loc = None
    best_scale = None
    best_template = None

    for scale in scales:
        resized = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        if resized.shape[0] > scene.shape[0] or resized.shape[1] > scene.shape[1]:
            continue

        result = cv2.matchTemplate(scene, resized, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_loc = max_loc
            best_scale = scale
            best_template = resized

    top_left = best_loc
    bottom_right = (top_left[0] + best_template.shape[1], top_left[1] + best_template.shape[0])

    x =  (top_left[0] + bottom_right[0])//2
    y = (top_left[1] + bottom_right[1])//2
    pyautogui.moveTo(x, y, duration=0.2)  # 平滑移动
    pyautogui.click()


def toutiao(title, port = 8555):
    proc = myluanch(port, 'https://mp.toutiao.com/profile_v4/graphic/publish?from=toutiao_pc')
    chrome_driver_path = path + r'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")  # 连接已经打开的浏览器
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.syl-toolbar-button')))

    find('submit.jpg')
    time.sleep(5)
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
    file_input.send_keys(r'C:\Users\10165\PycharmProjects\autopaper\main\words\\' + title + '.docx')

    print("文件上传成功！")
    time.sleep(5)
    textarea = driver.find_element(By.CSS_SELECTOR, 'div.editor-title textarea')
    textarea.clear()  # 可选，先清空内容
    if len(title) > 30:
        title = title[:30]
    textarea.send_keys(title)

    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.publish-btn.publish-btn-last')))
    button.click()

    time.sleep(5)

    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.publish-btn.publish-btn-last')))
    button.click()
