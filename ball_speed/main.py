import cv2
import time

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
camera = cv2.VideoCapture(0)

lower = (60, 140, 70)
upper = (70, 255, 255)

# lower = (20, 10, 70)
# upper = (30, 255, 255)

# lower = (10, 135, 70)
# upper = (20, 255, 255)
#
# lower = (90, 210, 70)
# upper = (110, 255, 255)

D = 0.077
prev_time = time.time()
curr_time = time.time()
r = 1
speed = 0
trajectory = []
speed_values = []  # Список для хранения значений скорости

while camera.isOpened():
    ret, frame = camera.read()
    curr_time = time.time()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(c)
        trajectory.append((int(x), int(y)))
        if len(trajectory) > 10:
            trajectory.pop(0)
        if r > 10:
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(x), int(y)), int(r), (0, 0, 255), 2)

        for i in range(1, len(trajectory)):
            cv2.line(frame, trajectory[i], trajectory[i - 1], (255 * (i / 10), 0, 0), i)

        time_diff = curr_time - prev_time

        if len(trajectory) >= 2:
            p1 = trajectory[-1]
            p2 = trajectory[-2]
            if p1[0] != p2[0] and p1[1] != p2[1]:
                dx = p1[0] - p2[0]
                dy = p1[1] - p2[1]
                dist = (dx ** 2 + dy ** 2) ** 0.5
                pxl_per_m = D / (2 * r)
                dist *= pxl_per_m
                speed = dist / time_diff

                speed_values.append(speed)

                if len(speed_values) > 100:
                    speed_values.pop(0)

            prev_time = curr_time

    average_speed = sum(speed_values) / len(speed_values) if speed_values else 0

    cv2.putText(frame, f"Speed = {speed:.3f} m/s",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 0))

    cv2.putText(frame, f"Avg Speed = {average_speed:.3f} m/s",
                (10, 90), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255))

    cv2.imshow("Mask", mask)
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
