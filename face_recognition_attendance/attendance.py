import sys
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import xlrd
from xlwt import Workbook
import time
import delete_file
delete_file.deleteFile()

path = 'Pictures'
images = []
classNames = []
details = []
names = []
surnames = []

# Excel files

wb = Workbook()
sheet1 = wb.add_sheet('sheet 1')

# Get directory for images location

imageList = os.listdir(path)

# Read images and get rid of extensions

for cl in imageList:
    currImg = cv2.imread(f'{path}/{cl}')
    images.append(currImg)
    classNames.append(os.path.splitext(cl)[0])  # gets rid of the extensions

# Store names and surnames separately

for i in range(len(classNames)):
    details.append(classNames[i].split())

for j in range(len(details)):
    names.append(details[j][0])
    surnames.append(details[j][1])


# Create Excel database folder

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error in creating directory: ' + directory)


createFolder('Excel')

record_check = os.listdir('Excel')


# Marking attendance function

def markAttendance(name, surname):
    data = xlrd.open_workbook("Excel/client_record.xls")
    table = data.sheet_by_index(0)
    for i in range(len(details)):
        if table.cell(i + 1, 2).value is not None:
            try:
                for k in range(len(details)):
                    if name == names[k].upper() and surname == surnames[k].upper():
                        sheet1.write(k + 1, 2, 'Yes')
                        wb.save("Excel/client_record.xls")
                        now = datetime.now()
                        dateString = now.strftime('%H:%M:%S')
                        sheet1.write(k + 1, 3, dateString)
                        wb.save('Excel/client_record.xls')
                print('\nAttendance registered!\nNext person please!\n')
                time.sleep(3)
                cap
            except:
                print('Attendance already registered.')
                pass
        else:
            pass


# create excel sheet and add names from images

if 'client_record.xls' not in record_check:
    for i in range(4):
        sheet1.col(i).width = 5000
    sheet1.write(0, 0, 'Name')
    sheet1.write(0, 1, 'Surname')
    sheet1.write(0, 2, 'Present')
    sheet1.write(0, 3, 'Time in')
    wb.save("Excel/client_record.xls")
    k = 0
    for k in range(len(details)):
        sheet1.col(k).width = 5000
        sheet1.write(k + 1, 0, names[k].upper())
        sheet1.write(k + 1, 1, surnames[k].upper())
        wb.save("Excel/client_record.xls")

print('\nStored images and names added to database!\n')

time.sleep(1)


# Encoding images function

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# Speed up image encoding

if os.path.exists('encodedImages.npy'):
    print('Encoded database found\nLoading encoded images...\n')
    encodeListKnown = np.load('encodedImages.npy')
    print('Loading complete!\n')
else:
    print('No encoded database found.\nEncoding in progress...\n')
    encodeListKnown = findEncodings(images)
    np.save('encodedImages.npy', np.asarray(encodeListKnown))
    print('Encoding complete\n')

# OPEN CV read camera and face matching

print('Looking for a registered face...')

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # 0.25 are the scales, 1/4th of the size
    # We do that to reduce the video feed size and speed up the process
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceLocInFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceLocInFrame)

    for encodeFace, faceLoc in zip(encodeCurrFrame, faceLocInFrame):  # zip because we are using them in the same loop
        # compare encodings of saved faces to the one from the video stream
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # lowest face distance means better match
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            fullName = classNames[matchIndex].upper()
            name = fullName.split()[0]
            surname = fullName.split()[1]
            print('\nFace found: ' + name, surname)
            y1, x2, y2, x1 = faceLoc
            # Since I was working on 1/4th of the initial size, we need to go back to normal size
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # From here it's just for looking good
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, fullName, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            markAttendance(name, surname)

            cap.release

    cv2.imshow('Camera', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        cv2.destroyAllWindows()
