import cv2
import time
import math
import numpy as np
import screen_brightness_control as sbc
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import webbrowser  # Import webbrowser module for opening YouTube

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.7)

# Initialize audio devices
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Get brightness range
minBr = 0  # Assuming the minimum brightness is 0
maxBr = 100  # Assuming the maximum brightness is 100

# Video capture initialization
cap = cv2.VideoCapture(0)
pTime = 0

# Define variables for gesture recognition
opened_youtube = False
prev_finger_state = None
prev_brightness = 50  # Assuming initial brightness level is 50%

while True:
    success, frame = cap.read()
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))
    cv2.putText(frame, f'FPS:{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)

    # Find hand landmarks
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw=False)

    if len(lmlist) != 0:
        # Determine hand type (left or right)
        if lmlist[0][1] < lmlist[17][1]:
            handType = "Right"
        else:
            handType = "Left"

        if handType == "Left":
            # Left hand volume control
            x1, y1 = lmlist[8][1:]  # Index finger coordinates
            x2, y2 = lmlist[4][1:]  # Thumb finger coordinates
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(frame, (x1, y1), 8, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
            cv2.circle(frame, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

            # Interpolate length to volume range
            vol = np.interp(length, [30, 300], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

        if handType == "Right":
            # Right hand brightness control
            x1, y1 = lmlist[8][1:]  # Index finger coordinates
            x2, y2 = lmlist[4][1:]  # Thumb finger coordinates
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(frame, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(frame, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
            length = math.hypot(x2 - x1, y2 - y1)

            # Interpolate length to brightness range
            brightness_level = np.interp(length, [50, 220], [0, 100])
            sbc.set_brightness(int(brightness_level))

        fingers = detector.fingersUp()

        # Check for pinky finger to open YouTube only once
        if fingers[4] and not all(fingers[0:4]):
            if not opened_youtube:
                print("Pinky finger Detected! Opening YouTube...")
                webbrowser.open("https://www.youtube.com/watch?v=id848Ww1YLo")
                opened_youtube = True  # Set the flag to True after opening YouTube

    cv2.imshow('Video Capture', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
