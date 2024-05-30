import os
import shutil
import random

def split_dataset(folder_path, percentage):
    # Paths for images and labels
    images_path = os.path.join(folder_path, "images")
    labels_path = os.path.join(folder_path, "labels")
    
    # Creating train and val subdirectories
    for subfolder in ['train', 'val']:
        os.makedirs(os.path.join(images_path, subfolder), exist_ok=True)
        os.makedirs(os.path.join(labels_path, subfolder), exist_ok=True)
    
    # Collect all images and labels
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    images = [f for f in all_files if f.endswith('.png')]
    labels = [f for f in all_files if f.endswith('.txt')]
    
    # Check that every image has a corresponding label
    image_names = set(os.path.splitext(img)[0] for img in images)
    label_names = set(os.path.splitext(lbl)[0] for lbl in labels)
    
    assert image_names == label_names, "Mismatch between images and labels"
    
    # Shuffle and split
    data = list(image_names)
    random.shuffle(data)
    split_point = int(len(data) * (percentage / 100))
    
    train_names = data[:split_point]
    val_names = data[split_point:]
    
    # Copy files to corresponding folders
    for name in train_names:
        shutil.copy(os.path.join(folder_path, name + '.png'), os.path.join(images_path, 'train', name + '.png'))
        shutil.copy(os.path.join(folder_path, name + '.txt'), os.path.join(labels_path, 'train', name + '.txt'))
    
    for name in val_names:
        shutil.copy(os.path.join(folder_path, name + '.png'), os.path.join(images_path, 'val', name + '.png'))
        shutil.copy(os.path.join(folder_path, name + '.txt'), os.path.join(labels_path, 'val', name + '.txt'))

split_dataset(r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\screenshots\CODALLY6', 80)
