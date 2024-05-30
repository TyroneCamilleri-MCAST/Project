import cv2
from ultralytics import YOLO
import numpy as np
import pyttsx3
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 300)  # Increase the speech rate

# Load the YOLOv8 model
model = YOLO(r"E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8M-300E-1kPI3\weights\best.pt")

# Open the video file
source = r"C:\Users\Abzsorb\Videos\2024-05-22 19-15-32.mkv"
cap = cv2.VideoCapture(source)

# Function to create a blank image for displaying text
def create_text_image(text, width=640, height=480):
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    y0, dy = 30, 30
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(image, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
    return image

# Function to determine the relative position of an object
def determine_position(player_x, player_y, obj_x, obj_y):
    dx = obj_x - player_x
    dy = player_y - obj_y  # Invert the y-axis

    angle = np.arctan2(dy, dx) * 180 / np.pi

    if -22.5 < angle <= 22.5:
        return "Right"
    elif 22.5 < angle <= 67.5:
        return "Top Right"
    elif 67.5 < angle <= 112.5:
        return "Top"
    elif 112.5 < angle <= 157.5:
        return "Top Left"
    elif -67.5 < angle <= -22.5:
        return "Bottom Right"
    elif -112.5 < angle <= -67.5:
        return "Bottom"
    elif -157.5 < angle <= -112.5:
        return "Bottom Left"
    else:
        return "Left"

# Function to handle text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Variable to track the pause state
paused = False

# Loop through the video frames
while cap.isOpened():
    if not paused:
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, device="0")

            # Extracting information from results
            player_boxes = []
            other_boxes = []

            for result in results:
                boxes = result.boxes

                for box in boxes:
                    class_id = int(box.cls)
                    label = model.names[class_id]  # Accessing names directly from the model
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()  # coordinates
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    if label == 'player':
                        player_boxes.append((center_x, center_y))
                    else:
                        other_boxes.append((label, center_x, center_y))

            if player_boxes:
                player_x, player_y = player_boxes[0]  # Assuming only one player

                detections = []

                for label, obj_x, obj_y in other_boxes:
                    distance = ((obj_x - player_x) ** 2 + (obj_y - player_y) ** 2) ** 0.5
                    distance = round(distance.item(), 2)  # Convert tensor to a numeric value
                    position = determine_position(player_x, player_y, obj_x, obj_y)
                    detections.append((label, position, distance))

                # Sort detections by distance
                detections.sort(key=lambda x: x[2])

                # Prepare the text to display for detections
                text_lines = []
                for label, position, distance in detections:
                    text_lines.append(f"{label} {position} {distance} units")

                text_to_display = "\n".join(text_lines)

                # Create the text image
                text_image = create_text_image(text_to_display)

                # Display the text image in a separate window
                cv2.imshow("Detections", text_image)

                # Announce the closest entity in a separate thread (without distance units)
                if detections:
                    closest_entity = detections[0]
                    speech_text = f"{closest_entity[0]} {closest_entity[1]}"
                    threading.Thread(target=speak, args=(speech_text,)).start()

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame without FPS
            cv2.imshow("YOLOv8 Inference", annotated_frame)

    # Break the loop if 'q' is pressed, pause if space is pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        paused = not paused

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
