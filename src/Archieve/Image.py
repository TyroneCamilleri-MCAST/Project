from ultralytics import YOLO

# Load a model
model = YOLO(r"E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8M-300E-1kPI2\weights\best.pt")

# Run batched inference on a list of images
results = model(r"E:\Thesis\Project\screenshots\20240516_180433 - Copy\Image-1.png")  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk