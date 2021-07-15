import os

from kivy.app import App
from kivy.uix.label import Label
import cv2
import numpy as np
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

class FaceTrackingKivy(App):
    def build(self):

        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            print(np.shape(frame))
            gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray_roi,
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(60,60)
            )
            for (x,y,w,h) in faces:
                video_cap = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

            cv2.imshow('video_cap',frame)

            if cv2.waitKey(1) & 0XFF == ord('q'):
                break
                cap.release()
                cv2.destroyAllWindows()



if __name__ == '__main__':
    FaceTrackingKivy().run()

