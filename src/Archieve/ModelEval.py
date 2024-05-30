from ultralytics import YOLO
import torch

# Load the trained YOLO model
model = YOLO(r'E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8S-100E-P5-LR0001-DO05-2kPI2\weights\best.pt')  # Replace with the actual path to your trained model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
# Calculate F1 score
precision = metrics.box.map50  # Assuming map50 as precision
recall = metrics.box.map75  # Assuming map75 as recall
F1 = 2 * (precision * recall) / (precision + recall)

print(f'Precision: {precision}, Recall: {recall}, F1 Score: {F1}')