from ultralytics import YOLO


def main():
    model = YOLO('yolov8n-cls.yaml')
    
    model.train(
        data=r"C:\Mini-mapObjectDetection\dataset\classifications\20240530_195850",
        epochs=50,
        patience=10,
        weight_decay=0.0005,
        dropout=0.5,
        pretrained= True,
        project='./src/CVModels/Ultralytics/Models/Classification',
        name='Icon-Rotation-V1',
        device=0
    )


if __name__ == '__main__':
   main() 