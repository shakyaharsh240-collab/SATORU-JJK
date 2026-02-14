import cv2
import mediapipe as mp
import numpy as np

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def detect_sukuna_gesture(hand_landmarks):
    # Sukuna gesture logic
    index_tip = hand_landmarks.landmark[8]
    middle_tip = hand_landmarks.landmark[12]
    distance = np.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)
    return distance < 0.03 

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
            if detect_sukuna_gesture(hand_lms):
                cv2.putText(img, "DOMAIN EXPANSION: MALEVOLENT SHRINE", (50, 100), 
                            cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 2)
                overlay = img.copy()
                cv2.rectangle(overlay, (0,0), (img.shape[1], img.shape[0]), (0,0,150), -1)
                cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

    cv2.imshow("JJK Code", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
