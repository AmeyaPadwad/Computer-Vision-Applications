import cv2 as cv
import mediapipe as mp
import math


class handDetector:
    def __init__(
        self, mode=False, HandNos=2, minDetectionConf=0.5, minTrackingConf=0.5
    ):
        self.mode = mode
        self.HandNos = HandNos
        self.minDetectionConf = minDetectionConf
        self.minTrackingConf = minTrackingConf
        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(
            self.mode,
            self.HandNos,
            min_detection_confidence=self.minDetectionConf,
            min_tracking_confidence=self.minTrackingConf,
        )
        self.tipIDs = [8, 12, 16, 20]

    def trackhands(self, img, draw=True):
        self.lmList = []
        h, w, c = img.shape
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for i in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, i, self.mpHands.HAND_CONNECTIONS)
                for id, lm in enumerate(i.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lmList.append([id, (cx, cy)])

        return self.lmList, img

    def fingersUp(self):
        # to check if fingers are open or not
        fingersOpen = []

        # for thumb
        if self.lmList[4][1][0] < self.lmList[2][1][0]:
            fingersOpen.append(1)
        else:
            fingersOpen.append(0)

        # for other fingers
        for id in self.tipIDs:
            if self.lmList[id][1][1] < self.lmList[id - 2][1][1]:
                fingersOpen.append(1)
            else:
                fingersOpen.append(0)

        return fingersOpen

    def findDistance(self, l1, l2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[l1][1]  # thumb tip
        x2, y2 = self.lmList[l2][1]  # index tip
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # center point

        if draw:
            cv.circle(img, (x1, y1), r, (255, 0, 0), cv.FILLED)  # for thumb tip
            cv.circle(img, (x2, y2), r, (255, 0, 0), cv.FILLED)  # for index tip
            cv.circle(img, (cx, cy), r, (255, 0, 0), cv.FILLED)  # for center
            cv.line(
                img, (x1, y1), (x2, y2), (255, 0, 0), t
            )  # for line between thumb and index
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img
