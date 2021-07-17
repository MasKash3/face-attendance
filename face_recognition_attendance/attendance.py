import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from xlwt import Workbook
import time

path = 'Pictures'
images = []
classNames = []
details = []
names = []
surnames = []
imageList = os.listdir(path)

# Read images and get rid of extensions

for cl in imageList:
    currImg = cv2.imread(f'{path}/{cl}')
    images.append(currImg)
    classNames.append(os.path.splitext(cl)[0])  # gets rid of the extensions

# Store names and surnames

for i in range(len(classNames)):
    details.append(classNames[i].split())

for j in range(len(details)):
    names.append(details[j][0])
    surnames.append(details[j][1])


# End store names and surnames

# Database

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error in creating directory: ' + directory)


createFolder('Excel')

record_check = os.listdir('Excel')

# create excel sheet and names from pictures
if 'client_record.xls' not in record_check:
    wb = Workbook()
    sheet1 = wb.add_sheet('sheet 1')
    for i in range(2):
        sheet1.col(i).width = 5000
    sheet1.write(0, 0, 'Name')
    sheet1.write(0, 1, 'Surname')
    wb.save("Excel/client_record.xls")
    k = 0
    for k in range(len(details)):
        sheet1.col(k).width = 5000
        sheet1.write(k + 1, 0, names[k].upper())
        sheet1.write(k + 1, 1, surnames[k].upper())
        wb.save("Excel/client_record.xls")

print('\nStored images and names added to database!\n')

time.sleep(1)

print('Encoding in progress...\n')


# Encoding images

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# End encoding images

encodeListKnown = findEncodings(images)
print('Encoding complete\n')

# OPEN CV read camera and match
print('Looking for a registered face...')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # 0.25 are the scales, 1/4th of the size
    # We do that to reduce the size and speed up the process
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceLocInFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceLocInFrame)

    for encodeFace, faceLoc in zip(encodeCurrFrame, faceLocInFrame):  # zip because we are using them in the same loop
        # compare encodings of saved faces compares to video from stream
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # lowest face distance means better match
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            # Since we were working on 1/4th the size, we need to go back to normal size
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # From here it's just for beauty
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        cv2.destroyAllWindows()
