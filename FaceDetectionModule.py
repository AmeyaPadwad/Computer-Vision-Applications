import cv2 as cv
import mediapipe as mp


class faceDetector:
    def __init__(self, minConf=0.5):
        self.minConf = minConf
        self.mpFaces = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaces.FaceDetection(self.minConf)

    def trackfaces(self, img, draw=True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.result = self.faceDetection.process(imgRGB)
        h, w, c = img.shape

        bboxs = []
        if self.result.detections:
            for id, detection in enumerate(self.result.detections):
                bboxC = detection.location_data.relative_bounding_box
                bbox = (
                    int(bboxC.xmin * w),
                    int(bboxC.ymin * h),
                    int(bboxC.width * w),
                    int(bboxC.height * h),
                )
                bboxs.append([id, (bbox[0], bbox[1])])
                if draw:
                    cv.rectangle(img, bbox, (0, 255, 0), 2)
                    cv.putText(
                        img,
                        str(int(detection.score[0] * 100)) + "%",
                        (bbox[0], bbox[1] - 20),
                        cv.FONT_HERSHEY_PLAIN,
                        2,
                        (0, 255, 0),
                        2,
                    )

        return bboxs, img
