import cv2
import pytesseract

# 如果Tesseract不在系统路径中，需手动指定路径（Windows常见）
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# 读取图片
image = cv2.imread(r'0003.png')

# 将图像转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 可选：二值化处理增强对比度
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 使用Tesseract进行OCR识别
text = pytesseract.image_to_string(image, lang='chi_sim+eng')  # 默认英语，中文用'chi_sim'

# 输出结果
print("识别结果：")
print(text)