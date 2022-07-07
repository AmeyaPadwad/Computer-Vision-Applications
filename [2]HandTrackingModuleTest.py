import cv2 as cv
import HandTrackingModule as htm
import time 

cap = cv.VideoCapture(0)
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    detector = htm.handDetector()
    lmList, img = detector.trackhands(img)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv.putText(img, "fps: " + str(int(fps)), (10,40), cv.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

    if len(lmList) != 0:
        print(lmList)

    cv.imshow("image", img)
    k = cv.waitKey(1)
    if k == 27:
        cv.destroyAllWindows()
        break