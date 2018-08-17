import cv2
import numpy as np
from pynput.mouse import Button,Controller
import wx
mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
#print(sx,sy)
(camx,camy)=(320,240)
cap=cv2.VideoCapture(0)
#Here I am checking that is it the camera is working and if not print the message
if(cap.isOpened()==False):
    print("Error in opening camera")
#The loop will execute until the camera is open or esc not pressed
while(cap.isOpened()):

    ret,frame=cap.read()
    
    #Here I am flipping the frame vertically
    frame=cv2.flip(frame,1)

    #Region of Interest 
    image=frame[100:400,50:300]
    
    #A Rectangle at region of interest
    cv2.rectangle(frame,(50,100),(300,400),(0,255,0),0)
    
    #convert bgr to gray
    img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    #reducing noise using GaussianBlur method
    blur=cv2.GaussianBlur(img,(35,35),0)
    ret,thresh = cv2.threshold(blur,0,255,1+cv2.THRESH_OTSU)

    #find contours
    _,contours,hierarchy=cv2.findContours(thresh,1,1)
    max_area=0
    pos=0
    for i in contours:
        area=cv2.contourArea(i)
        if area>max_area:
            max_area=area
            pos=i
    peri=cv2.arcLength(pos,True)
    approx=cv2.approxPolyDP(pos,0.02*peri,True)
    hull=cv2.convexHull(pos)
    cv2.drawContours(image,[hull],-1,(0,0,255),2)
    hull=cv2.convexHull(pos,returnPoints=False)
    defects=cv2.convexityDefects(pos,hull)
    num=0
    l=defects.shape[0]
    for i in range(1,defects.shape[0]):
        s,e,f,d=defects[i,0]
        far=tuple(pos[f][0])
        if d>10000:
            num+=1
            cv2.circle(image,far,3,[0,0,255],-1)
    num+=1
    if num==1:
        s="CLICK"
        mouse.click(Button.left,1)
        #mouse.press(Button.left)
        #mouse.release(Button.left)
        #print("left button pressed")
        #mouse.release(Button.left);#print("left button released")

    elif num==2:
        s="LEFT"
        mouse.move(-5,0)
        
    elif num==3:
        s="RIGHT"
        mouse.move(5,0)
    elif num==4:
        s="DOWN"
        mouse.move(0,5)
    elif num==5:
        s="UP"
        mouse.move(0,-5)
    else:
        s="WRONG INPUT"
        #mouse.release(Button.left)
    frame[100:400,50:300]=image
    font=cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame,s,(100,450), font, 2,(255,10,10),2,cv2.LINE_AA)

    #Here I am showing the frame
    cv2.imshow("Frame",frame)

    #cv2.imshow("Thresh",thresh)
    
    #This is to stop the execution of frame by pressing esc
    if cv2.waitKey(1)== 27:
      break
    

cap.release()
cv2.destroyAllWindows()

