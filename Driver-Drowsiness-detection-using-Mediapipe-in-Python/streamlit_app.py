import os
import av
import threading
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, VideoHTMLAttributes, webrtc_streamer

# Import thư viện nhận dạng hình ảnh (ví dụ: OpenCV)
import cv2

# Define the audio file to use.
alarm_file_path = os.path.join(
    r'C:\Users\PC_LETRUONG\Desktop\le\Nhan_dien_lai_xe\Driver-Drowsiness-detection-using-Mediapipe-in-Python\audio',
    'wake_up.wav'
)

# Streamlit Components
st.set_page_config(
    page_title="Image Recognition from Camera",
    page_icon="https://learnopencv.com/wp-content/uploads/2017/12/favicon.png",
    layout="wide",  # centered, wide
    initial_sidebar_state="expanded",
    menu_items={
        "About": "### Visit www.learnopencv.com for more exciting tutorials!!!",
    },
)

col1, col2 = st.columns(spec=[6, 2], gap="medium")

with col1:
    st.title("Image Recognition from Camera")
    with st.container():
        c1, c2 = st.columns(spec=[1, 1])
        with c1:
            # The amount of time (in seconds) to wait before sounding the alarm.
            WAIT_TIME = st.slider("Seconds to wait before sounding alarm:", 0.0, 5.0, 1.0, 0.25)

        with c2:
            # You can add any other settings or sliders you need here.
            pass

thresholds = {
    "WAIT_TIME": WAIT_TIME,
}

# For streamlit-webrtc
class ImageTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Process frame from the webcam (frame.to_ndarray(format="bgr24"))
        # Perform image recognition using OpenCV or another library
        # Replace the following line with your image recognition code
        result_frame = self.image_recognition(frame.to_ndarray(format="bgr24"))
        return av.VideoFrame.from_ndarray(result_frame, format="bgr24")

    def image_recognition(self, frame):
        # This is where you perform image recognition using OpenCV or other libraries
        # Replace this example with your actual image recognition code
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return gray_frame

video_handler = ImageTransformer()

lock = threading.Lock()  # For thread-safe access & to prevent race-condition
shared_state = {"play_alarm": False}


def video_frame_callback(frame: av.VideoFrame):
    frame = video_handler.transform(frame)
    with lock:
        play_alarm = shared_state["play_alarm"]
    return frame

# https://github.com/whitphx/streamlit-webrtc/blob/main/streamlit_webrtc/config.py

with col1:
    ctx = webrtc_streamer(
        key="image-recognition",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"video": {"height": {"ideal": 480}}, "audio": False},
        video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
    )

with col2:
    # Banner for newsletter subscription, jobs, and consulting.
    st.write("You can add any content here, such as additional settings or information.")
