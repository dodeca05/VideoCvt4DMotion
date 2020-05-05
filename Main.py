import threading, time 
from tkinter.ttk import Progressbar, Frame 
from tkinter import *
import pross


root = Tk()
root.title("4D")
root.geometry("640x300")
root.resizable(False, False)

ft = Frame()
ft.pack()
class Progress:  
     
    kill_threads = False # variable to see if threads should be killed 

    def __init__(self,ft,maxval=100,r=0,c=0):
     self.val = IntVar() 
     self.ft=ft   
     self.pb = Progressbar(self.ft, length=500,orient="horizontal",maximum=maxval, mode="determinate",variable=self.val) 
     self.pb.grid(row=r,column=c,pady=30)
     self.maxval=maxval
     self.IsThRun=False
     #self.check_thread()

     

    def check_thread(self):
        if not self.IsThRun:
            self.IsThRun=True
            self.setStep0()
            threading.Thread(target=self.check_progress).start()
            
        
    def check_progress(self): 
     while True: 
      if self.kill_threads: # if window is closed 
       return    # return out of thread 
      val = self.val.get() 
      
      if val >= self.maxval: 
       self.finish()
       self.IsThRun=False
       return
      time.sleep(1)#테스트용 코드
      self.step(10)#테스트용 코드
        
      
    def setStep0(self):
        self.val.set(0)
    def setStep(self,val):
        self.val.set(val)
    def step(self,val):
        self.val.set(self.val.get()+val)
    def finish(self): 
     #self.ft.pack_forget() 
     print("Finish!")
     #self.setStep0()



lbl = Label(ft, text="전체작업진행률")
lbl.grid(row=0,column=0)
progressbar1 = Progress(ft,maxval=100,r=0,c=1)

lblm = Label(ft, text="작업중")
lblm.grid(row=1,column=1)

lbl = Label(ft, text="현재작업진행률")
lbl.grid(row=2,column=0)
progressbar2 = Progress(ft,r=2,c=1)

def buttonevent():
    Th=threading.Thread(target=pross.prc,args=(progressbar1,progressbar2,lblm))
    Th.start()
    
    

button1=Button(ft,text="분석",overrelief="solid", width=15, command=buttonevent, repeatdelay=1000, repeatinterval=100)
button1.grid(row=5,column=1,pady=30)


def on_closing():  # function run when closing 
    progressbar2.kill_threads = True # set the kill_thread attribute to tru 
    time.sleep(0.1) # wait to make sure that the loop reached the if statement 
    root.destroy() # then destroy the window 

root.protocol("WM_DELETE_WINDOW", on_closing) # bind a function to close button 

root.mainloop()


