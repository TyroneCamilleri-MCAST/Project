from ultralytics import YOLO

if __name__ == "__main__":
    model_path = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\Models\LargeDataset-300E\weights\best.pt"
    data_path = r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\configTest.yaml"

    model = YOLO(model_path)

    metrics = model.val(data=data_path, split="test", device="0")

    print(f"Precision: {metrics.box.p}")
    print(f"Recall: {metrics.box.r}")
    print(f"F1 Score: {metrics.box.f1}")
    print(f"mAP50: {metrics.box.map50}")
    print(f"mAP50-95: {metrics.box.map}")
