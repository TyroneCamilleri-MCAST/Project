import os
import shutil
import random

def split_dataset(folder_path, train_percentage, val_percentage, test_percentage, seed=None):
    # Paths for images and labels
    images_path = os.path.join(folder_path, "images")
    labels_path = os.path.join(folder_path, "labels")
    
    # Creating train, val, and test subdirectories
    for subfolder in ['train', 'val', 'test']:
        os.makedirs(os.path.join(images_path, subfolder), exist_ok=True)
        os.makedirs(os.path.join(labels_path, subfolder), exist_ok=True)
    
    # Collect all images and labels
    images = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    labels = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    # Ensure that every image has a corresponding label
    image_names = set(os.path.splitext(img)[0] for img in images)
    label_names = set(os.path.splitext(lbl)[0] for lbl in labels)
    
    assert image_names == label_names, "Mismatch between images and labels"
    1
    
    # Pair images and labels
    paired_files = [(name, name + '.png', name + '.txt') for name in image_names]
    
    # Shuffle the paired files
    if seed is not None:
        random.seed(seed)
    random.shuffle(paired_files)
    
    total = len(paired_files)
    train_split = int(total * (train_percentage / 100))
    val_split = int(total * (val_percentage / 100))
    
    train_files = paired_files[:train_split]
    val_files = paired_files[train_split:train_split + val_split]
    test_files = paired_files[train_split + val_split:]
    
    # Function to copy files
    def copy_files(files, split_type):
        for _, image_file, label_file in files:
            shutil.copy(os.path.join(folder_path, image_file), os.path.join(images_path, split_type, image_file))
            shutil.copy(os.path.join(folder_path, label_file), os.path.join(labels_path, split_type, label_file))
    
    # Copy files to corresponding folders
    copy_files(train_files, 'train')
    copy_files(val_files, 'val')
    copy_files(test_files, 'test')

# Example usage with a seed for deterministic shuffling
# split_dataset(r'E:\Mini-mapObjectDetection\dataset\object_detection\Manual\Manual', 70, 20, 10, seed=42)
split_dataset(r'E:\Mini-mapObjectDetection\dataset\object_detection\MainModel2', 70,20,10)

