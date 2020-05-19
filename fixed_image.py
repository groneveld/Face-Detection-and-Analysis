import cv2
from mtcnn import MTCNN
import insightface
import numpy as np
import matplotlib.pyplot as plt

detector = MTCNN()

model = insightface.app.FaceAnalysis()
ctx_id = -1
model.prepare(ctx_id = ctx_id, nms=0.4)

image = plt.imread("faces.jpg") # Read an image into an array
# find facial features in image
result = detector.detect_faces(image)

#faces = model.get(image)

n_boxes = len(result)
for i in range (n_boxes):
# Result is an array with all the bounding boxes detected. We know that for 'ivan.jpg' there is only one.
	bounding_box = result[i]['box']
	keypoints = result[i]['keypoints']
	crop_img = image[bounding_box[1]:bounding_box[1]+bounding_box[3], bounding_box[0]:bounding_box[0] + bounding_box[2]].copy()
	faces = model.get(crop_img)
	cv2.rectangle(image,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (0,155,255),
              2)
	cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
	cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
	cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
	cv2.circle(image,(keypoints['mouth_left']), 2, (0,155,255), 2)
	cv2.circle(image,(keypoints['mouth_right']), 2, (0,155,255), 2)
	gender = " male"
	if faces[0].gender == 0:
		gender = " female"
	cv2.putText(image, str(faces[0].age) + gender, (bounding_box[0], bounding_box[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 155, 255), 1, cv2.LINE_AA) 

cv2.imwrite("image.jpg", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
cv2.imshow('img', image)
cv2.waitKey(0)