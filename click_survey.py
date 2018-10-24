import numpy as np
import cv2
import time

## coordinate of parallelogram
#pts = np.array([(10,10), (230,100), (290,200), (200,290), (100,240)])
#pts = np.array([(10,10), (230,100), (279,150), (280,290), (100,240)])

class click:
    #pts = np.array([], dtype='int32')
    #pts = np.array([[133,29], [40,104], [42,220], [175,276], [239,194], [232,86]])
    pts = np.array([(10,10), (230,100), (280,150), (280,290), (100,240)])

## parameter
spacing = 5  # distance between paths

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
    return [round(x), round(y)]

def createPolygonBounds(points):
    x = []
    y = []
    
    for i in range(len(points)):
        x.append(click.pts[i][0])
        y.append(click.pts[i][1])

    max_x = max(x)
    max_y = max(y)
    min_x = min(x)
    min_y = min(y)

    center = ((max_x +min_x)/2, (max_y +min_y)/2)
    nw = (max_x, min_y)
    ne = (max_x, max_y)
    sw = (min_x, max_y)
    se = (min_x, min_y)
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

def calculate():
    ## External Rectangle
    outRect = createPolygonBounds(click.pts)

    ## x Line
    xLines = calcLatsInPolygon(outRect, spacing)

    ## Traversing each x Line
    line = []
    path = []
    for i in range(xLines["lines"]+4):
        ## Traversing each polygon vertex
        line = []
        for j in range(len(click.pts)):
            print i, j
            point = calcPointInLineWithY((click.pts[j][0], click.pts[j][1]), (click.pts[si(j+1, len(click.pts))][0], 
                                          click.pts[si(j+1, len(click.pts))][1]), 
                                          outRect["nw"][0] - i * xLines["x"])
            if point != False:
                print point
                line = np.append(line, point)
                line = line.reshape(line.shape[0]/2, 2)

        if len(line) < 2:
            continue
        if line[0][0] == line[1][0]:
            continue
        path = np.append(path, [line[0],line[1]])
        
    path = path.reshape(path.shape[0]/2, 2)
    path = path.astype(np.int)
    print path
    return path

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        #cv2.circle(img, (x,y), 50, (0,0,255), thickness=-1)
        click.pts = np.append(click.pts, (x,y))
        click.pts = click.pts.reshape(click.pts.shape[0]/2, 2)
        print click.pts

## display and mouse event setting
img = np.full((300,300,3), 128, dtype=np.uint8)
cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("img", mouse_event)
while True:
    cv2.polylines(img, [click.pts], True, (255,0,0), 1)
    cv2.imshow("img", img)
    k = cv2.waitKey(0)
    if k==27:
        break
    if k==ord("c"):
        path = calculate()
        cv2.polylines(img, [path], False, (0,0,255), 2)
    if k==ord("r"):
        click.pts = np.array([], dtype='int32')
        img = np.full((300,300,3), 128, dtype=np.uint8)
cv2.destroyAllWindows()
