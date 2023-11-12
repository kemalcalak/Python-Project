import numpy as np
import cv2
import imageProcesing as imgprocess

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    img = imgprocess.rec(frame)
    cv2.imshow('Screen', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


