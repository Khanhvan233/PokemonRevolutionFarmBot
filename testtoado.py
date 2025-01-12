import cv2
import numpy as np
from mss import mss
from PIL import Image
import time

# Định nghĩa các nút và ảnh mẫu tương ứng
button_templates = {
    "FIGHT": "fight.png",
    "RUN": "run.png",
    "ITEMS": "items.png",
    "POKEMON": "pokemon.png",
    "SKILL1": "skill1.png",
    "SKILL2": "skill2.png",
    "SKILL3": "skill3.png",
    "SKILL4": "skill4.png"
}

# Hàm chụp màn hình
def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

# Hàm tìm tọa độ của hình ảnh trên màn hình
def find_button(screen, template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"[Error] Không tìm thấy tệp: {template_path}")
        return None, None
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        return top_left, bottom_right
    return None, None

# Hàm lưu tọa độ vào tệp
def save_coordinates(coordinates, file_path="coordinates.txt"):
    with open(file_path, "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value}\n")
    print(f"[Info] Tọa độ đã được lưu vào {file_path}")

# Hàm chính
def main():
    print("[Info] Chuyển sang màn hình mục tiêu trong 5 giây...")
    time.sleep(5)  # Chờ 5 giây để chuyển màn hình
    
    coordinates = {}
    screen = capture_screen()

    for key, template_path in button_templates.items():
        print(f"[Info] Đang tìm nút: {key}")
        top_left, bottom_right = find_button(screen, template_path)
        if top_left and bottom_right:
            coordinates[key] = (top_left, bottom_right)
            print(f"[Success] Đã tìm thấy {key} tại: {top_left} -> {bottom_right}")
        else:
            print(f"[Warning] Không tìm thấy nút: {key}")

    save_coordinates(coordinates)

if __name__ == "__main__":
    main()
