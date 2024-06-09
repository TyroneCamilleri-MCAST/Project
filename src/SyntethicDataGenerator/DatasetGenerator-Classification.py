import pygame
import random
import sys
import os
from datetime import datetime
import math

# Timestamp for dataset path
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Dataset path
dataset_path = f"./dataset/classification/{timestamp}"
train_path = os.path.join(dataset_path, "train")
val_path = os.path.join(dataset_path, "val")

# Create directories if they don't exist
os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
CENTRAL_ICON_PATH = '../../data/Player.png'
ENEMY_IMAGE_PATH = '../../data/Enemy.png'
ALLY_IMAGE_PATH = '../../data/Ally.png'
BACKGROUND_FOLDER_PATH = r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\data\images\Background\CallOfDutyMap'

# Settings
SAVE_IMAGE = True
SAVE_LABELS = False
ROTATE_CENTER_ICON = True
ENABLE_PLAYER_ROTATION = True
SHOW_ENEMIES = False
SHOW_ALLIES = False
NUMBER_OF_FRAMES = 5000
FRAMES_PER_SET = 3000

# Define angles and folders
angles_and_folders = {
    0: 'top',
    315: 'top_right',
    90: 'right',
    225: 'bottom_right',
    180: 'bottom',
    135: 'bottom_left',
    270: 'left',
    45: 'top_left'
}

# Create subdirectories for each angle in train and val
for folder in angles_and_folders.values():
    os.makedirs(os.path.join(train_path, folder), exist_ok=True)
    os.makedirs(os.path.join(val_path, folder), exist_ok=True)

# Entity settings
ENTITY_SETTINGS = {
    "size": (35, 35),
    "enemy_count_range": (1, 5),
    "ally_count_range": (1, 5),
    "speed_range": {"enemies": (2, 5), "allies": (1, 3)}
}

# Load and scale image
def load_and_scale_image(path, size, opacity=None):
    image = pygame.image.load(path).convert_alpha()
    scaled_image = pygame.transform.scale(image, size)
    if opacity is not None:
        scaled_image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return scaled_image

# Function to get rotated image and rect
def get_rotated_image_and_rect(image, rect, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, rotated_rect

# Load images from a folder
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            image = pygame.image.load(image_path).convert()
            images.append(image)
    return images

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    central_icon_base = load_and_scale_image(CENTRAL_ICON_PATH, (24, 24))
    central_icon_rect = central_icon_base.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    background_images = load_images_from_folder(BACKGROUND_FOLDER_PATH)

    clock = pygame.time.Clock()
    running = True
    FRAME = 0
    current_angle_index = 0
    angles = list(angles_and_folders.keys())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        FRAME += 1
        background_image = random.choice(background_images)
        screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        angle = angles[current_angle_index]
        if ROTATE_CENTER_ICON:
            central_icon, central_icon_rect = get_rotated_image_and_rect(central_icon_base, central_icon_rect, angle)
        else:
            central_icon = central_icon_base

        screen.blit(central_icon, central_icon_rect)

        pygame.display.flip()

        if SAVE_IMAGE:
            # Determine whether to save in train or val
            if FRAME <= FRAMES_PER_SET:
                base_path = train_path
            else:
                base_path = val_path

            # Capture a 35x35 area centered on the player
            capture_rect = pygame.Rect(central_icon_rect.centerx - 17, central_icon_rect.centery - 17, 35, 35)
            player_surface = screen.subsurface(capture_rect).copy()
            direction_folder = angles_and_folders[angle]
            image_filename = f"{base_path}/{direction_folder}/player_capture_{FRAME}.png"
            pygame.image.save(player_surface, image_filename)

        current_angle_index = (current_angle_index + 1) % len(angles)

        if FRAME == NUMBER_OF_FRAMES:
            pygame.quit()
            sys.exit()

        clock.tick(20)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
