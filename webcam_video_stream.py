import cv2
from mtcnn import MTCNN
import insightface
import numpy as np

detector = MTCNN()
model = insightface.app.FaceAnalysis()
ctx_id = -1
model.prepare(ctx_id = ctx_id, nms=0.4)

cap = cv2.VideoCapture(0)
while True: 
    #Capture frame-by-frame
    __, frame = cap.read()
    
    #Use MTCNN to detect faces
    result = detector.detect_faces(frame)
    if result != []:
        for person in result:
            bounding_box = person['box']
            keypoints = person['keypoints']
            crop_img = frame[bounding_box[1]:bounding_box[1]+bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]].copy()
            faces = model.get(crop_img)
            cv2.rectangle(frame,
                          (bounding_box[0], bounding_box[1]),
                          (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                          (0,155,255),
                          2)
    
            cv2.circle(frame,(keypoints['left_eye']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['right_eye']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['nose']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['mouth_left']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['mouth_right']), 2, (0,155,255), 2)
            gender = " male"
            if faces[0].gender == 0:
                gender = " female"
            cv2.putText(frame, str(faces[0].age) + gender, (bounding_box[0], bounding_box[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 155, 255), 1, cv2.LINE_AA)
    #display resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) &0xFF == ord('q'):
        break
#When everything's done, release capture
cap.release()
cv2.destroyAllWindows()