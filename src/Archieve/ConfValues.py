import numpy as np
import os
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
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
    return len(lines)

# Initialize lists to store true counts, predicted counts, processing times, and confidences
true_counts = []
pred_counts = []
processing_times = []
confidences = []

# Confidence threshold
confidence_threshold = 0.5

# Run predictions and collect true counts, predicted counts, processing times, and confidences
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
    
    # Load ground truth count
    true_count = load_labels(os.path.join(labels_path, label_file))
    
    # Extract predicted count with confidence filtering
    pred_count = 0
    img_confidences = []
    for result in results:
        for det in result.boxes:
            conf = det.conf.item()
            img_confidences.append(conf)
            if conf >= confidence_threshold:
                pred_count += 1
    
    # Append to the main lists
    true_counts.append(true_count)
    pred_counts.append(pred_count)
    confidences.append(img_confidences)

# Print the confidence values for each image
for i, img_file in enumerate(image_files):
    print(f"Image: {img_file}")
    print(f"Confidence values: {confidences[i]}")
    print("")

# Calculate exact match accuracy
exact_match_accuracy = np.mean(np.array(true_counts) == np.array(pred_counts))

# Calculate precision, recall, and F1 score for counts
true_positive_counts = sum(1 for t, p in zip(true_counts, pred_counts) if t == p)
false_positive_counts = sum(1 for t, p in zip(true_counts, pred_counts) if t != p and p > t)
false_negative_counts = sum(1 for t, p in zip(true_counts, pred_counts) if t != p and p < t)

precision = true_positive_counts / (true_positive_counts + false_positive_counts) if (true_positive_counts + false_positive_counts) > 0 else 0
recall = true_positive_counts / (true_positive_counts + false_negative_counts) if (true_positive_counts + false_negative_counts) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Calculate average processing time
average_processing_time = np.mean(processing_times)

# Print the results
print(f'Exact Match Accuracy: {exact_match_accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')
print(f'Average processing time per image: {average_processing_time:.4f} seconds')

