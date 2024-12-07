import cv2
import random
import numpy as np

colors = ["g", "y", "b", "o"]
random.shuffle(colors)

color_ranges = {
    "y": ((20, 55, 200), (30, 255, 255)),
    "g": ((70, 120, 160), (102, 245, 255)),
    "b": ((90, 210, 70), (110, 255, 255)),
    "o": ((6, 100, 70), (20, 255, 255))
}

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        break

    cv2.putText(frame, f"Required sequence: {colors}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255))

    # Словарь для хранения координат
    coordinates = {
        "g": None,
        "b": None,
        "y": None,
        "o": None
    }

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    for color in color_ranges.keys():
        mask = cv2.inRange(hsv, color_ranges[color][0], color_ranges[color][1])
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            (x, y), r = cv2.minEnclosingCircle(c)
            coordinates[color] = (x, y)

            if r > 10:
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 2)

    if all(coordinates[color] is not None for color in colors):
        y_coords = [coordinates["y"][1], coordinates["y"][1]]
        other_coords = [coordinates[color][1] for color in colors if color != "y"]

        if (y_coords[0] > other_coords[0]) and (y_coords[1] > other_coords[1]):
            sorted_colors = sorted(colors, key=lambda color: coordinates[color][0])
            sorted_colors = sorted(colors, key=lambda color: coordinates[color][0])
            print(sorted_colors)
            if colors == sorted_colors:
                cv2.putText(frame, "Correct sequence", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            else:
                cv2.putText(frame, "Incorrect sequence", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        else:
            cv2.putText(frame, "Incorrect sequence", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
    else:
        cv2.putText(frame, "Waiting for colors...", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0))

    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()



