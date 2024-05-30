import numpy as np
import os
import time
from sklearn.metrics import accuracy_score, precision_score
from ultralytics import YOLO

# Define paths
images_path = r'E:\Thesis\Project\screenshots\Testdataset'
labels_path = r'E:\Thesis\Project\screenshots\Testdataset'

# Load the YOLOv8 model
model = YOLO(r'E:\Thesis\Project\src\CVModels\Ultralytics\Models\Minimap500Images100EphocsPatience53\weights\best.pt')

# List of images and labels
image_files = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])
label_files = sorted([f for f in os.listdir(labels_path) if f.endswith('.txt')])

# Function to load ground truth labels
def load_labels(label_file):
    with open(label_file, 'r') as file:
        lines = file.readlines()
    labels = []
    for line in lines:
        parts = line.strip().split()
        labels.append((int(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4])))
    return labels

# Initialize lists to store true labels, predicted labels, and processing times
true_labels = []
pred_labels = []
processing_times = []

# Run predictions and collect true labels, predicted labels, and processing times
for img_file, label_file in zip(image_files, label_files):
    # Load image
    img_path = os.path.join(images_path, img_file)
    
    # Measure inference time
    start_time = time.time()
    results = model(img_path)
    end_time = time.time()
    
    # Calculate processing time
    processing_time = end_time - start_time
    processing_times.append(processing_time)
    
    # Load ground truth labels
    ground_truths = load_labels(os.path.join(labels_path, label_file))
    
    # Extract true labels
    true_labels_batch = [gt[0] for gt in ground_truths]
    
    # Extract predicted labels
    pred_labels_batch = [int(det.cls) for result in results for det in result.boxes]
    
    # Align true and predicted labels
    # This is a naive approach for demonstration purposes
    max_len = max(len(true_labels_batch), len(pred_labels_batch))
    true_labels.extend(true_labels_batch + [0] * (max_len - len(true_labels_batch)))
    pred_labels.extend(pred_labels_batch + [0] * (max_len - len(pred_labels_batch)))

# Calculate accuracy
accuracy = accuracy_score(true_labels, pred_labels)

# Calculate precision for each class
precision_per_class = precision_score(true_labels, pred_labels, average=None)

# Calculate average processing time
average_processing_time = np.mean(processing_times)

# Print the results
print(f'Accuracy: {accuracy:.4f}')
for i, precision in enumerate(precision_per_class):
    print(f'Precision for class {i}: {precision:.4f}')
print(f'Average processing time per image: {average_processing_time:.4f} seconds')
