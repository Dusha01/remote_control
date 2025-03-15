import cv2
import mediapipe as mp
from math import sqrt
import pycaw.pycaw as pycaw
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import time

#----------------------------------------------------------------------

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

roi_x = 250
roi_y = 10
roi_width = 350
roi_height = 350

#========================================================================================================
#1
def find_dig(point_1, point_2):
    return sqrt((point_1[0]-point_2[0])**2 + (point_1[1]-point_2[1])**2)

def detect_volume_gesture(hand_landmarks, img_width, img_height, min_distance=20, max_distance=150):
    tip_big_finger = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    tip_ukaz_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    big_x, big_y = int(tip_big_finger.x * img_width), int(tip_big_finger.y * img_height)
    ukaz_x, ukaz_y = int(tip_ukaz_finger.x * img_width), int(tip_ukaz_finger.y * img_height)
    distance = find_dig((big_x, big_y), (ukaz_x, ukaz_y))

    if min_distance <= distance <= max_distance:
        return distance
    else:
        return None

def set_volume(distance, max_distance, min_distance):
    distance = max(min_distance, min(max_distance, distance))
    normalized_distance = (distance - min_distance) / (max_distance - min_distance)
    volume_level = minVol + (normalized_distance * (maxVol - minVol))
    volume.SetMasterVolumeLevel(volume_level, None)
    current_volume = volume.GetMasterVolumeLevel()
    return current_volume
#2
def detect_stop_one(hand_landmarks, img_width, img_height, threshold=0.07):
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]

    tip_y = pinky_tip.y
    pip_y = pinky_pip.y
    mcp_y = pinky_mcp.y

    if tip_y < pip_y and pip_y < mcp_y:
        return True

    return False
#========================================================================================================

min_distance = 20
max_distance = 150
previous_volume = None
volume_control_active = False

gesture_recognition_time = 2
gesture_start_time = None
pinky_straight_start_time = None

while cap.isOpened():
    volume_text = "Volume: N/A"
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    image_rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    image_height, image_width = roi.shape[:2]
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        filtered_hand_landmarks = []
        for hand_landmarks in results.multi_hand_landmarks:
            is_inside_roi = False
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * image_width)
                y = int(landmark.y * image_height)
                if 0 <= x <= image_width and 0 <= y <= image_height:
                    is_inside_roi = True
                    break
            if is_inside_roi:
                filtered_hand_landmarks.append(hand_landmarks)

        for hand_landmarks in filtered_hand_landmarks:
            mp_drawing.draw_landmarks(roi, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            distance = detect_volume_gesture(hand_landmarks, image_width, image_height)
            is_pinky_straight = detect_stop_one(hand_landmarks, image_width, image_height)

            if is_pinky_straight:
                if pinky_straight_start_time is None:
                    pinky_straight_start_time = time.time()
                elif time.time() - pinky_straight_start_time >= 1.5:
                    gesture_start_time = None
                    volume_control_active = False
                    pinky_straight_start_time = None
                    volume_text = "Volume: mini_pr+"
                    print("Volume: mini_pr-")
                    continue

            else:
                pinky_straight_start_time = None


            if distance is not None:
                if gesture_start_time is None:
                    gesture_start_time = time.time()
                    print("Gesture started...")

                elif time.time() - gesture_start_time >= gesture_recognition_time:
                    volume_control_active = True
                    current_volume = set_volume(distance, max_distance, min_distance)
                    volume_percentage = int(((current_volume - minVol) / (maxVol - minVol)) * 100)
                    volume_text = f"Volume: {volume_percentage}% (Control Active)"
                    previous_volume = current_volume
                    print("Active_1")

                elif volume_control_active:
                    current_volume = set_volume(distance, max_distance, min_distance)
                    volume_percentage = int(((current_volume - minVol) / (maxVol - minVol)) * 100)
                    volume_text = f"Volume: {volume_percentage}% (Adjusting)"
                    previous_volume = current_volume

                else:
                    volume_percentage = 0
                    volume_text = f"Recognizing ({round(time.time()-gesture_start_time, 1)}/{gesture_recognition_time} sec)"


            else:
                gesture_start_time = None
                if volume_control_active:
                    volume_text = "Gesture lost."
                else:
                    volume_text = "Volume: N/A"


            text_color = (0, 255, 0)

            cv2.putText(roi, volume_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2)

    else:
        gesture_start_time = None
        volume_control_active = False
        pinky_straight_start_time = None

    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 255, 255), 2)

    frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width] = roi

    cv2.imshow('window: ', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# добавить несколько жестов
#----------------------------------------------------------------------

cap.release()
cv2.destroyAllWindows()