import cv2
from ultralytics import YOLO

def load_image(image_path):
    """Load an image from a specified path."""
    print("Loading image from:", image_path)
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Failed to load image from the specified path.")
    return img

def detect_objects(model, img):
    """Perform object detection using the provided model on the given image."""
    results = model.predict(img)
    return results

def categorize_position(width, height, bbox):
    """Categorize the position of the detected object based on bounding box coordinates."""
    x1, y1, x2, y2 = bbox[:4]
    bbox_center_x = (x1 + x2) / 2
    bbox_center_y = (y1 + y2) / 2
    center_x, center_y = width / 2, height / 2

    # Determine position
    vertical = "Top" if bbox_center_y < center_y / 2 else "Bottom" if bbox_center_y > center_y + center_y / 2 else ""
    horizontal = "Left" if bbox_center_x < center_x / 2 else "Right" if bbox_center_x > center_x + center_x / 2 else ""

    # Combine positions
    if vertical and horizontal:
        position = f"{vertical} {horizontal}"
    elif vertical:
        position = vertical
    elif horizontal:
        position = horizontal
    else:
        position = "Center"
    return position

def main():
    # Initialize YOLO model
    model_path = 'E:\\Thesis\\Project\\src\CVModels\\Ultralytics\\Models\\Minimap200Images100EphocsPatience5\\weights\\best.pt' # Adjust to your model weights path
    model = YOLO(model_path)

    # Image path
    image_path = r'E:\\Thesis\\Project\\screenshots\\20240516_165635\\Image-1.png'  # Use a raw string for the path

    # Load the image
    img = load_image(image_path)

    # Get dimensions of the image
    height, width, _ = img.shape

    # Perform object detection
    results = detect_objects(model, img)

    # Analyze and print results
    for detection in results.xyxy[0]:  # Assuming results.xyxy[0] contains the detections
        cls, bbox = detection[-1], detection[:4]
        position = categorize_position(width, height, bbox)
        print(f"Class {int(cls)}, Position: {position}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", str(e))

