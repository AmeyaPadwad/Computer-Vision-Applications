import cv2 as cv
import FaceDetectionModule as fdm
import time

cap = cv.VideoCapture(0)
pTime = 0
cTime = 0
while True:
    success, img = cap.read()
    detector = fdm.faceDetector()
    bbox, img = detector.trackfaces(img)
    print(bbox)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(
        img,
        "fps: " + str(int(fps)),
        (10, 40),
        cv.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv.imshow("image", img)
    k = cv.waitKey(1)
    if k == 27:
        cv.destroyAllWindows()
        break
