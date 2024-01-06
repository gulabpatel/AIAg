import os
from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS
import cv2
import base64
from ultralytics import YOLO
import threading
import json

app = Flask(__name__)
CORS(app)

model = YOLO('best.pt')
video_processing_thread = None
stop_processing = threading.Event()

@app.route('/',methods=['GET'])
def test_flask():
    return "App is working well"

@app.route('/upload', methods=['POST'])
def upload_file():
    global video_processing_thread
    global stop_processing

    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Stop the current processing if there is one
        if video_processing_thread is not None and video_processing_thread.is_alive():
            stop_processing.set()  # Signal the thread to stop
            video_processing_thread.join()  # Wait for the thread to stop

        # Reset the event for the new thread
        stop_processing.clear()

        filename = 'uploaded_video.mp4'  # you can use a dynamic name as well
        filepath = os.path.join('uploads', filename)
        file.save(filepath)  # save file to disk

        # Start a new processing thread
        video_processing_thread = threading.Thread(target=generate_frames, args=(stop_processing,))
        video_processing_thread.start()

        return jsonify({'message': 'Upload successful', 'filepath': filepath}), 200

def generate_frames(stop_event):
    filepath = os.path.join('uploads', 'uploaded_video.mp4')
    count = 0
    while not stop_event.is_set():
        results = model.track(source=filepath, save = False, show = False, stream = True, tracker='botsort.yaml', conf = 0.5)
        for result in results:
            frame = result.orig_img
            boxesData = result.boxes
            if boxesData.xywh is not None and boxesData.id is not None:
                boxes = boxesData.xywh.cpu().numpy()
                ids = boxesData.id.cpu().numpy()
                if max(ids) > count:
                    count = max(ids)
                for i in range(len(boxes)):
                    x_center, y_center, width, height = boxes[i]
                    x1 = int(x_center - width / 2)
                    y1 = int(y_center - height / 2)
                    x2 = int(x_center + width / 2)
                    y2 = int(y_center + height / 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, 'weed' + ' ' +str(int(ids[i])), (x1, y1+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = base64.b64encode(buffer).decode('utf-8')  # Encode frame as base64

            data = {'frame': frame, 'count': int(count)}

            yield f"data:{json.dumps(data)}\n\n"

@app.route('/stream', methods=['GET'])
def stream_video():
    return Response(stream_with_context(generate_frames(stop_processing)), content_type='text/event-stream')

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')  # create folder for uploaded videos
    app.run(debug=True)