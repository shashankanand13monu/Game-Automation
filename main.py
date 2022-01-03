import cv2
import mediapipe as mp
import time
video= cv2.VideoCapture(0)
import pyautogui
import  pydirectinput
# from tensorflow.keras.models import load_model
mp_draw= mp.solutions.drawing_utils
mp_hand= mp.solutions.hands
import numpy as np
previousTime = 0
currentTime = 0
tipIds= [4,8,12,16,20]
classNames= ['okay', 'peace', 'thumbs up', 'thumbs down', 'call me', 'stop', 'rock', 'live long', 'fist', 'smile']
from directkeys import ReleaseKey,PressKey, W, A, S, D
# ------------------------------------------------------------
import webbrowser

url = 'http://google.com/'


# Windows
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'


# model = load_model('mp_hand_gesture')




# --------------------------------------------------------------



with mp_hand.Hands(max_num_hands=1,min_detection_confidence=0.5,min_tracking_confidence=0.5) as hands:

    while True:
        ret, image= video.read()
        image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        image.flags.writeable=False #To improve performance, optionally mark the image as not writeable to
                                    # pass by reference

        results= hands.process(image)
        image.flags.writeable=True
        image= cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        
        # Calculating the FPS
        currentTime = time.time()
        fps = 1 / (currentTime-previousTime)
        previousTime = currentTime
        
        
        
        lmList=[]
        lmList2forModel=[]
        # Displaying FPS on the image
        cv2.putText(image, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                
                myHands=results.multi_hand_landmarks[0]
                for id,lm in enumerate(myHands.landmark):
                    h,w,c=image.shape
                    cx,cy=int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])
                    lmList2forModel.append([cx,cy])
                
                
                mp_draw.draw_landmarks(image,hand_landmark,mp_hand.HAND_CONNECTIONS,
            mp_draw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
            mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
            
                fingers=[]

               
                
                if len(lmList)!=0: # No Hand in BackGround
                    
#  ----------------------------------------------------------------------------------------------------------                   
                    #  # Predict gesture in Hand Gesture Recognition project
                    # prediction = model.predict([lmList2forModel])
                    # print(prediction)
                    # classID = np.argmax(prediction)
                    # className = classNames[classID]
                    # # show the prediction on the frame
                    # cv2.putText(image, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    #             1, (0,0,255), 2, cv2.LINE_AA)
#  ----------------------------------------------------------------------------------------------------------                   
                    
                    if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)  
                    
                    for id in range(1,5):
                        if lmList[tipIds[id]][2] < lmList[tipIds[id]-1][2]:
                            fingers.append(1)
                            
                        else:
                            fingers.append(0)
                    total= fingers.count(1)
                    # print(total)
                    if total==0:
                        print("Brake")
                        # webbrowser.get(chrome_path).open(url)
                        # pyautogui.press('w')
                        # pyautogui.keyDown('s')
                        # pydirectinput.press('S')
                        # pydirectinput.keyUp('w')
                        # pydirectinput.keyDown('s')
                        ReleaseKey(W)
                        ReleaseKey(A)
                        ReleaseKey(S)
                        PressKey(S)
                        time.sleep(2)
                        ReleaseKey(S)
                    elif total==5:
                        print("GAS")
                        ReleaseKey(S)
                        ReleaseKey(A)
                        ReleaseKey(S)
                        PressKey(W)
                        time.sleep(2)
                        ReleaseKey(W)
                        # pydirectinput.keyUp('s')
                        # pydirectinput.keyDown('w')        
                    elif total==4:
                        print("Right")
                        # ReleaseKey(W)
                        PressKey(D)
                        time.sleep(1)
                        ReleaseKey(D)
                    elif total==2:
                        print("LEFT")
                        
                        PressKey(A)
                        time.sleep(1)
                        ReleaseKey(A)
                   
                #    if lmList[8][2]<lmList[6][2]: 
                #         print("open")
                #    else:
                #     print("close") 
        
        cv2.imshow("Frame",image)
        k= cv2.waitKey(1)
        if k==ord('q'):
            break
        
video.release()
cv2.destroyAllWindows()