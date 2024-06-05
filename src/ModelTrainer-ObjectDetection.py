from ultralytics import YOLO

def main():
    yoloModel = YOLO('yolov8n.yaml')

    results = yoloModel.train(
        data=r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\config-ObjectDetection.yaml",
        epochs=300,
        weight_decay=0.0005,
        dropout=0.5,
        project='./src/Models/',
        pretrained=False,
        name='LargeDataset-Complex_Background',
        device=0,
        plots=True
    )

    with open('./src/Models/results.txt', 'w') as f:
        f.write(str(results))

if __name__ == '__main__':
    main()
