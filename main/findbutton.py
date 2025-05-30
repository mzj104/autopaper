import cv2
import numpy as np

# 加载大图和模板图
scene = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
template = cv2.imread('submit.jpg', cv2.IMREAD_COLOR)

# 定义缩放范围
scales = np.linspace(0.5, 2.0, 20)  # 20个缩放级别

best_val = -np.inf
best_loc = None
best_scale = None
best_template = None

# 遍历所有缩放比例
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

# 输出匹配坐标
top_left = best_loc
bottom_right = (top_left[0] + best_template.shape[1], top_left[1] + best_template.shape[0])

print(f"最佳匹配位置 (左上角): {top_left}")
print(f"最佳匹配位置 (右下角): {bottom_right}")
print(f"最佳缩放比例: {best_scale:.2f}")
print(f"匹配分数: {best_val:.2f}")

# 可视化并保存结果
matched = scene.copy()
cv2.rectangle(matched, top_left, bottom_right, (0, 0, 255), 2)
cv2.putText(matched, f'Scale: {best_scale:.2f}, Score: {best_val:.2f}', (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

# 保存结果
output_path = 'matched_result.jpg'
cv2.imwrite(output_path, matched)
print(f"匹配结果已保存为: {output_path}")

# 显示结果
cv2.imshow('Matched', matched)
cv2.waitKey(0)
cv2.destroyAllWindows()
