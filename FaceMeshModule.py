import cv2 as cv
import mediapipe as mp

class faceMesh():
    def __init__(self, staticMode = False, maxNumofFaces = 2, minDetectionConf = 0.5, minTrackingConf = 0.5):
        self.staticMode = staticMode
        self.maxNumofFaces = maxNumofFaces
        self.minDetectionConf = minDetectionConf
        self.minTrackingConf = minTrackingConf
        self.mpFaceMesh = mp.solutions.face_mesh
        self.mpDraw = mp.solutions.drawing_utils
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.staticMode, self.maxNumofFaces, min_detection_confidence = self.minDetectionConf, min_tracking_confidence = self.minTrackingConf)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)

    def trackFaceMesh(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.faceMesh.process(imgRGB)
        h, w, c = img.shape

        lms = []
        if self.result.multi_face_landmarks:
            for faceLms in self.result.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
                for id, lm in enumerate(faceLms.landmark):
                    x, y = int(lm.x*h), int(lm.y*w)
                    lms.append([id, (x,y)])

        return lms, img