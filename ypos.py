#블러 처리?
import numpy as np
import cv2 as cv
import pickle

term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )
class Point:
    def __init__(self,roi,roiSize):
        self.frist_window=roiSize
        self.s=0
        self.roi=roi
        self.hsv_roi=cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        self.mask = cv.inRange(self.hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        self.roi_hist = cv.calcHist([self.hsv_roi],[0],self.mask,[180],[0,180])
        self.track_window=roiSize
        cv.normalize(self.roi_hist,self.roi_hist,0,255,cv.NORM_MINMAX)

    def track(self,hsvf):
        #hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsvf],[0],self.roi_hist,[0,180],1)
        ret, Ntrack_window = cv.meanShift(dst, self.track_window, term_crit)
        x1,y1,w1,h1=self.track_window
        x2,y2,w2,h2=Ntrack_window
        self.track_window=Ntrack_window
        self.s=self.s+np.sqrt((x2-x1)**2+(y2-y1)**2)
        return self.track_window
#######################################


def Tracking(videopath, prc, name, number, num=0):
    cap = cv.VideoCapture(videopath)
    ret,frame=cap.read()
    frame_all = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    cnt = 0
    i = 1
    pointlst=[]
    height, width, _ = frame.shape
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    retval, thresh_gray = cv.threshold(gray, thresh=50, maxval=200, \
                                   type=cv.THRESH_BINARY_INV)

    image, contours, hierarchy = cv.findContours(thresh_gray,cv.RETR_LIST, \
                                   cv.CHAIN_APPROX_SIMPLE)
    # Find object with the biggest bounding box
    mx = (0,0,0,0)      # biggest bounding box so far
    mx_area = 0
    for cont in contours:
        x,y,w,h = cv.boundingRect(cont)
        area = w*h
        if area > (height*width)*(3/5) or area < 1000:
            continue
        if area > mx_area:
            mx = x,y,w,h
            mx_area = area
    x,y,w,h = mx
    cnt += 1
    if not(x ==0 and y ==0 and w == 0 and h == 0):
        p = Point(frame[y:y+h, x:x+w], (x, y, w, h))
    Log=[[(y+h)//2,(x+w)//2]]
    while True:
        prc.setStep(int(cap.get(cv.CAP_PROP_POS_FRAMES)/cap.get(cv.CAP_PROP_FRAME_COUNT)*100))
        ret ,frame = cap.read()
       
        if not ret:
            break;
        hsv=cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        if not(x ==0 and y ==0 and w == 0 and h == 0):
            x,y,w,h=p.track(hsv)
        #img2 = cv.rectangle(frame, (x,y), (x+w,y+h), 255,2)
        cnt += 1
        if cnt == int(frame_all * (i / 10)):
            print("{0}% 진행".format(i * 10))
            i += 1
        Log.append([x+(w/2),y+(h/2)])
        
##        cv.imshow('img2',img2)
##        k = cv.waitKey(60) & 0xff
##        if k == 27:
##            break
    with open("./" + name + "_ypos/" + number + "_" + name + "_ypos.pkl", 'wb') as f:
        pickle.dump(Log, f)
        
    return
