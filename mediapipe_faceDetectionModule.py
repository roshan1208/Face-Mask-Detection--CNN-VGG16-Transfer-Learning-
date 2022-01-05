import cv2
import mediapipe as mp
import time


class FaceDetection:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(threshold)
        self.mpDraw = mp.solutions.drawing_utils

    def findFaces(self, frame, draw=True):
        '''

        :param frame: take each frame or image as an input
        :param draw:
        :return: final image and bbox:list of (xmin,ymin,w,h)--boundry for face
        '''
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(frameRGB)

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                ih, iw, ic = frame.shape
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                self.fancydraw(frame, bbox)
                cv2.putText(frame, f"{int(detection.score[0] * 100)}%", (bbox[0], bbox[1] - 28),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
        return frame

    def detectbbox(self, frame):
        '''

        :param frame: take frame as input
        :return: bbox:list of x,y,w,h of each detected face in frame
        '''
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(frameRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                ih, iw, ic = frame.shape
                bboxC = detection.location_data.relative_bounding_box
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
            return bbox
        return None

    def fancydraw(self, img, bbox, l=30, t=10, rt=1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h
        cv2.rectangle(img, bbox, (0, 0, 255), rt)
        cv2.line(img, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(img, (x, y), (x, y + l), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = FaceDetection()
    while True:
        success, frame = cap.read()
        # xh, xw, xc = frame.shape
        # frame = cv2.resize(frame, (int(xw / 5), int(xh / 5)))
        results = detector.findFaces(frame)
        frame = results[0]

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f"FPS:{int(fps)}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3)

        cv2.imshow('Final', frame)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break


if __name__ == "__main__":
    main()
