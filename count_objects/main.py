import zmq
import cv2
import numpy as np


def on_mouse_callback(event, x, y, *params):
    global position
    if event == cv2.EVENT_LBUTTONDOWN:
        position = [y, x]
        # pass

count = 0

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
port = 5555
socket.connect(f"tcp://192.168.0.100:{port}")

window_name = "client"
cv2.namedWindow(window_name, cv2.WINDOW_GUI_NORMAL)
cv2.setMouseCallback(window_name, on_mouse_callback)
position = []


background = {
    "lower": (0, 4, 0),
    "upper": (255, 50, 255),
}

limits = [[255, 0], [255, 0], [255, 0]]

def supdate(value):
    global slimit
    slimit = value


while True:
    count = 0
    cubes = 0
    circles = 0

    msg = socket.recv(1024)
    frame = cv2.imdecode(np.frombuffer(msg, np.uint8), -1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_sat = 60
    upper_sat = 255

    mask = cv2.inRange(hsv, (0, lower_sat, 0), (180, upper_sat, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(len(contours)):
        contour = contours[i]
        area = cv2.contourArea(contour)
        if area > 500 and area < 50000:
            count += 1
            if area < 6500:
                cubes += 1
            else:
                circles += 1
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

    key = cv2.waitKey(100)
    if key == ord('q'):
        break
    elif key == ord('u'):
        limits = [[255, 0], [255, 0], [255, 0]]


    cv2.putText(frame,
                f"Count: {count}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 2))

    cv2.putText(frame,
                f"Cubes: {cubes}",
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 2))

    cv2.putText(frame,
                f"Circles: {circles}",
                (10, 130), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 255, 2))

    cv2.imshow("Image", frame)

cv2.destroyAllWindows()
