from ultralytics import YOLO

if __name__ == "__main__":
    # Paths to your model and configuration files
    model_path = r"src\CVModels\Ultralytics\Models\YOLO8N-Automatic-Images-80SplitV2\weights\best.pt"
    data_path = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\configTest.yaml"

    # Load your trained model
    model = YOLO(model_path)

    # Validate the model on the test set, forcing the use of CPU
    metrics = model.val(data=data_path, split="test", device="0")

    # Print the resulting metrics using the correct attributes
    print(f"Precision: {metrics.box.p}")
    print(f"Recall: {metrics.box.r}")
    print(f"F1 Score: {metrics.box.f1}")
    print(f"mAP50: {metrics.box.map50}")
    print(f"mAP50-95: {metrics.box.map}")
