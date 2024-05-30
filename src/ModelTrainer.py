# ModelTrainer.py
from ultralytics import YOLO


def main():
    # Create a YOLO model instance
    model = YOLO('yolov8s.yaml')
    
#     # Train the model
    model.train(
        data=r"C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\src\config.yaml",
        epochs=50,
        patience=10,
        weight_decay=0.0005,
        dropout=0.5,
        project='./src/CVModels/Ultralytics/Models',
        name='YOLO8N-COD',
        device=0
    )


if __name__ == '__main__':
   main() 