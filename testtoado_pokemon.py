import cv2
import numpy as np
from mss import mss
from PIL import Image
import time

# Cấu hình các template Pokémon
pokemon_templates = {
    "POKEMON1": ("pokemon1.png", None),
    "POKEMON2": ("pokemon2.png", None),
    "POKEMON3": ("pokemon3.png", None),
    "POKEMON4": ("pokemon4.png", None),
    "POKEMON5": ("pokemon5.png", None),
    "POKEMON6": ("pokemon6.png", None),
}

# Đọc template cho mỗi Pokémon
for key in pokemon_templates:
    template_path = pokemon_templates[key][0]
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    pokemon_templates[key] = (template_path, template)

# Hàm chụp màn hình
def capture_screen():
    with mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)

# Hàm tìm vị trí Pokémon trên màn hình
def find_pokemon(screen, template):
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        return top_left, (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    return None, None

# Hàm lưu tọa độ vào file
def save_pokemon_coordinates(coordinates, file_path="pokemon_coordinates.txt"):
    with open(file_path, "w") as f:
        for key, value in coordinates.items():
            f.write(f"{key}: {value}\n")

# Chương trình xác định tọa độ Pokémon
def find_pokemon_coordinates():
    print("Đang xác định tọa độ của 6 Pokémon trên màn hình...")
    coordinates = {}
    screen = capture_screen()

    for key, (_, template) in pokemon_templates.items():
        if template is not None:
            top_left, bottom_right = find_pokemon(screen, template)
            if top_left and bottom_right:
                coordinates[key] = (top_left, bottom_right)
                print(f"Tìm thấy {key} tại tọa độ {coordinates[key]}")
            else:
                print(f"Không tìm thấy {key} trên màn hình.")

    save_pokemon_coordinates(coordinates)
    print("Hoàn thành việc lưu tọa độ Pokémon vào file 'pokemon_coordinates.txt'.")

if __name__ == "__main__":
    find_pokemon_coordinates()
