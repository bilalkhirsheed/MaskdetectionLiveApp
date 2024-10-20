from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import threading
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing import image

model_path = 'D:\\DiskEdata\\PythonWorking\\deployingproject\\firstproject\\mask_detection\\mymodel.h5'
mymodel = load_model(model_path)

class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.lock = threading.Lock()
        self.face_cascade = cv2.CascadeClassifier(r'D:\DiskEdata\PythonWorking\deployingproject\firstproject\mask_detection\haarcascade_frontalface_default.xml')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        with self.lock:
            success, frame = self.video.read()
            if not success:
                print("Failed to read frame from webcam.")
                return None

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                face_img = frame[y:y+h, x:x+w]
                cv2.imwrite('temp.jpg', face_img)
                test_image = image.load_img('temp.jpg', target_size=(150, 150))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis=0)
                prediction = mymodel.predict(test_image)[0][0]

                if prediction == 1:
                    label = 'NO MASK'
                    color = (0, 0, 255)  # Red
                else:
                    label = 'MASK'
                    color = (0, 255, 0)  # Green

                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

def generate_frames(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            continue  # Skip this iteration if frame is None
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'mask_detection/index.html')
