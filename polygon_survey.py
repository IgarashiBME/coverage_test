import numpy as np
import cv2
import time

## coordinate of parallelogram
point1 = (10,10)
point2 = (230, 60)
point3 = (290,200)
point4 = (200, 290)
point5 = (70, 240)
pts = np.array([point1, point2, point3, point4, point5])

## parameter
spacing = 10  # distance between paths

def distance(p1,p2):
    return np.linalg.norm(np.array([p2[0], p1[1]])-np.array([p1[0], p1[1]]))

def transform(x, y, tx, ty, deg, sx, sy):
    deg = deg * np.pi /180
    try:
        sy
    except NameError:
        sy = 1
    try:
        sx
    except NameError:
        sx = 1

    return [sx*((x-tx)*np.cos(deg) -(y-ty)*np.sin(deg)) +tx,\
            sy*((x-tx)*np.sin(deg) -(y-ty)*np.cos(deg)) +ty]

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

def createPolygonBounds(points):
    x = []
    y = []
    
    for i in range(len(points)):
        x.append(pts[i][0])
        y.append(pts[i][1])

    max_x = max(x)
    max_y = max(y)
    min_x = min(x)
    min_y = min(y)

    center = ((max_x +min_x)/2, (max_y +min_y)/2)
    nw = (min_x, min_y)
    ne = (max_x, min_y)
    sw = (min_x, max_y)
    se = (max_x, max_y)
    return {"center":center, "nw":nw, "ne":ne, "sw":sw, "se":se, }

def calcLatsInPolygon(rect, spacing):
    lines = distance(rect["nw"],rect["se"])/spacing/2
    x = (rect["nw"][0] -rect["se"][0])/lines
    return {"lines":int(lines), "x":x}

## prevent survey overflaw
def si(i, j):
    if i > j -1:
        return i-j
    if i < 0:
        return i+j
    return i    

## External Rectangle
outRect = createPolygonBounds(pts)
print outRect
#print outRect['center'], outRect["nw"], outRect["ne"], outRect["sw"], outRect["se"]

## x Line
xLines = calcLatsInPolygon(outRect, spacing)
print xLines

## Traversing each x Line
line = []
for i in range(xLines["lines"]):
    ## Traversing each polygon vertex
    for j in range(len(pts)):
        print i, j
        point = calcPointInLineWithY((pts[j][0], pts[j][1]), (pts[si(j+1, len(pts))][0], 
                                      pts[si(j+1, len(pts))][1]), 
                                      outRect["nw"][0] - i * xLines["x"])
        if point != False and i+j >0:
            print point
            line = np.append(line, point)

line = line.reshape(line.shape[0]/2, 2)
line = line.astype(np.int)
print line

path = []
for i in range(line.shape[0] -1):
    if (i+4) % 4 == 3:
        path = np.append(path, line[i-1])            
    elif (i+4) % 4 == 2:
        path = np.append(path, line[i+1])
    elif (i+4) % 4 == 1:
        path = np.append(path, line[i])
    else:
        path = np.append(path, line[i])
    print i, path
path = path.reshape(path.shape[0]/2, 2)
path = path.astype(np.int)
print path

img = np.full((300,300,3), 128, dtype=np.uint8)
cv2.polylines(img, [pts], True, (255,0,0), 1)
cv2.polylines(img, [path], False, (0,0,255), 2)

cv2.imshow('', img)
k = cv2.waitKey(0)
if k==27:
    cv2.destroyAllWindows()
