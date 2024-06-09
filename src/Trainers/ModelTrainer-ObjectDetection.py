from ultralytics import YOLO

def main():
    model = YOLO('yolov8n.yaml')
    results = model.train(
        data=r".\src\config-ObjectDetection.yaml",
        epochs=200,
        batch=32,
        pretrained=False,
        plots=True,
        device=0,
        name="Model1",
        project="./Models",
    )

if __name__ == '__main__':
    main()