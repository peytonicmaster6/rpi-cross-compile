import numpy as np
import cv2
import time
from threading import Thread
#import psutil

class VideoGet():
    
    def __init__(self, src, frameHeight = 480, frameWidth = 640):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(3, frameWidth)
        self.cap.set(4, frameHeight)
        #self.cap.set(cv2.CAP_PROP_FPS, 40)
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False
    
    def start(self):
        Thread(target=self.get, args=()).start()
        return self
        
    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.grabbed, self.frame = self.cap.read()
                
    
    def stop(self):
        self.stopped = True

class VideoShow():

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
    
    def start(self):
        Thread(target=self.show, args=()).start()
        return self
    
    def show(self):
        #cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        while not self.stopped:
            if self.frame is not None:
                cv2.imshow("Video", self.frame)
                self.frame = None
            
            if cv2.waitKey(1) == ord("q"): #or KeyboardInterrupt:
            #if N_frames > max_frames or cv2.waitKey(1) == ord("q"):

                self.stopped = True
                    
    def stop(self):
        cv2.destroyAllWindows()
        self.stopped = True
        
def BarrelDistortion():
    width = 640
    height = 480
    
    distCoeff = np.zeros((4,1),np.float64)
        
    k1 = 5.0e-5
    k2 = 0.0
    p1 = 0.0
    p2 = 0.0
    
    distCoeff[0,0] = k1
    distCoeff[1,0] = k2
    distCoeff[2,0] = p1
    distCoeff[3,0] = p2
    
    cam = np.eye(3,dtype=np.float32)
    
    cam[0,2] = width/2.0
    cam[1,2] = height/2.0
    cam[0,0] = 8
    cam[1,1] = 8
    
    global map1
    global map2
    
    map1, map2 = cv2.initUndistortRectifyMap(cam, distCoeff, None, None, (640,480), cv2.CV_16SC2)


    return map1, map2

def main():
    
    frames = []
    print(len(frames))
    
    cap = VideoGet(0).start()
    cap2 = VideoGet(1).start()
    
    stream = VideoShow().start()
    
    #BarrelDistortion()
    
    print("Recording...")
    
    start = time.time()
    while True:
        if stream.stopped or cap.stopped or cap2.stopped:
            break
        
        img = cap.frame
        img2 = cap2.frame
        
        #cv2.putText(img, str(psutil.cpu_percent(percpu=True)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        
        #dst = cv2.remap(img, map1, map2, 3)
        #dst2 = cv2.remap(img2, map1, map2, 3)
        
        stereo = np.hstack((img, img2))
        stream.frame = stereo
        
        frames.append(stereo)
        
    print("finishing...")
    print(len(frames))
    stop = time.time()
    stream.stop()
    cap.stop()
    #cap2.stop()
    
    print("FPS: ", str(len(frames)/(stop - start)))

if __name__ == "__main__":
    main()    
