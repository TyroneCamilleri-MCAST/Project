import pygame
import random
import sys
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Paths
CENTRAL_ICON_PATH = 'data/Icons/player.png'
BACKGROUND_FOLDER_PATH = r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\data\images\Background\CallOfDutyMap'  # Folder containing background images

# General Settings
SAVE_IMAGE = True
SAVE_LABELS = False  # Labels are disabled

# Game settings
ROTATE_CENTER_ICON = True  # Enable rotation
ENABLE_PLAYER_ROTATION = True  # Enable rotation
SHOW_ENEMIES = False  # Enemies are not shown
SHOW_ALLIES = False  # Allies are not shown
NUMBER_OF_FRAMES = 5000
FRAMES_PER_SET = 2000  # Number of frames before switching to validation set

# Rotation angles and corresponding classification folders
angles_and_folders = {
    0: 'top',
    45: 'top_right',
    90: 'right',
    135: 'bottom_right',
    180: 'bottom',
    225: 'bottom_left',
    270: 'left',
    315: 'top_left'
}

def load_and_scale_image(path, size, opacity=None):
    image = pygame.image.load(path).convert_alpha()
    scaled_image = pygame.transform.scale(image, size)
    if opacity is not None:
        scaled_image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return scaled_image

def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(folder_path, filename)
            image = pygame.image.load(image_path).convert()
            images.append(image)
    return images

def get_rotated_image_and_rect(image, rect, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, rotated_rect

def create_directories(base_dir):
    for set_type in ['train', 'val']:
        for folder in angles_and_folders.values():
            dir_path = os.path.join(base_dir, set_type, folder)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    central_icon_base = load_and_scale_image(CENTRAL_ICON_PATH, (24, 24))  # Base image without rotation

    central_icon_rect = central_icon_base.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    clock = pygame.time.Clock()  # Create a clock object

    # Load background images
    background_images = load_images_from_folder(BACKGROUND_FOLDER_PATH)

    # Create a unique directory based on the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_dir = os.path.join('dataset/classifications', timestamp)
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Create directories for each classification
    create_directories(base_dir)

    running = True
    FRAME = 0
    current_angle_index = 0
    angles = list(angles_and_folders.keys())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        FRAME += 1

        # Select a random background image
        background_image = random.choice(background_images)
        screen.blit(pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        # Rotate player sprite based on current angle
        angle = angles[current_angle_index]
        central_icon, central_icon_rect = get_rotated_image_and_rect(central_icon_base, central_icon_rect, angle)
        
        # Invert the image for 'right' and 'left' orientations
        if angle == 90 or angle == 270:
            central_icon = pygame.transform.flip(central_icon, True, False)

        screen.blit(central_icon, central_icon_rect)

        pygame.display.flip()

        if SAVE_IMAGE:
            folder_name = angles_and_folders[angle]
            set_type = 'train' if (FRAME // FRAMES_PER_SET) % 2 == 0 else 'val'
            save_dir = os.path.join(base_dir, set_type, folder_name)
            pygame.image.save(screen, os.path.join(save_dir, f"Image-{FRAME}.png"))

        # Move to the next angle
        current_angle_index = (current_angle_index + 1) % len(angles)

        if FRAME == NUMBER_OF_FRAMES:
            pygame.quit()
            sys.exit()

        clock.tick(20)  # Aim for 20 frames per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
