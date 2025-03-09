# Hand Gesture Volume Control

This project implements a hand gesture recognition system to control the volume of your computer using a webcam.  It leverages the Mediapipe library for hand tracking and pycaw for volume control in Windows.

## Features

*   **Volume Control:** Adjust the system volume by moving your thumb and index finger closer or farther apart within a designated Region of Interest (ROI).
*   **Gesture Recognition Delay:** A short delay to prevent accidental volume changes.
*   **Stop Gesture:** Mute the volume with a specific finger gesture (straight pinky finger).
*   **Real-time Feedback:** Displays the current volume level and status (recognizing, adjusting, etc.) on the screen.

## Requirements

*   **Python 3.6 or higher**
*   **Libraries:**
    *   `opencv-python` (`cv2`)
    *   `mediapipe`
    *   `pycaw`
    *   `comtypes`

## Installation

1.  **Install Python:** Make sure you have Python 3.6 or higher installed on your system.  You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

    Replace `<repository_url>` with the actual URL of this repository.
    Replace `<repository_directory>` with the actual name of the directory that you just cloned to.

3.  **Install dependencies:**

    ```bash
    pip install opencv-python mediapipe pycaw comtypes
    ```

    **Note for pycaw installation:**  Sometimes `pycaw` installation might require additional steps, especially on Windows. If you encounter errors, refer to the `pycaw` documentation for specific instructions ([https://github.com/AndreMiras/pycaw](https://github.com/AndreMiras/pycaw)).

## Usage

1.  **Run the script:**

    ```bash
    python your_script_name.py
    ```

    Replace `your_script_name.py` with the actual name of your Python script (e.g., `main.py` or whatever you named it).

2.  **Usage Instructions:**

    *   **Volume Control:** Place your hand within the outlined rectangle (ROI) visible on the screen. Pinch your thumb and index finger together to decrease the volume, and move them apart to increase it.
    *   **Gesture Recognition:** The system needs a brief moment to recognize the volume control gesture.  A message will appear while it's recognizing.  Once recognized, volume adjustments become active.
    *   **Stop Gesture (Mute):** Extend your pinky finger straight. Holding this gesture for approximately 1.5 seconds will mute the volume.
    *   **Exit:** Press 'q' on the keyboard to exit the program.

## Code Explanation

*   **`mediapipe`:**  Used for hand tracking, detecting hand landmarks (positions of fingertips, joints, etc.).
*   **`pycaw`:**  Used to control the system's master volume in Windows.
*   **`cv2` (OpenCV):**  Used for capturing video from the webcam and displaying the video feed with overlays.
*   **Region of Interest (ROI):** A specific area in the camera feed where the system looks for hand gestures. The ROI's position and size are defined by `roi_x`, `roi_y`, `roi_width`, and `roi_height` variables.  You might need to adjust these values to suit your camera and setup.
*   **`detect_volume_gesture(hand_landmarks, img_width, img_height)`:** Calculates the distance between the thumb and index finger tips. If the distance falls within a defined range (`min_distance` and `max_distance`), the function returns the distance.
*   **`set_volume(distance, max_distance, min_distance)`:**  Maps the distance between the fingers to the volume range. It normalizes the distance and sets the system volume accordingly.
*   **`detect_stop_one(hand_landmarks, img_width, img_height)`:**  Detects if the pinky finger is straight based on the y-coordinates of the pinky tip, PIP (proximal interphalangeal) joint, and MCP (metacarpophalangeal) joint.
*   **Main Loop:**
    *   Captures video frames from the webcam.
    *   Detects hand landmarks within the ROI.
    *   Calls `detect_volume_gesture` and `detect_stop_one` to identify gestures.
    *   Adjusts the volume based on the detected gestures.
    *   Displays the video feed with the ROI rectangle, hand landmarks, and volume information.

## Customization

*   **ROI Position and Size:** Modify `roi_x`, `roi_y`, `roi_width`, and `roi_height` to adjust the Region of Interest.  Experiment to find the best placement for your hand.
*   **Distance Range:** Change `min_distance` and `max_distance` to adjust the sensitivity of the volume control. These values determine the minimum and maximum distances between the thumb and index finger that will be recognized.
*   **Gesture Recognition Time:** Modify `gesture_recognition_time` to increase or decrease the time required to recognize the volume control gesture. A longer time reduces false positives but makes volume adjustment slightly less responsive.
*   **Minimum Confidence:**  Adjust `min_detection_confidence` parameter in `hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)` to control the confidence threshold for hand detection.  Lowering it might detect hands more often, but could also increase false positives.
*   **Volume Range:** The code automatically retrieves the minimum and maximum volume levels from your system. If needed, you can manually override these values by modifying `minVol` and `maxVol`.

## Troubleshooting

*   **`pycaw` errors:** Ensure that `pycaw` is installed correctly. Refer to the `pycaw` documentation for troubleshooting.  Common issues relate to permissions and COM object initialization on Windows.
*   **Hand tracking not working:** Make sure the lighting is good and that your hand is clearly visible to the webcam.  Adjust the ROI if needed.
*   **Volume not changing:** Verify that the correct audio output device is selected as the default in your system's sound settings.  Also, double-check that `pycaw` has the necessary permissions to control the volume.
*   **High CPU usage:** Mediapipe can be resource-intensive. Reducing the frame size of the webcam feed (by setting a lower resolution in `cv2.VideoCapture()`) might help.

## Future Enhancements

*   Implement more sophisticated gestures for other actions (e.g., play/pause, next track, previous track).
*   Add support for multiple hand gestures simultaneously.
*   Improve the robustness of hand tracking in varying lighting conditions.
*   Create a graphical user interface (GUI) for easier configuration.

## License

[License](LICENSE) (Replace with the actual license file if you have one.)