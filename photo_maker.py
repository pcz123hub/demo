import cv2
import numpy as np

# 步骤1：采集图像
# 使用摄像头拍摄一张照片
cap = cv2.VideoCapture(0)  # 打开摄像头
print("按下 's' 键保存照片，按下 'q' 键退出。")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Capture", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # 按下 's' 键保存照片
        cv2.imwrite("photo.jpg", frame)
        print("照片已保存为 'photo.jpg'")
        break
    elif key == ord('q'):  # 按下 'q' 键退出
        break
cap.release()
cv2.destroyAllWindows()

# 步骤2：裁剪图像
# 加载照片
img = cv2.imread("photo.jpg")
if img is None:
    print("无法加载照片，请检查文件路径。")
    exit()

# 裁剪照片（根据需要调整裁剪区域）
# 假设证件照的宽高比例为 7:10
height, width = img.shape[:2]
crop_width = int(height * 7 / 10)
crop_height = height
start_x = (width - crop_width) // 2
start_y = 0
cropped_img = img[start_y:start_y + crop_height, start_x:start_x + crop_width]

# 步骤3：调整大小
# 将裁剪后的图像调整为指定的尺寸（如2寸证件照350x490像素）
target_size = (350, 490)  # 2寸证件照的尺寸
resized_img = cv2.resize(cropped_img, target_size, interpolation=cv2.INTER_AREA)

# 步骤4：颜色校正（可选）
# 调整亮度和对比度
alpha = 1.2  # 对比度增益
beta = 30    # 亮度偏移
corrected_img = cv2.convertScaleAbs(resized_img, alpha=alpha, beta=beta)

# 步骤5：添加背景
# 创建一个纯色背景（白色背景）
background_color = (255, 255, 255)  # 白色
background = np.full((490, 350, 3), background_color, dtype=np.uint8)

# 将校正后的图像放置在背景上
x_offset = 0
y_offset = 0
background[y_offset:y_offset + target_size[1], x_offset:x_offset + target_size[0]] = corrected_img

# 保存最终的证件照
cv2.imwrite("id_photo.jpg", background)
print("证件照已保存为 'id_photo.jpg'")
cv2.imshow("ID Photo", background)
cv2.waitKey(0)
cv2.destroyAllWindows()
