import cv2
import pyautogui
import HandTrackingModule as htm

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.7)

# Video capture initialization
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))

    # Find hand landmarks
    frame = detector.findHands(frame)
    lmlist = detector.findPosition(frame, draw=False)

    if len(lmlist) != 0:
        # Check for hand open/close gesture (left hand)
        if lmlist[0][1] > lmlist[17][1]:  # Left hand
            fingers = detector.fingersUp()
            if fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:  # All fingers closed except thumb
                pyautogui.hotkey('shift', 'p')  # Previous video using Shift + P
                print("Previous Video")
            elif not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:  # Thumb open, all other fingers closed
                pyautogui.hotkey('shift', 'n')  # Next video using Shift + N
                print("Next Video")

    cv2.imshow('Video Capture', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
