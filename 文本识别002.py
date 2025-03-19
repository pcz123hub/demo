import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, scrolledtext
import os

# 如果 Tesseract 不在系统路径中，需手动指定路径（Windows 常见）
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


def select_image():
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename()
    if file_path:
        if not os.path.exists(file_path):
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"错误：文件 {file_path} 不存在。")
            return
        # 读取图片
        image = cv2.imread(file_path)
        if image is None:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"错误：无法读取文件 {file_path}，请检查文件完整性。")
            return

        # 将图像转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 可选：二值化处理增强对比度
        thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # 使用 Tesseract 进行 OCR 识别
        text = pytesseract.image_to_string(
            thresh, lang='chi_sim+eng')  # 默认英语，中文用'chi_sim'

        # 创建窗口并显示原始图像
        cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Original Image', image)

        # 创建窗口并显示处理后的图像
        cv2.namedWindow('Processed Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Processed Image', thresh)

        # 清空文本框内容
        result_text.delete(1.0, tk.END)
        # 在文本框中显示识别结果
        result_text.insert(tk.END, text)

        # 等待按键事件
        cv2.waitKey(0)

        # 关闭所有窗口
        cv2.destroyAllWindows()


# 创建主窗口
root = tk.Tk()
root.title("图片 OCR 识别")

# 创建选择图片的按钮
select_button = tk.Button(root, text="选择图片", command=select_image)
select_button.pack(pady=20)

# 创建一个滚动文本框用于显示识别结果
result_text = scrolledtext.ScrolledText(root, width=40, height=10)
result_text.pack(pady=20)

# 运行主循环
root.mainloop()