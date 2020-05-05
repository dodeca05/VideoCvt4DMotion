"""
기존 -> 영상 전체 픽셀에 대한 크기 값과 각도를 계산
개선방안
main object detection 수행
해당 물체에 대한 각도를 계산
1. Invert Color
2. Sobel filter
3. Gaussian blur
4. Thresholding
5. Caculate degree
https://making.lyst.com/2014/02/13/background-removal
"""
import numpy as np
import cv2
import pickle
import sys

def angle(videopath, prc, name, number, num=0):
    cap = cv2.VideoCapture(videopath)
    frame_all = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cnt = 0
    Log = []
    i = 1
    #정규화 블러 처리 필요
    while True:
        ret, frame = cap.read()
        prc.setStep(int(cap.get(cv2.CAP_PROP_POS_FRAMES)/frame_all*100))
        if not ret:
            break;

        img = np.float32(frame) / 255.0
        gx = cv2.Sobel(img, cv2.CV_32F, 1, 0, ksize=1)
        gy = cv2.Sobel(img, cv2.CV_32F, 0, 1, ksize=1)
        mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
        mag_sum = 0
        total = 0
        mag = mag.flatten()
        angle = angle.flatten()
        total = np.multiply(mag, angle)
        mag = abs(mag)
        mag_sum = np.sum(mag)
        if mag_sum == 0:
            result = 180
        else:
            result = np.sum(total) / mag_sum
        result = result - 180
        result = -result
        cnt += 1
        if cnt == int(frame_all * (i / 10)):
            print("{0}% 진행".format(i * 10))
            i += 1
        Log.append(result)

    print("done")
    with open("./" + name + "_xpos/" + number + "_" + name + "_xpos.pkl", 'wb') as f:
            pickle.dump(Log, f)
            
    return
