import cv2
import numpy as np

video_path = 'output.avi'
image_path = 'image.png'

image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cap = cv2.VideoCapture(video_path)

frame_count = 0
image_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_frame, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= 0.7:
        # cv2.imshow('frame', gray_frame)
        # cv2.imshow('image', image)
        image_count += 1
    frame_count += 1
cap.release()


print(f"Количество кадров: {frame_count}")
print(f"Количество кадров с моим изображением: {image_count}")
