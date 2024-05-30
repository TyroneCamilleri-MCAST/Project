from ultralytics import YOLO

# Load a model
model = YOLO(r"E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8S-100E-P5-LR0001-DO05-2kPI2\weights\best.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model.predict(r"E:\Thesis\Project\screenshots\20240521_133401\Image-1.png")  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen