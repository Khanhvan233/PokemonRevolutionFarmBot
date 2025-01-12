import cv2
import numpy as np
from mss import mss
from PIL import Image
import time
import random
import pyautogui
import threading

# Cấu hình các nút và file mẫu
button_templates = {
    "FIGHT": ("fight.png", None),
    "RUN": ("run.png", None),
    "DITTO": ("ditto.png", None),
    "DITTO1": ("ditto1.png", None),
    "SHINY": ("shiny.png", None),
    "PP": ("nopp.png", None),
}

# Đọc template cho mỗi nút
for key in button_templates:
    template_path = button_templates[key][0]
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    button_templates[key] = (template_path, template)

# Hàm chụp màn hình
def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

# Hàm tìm vị trí nút trên màn hình
def find_button(screen, template):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.7  # Giảm ngưỡng để tìm kiếm dễ dàng hơn
    if max_val >= threshold:
        top_left = max_loc
        return top_left, (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    return None, None

# Hàm lưu tọa độ vào file
def save_coordinates(coordinates, file_path="coordinates.txt"):
    with open(file_path, "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value}\n")

# Hàm tải tọa độ từ file
def load_coordinates(file_path="coordinates.txt"):
    coordinates = {}
    try:
        with open(file_path, "r") as f:
            for line in f:
                key, value = line.strip().split(": ")
                coordinates[key] = eval(value)
    except FileNotFoundError:
        pass
    return coordinates

# Hàm di chuyển và click chuột
def move_and_click(region):
    x = random.randint(region[0][0], region[1][0])
    y = random.randint(region[0][1], region[1][1])
    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.2))
    pyautogui.click()
    
# Hàm di chuyển trái/phải liên tục
def move_left_right():
    while True:
        direction = random.choice(["a", "d"])
        pyautogui.keyDown(direction)  # Giữ phím
        time.sleep(random.uniform(0.4, 0.6))  # Giữ phím lâu hơn
        pyautogui.keyUp(direction)  # Nhả phím
        time.sleep(random.uniform(0.005, 0.001))  # Khoảng nghỉ ngắn hơn


# Chương trình chính
def main():
    print("Đang chuyển màn hình, vui lòng đợi 5 giây...")
    time.sleep(5)
    useSkill=1
    coordinates = load_coordinates()
    if not coordinates:
        screen = capture_screen()
        for key, (_, template) in button_templates.items():
            top_left, bottom_right = find_button(screen, template)
            if top_left and bottom_right:
                coordinates[key] = (top_left, bottom_right)
        save_coordinates(coordinates)

    # Tạo luồng di chuyển trái/phải
    movement_thread = threading.Thread(target=move_left_right)
    movement_thread.daemon = True
    movement_thread.start()

    encounter_count = 0

    # Vòng lặp kiểm tra hình ảnh
    # Vòng lặp kiểm tra hình ảnh
    while True:
        screen = capture_screen()

        # Kiểm tra nút FIGHT
        top_left_fight, bottom_right_fight = find_button(screen, button_templates["FIGHT"][1])
        if top_left_fight and bottom_right_fight:
            # Kiểm tra các nút và trạng thái khác
            top_left_no_pp, bottom_right_no_pp = find_button(screen, button_templates["PP"][1])
            top_left_ditto, _ = find_button(screen, button_templates["DITTO"][1])
            top_left_ditto1, _ = find_button(screen, button_templates["DITTO1"][1])
            top_left_shiny, bottom_right_shiny = find_button(screen, button_templates["SHINY"][1])

            if top_left_shiny:
                # Nếu phát hiện shiny Pokémon
                center_x = (top_left_shiny[0] + bottom_right_shiny[0]) // 2
                center_y = (top_left_shiny[1] + bottom_right_shiny[1]) // 2
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                print("Shiny Pokémon found! Stopping program.")
                break
            elif top_left_ditto1:
                # Nếu phát hiện Ditto1
                print("Ditto1 found! Stopping program.")
                move_and_click((top_left_ditto1, _))
                break
            else:
                # Nếu không có shiny hoặc Ditto1
                print(f"Using skill {useSkill}: Pressing '1', then '{useSkill}'.")

                # Nhấn tổ hợp phím 1 và useSkill
                pyautogui.press("1")
                time.sleep(0.3)
                pyautogui.press(str(useSkill))

                # Nếu phát hiện "No PP left!" thì tăng useSkill
                if top_left_no_pp and bottom_right_no_pp:
                    useSkill += 1
                    print(f"No PP left detected! Switching to skill {useSkill}.")
                    time.sleep(3)
                encounter_count += 1
                print(f"Encountered {encounter_count} Pokémon!")
                time.sleep(2)
            if useSkill >4:
                pyautogui.press("1")
                pyautogui.press("2")
                useSkill = 1


if __name__ == "__main__":
    main() 