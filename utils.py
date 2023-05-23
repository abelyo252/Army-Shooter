
import cv2
import mediapipe as mp
import math


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose   = mpPose.Pose(static_image_mode= False, smooth_landmarks=True,
                                     min_detection_confidence=0.8,
                                     min_tracking_confidence=0.8)


def findPose(img, draw=True, bboxWithHands=False):

    lmList = []
    bboxInfo = {}

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        #if draw:
            #mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy, cz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
            lmList.append([id, cx, cy, cz])

        # Bounding Box
        ad = abs(lmList[12][1] - lmList[11][1]) // 2
        if bboxWithHands:
            x1 = lmList[16][1] - ad
            x2 = lmList[15][1] + ad
        else:
            x1 = lmList[12][1] - ad
            x2 = lmList[11][1] + ad

        y2 = lmList[29][2] + ad
        y1 = lmList[1][2] - ad
        bbox = (x1, y1, x2 - x1, y2 - y1)
        cx, cy = bbox[0] + (bbox[2] // 2), \
                 bbox[1] + bbox[3] // 2

        shot = (lmList[0][1], lmList[0][2])

        cv2.circle(img, shot , 6, (0, 0, 255), -1)


        return bbox , shot

    else:
        return None,None


def trucate(number,decimals=0):
    if not isinstance(decimals,int):
        raise TypeError("Decimal place must be integer")

    elif decimals<0:
        raise ValueError("Decimal place has to be 0 or more")

    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number*factor) / factor






def fancyDraw(img, bbox ,text="" ,l=10 , sl = 10, t=5, rt=1 , alpha = 0.75 , shot = False):


    overlay = img.copy()
    eh ,ew , _ =  img.shape

    x, y, w, h = bbox
    start , end = (x, y) , (x+w, y+h)
    c1,c2 = x,y

    shotBox = [x+sl, y+sl, (w-(2*sl)), (h-(2*sl))]
    sx, sy, sw, sh = shotBox
    start2, end2 = (sx, sy), (sx + sw, sy + sh)
    x1, y1 = x + w, y + h


    if rt != 0:
        cv2.rectangle(img, start, end , (255, 255, 255), rt)

        # Top Left  x,y
        cv2.line(img, (x, y), (x + l, y), (0, 0, 255), t)
        cv2.line(img, (x, y), (x, y + l), (0, 0, 255), t)
        # Top Right  x1,y
        cv2.line(img, (x1, y), (x1 - l, y), (0, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (0, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(img, (x, y1), (x + l, y1), (0, 0, 255), t)
        cv2.line(img, (x, y1), (x, y1 - l), (0, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (0, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (0, 0, 255), t)

        cv2.line(img, (x + w // 2, y), (x + w // 2, 0), (255, 255, 255), rt)
        cv2.line(img, (x + w // 2, y + h), (x + w // 2, eh), (255, 255, 255), rt)
        cv2.line(img, (x, y + h // 2), (0, y + h // 2), (255, 255, 255), rt)
        cv2.line(img, (x + w, y + h // 2), (ew, y + h // 2), (255, 255, 255), rt)

    cv2.rectangle(img, start2, end2 , (0, 0, 255), -1)
    img_overlay = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    return img_overlay

