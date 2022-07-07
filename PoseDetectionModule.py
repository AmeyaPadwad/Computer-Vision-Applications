import cv2 as cv
import mediapipe as mp
import math

from numpy import angle

class poseDetector():
    def __init__(self, mode = False, upper_body_only = False, smooth_landmarks = False, minDetectionConf = 0.5, minTrackingConf = 0.5):
        self.mode = mode
        self.upper_body_only = upper_body_only
        self.smooth_landmarks = smooth_landmarks
        self.minDetectionConf = minDetectionConf
        self.minTrackingConf = minTrackingConf
        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.mode, self.upper_body_only, self.smooth_landmarks, min_detection_confidence = minDetectionConf, min_tracking_confidence = minTrackingConf)

    def trackPose(self, img, draw = True):
        self.lmList = []
        h, w, c = img.shape
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)

        if self.result.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
            for id, lm in enumerate(self.result.pose_landmarks.landmark):
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, (cx, cy)])

        return self.lmList, img

    def findAngle(self, img, l1, l2, l3, draw=True):
        #Getting landmarks
        x1, y1 = self.lmList[l1][1]
        x2, y2 = self.lmList[l2][1]
        x3, y3 = self.lmList[l3][1]

        #Calculating angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))
        if angle<0:
            angle += 360
        
        #Draw
        if draw:
            cv.line(img, (x1,y1), (x2,y2), (255,0,0), 2)
            cv.line(img, (x3,y3), (x2,y2), (255,0,0), 2)
            cv.circle(img, (x1, y1), 15, (255,0,0), 3, 2)
            cv.circle(img, (x1, y1), 10, (255,0,0), cv.FILLED)
            cv.circle(img, (x2, y2), 15, (255,0,0), 3, 2)
            cv.circle(img, (x2, y2), 10, (255,0,0), cv.FILLED)
            cv.circle(img, (x3, y3), 15, (255,0,0), 3, 2)
            cv.circle(img, (x3, y3), 10, (255,0,0), cv.FILLED)
            cv.putText(img, str(int(angle)), (x2-20, y2-20), cv.FONT_HERSHEY_PLAIN, 2, (0,255,0), 3)
            cv.arc
        
        return angle