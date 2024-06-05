import cv2
from ultralytics import YOLO
import numpy as np
import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 300)

objectDetectionModel = YOLO(r"E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8M-300E-1kPI3\weights\best.pt")
classificationModel = YOLO(r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\CVModels\Ultralytics\Models\Classification\Icon-Rotation-V16\weights\best.pt")

cap = cv2.VideoCapture(r"C:\Users\Abzsorb\Videos\2024-05-22 19-15-32.mkv")

direction_mapping = {
    0: 'bottom',
    1: 'bottom_left',
    2: 'bottom_right',
    3: 'left',
    4: 'right',
    5: 'top',
    6: 'top_left',
    7: 'top_right'
}

def create_text_image(text, width=640, height=480):
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    y0, dy = 30, 30
    for i, line in enumerate(text.split('\n')):
        y = y0 + i * dy
        cv2.putText(image, line, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
    return image

def determine_position(player_x, player_y, obj_x, obj_y, direction):
    dx, dy = obj_x - player_x, player_y - obj_y
    if direction == 'bottom': dx, dy = -dx, -dy
    elif direction == 'left': dx, dy = dy, -dx
    elif direction == 'right': dx, dy = -dy, dx
    elif direction == 'top_left': dx, dy = (dx + dy) / np.sqrt(2), (dy - dx) / np.sqrt(2)
    elif direction == 'top_right': dx, dy = (dx - dy) / np.sqrt(2), (dx + dy) / np.sqrt(2)
    elif direction == 'bottom_left': dx, dy = (-dx + dy) / np.sqrt(2), (-dy - dx) / np.sqrt(2)
    elif direction == 'bottom_right': dx, dy = (-dx - dy) / np.sqrt(2), (-dy + dx) / np.sqrt(2)
    direction_str = ""
    if dy > 0: direction_str += "Top "
    elif dy < 0: direction_str += "Bottom "
    if dx > 0: direction_str += "Right"
    elif dx < 0: direction_str += "Left"
    if abs(dx) < abs(dy) * 0.5: direction_str = "Top" if dy > 0 else "Bottom"
    elif abs(dy) < abs(dx) * 0.5: direction_str = "Right" if dx > 0 else "Left"
    return direction_str.strip()

def speak(text):
    threading.Thread(target=_speak, args=(text,)).start()

def _speak(text):
    engine.say(text)
    engine.runAndWait()

paused = False

while cap.isOpened():
    if not paused:
        success, frame = cap.read()
        if success:
            detection_results = objectDetectionModel(frame, device="0")
            player_boxes, other_boxes = [], []
            for result in detection_results:
                for box in result.boxes:
                    class_id = int(box.cls)
                    label = objectDetectionModel.names[class_id]
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
                    if label == 'player':
                        player_boxes.append((center_x, center_y, x1, y1, x2, y2))
                    else:
                        other_boxes.append((label, center_x, center_y))
            if player_boxes:
                player_x, player_y, px1, py1, px2, py2 = player_boxes[0]
                player_crop = frame[int(py1):int(py2), int(px1):int(px2)]
                classification_results = classificationModel(player_crop, device="0")
                top1_idx = classification_results[0].probs.top1
                player_direction = direction_mapping[top1_idx]
                detections = []
                for label, obj_x, obj_y in other_boxes:
                    distance = round(((obj_x - player_x) ** 2 + (obj_y - player_y) ** 2) ** 0.5, 2)
                    position = determine_position(player_x, player_y, obj_x, obj_y, player_direction)
                    detections.append((label, position, distance))
                detections.sort(key=lambda x: x[2])
                text_lines = [f"{label} {position} {distance} units" for label, position, distance in detections]
                text_image = create_text_image("\n".join(text_lines))
                cv2.imshow("Detections", text_image)
                if detections:
                    speak(f"{detections[0][0]} {detections[0][1]}")
            annotated_frame = detection_results[0].plot()
            cv2.imshow("YOLOv8 Inference", annotated_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        paused = not paused

cap.release()
cv2.destroyAllWindows()