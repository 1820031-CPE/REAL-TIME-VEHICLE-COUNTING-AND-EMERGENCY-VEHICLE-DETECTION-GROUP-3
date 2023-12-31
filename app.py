from flask import Flask, render_template, Response
from ultralytics import YOLO
import cv2
from time import sleep
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="verysecure",
    port = 3303,
    database = "vehiclecount"
)

mycursor = db.cursor()

app = Flask(__name__)

# Load YOLO model
model = YOLO('best1.pt')

offset = 8  # Allowed error between pixels

# Open camera
cap = cv2.VideoCapture(1)
line_position = 400  # Position of the counting line
def compute_center(coordinates):
    x_center = (coordinates[0] + coordinates[2]) / 2
    y_center = (coordinates[1] + coordinates[3]) / 2
    return x_center, y_center

def generate_frames():
    fps = 60  # Video frames per second

    count = 0
    
    while True:
        success, frame = cap.read()
        time = float(1 / fps)
        sleep(time)
        if not success:
            break
        else:
            #cv2.line(frame, (25, line_position), (1200, line_position), (255, 127, 0), 3)
            cv2.putText(frame, "VEHICLE COUNT: " + str(count), (200, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
            results = model.track(frame, persist=True, conf=0.10)
            result = results[0]
            if len(result.boxes) > 0:
                box = result.boxes[0]
                cords = box.xyxy[0].tolist()
                cords = [round(x) for x in cords]
                class_id = result.names[box.cls[0].item()]
                conf = round(box.conf[0].item(), 2)

                # Compute center of bounding box
                x_center, y_center = compute_center(cords)

                #print("Object type:", class_id)
                #print("Coordinates:", cords)
                #print("Probability:", conf)
                #print("Center Coordinates:", (x_center, y_center))

                if y_center < (line_position + offset) and y_center > (line_position - offset):
                    count=count+1
                    current_time = datetime.now()

                    insert_query = "INSERT INTO vehicle_data (date_and_time, number_of_vehicles) VALUES (%s, %s)"
                    mycursor.execute(insert_query, (current_time, count))
                    db.commit()

                #print("Count:", count)
                
                frame = results[0].plot()
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.php')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)