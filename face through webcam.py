import cv2
import numpy as np

w, h = 640, 480
fbRange = [6200, 6800]
pid = [0, 5, 0.5, 0]
pError = 0

##turning the picture in gray color.

def findFace(img):
    faceCascade = cv2.CascadeClassifier ( "Resources/haarcascade_frontalface_default.xml" )
    imgGray = cv2.cvtColor ( img, cv2.COLOR_BGR2GRAY )
    faces = faceCascade.detectMultiScale ( imgGray, 1.1, 8 )

    myFaceListC = []
    myFaceListArea = []

    ##Making a rectangle to follow my face and the center is denoted by a circle.

    for (x, y, w, h) in faces:
        cv2.rectangle ( img, (x, y), (x + w, y + h), (0, 0, 255), 2 )
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle ( img, (cx, cy), 5, (0, 255, 0), cv2.FILLED )
        myFaceListC.append ( [cx, cy] )
        myFaceListArea.append ( area )
    # Lenght
    if len(myFaceListArea ) != 0:
        i = myFaceListArea.index ( max ( myFaceListArea ) )
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w//2
    speed = pid[0]*error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20



    if x == 0:
        speed = 0
        error = 0

    print ( speed, fb )

    #me.send_rc_control(0, fb, 0, speed)
    return error

cap = cv2.VideoCapture ( 0 )

while True:
    _, img = cap.read ()
    img = cv2.resize(img, (w, h))
    img, info = findFace ( img )
    pError = trackFace ( info, w, pid, pError )
    #print ( "Center", info[0], "Area", info[1] )
    cv2.imshow ( "Output", img )

    cv2.waitKey(1)
