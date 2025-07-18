# app.py

from flask import Flask, Response, request, render_template
from config import YOLO_MODEL_PATH, VIDEO_PATH, SHIRT_IMAGES, T_SHIRT_POINTS
from video_processor import ModelProcessor
import cv2

app = Flask(__name__)

def generate_video(video_path, processor):
    """
    Generate a video stream by processing frames in real time.
    """
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = processor.process_frame(frame)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    """
    Endpoint to serve the video feed with overlaid shirt based on selected model.
    """
    shirt_id = request.args.get('shirt_id', 'shirt_natural')
    model_name = request.args.get('model', 'Pose')
    shirt_image = SHIRT_IMAGES.get(shirt_id, SHIRT_IMAGES['shirt_natural'])

    processor = ModelProcessor(model_name, shirt_image, T_SHIRT_POINTS)
    return Response(generate_video(VIDEO_PATH, processor),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """
    Serve the main page for the application.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
