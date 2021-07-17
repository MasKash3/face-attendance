import cv2
import numpy as np
import face_recognition

# RESCALING THE IMAGES
jordan_first = face_recognition.load_image_file('Pictures/jordan_first.jpg')
scale_percentage = 30
width = int(jordan_first.shape[1] * scale_percentage / 100)
height = int(jordan_first.shape[0] * scale_percentage / 100)
dim = (width, height)
imgJordan = cv2.resize(jordan_first, dim, interpolation=cv2.INTER_AREA)

jordan_second = face_recognition.load_image_file('Pictures/jordan_second.png')
scale_percentage = 100
width = int(imgJordan.shape[1] * scale_percentage / 100)
height = int(imgJordan.shape[0] * scale_percentage / 100)
dim = (width, height)
jordan_2_resized = cv2.resize(jordan_second, dim, interpolation=cv2.INTER_AREA)

imgJordan = cv2.cvtColor(imgJordan, cv2.COLOR_BGR2RGB)
imgJordanTest = cv2.cvtColor(jordan_2_resized, cv2.COLOR_BGR2RGB)

# MANUAL PROCESS, FOR DEMONSTRATION ONLY

# 0 because we are sending a single image, so we only need the first element
faceLoc = face_recognition.face_locations(imgJordan)[0]
# encode face
encodeJordan = face_recognition.face_encodings(imgJordan)[0]
cv2.rectangle(imgJordan, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(imgJordanTest)[0]
encodeJordanTest = face_recognition.face_encodings(imgJordanTest)[0]
cv2.rectangle(imgJordanTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

# compare encoding between the faces
# To test, print results. If true, faces are matching
results = face_recognition.compare_faces([encodeJordan],encodeJordanTest)
# Lower the distance, better the match
faceDis = face_recognition.face_distance([encodeJordan], encodeJordanTest)
print(faceDis)

cv2.imshow('Jordan', imgJordan)
cv2.imshow('Jordan Second', imgJordanTest)
cv2.waitKey(0)
