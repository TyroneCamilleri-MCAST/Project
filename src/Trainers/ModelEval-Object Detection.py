from ultralytics import YOLO

if __name__ == "__main__":
    model_path = r"E:\Mini-mapObjectDetection\Models\object_detection\MainModel\weights\best.pt"
    data_path = r"E:\Mini-mapObjectDetection\src\config-ObjectDetection.yaml"

    model = YOLO(model_path)

    metrics = model.val(data=data_path, split="test", device="0", plots=True, conf=0.25)

    print(f"Precision: {metrics.box.p}")
    print(f"Recall: {metrics.box.r}")
    print(f"F1 Score: {metrics.box.f1}")
    print(f"mAP50: {metrics.box.map50}")
    print(f"mAP50-95: {metrics.box.map}")
