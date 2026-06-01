from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO("yolo11n.pt")


def classify_jersey_color(player_crop):

    if player_crop.size == 0:
        return "person"

    hsv = cv2.cvtColor(player_crop, cv2.COLOR_BGR2HSV)

    red1 = cv2.inRange(
        hsv,
        np.array([0, 70, 50]),
        np.array([10, 255, 255])
    )

    red2 = cv2.inRange(
        hsv,
        np.array([170, 70, 50]),
        np.array([180, 255, 255])
    )

    red_mask = red1 + red2

    blue_mask = cv2.inRange(
        hsv,
        np.array([100, 50, 50]),
        np.array([140, 255, 255])
    )

    yellow_mask = cv2.inRange(
        hsv,
        np.array([20, 100, 100]),
        np.array([35, 255, 255])
    )

    red_pixels = cv2.countNonZero(red_mask)
    blue_pixels = cv2.countNonZero(blue_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)

    maximum = max(
        red_pixels,
        blue_pixels,
        yellow_pixels
    )

    if maximum < 500:
        return "person"

    if maximum == red_pixels:
        return "attacker"

    if maximum == blue_pixels:
        return "defender"

    if maximum == yellow_pixels:
        return "referee"

    return "person"


def detect(frame):

    results = model(frame)

    detections = []

    for result in results:

        for box in result.boxes:

            cls = int(box.cls[0])

            label = model.names[cls]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            confidence = float(box.conf[0])

            if label == "person":

                crop = frame[y1:y2, x1:x2]

                role = classify_jersey_color(crop)

                detections.append({
                    "label": role,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence
                })

            elif label == "sports ball":

                detections.append({
                    "label": "ball",
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence
                })

    return detections




