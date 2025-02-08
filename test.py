import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)

roi_x = 100
roi_y = 100
roi_width = 400
roi_height = 300

cap = cv2.VideoCapture(0) 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]

    image = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * roi_width)
                y = int(landmark.y * roi_height)

                x_original = x + roi_x
                y_original = y + roi_y

                cv2.circle(frame, (x_original, y_original), 5, (0, 255, 0), -1)

            cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)


    cv2.imshow('Hand Tracking', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()