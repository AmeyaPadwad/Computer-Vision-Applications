import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands(False, 4)

pTime = 0
cTime = 0

while True:
    
    success, img = cap.read()
    h, w, c = img.shape

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    #print(result.multi_hand_landmarks)

    if result.multi_hand_landmarks:
        for i in result.multi_hand_landmarks:
            for id, lm in enumerate(i.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id, cx, cy)

                if id == 0:
                    cv.circle(img, (cx,cy), 10, (0,255,0), 2)
            mpDraw.draw_landmarks(img, i, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv.putText(img, "fps: " + str(int(fps)), (10,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
    cv.imshow("image", img)
    k = cv.waitKey(1)
    if k == 27:
        cv.destroyAllWindows()
        break