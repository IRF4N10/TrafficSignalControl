import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from captureframe import capture_frames
from detactV import detect_vehicles_and_emergency
from IntersectionControl import intersection_control

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
socketio = SocketIO(app)


@app.route("/")
def index():

    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("result")
def handle_message(data):

    capture_interval = 0

    capture_frames(capture_interval)

    road_vehicles = {}

    # Process each road
    for i in range(1, 5):
        image_path = f"frames/frame_road({i}).jpg"
        total_vehicles, emergency_detected = detect_vehicles_and_emergency(image_path)

        # Input number of vehicles and emergency status for each road
        road_vehicles[i] = {
            "vehicles": total_vehicles,
            "emergency": emergency_detected,
        }

    for i in intersection_control(road_vehicles):
        emit("response", i, broadcast=True)


@socketio.on("message")
def handle_message(data):
    print(f"Received message: {data}")
    emit("response", data, broadcast=True)


if __name__ == "__main__":
    socketio.run(app)
