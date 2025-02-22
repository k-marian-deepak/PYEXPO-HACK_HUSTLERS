from flask import Flask, Response, render_template, jsonify
import cv2
import threading
from main_traffic_logic import process_traffic_data, get_congestion_level
from mail_report import send_violation_email
from roboflow_dataset import process_video_frame

app = Flask(__name__)

# Open video file
cap = cv2.VideoCapture("Cars Moving On Road Stock Footage - Free Download.mp4")

# Global dictionary to store traffic data per lane
traffic_signals = {}

def generate_frames():
    global traffic_signals
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            # Process frame for vehicle detection
            vehicle_count, violations = process_video_frame(frame)

            # Get congestion level and signal time
            congestion_status, signal_time = get_congestion_level(vehicle_count)

            # Update traffic signal data
            traffic_signals = {
                "vehicle_count": vehicle_count,
                "congestion_level": congestion_status,
                "signal_time": signal_time
            }

            # Display traffic signal info on frame
            display_text = f"Signal Time: {signal_time}s | {congestion_status}"
            cv2.putText(frame, display_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Display vehicle count
            count_text = f"Vehicles: {vehicle_count}"
            cv2.putText(frame, count_text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            # Draw violation info on frame
            if violations:
                violation_text = f"Violations: {', '.join(violations)}"
                cv2.putText(frame, violation_text, (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Send email for detected violations
                for violation in violations:
                    send_violation_email(violation)

            # Encode frame to stream
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + 
                   buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    """Render HTML page for video display."""
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/report')
def report():  
    return render_template("report.html")

@app.route('/video_feed')
def video_feed():
    """Stream video with live detections."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/traffic_info')
def traffic_info():
    """Return latest traffic signal, vehicle count, and congestion level."""
    return jsonify(traffic_signals)

if __name__ == "__main__":
    app.run(debug=True)