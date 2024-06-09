from ultralytics import YOLO
import os

def validate_paths(*paths):
    for path in paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path '{path}' does not exist.")

if __name__ == "__main__":
    model_path = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\CVModels\Ultralytics\Models\Classification\Player-Classifier\weights\best.pt"
    data_path = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\dataset\classifications\TestingDataset"
    train_path = os.path.join(data_path, "train")
    test_path = os.path.join(data_path, "test")

    # Validate paths
    validate_paths(model_path, train_path, test_path)

    # Load model
    model = YOLO(model_path)

    # Validate model with test data
    metrics = model.val(data=data_path, split="test", device="0", save_json=True)

    # Print metrics
    print(metrics.top1)
    print(metrics.top5)
