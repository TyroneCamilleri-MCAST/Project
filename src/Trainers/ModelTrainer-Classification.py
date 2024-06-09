from ultralytics import YOLO
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

def main():
    model = YOLO('yolov8n-cls.yaml')
    model.train(
        data="./dataset/classifications/Player-35x35-COD",
        epochs=200,
        pretrained=False,
        project='./src/CVModels/Ultralytics/Models/Classification',
        name='MainModel',
        device=0,
        plots=True
    )

if __name__ == '__main__':
   main()