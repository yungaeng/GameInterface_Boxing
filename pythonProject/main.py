import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector

import socket

width, height = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

hand_detector = HandDetector(maxHands=2, detectionCon=0.8)
face_detector = FaceDetector()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 10500)

while True:
    success, img = cap.read()

    hands, img = hand_detector.findHands(img)
    img, bboxs = face_detector.findFaces(img)

    hand_data = []

    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        print(lmList)
        for lm in lmList:
            hand_data.extend([lm[0], height - lm[1], lm[2]])
        sock.sendto(str.encode(str(hand_data)), serverAddressPort)

    cv2.imshow("image", img)
    cv2.waitKey(1)