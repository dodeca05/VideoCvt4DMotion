from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import xpos
import ypos
import zpos
import tkinter.messagebox as tmb
import Load as load
import DivideScene as ds
import shutil
import play

def prc(prgr1,prgr2,label):

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    VideoPath = askopenfilename(filetypes=[("mp4 files", "*.mp4"), ("avi files", "*.avi")])
    print(VideoPath)
    base = os.path.basename(VideoPath)
    head = os.path.splitext(base)
    name = head[0]
    save_dir = VideoPath.split('/')
    save = ''
    for s in save_dir[:-1]:
        save += s + '/'
    
    ####hist분석
    prgr1.setStep0()
    prgr2.setStep0()
    label.config(text="hist분석중 입니다")
    if not os.path.exists("./" + name + "_cut"):
            os.makedirs("./" + name + "_cut")
    if not os.path.exists("./" + name + "_hist"):
            os.makedirs("./" + name + "_hist")
    ds.SceneCut(VideoPath,prgr2,name)
   
    prgr1.step(int(100/6))
    
    ####x축
    prgr2.setStep0()

    path, dirs, files = next(os.walk("./" + name + "_cut"))
    num = len(files)
    #num = 5
    if not os.path.exists("./" + name + "_xpos"):
        os.makedirs("./" + name + "_xpos")
    for i in range(0, num):
        prgr1.setStep(int(100/6)+int(100/6/num*i))
        label.config(text="x축을 분석중 입니다("+str(i+1)+"/"+str(num)+")")
        temp = VideoPath.split('/')
        #temp[-1] = name + "_cut/" + str(i) + "_" + temp[-1]
        path2=path
        #path = ''
        #for s in temp:
        #    path += s + '/'
        #print(path[:-1])
        path2+="/"+str(i)+"_"+temp[-1]
        print(path2)
        xpos.angle(path2, prgr2, name=name, number = str(i))
    
    
    ####y축
    
    prgr2.setStep0()
    if not os.path.exists("./" + name + "_ypos"):
            os.makedirs("./" + name + "_ypos")

    for i in range(0, num):
        label.config(text="y축을 분석중 입니다("+str(i+1)+"/"+str(num)+")")
        prgr1.setStep(int(100/6)*2+int(100/6/num*i))
        temp = VideoPath.split('/')
        #temp[-1] = name + "_cut/" + str(i) + "_" + temp[-1]
        path2 = path
        #for s in temp:
        #    path += s + '/'
        #print(path[:-1])
        path2+="/"+str(i)+"_"+temp[-1]
        ypos.Tracking(path2, prgr2, name=name, number = str(i))
    
    
    ####z축
    
    prgr2.setStep0()
    if not os.path.exists("./" + name + "_zpos"):
            os.makedirs("./" + name + "_zpos")

    for i in range(0, num):
        label.config(text="z축을 분석중 입니다("+str(i+1)+"/"+str(num)+")")
        prgr1.setStep(int(100/6)*3+int(100/6/num*i))
        temp = VideoPath.split('/')
        #temp[-1] = name + "_cut/" + str(i) + "_" + temp[-1]
        path2 = path
        #for s in temp:
        #    path += s + '/'
        #print(path[:-1])
        path2+="/"+str(i)+"_"+temp[-1]
        zpos.horizon(path2, prgr2, name=name, number = str(i))
    
    
    ####퍼지
    label.config(text="시나리오를 작성중 입니다.")
    if not os.path.exists("./" + name + "_4ds"):
            os.makedirs("./" + name + "_4ds")
    prgr2.setStep0()
    for i in range(0, num):
        prgr1.setStep(int(100/6)*4+int(100/6/num*i))
        prgr2.setStep(int((i+1)/num*100))
        temp = VideoPath.split('/')
        #temp[-1] = name + "_cut/" + str(i) + "_" + temp[-1]
        path2 = path
        #for s in temp:
        #    path += s + '/'
        #print(path[:-1])
        path2+="/"+str(i)+"_"+temp[-1]
        load.analysis(path2, prgr2, name=name, number = str(i))
    shutil.rmtree("./" + name + "_hist")
    shutil.rmtree("./" + name + "_xpos")
    shutil.rmtree("./" + name + "_ypos")
    shutil.rmtree("./" + name + "_zpos")
        
    ####파일출력
    label.config(text="파일 출력 및 정리중 입니다.")
    prgr2.setStep(100)
    play.play_video(VideoPath, name, save)
    shutil.rmtree("./" + name + "_4ds")
    shutil.rmtree("./" + name + "_cut")
    prgr1.setStep(100)
    tmb.showinfo("정보","끝")
    
