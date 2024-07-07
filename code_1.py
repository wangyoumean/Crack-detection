import cv2
import math
import numpy as np

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 初始化窗口
window_width = 800
window_height = 600
window = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255  # 创建白色背景
window_copy = window.copy()  # 备份窗口

# 设置字体
font = cv2.FONT_HERSHEY_SIMPLEX  # 使用OpenCV内置字体
font_scale = 1  # 字体尺寸缩放倍数
font_thickness = 2  # 字体线条粗细

# 鼠标轨迹点
points = []

def calculate_length(points):
    """
    计算鼠标轨迹的总长度
    """
    total_length = 0
    for i in range(len(points) - 1):
        length = math.sqrt((points[i+1][0] - points[i][0])**2 + (points[i+1][1] - points[i][1])**2)# 欧几里得距离公式
        total_length += length
    return total_length

def draw_curve(image, points):
    """
    在图像上绘制鼠标轨迹，并显示轨迹的总长度
    """
    for i in range(len(points) - 1):
        cv2.line(image, points[i], points[i+1], BLACK, 2)  # 绘制轨迹
    length = calculate_length(points)
    cv2.putText(image, f"Length: {length:.2f}", (10, 30), font, font_scale, BLACK, font_thickness)  # 显示轨迹总长度

def mouse_callback(event, x, y, flags, param):
    """
    回调函数，处理鼠标事件，并记录轨迹
    """
    global points
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键按下事件
        points.append((x, y))  # 记录鼠标位置
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:  # 鼠标移动事件
        points.append((x, y))  # 记录鼠标位置

cv2.namedWindow("Draw Curve")  # 创建窗口
cv2.setMouseCallback("Draw Curve", mouse_callback)  # 设置鼠标事件回调函数

while True:
    cv2.imshow("Draw Curve", window)
    key = cv2.waitKey(1) & 0xFF  # 获取键盘输入
    if key == 13:  # 按回车键关闭窗口
        break
    elif key == ord("r"):  # 按r键重置窗口，注意要在英文输入法下输入
        window = window_copy.copy()
        points = []  # 清空轨迹点

    if len(points) > 1:  # 当轨迹点大于1时才绘制轨迹
        window = window_copy.copy()
        draw_curve(window, points)  # 绘制轨迹

cv2.destroyAllWindows()  # 关闭窗口