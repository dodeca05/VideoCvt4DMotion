import cv2
import numpy as np
import pickle
import math
cameraangle=120#카메라 화각

def horizon(videopath, prc, name, number):
    cap = cv2.VideoCapture(videopath)
    frame_all = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cnt = 0
    per = 1
    Log = []
    print("zpos")
    while True:
        prc.setStep(int(cap.get(cv2.CAP_PROP_POS_FRAMES)/cap.get(cv2.CAP_PROP_FRAME_COUNT)*100))
        ret, frame = cap.read()
        state = True

        if not ret:
            break;

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray,50,150,apertureSize=3)
        interval = 10
        for i in range(100,1000,interval):
            lines = cv2.HoughLines(edges,1,np.pi/180,i)
            if lines is None:
                state = False
                break;
##            elif len(lines)<=10:
##                interval = 5
            elif len(lines)<=5:
                break;

        if state:
            DB=[]
            for i in range(len(lines)):
                for rho, theta in lines[i]:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a*rho
                    y0 = b*rho
    ##                if abs(a/b)<1:
    ##                    continue
                    #print(a/b," : ",np.degrees(np.arctan(a/b)))
                   
                    x1 = int(x0 + 1000*(-b))
                    y1 = int(y0+1000*(a))
                    x2 = int(x0 - 1000*(-b))
                    y2 = int(y0 -1000*(a))
                    #cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),2)
                    
                    x3=int(x1+(x2-x1)*((int(len(frame)/2)-y1)/(y2-y1)))
                    #print("X3 = ",x3)
                    #cv2.circle(img,(x3,midY),10,(0,255,0),-1)
                    #print("P1:",x1, y1)
                    #print("P2:",x2, y2)
                    #print("========================")
                    DB.append([np.arctan(a/b),x3])
            avg=0
            for i,x in DB:
                avg+=i
            avg/=len(DB)
                
            avg1=0#각도
            avx1=0#직선의 위치 y값
            avc1=0#갯수
            avg2=0
            avx2=0
            avc2=0
            for i,x in DB:
                if i>avg:
                    avg1+=i
                    avc1+=1
                    avx1+=x
                else:
                    avg2+=i
                    avc2+=1
                    avx2+=x


            avg2=avg2/avc2
            avx2=avx2/avc2
            if avc1==0:
                avg1=avg2
            else :
                avg1=avg1/avc1
                avx1=avx1/avc1
            #print(np.degrees(avg1),"/",np.degrees(avg),"/",np.degrees(avg2))
            #print(avx1,"/",avx2)
            T=1
            if avx1>avx2:
                avg1,avg2=avg2,avg1
            degree=0
            if avg1>0 and avg2>0:
                if avg2>avg1:
                    degree=np.radians(180)-avg1-(np.radians(180)-avg2)
                else :
                    degree=np.radians(180)-avg2-(np.radians(180)-avg1)
                    T=-1
            elif avg1>0 and avg2<0:
                degree=np.radians(180)-avg1+avg2
            elif avg1<0 and avg2>0:
                degree=np.radians(180)+avg1-avg2
                T=-1

            cnt += 1
            if cnt == int(frame_all * (per / 10)):
                print("{0}% 진행".format(per * 10))
                per += 1
            Log.append(np.degrees(np.arctan(degree))*T/180*cameraangle)

        else:
            Log.append(0)
            state = True
        
    print("done")
    with open("./" + name + "_zpos/" + number + "_" + name + "_zpos.pkl", 'wb') as f:
            pickle.dump(Log, f)
            
    return
