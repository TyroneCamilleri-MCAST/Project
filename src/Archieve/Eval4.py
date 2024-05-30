import numpy as np
import os
import time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ultralytics import YOLO

# Define paths
images_path = r'E:\Thesis\Project\screenshots\20240516_180433'
labels_path = r'E:\Thesis\Project\screenshots\20240516_180433'

# Load the YOLOv8 model
model = YOLO(r'E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8S-100E-P5-LR0001-DO05-2kPI2\weights\best.pt')

# List of images and labels
image_files = sorted([f for f in os.listdir(images_path) if f.endswith('.jpg') or f.endswith('.png')])
label_files = sorted([f for f in os.listdir(labels_path) if f.endswith('.txt')])

# Function to load ground truth labels
def load_labels(label_file):
    with open(label_file, 'r') as file:
        lines = file.readlines()
    return len(lines)

# Initialize lists to store true counts, predicted counts, and processing times
true_counts = []
pred_counts = []
processing_times = []

# Confidence threshold
confidence_threshold = 0.10

# Run predictions and collect true counts, predicted counts, and processing times
for img_file, label_file in zip(image_files, label_files):
    # Load image
    img_path = os.path.join(images_path, img_file)
    
    # Measure inference time
    start_time = time.time()
    results = model(img_path, conf=confidence_threshold)
    end_time = time.time()
    
    # Calculate processing time
    processing_time = end_time - start_time
    processing_times.append(processing_time)
    
    # Load ground truth count
    true_count = load_labels(os.path.join(labels_path, label_file))
    
    print(true_count)
    
    # Extract predicted count with confidence filtering
    pred_count = sum(len(result.boxes) for result in results)
    
    # Append to the main lists
    true_counts.append(true_count)
    pred_counts.append(pred_count)

# Print ground truth counts and predicted counts for each image
for i, img_file in enumerate(image_files):
    print(f"Image: {img_file}")
    print(f"Ground Truth Count: {true_counts[i]}")
    print(f"Predicted Count: {pred_counts[i]}")
    print("")

# Calculate true positives, false positives, false negatives, and true negatives
true_positive_counts = sum(1 for t, p in zip(true_counts, pred_counts) if t == p and t != 0)
false_positive_counts = sum(1 for t, p in zip(true_counts, pred_counts) if p > t)
false_negative_counts = sum(1 for t, p in zip(true_counts, pred_counts) if p < t)
true_negative_counts = sum(1 for t, p in zip(true_counts, pred_counts) if t == p == 0)

# Calculate total predicted and ground truth counts
total_true_counts = sum(true_counts)
total_pred_counts = sum(pred_counts)

# Calculate precision, recall, and F1 score
precision = true_positive_counts / (true_positive_counts + false_positive_counts) if (true_positive_counts + false_positive_counts) > 0 else 0
recall = true_positive_counts / (true_positive_counts + false_negative_counts) if (true_positive_counts + false_negative_counts) > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Calculate accuracy (exact match accuracy)
accuracy = (true_positive_counts + true_negative_counts) / len(true_counts)

# Calculate average processing time
average_processing_time = np.mean(processing_times)

# Print the results
print(f'Total Ground Truth Count: {total_true_counts}')
print(f'Total Predicted Count: {total_pred_counts}')
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')
print(f'Average processing time per image: {average_processing_time:.4f} seconds')
print(f'True Positives: {true_positive_counts}')
print(f'False Positives: {false_positive_counts}')
print(f'False Negatives: {false_negative_counts}')
print(f'True Negatives: {true_negative_counts}')
