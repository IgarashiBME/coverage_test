import numpy as np
import cv2
import time

#def transform(x, y, tx, ty, deg, sx, sy)
point1 = (10,10)
point2 = (290,290)

def distance(p1,p2):
    return np.linalg.norm(np.array([p2[0], p1[1]])-np.array([p1[0], p1[1]]))

# survey calc
dist = distance(point1,point2)
lines = dist/20
step_x = (point1[0]-point2[0])/lines

print dist, lines, step_x
NN = np.empty([0,2],dtype=np.int32)
for i in range(int(lines)):
    if i % 2 == 0:
        NN = np.append(NN, np.array([[point1[0] -i*step_x, point1[1]]], dtype=np.int32), axis=0)
        NN = np.append(NN, np.array([[point1[0] -i*step_x, point2[1]]], dtype=np.int32), axis=0)
    else:
        NN = np.append(NN, np.array([[point1[0] -i*step_x, point2[1]]], dtype=np.int32), axis=0)
        NN = np.append(NN, np.array([[point1[0] -i*step_x, point1[1]]], dtype=np.int32), axis=0)
print [NN]

img = np.full((300,300,3), 128, dtype=np.uint8)

cv2.polylines(img, [NN], False, (0,0,255), 2)
cv2.rectangle(img, point1, point2, (255,0,0))

cv2.imshow('', img)
k = cv2.waitKey(0)
if k==27:
    cv2.destroyAllWindows()
