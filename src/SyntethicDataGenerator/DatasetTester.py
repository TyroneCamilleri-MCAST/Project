import os
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

def load_labels(label_file):
    """
    Load YOLO format labels from a text file.
    """
    labels = []
    with open(label_file, 'r') as f:
        for line in f:
            labels.append([float(x) for x in line.strip().split()])
    return labels

def draw_bounding_boxes(image_path, labels, save_path=None):
    """
    Draw bounding boxes on the image.
    """
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = img.size

        for label in labels:
            cls, x_center, y_center, w, h = label
            x_center *= width
            y_center *= height
            w *= width
            h *= height

            x_min = x_center - w / 2
            y_min = y_center - h / 2
            x_max = x_center + w / 2
            y_max = y_center + h / 2

            draw.rectangle([x_min, y_min, x_max, y_max], outline="red", width=2)
            draw.text((x_min, y_min), str(int(cls)), fill="red")

        if save_path:
            img.save(save_path)

        img.show()

def main():
    # Example usage
    image_path = r'E:\Mini-mapObjectDetection\dataset\object_detection\20240608_173634\Image-50.png'
    label_file = r'E:\Mini-mapObjectDetection\dataset\object_detection\20240608_173634\Image-50.txt'
    save_path = 'output_image.png'

    labels = load_labels(label_file)
    draw_bounding_boxes(image_path, labels, save_path)

if __name__ == "__main__":
    main()
