import numpy as np
import cv2
import time
import psutil

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

cap1 = cv2.VideoCapture(1)
cap1.set(3, frameWidth)
cap1.set(4, frameHeight)

#cap.set(cv2.CAP_PROP_FPS, 40)
#cap1.set(cv2.CAP_PROP_FPS, 40)


#img2 = img
#time = datetime.datetime.now()
#current_time = time.strftime("%H:%M:%S")
#cv2.putText(img, current_time, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)

#width = img.shape[1]
#height = img.shape[0]

distCoeff = np.zeros((4,1),np.float64)

k1 = 5.0e-5;
k2 = 0.0
p1 = 0.0
p2 = 0.0

distCoeff[0,0] = k1
distCoeff[1,0] = k2
distCoeff[2,0] = p1
distCoeff[3,0] = p2

cam = np.eye(3,dtype=np.float32)

cam[0,2] = frameWidth/2.0
cam[1,2] = frameHeight/2.0
cam[0,0] = 10.
cam[1,1] = 10.

map1, map2 = cv2.initUndistortRectifyMap(cam, distCoeff, None, None, (640,480), cv2.CV_16SC2)

frames = []
start = time.time()
#cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    sucess, img = cap.read()
    sucess2, img2 = cap1.read()
    cv2.putText(img, str(psutil.cpu_percent(percpu=True)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
    dst = cv2.remap(img, map1, map2, 3)
    dst2 = cv2.remap(img2, map1, map2, 3)
    #k12 = 1.0e-4
    #distCoeff[0,0] = k12
    
    #dst2 = cv2.undistort(img2,cam,distCoeff)
    
    numpy_horizontal = np.hstack((dst, dst2))
    frames.append(numpy_horizontal)
    cv2.imshow("Video", numpy_horizontal)
    
    #print("CPU Load: " + str(psutil.cpu_percent(percpu=True)) + "%  " + \
         #"Mem Usage: " + str(psutil.virtual_memory().percent) + "%")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

stop = time.time()
print("FPS: ", str(len(frames) / (stop-start)))
cv2.waitKey(0)
cv2.destroyAllWindows()
    