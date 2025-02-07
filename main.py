import cv2
import mediapipe as mp
from math import sqrt
import pycaw.pycaw as pycaw
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

devices = pycaw.AudioUtilities.GetSpeakers()
interface = devices.Activate(pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(pycaw.IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

cap = cv2.VideoCapture(0)

def find_dig(point_1, point_2):
    return sqrt((point_1[0]-point_2[0])**2 + (point_1[1]-point_2[1])**2)

def detect_gesture(hand_landmarks, img_width, img_height):
    tip_big_finger = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    tip_ukaz_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    big_x, big_y = int(tip_big_finger.x * img_width), int(tip_big_finger.y * img_height)
    ukaz_x, ukaz_y = int(tip_ukaz_finger.x * img_width), int(tip_ukaz_finger.y * img_height)
    distance = find_dig((big_x, big_y), (ukaz_x, ukaz_y))
    return distance


def set_volume(distance, max_distance, min_distance):
    distance = max(min_distance, min(max_distance, distance))
    normalized_distance = (distance - min_distance) / (max_distance - min_distance)
    volume_level = minVol + (normalized_distance * (maxVol - minVol))
    volume.SetMasterVolumeLevel(volume_level, None)
    current_volume = volume.GetMasterVolumeLevel()
    return current_volume

min_distance = 20  
max_distance = 150
previous_volume = None  

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
            distance = detect_gesture(hand_landmarks, image_width, image_height)

            if distance is not None:
                current_volume = set_volume(distance, max_distance, min_distance)
                volume_percentage = int(((current_volume - minVol) / (maxVol - minVol)) * 100)
                volume_text = f"Volume: {volume_percentage}%"
                cv2.putText(frame, volume_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if previous_volume is None or abs(current_volume - previous_volume) > 0.5:
                    previous_volume = current_volume
                    print(f"Volume changed: {volume_percentage}%")

    cv2.imshow('window: ', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()