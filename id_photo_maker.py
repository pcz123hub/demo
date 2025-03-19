import cv2
import numpy as np


def make_id_photo(image_path, output_path, target_size=(354, 472), background_color=(255, 255, 255)):
    try:
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            print("错误: 无法读取图像，请检查文件路径。")
            return

        # 转换为 HSV 颜色空间
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # 定义绿色背景的 HSV 范围
        lower_green = np.array([35, 43, 46])
        upper_green = np.array([77, 255, 255])

        # 创建掩码
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # 对掩码进行形态学操作，去除噪声
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 替换背景
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                if mask[i, j] == 255:
                    image[i, j] = background_color

        # 裁剪图像（这里简单假设裁剪中心部分）
        height, width, _ = image.shape
        center_x, center_y = width // 2, height // 2
        half_width, half_height = target_size[0] // 2, target_size[1] // 2
        cropped_image = image[center_y - half_height:center_y + half_height,
                        center_x - half_width:center_x + half_width]

        # 调整图像大小
        resized_image = cv2.resize(cropped_image, target_size)

        # 保存图像
        cv2.imwrite(output_path, resized_image)
        print(f"证件照已保存到 {output_path}")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    input_image_path = "wemeet image_20250312091912443.png"
    output_image_path = "output.png"
    make_id_photo(input_image_path, output_image_path)
