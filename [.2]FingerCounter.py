import cv2 as cv
import time
import os
import HandTrackingModule as htm

######### PARAMETERS #########
drawHand = False  # To draw the hand detection on screen
showFPS = True  # To show the FPS on screen
fingerImagesPath = "./Finger_Images"
##############################


# WebCam
camW, camH = 1920, 1080
cap = cv.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

pTime = 0  # for fps

# Getting image paths
imagesPathList = os.listdir(fingerImagesPath)
images = []
for imagePath in imagesPathList:
    image = cv.imread(fingerImagesPath + "/" + imagePath)
    images.append(image)
print(len(images))

detector = htm.handDetector(minDetectionConf=0.7)  # object to detect and track hands

while True:
    success, img = cap.read()

    # hand detection and tracking for index and thumb tip
    lms, img = detector.trackhands(img, drawHand)  # hand detection
    cv.rectangle(img, (0, 0), (512, 512), (255, 255, 255), cv.FILLED)
    img[0:512, 0:512] = images[0]
    tipIDs = [8, 12, 16, 20]
    totalFingersUp = 0

    if len(lms) != 0:

        # to check if fingers are open or not
        fingersOpen = []

        # for thumb
        if lms[4][1][0] < lms[2][1][0]:
            fingersOpen.append(1)
        else:
            fingersOpen.append(0)

        # for other fingers
        for id in tipIDs:
            if lms[id][1][1] < lms[id - 2][1][1]:
                fingersOpen.append(1)
            else:
                fingersOpen.append(0)

        # showing image according to the number of fingers held up
        totalFingersUp = fingersOpen.count(1)
        img[0:512, 0:512] = images[totalFingersUp]
    cv.rectangle(img, (40, 540), (500, 590), (0, 0, 0), cv.FILLED)
    cv.putText(
        img,
        "Finger count : " + str(totalFingersUp),
        (50, 580),
        cv.FONT_HERSHEY_PLAIN,
        3,
        (0, 255, 0),
        2,
    )

    # fps
    if showFPS:
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(
            img,
            "FPS: " + str(int(fps)),
            (30, 40),
            cv.FONT_HERSHEY_PLAIN,
            2,
            (0, 255, 0),
            2,
        )

    cv.imshow("img", img)
    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break
