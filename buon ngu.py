import cv2
import numpy as np
import time

# Load mô hình phát hiện khuôn mặt và mắt
face_cascade = cv2.CascadeClassifier(r'C:\Users\PC_LETRUONG\Desktop\le\Nhan_dien_lai_xe\haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\PC_LETRUONG\Desktop\le\Nhan_dien_lai_xe\haarcascade_eye.xml')

# Mở camera
cap = cv2.VideoCapture(0)

# Biến để theo dõi thời gian mắt đã đóng
eye_closed_time = 0

def display_text(frame, text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)
    fontScale = 1
    color = (255, 255, 255)
    thickness = 2
    frame = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    return frame

while True:
    ret, frame = cap.read()

    # Chuyển ảnh sang ảnh xám để tăng hiệu suất
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Nhận diện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Trong khuôn mặt đã nhận diện, kiểm tra mắt
        roi_gray = gray[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        
        if len(eyes) == 0:
            # Không có mắt nào được nhận diện
            # Tính thời gian mắt đã đóng
            if eye_closed_time == 0:
                eye_closed_time = time.time()
            elif time.time() - eye_closed_time >= 2:
                frame = display_text(frame, "WARNING: Eyes Closed!")
        else:
            eye_closed_time = 0  # Reset thời gian mắt đã đóng

    cv2.imshow("Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()