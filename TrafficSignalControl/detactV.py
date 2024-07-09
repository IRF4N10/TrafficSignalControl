from pathlib import Path

import cv2
from ultralytics import YOLO


def detect_vehicles_and_emergency(image_path):

    # Load the YOLOv8 model
    model_path = "vehicle_detection_model/best25.pt"
    model = YOLO(model_path)

    # Load the image
    image = cv2.imread(str(image_path))  # Assuming image is in OpenCV format

    # save results
    res = model.predict(image, conf=0.3, save=True)
    # save class label names
    names = res[0].names  # same as model.names

    # store number of objects detected per class label
    class_detections_values = []
    for k, v in names.items():
        class_detections_values.append(res[0].boxes.cls.tolist().count(k))
    # create dictionary of objects detected per class
    classes_detected = dict(zip(names.values(), class_detections_values))

    # Count the total number of detected objects across all classes
    total_detected_objects = sum(class_detections_values)

    # Define the emergency vehicle classes
    emergency_vehicle_classes = ["ambulance", "firetruck", "police car"]
    # Check if any emergency vehicle class has at least one detection
    emergency_vehicle_detected = 0
    for class_name in emergency_vehicle_classes:
        if class_name in classes_detected and classes_detected[class_name] > 0:
            emergency_vehicle_detected = 1
            break
    return total_detected_objects, emergency_vehicle_detected
