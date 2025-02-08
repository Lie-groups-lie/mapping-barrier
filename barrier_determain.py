# image_processing.py
from PIL import Image
import numpy as np

# 取消 PIL 对大图像尺寸的限制
Image.MAX_IMAGE_PIXELS = None

def extract_pixels(input_png, output_png, rgb_ranges):
    from PIL import Image
    import numpy as np

    Image.MAX_IMAGE_PIXELS = None
    img = Image.open(input_png).convert("RGB")
    img_data = np.array(img)
    new_img_data = np.zeros_like(img_data)

    # 对于每个范围，创建布尔掩码，然后将符合条件的像素赋值为白色
    for rgb_min, rgb_max in rgb_ranges:
        r_min, g_min, b_min = rgb_min
        r_max, g_max, b_max = rgb_max
        mask = ((img_data[:,:,0] >= r_min) & (img_data[:,:,0] <= r_max) &
                (img_data[:,:,1] >= g_min) & (img_data[:,:,1] <= g_max) &
                (img_data[:,:,2] >= b_min) & (img_data[:,:,2] <= b_max))
        new_img_data[mask] = [255, 255, 255]

    new_img = Image.fromarray(new_img_data)
    new_img.save(output_png)
