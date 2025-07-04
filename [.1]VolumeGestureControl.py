import cv2 as cv
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######### PARAMETERS #########
showBarOnScreen = True  # To show the volume bar on screen
drawHand = False  # To draw the hand detection on screen
showControlLine = True  # To show the volume control line on screen
showFPS = True  # To show the FPS on screen
##############################

# initialization for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]

# WebCam
camW, camH = 1920, 1080
cap = cv.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

pTime = 0  # for fps

detector = htm.handDetector(minDetectionConf=0.7)  # object to detect and track hands

while True:
    success, img = cap.read()

    # hand detection and tracking for index and thumb tip
    lms, img = detector.trackhands(img, drawHand)  # hand detection

    if len(lms) != 0:
        length, img = detector.findDistance(4, 8, img, showControlLine)

        # Assigning length to volume
        lMin, lMax = 15, 150
        vol = np.interp(length, [lMin, lMax], [minVol, maxVol])
        volume.SetMasterVolumeLevel(vol, None)

        # showing volume bar on screen
        if showBarOnScreen:
            volBar = np.interp(
                length, [lMin, lMax], [250, 150]
            )  # range length to volume bar
            volPer = np.interp(
                length, [lMin, lMax], [0, 100]
            )  # range length to percentage
            cv.rectangle(img, (30, 250), (50, 150), (0, 0, 255), 2)
            cv.rectangle(img, (30, int(volBar)), (50, 250), (0, 0, 255), cv.FILLED)
            cv.putText(
                img,
                str(int(volPer)) + "%",
                (20, 280),
                cv.FONT_HERSHEY_PLAIN,
                1.5,
                (0, 0, 255),
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
