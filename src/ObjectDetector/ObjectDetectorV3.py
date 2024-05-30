import cv2  # OpenCV for image processing
from ultralytics import YOLO  # Import the YOLO class from the Ultralytics library for object detection
image_path = r'E:\Thesis\Project\screenshots\20240516_165635\Image-1.png'
model_path = r'E:\Thesis\Project\src\CVModels\Ultralytics\Models\Minimap200Images100EphocsPatience5\weights\best.pt'
def load_image(image_path):
    """Load an image from a specified path and return the image object."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or path is incorrect: {}".format(image_path))
    return img

def detect_objects(model, img):
    """Predict using the model and return the detection results."""
    results = model.predict(img)
    print(f"Model raw output: {results}")

    if not results or not hasattr(results, 'boxes') or not results.boxes or len(results.boxes) == 0:
        raise ValueError("No detections were made or results are improperly formatted.")

    # Print each box to see its content
    for box in results.boxes:
        print(f"Box: {box}")
    
    return results



def categorize_position(width, height, bbox):
    """Categorize the position of the detected object based on bounding box coordinates."""
    x1, y1, x2, y2 = bbox
    bbox_center_x = (x1 + x2) / 2
    bbox_center_y = (y1 + y2) / 2
    center_x, center_y = width / 2, height / 2

    horizontal = "Left" if bbox_center_x < center_x / 3 else "Right" if bbox_center_x > 2 * center_x / 3 else "Center"
    vertical = "Top" if bbox_center_y < center_y / 3 else "Bottom" if bbox_center_y > 2 * center_y / 3 else "Center"

    if vertical == "Center" and horizontal == "Center":
        return "Center"
    else:
        return f"{vertical} {horizontal}"

def main():
    model = YOLO(model_path)
    img = load_image(image_path)
    height, width, _ = img.shape

    try:
        results = detect_objects(model, img)
        position_counter = {}
        # Ensure you are iterating over the correct structure
        detections = results.boxes  # Adjust this line based on the actual structure

        for det in detections:
            confidence = det.confidence  # Adjust attribute name as per actual output
            bbox = det.xyxy  # Example attribute, adjust as per actual output
            if confidence > 0.3:  # Confidence threshold
                position = categorize_position(width, height, bbox)
                position_counter[position] = position_counter.get(position, 0) + 1

        if position_counter:
            for position, count in sorted(position_counter.items()):
                print(f"{count} {position}")
        else:
            print("No objects detected with sufficient confidence.")
    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()
