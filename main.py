import cv2
import mediapipe as mp
import os
from math import sqrt

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def find_dig(point_1, point_2):
    return sqrt((point_1[0]-point_2[0])**2 + (point_1[1]-point_2[1])**2)

def detect_gesture(hand_landmarks, img_width, img_height, threshold=50):
    tip_big_finger = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    tip_ukaz_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    big_x, big_y = int(tip_big_finger.x * img_width), int(tip_big_finger.y * img_height)
    ukaz_x, ukaz_y = int(tip_ukaz_finger.x * img_width), int(tip_ukaz_finger.y * img_height)

    distance = find_dig((big_x, big_y), (ukaz_x, ukaz_y))

    if distance < threshold:
        return True
    else:
        return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = frame.shape

    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if detect_gesture(hand_landmarks, image_width, image_height):
                cv2.putText(frame, "Chmok!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    cv2.imshow('window: ', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()