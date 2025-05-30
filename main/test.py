import pyautogui
import time
time.sleep(5)
# 点击目标位置（以屏幕左上角为原点）
target_x = 2270
target_y = 360

# 可选: 移动鼠标到目标位置
pyautogui.moveTo(target_x, target_y, duration=0.5)  # 平滑移动

# 点击
pyautogui.click()

print(f"已在屏幕坐标 ({target_x}, {target_y}) 点击")

# 可选: 等待确认

