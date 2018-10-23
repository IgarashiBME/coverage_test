import numpy as np
import cv2
import time

#def transform(x, y, tx, ty, deg, sx, sy)

## coordinate of parallelogram
point1 = (10,10)
point2 = (290,290)
point3 = (230, 10)
point4 = (70, 290)
pts = np.array([point1, point3, point2, point4])

## parameter
spacing = 10  # distance between paths

def distance(p1,p2):
    return np.linalg.norm(np.array([p2[0], p1[1]])-np.array([p1[0], p1[1]]))

## calculate survey lines on parallelogram 
def calcPointInLineWithY(p1,p2,y):
    s = p1[1] - p2[1]
    
    try:
        s
    except NameError:
        return False

    x = (y - p1[1]) * (p1[0] - p2[0]) / s + p1[0]
    if x > p1[0] and x > p2[0]:
        return False
    if x < p1[0] and x < p2[0]:
        return False
    #print x
    return [x, y]

# survey calc
dist = distance(point1,point2)
lines = dist/spacing
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
print NN.shape

## survey lines on parallelogram 
WE = np.empty([0,2],dtype=np.int32)
j=0
for i in range(NN.shape[0]):
    westPoint = calcPointInLineWithY(point1, point4, NN[i][0])
    eastPoint = calcPointInLineWithY(point3, point2, NN[i][0])

    j += 1
    if j > 4:
        j = 1
    if westPoint != False and eastPoint != False:
        if j % 4 == 0:
            WE = np.append(WE, westPoint)            
        elif j % 3 == 0:
            WE = np.append(WE, eastPoint)
        elif j % 2 == 0:
            WE = np.append(WE, eastPoint)
        else:
            WE = np.append(WE, westPoint)
WE = WE.reshape(WE.shape[0]/2, 2)
print WE
img = np.full((300,300,3), 128, dtype=np.uint8)

cv2.polylines(img, [WE], False, (0,0,255), 2)
cv2.polylines(img, [pts], True, (255,0,0), 1)

cv2.imshow('', img)
k = cv2.waitKey(0)
if k==27:
    cv2.destroyAllWindows()
