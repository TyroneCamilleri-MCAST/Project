import cv2
from ultralytics import YOLO

def load_image(image_path):
    """Load an image from a specified path and return the image object."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or path is incorrect: {}".format(image_path))
    return img

def detect_objects(model, img):
    """Predict using the model and return the detection results."""
    results = model.predict(img)
    if not results or not hasattr(results, 'pred') or not results.pred or len(results.pred) == 0:
        raise ValueError("No detections were made or results are improperly formatted.")
    return results

def categorize_position(width, height, bbox):
    """Categorize the position of the detected object based on bounding box coordinates."""
    x1, y1, x2, y2 = bbox
    bbox_center_x = (x1 + x2) / 2
    bbox_center_y = (y1 + y2) / 2
    center_x, center_y = width / 2, height / 2

    # Determine position
    vertical = "Top" if bbox_center_y < center_y else "Bottom"
    horizontal = "Left" if bbox_center_x < center_x else "Right"

    return f"{vertical} {horizontal}" if vertical != horizontal else "Center"

def main():
    model_path = 'E:\\Thesis\\Project\\src\CVModels\\Ultralytics\\Models\\Minimap200Images100EphocsPatience5\\weights\\best.pt' # Adjust to your model weights path
    model = YOLO(model_path)

    image_path = r'E:\\Thesis\\Project\\screenshots\\20240516_165635\\Image-1.png'
    img = load_image(image_path)
    height, width, _ = img.shape

    try:
        results = detect_objects(model, img)
        # Initialize position counter
        position_counter = {}
        detections = results.pred[0]  # Access predictions; ensure there's at least one batch

        for det in detections:
            # det: [x1, y1, x2, y2, conf, class]
            if det[4] > 0.3:  # Check confidence threshold
                position = categorize_position(width, height, det[:4])  # Send only bbox coordinates
                position_counter[position] = position_counter.get(position, 0) + 1

        # Print position counts
        if position_counter:
            for position, count in position_counter.items():
                print(f"{count} {position}")
        else:
            print("No objects detected with sufficient confidence.")

    except ValueError as e:
        print(str(e))

if __name__ == "__main__":
    main()
