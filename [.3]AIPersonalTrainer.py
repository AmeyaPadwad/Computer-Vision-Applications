from os import curdir
import cv2 as cv
import numpy as np
import time
import PoseDetectionModule as pdm

cap = cv.VideoCapture("bicep curls.mp4")
detector = pdm.poseDetector()
curlCount = 0
flag = True

while True:
    success, img = cap.read()
    img = cv.resize(img, (1280, 720))
    lmList, img = detector.trackPose(img, draw=False)

    if len(lmList) != 0:
        angle = detector.findAngle(img, 11, 13, 15)
        # detector.findAngle(img, 12, 14, 16)

        per = np.interp(angle, (210, 310), (0, 100))

        if per == 100 and flag:
            curlCount += 1
            flag = False
        if per == 0:
            flag = True

        cv.rectangle(img, (40, 30), (290, 70), (0, 0, 0), cv.FILLED)
        cv.putText(
            img,
            "Curl Count: " + str(curlCount),
            (50, 60),
            cv.FONT_HERSHEY_PLAIN,
            2,
            (0, 255, 0),
            3,
        )

    cv.imshow("img", img)
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break
