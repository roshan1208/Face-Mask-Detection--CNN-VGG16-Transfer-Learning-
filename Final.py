from tensorflow.keras.models import load_model
import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from mediapipe_faceDetectionModule import FaceDetection
from realsense_3D_depth_camera import RealsenseCamera

new_model = load_model('FaceMaskDetection.h5')
fc = FaceDetection()
dc = RealsenseCamera()


# cap = cv2.VideoCapture(0)
# image_shape = (400, 570, 3)
# new_shape = (430, 370)
# class : {'Mask': 0, 'NoMask': 1}

while True:
    # ret, frame = cap.read()
    ret, depth_intrin, depth_scale, frame, img_depth = dc.get_frame_stream()
    bbox = fc.detectbbox(frame)
   
    if bbox != None:

        x,y,w,h = bbox
        if y-60 > 0 and x-60 > 0 and y+h+30 < 720 and x+w+30 < 1280:
            roi = frame[y-60:y+h+30, x-60:x+w+30]
        else:
            roi = frame[y:y+h, x:x+w]

        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(roi, (570, 400))
        my_img_arr = image.img_to_array(roi)
        my_img_arr = np.expand_dims(my_img_arr, axis = 0)

        predd = new_model.predict(my_img_arr)
        predd = predd > 0.5
        print(predd)
        if predd == False:
            cv2.putText(frame, f'Mask', (30, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)
        else:
            cv2.putText(frame, f'No Mask', (30, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        frame = fc.findFaces(frame)
        cv2.imshow('Final', frame)
    else:
        roi = frame
        frame = fc.findFaces(frame)
        cv2.putText(frame, f'No Human detected', (30, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Final', frame)
    
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
