import cv2
import numpy as np

path = "https://cloud.iszf.irk.ru/index.php/s/ukRhcQNVViq5LH6/download"
video = cv2.VideoCapture(path)

if not video.isOpened():
    print("Ошибка: Не удалось открыть видео.")
    exit()

counter = 0

# Цветовые диапазоны в HSV
red_lower = np.array([0, 50, 50], dtype=np.uint8)
red_upper = np.array([10, 255, 255], dtype=np.uint8)
yellow_lower = np.array([20, 100, 100], dtype=np.uint8)
yellow_upper = np.array([30, 255, 255], dtype=np.uint8)
black_lower = np.array([0, 0, 0], dtype=np.uint8)
black_upper = np.array([180, 255, 50], dtype=np.uint8)
white_lower = np.array([0, 0, 200], dtype=np.uint8)
white_upper = np.array([180, 30, 255], dtype=np.uint8)

while True:
    ret, frame = video.read()

    if not ret or frame is None:
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Маски для каждого цвета
    mask_red = cv2.inRange(hsv_frame, red_lower, red_upper)
    mask_yellow = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    mask_black = cv2.inRange(hsv_frame, black_lower, black_upper)

    count_red = np.sum(mask_red == 255)
    count_yellow = np.sum(mask_yellow == 255)
    count_black = np.sum(mask_black == 255)


    if abs(count_red - 185821) < 10000 and abs(count_yellow - 16721) < 1400 and abs(count_black - 78201) < 1400:
        counter += 1


print(counter)

video.release()
