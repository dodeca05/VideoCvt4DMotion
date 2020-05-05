import Load
import os
import struct
import numpy as np

def smoothing(X,size=101):
    avg=sum(X)
    avg/=len(X)
    if size%2==0:
        size+=1
    result=[]
    for i in range(len(X)):
        sumv=0
        for j in range(i-(size//2),i+(size//2)+1):
            if j<0 or j>=len(X):
                sumv+=avg
            else:
                sumv+=X[j]
        result.append(sumv/size)
    return result

def play_video(VideoPath, name):
    print("데이터 파일 생성")
    vs = VideoPath.split("/")
    temp = vs[-1]
    temp = temp.split("_")
    temp2 = str(temp[0]).split(".")
    temp2 = temp2[0]
    #videonum = int(temp[0])
    videonum = 0
    result = []
    result.append(0)

    while True:
        #if os.path.exists("./" + str(videonum) + "_" + temp[len(temp) - 1]):
        if os.path.exists("./" + name + "_4ds/" + str(videonum) + "_" + temp2 + ".4ds"):
            #Load.analysis("./" + str(videonum) + "_" + temp[len(temp) - 1], name)

            file = open("./" + name + "_4ds/" + str(videonum) + "_" + temp2 + ".4ds")
            data = np.fromfile(file, dtype = int)
            result[0] += data[0]
            for i in range(1, len(data)):
                result.append(data[i])
            file.close()
            os.remove("./" + name + "_4ds/"  + str(videonum) + "_" + temp2 + ".4ds")
            videonum += 1
        else:
            xlist = []
            ylist = []
            zlist = []
            for i in range(1, len(result), 3):
                xlist.append(result[i])
            for i in range(2, len(result), 3):
                ylist.append(result[i])
            for i in range(3, len(result), 3):
                zlist.append(result[i])
            xlist = smoothing(xlist)
            ylist = smoothing(ylist)
            zlist = smoothing(zlist)
            idx = 0
            final = []
            final.append(result[0])
            for i in range(1, len(result)):
                if i%3==1:
                    final.append(xlist[idx])
                elif i%3==2:
                    final.append(ylist[idx])
                else:
                    final.append(zlist[idx])
                    idx += 1
            file = open(temp2 + ".4ds", "wb")
            final = np.multiply(final, 2)
            final[0] = final[0] / 2
            for i in range(len(final)):
                bf = struct.pack("i", int(final[i]))
                file.write(bf)
            file.close()
            print("데이터 생성 완료")
            break
