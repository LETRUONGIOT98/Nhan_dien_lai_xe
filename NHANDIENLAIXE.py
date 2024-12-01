import cv2
import pygame
import time
# Load mô hình phát hiện khuôn mặt và mắt
face_cascade = cv2.CascadeClassifier(r'C:\Users\PC_LETRUONG\Desktop\le\Nhan_dien_lai_xe\haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\PC_LETRUONG\Desktop\le\Nhan_dien_lai_xe\haarcascade_eye.xml')

# Hàm để phát âm thanh thông báo
def play_alert_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Sử dụng hàm này để dừng âm thanh khi cần
def stop_alert_sound():
    pygame.mixer.music.stop()
# Mở camera
cap = cv2.VideoCapture(0)

# Biến để theo dõi thời gian mắt đã đóng
eye_closed_time = 0

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
                play_alert_sound('thongbao.mp3')
        else:
            eye_closed_time = 0  # Reset thời gian mắt đã đóng

    cv2.imshow("Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()