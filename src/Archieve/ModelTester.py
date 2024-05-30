import os
from ultralytics import YOLO
from sklearn.preprocessing import label_binarize
from sklearn.metrics import precision_recall_curve, auc
import matplotlib.pyplot as plt
import numpy as np

# Load the trained YOLO model
model = YOLO(r'E:\Thesis\Project\src\CVModels\Ultralytics\Models\YOLO8S-100E-P5-LR0001-DO05-2kPI2\weights\best.pt')

# Path to the test dataset folder
test_dataset_path = r'E:\Thesis\Project\screenshots\20240516_185327'


# Lists to store true labels and predicted scores
true_labels = []
predicted_scores = []

# Function to read annotations from a YOLO-format txt file
def read_annotations(txt_file):
    labels = []
    with open(txt_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            label = int(line.split()[0])
            labels.append(label)
    return labels

# Run inference on the test dataset
for file in os.listdir(test_dataset_path):
    if file.endswith('.png') or file.endswith('.jpg'):
        # Image file
        # Corresponding annotation file
        annotation_path = os.path.join(test_dataset_path, file.replace('.png', '.txt').replace('.jpg', '.txt'))

        # Get true labels from the annotation file
        if os.path.exists(annotation_path):
            true_labels.extend(read_annotations(annotation_path))

            # Get predictions from the model
            results = model.predict(source=image_path, save=False)

            # Extracting the predicted class IDs and confidence scores
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        predicted_scores.append(box.conf.item())  # Confidence score

# Ensure true_labels and predicted_scores are numpy arrays
true_labels = np.array(true_labels)
predicted_scores = np.array(predicted_scores)

# Ensure lengths of true_labels and predicted_scores match
min_length = min(len(true_labels), len(predicted_scores))
true_labels = true_labels[:min_length]
predicted_scores = predicted_scores[:min_length]

# Binarize the true labels for multiclass precision-recall calculation
classes = np.unique(true_labels)
true_labels_binarized = label_binarize(true_labels, classes=classes)

# Plot Precision-Recall curve for each class
plt.figure()
for i, class_id in enumerate(classes):
    precision, recall, _ = precision_recall_curve(true_labels_binarized[:, i], predicted_scores)
    auc_pr = auc(recall, precision)
    plt.plot(recall, precision, label=f'Class {class_id} (AUC = {auc_pr:.2f})')

plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve for Each Class')
plt.legend(loc="lower left")
plt.grid()
plt.savefig('precision_recall_curve.png')
plt.show()
