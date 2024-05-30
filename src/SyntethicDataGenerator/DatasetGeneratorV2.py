import pygame
import random
import sys
import math
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Paths
CENTRAL_ICON_PATH = 'data/Player.png'
ENEMY_IMAGE_PATH = 'data/Enemy.png'
ALLY_IMAGE_PATH = 'data/Ally.png'

# General Settings
SAVE_IMAGE = True
SAVE_LABELS = True

# Enemy settings
ENEMY_COUNT = random.randint(0, 4)
MIN_SPEED = 2  # Minimum speed
MAX_SPEED = 5  # Maximum speed

# Ally settings
ALLY_COUNT = random.randint(0, 4)
ALLY_MIN_SPEED = 1  # Minimum speed
ALLY_MAX_SPEED = 3  # Maximum speed

# Game settings
ROTATE_CENTER_ICON = True  # Set to True if rotation is needed
ENABLE_PLAYER_ROTATION = True  # Set to True if rotation is needed
ENABLE_ENEMY_MOVEMENT = False  # Set to False to stop enemy movement
REGENERATE_ENTITIES_EVERY_FRAME = True  # Set to True to regenerate entities every frame
ENABLE_ENEMY_OPACITY = True  # Set to False to disable enemy opacity
ENEMY_OPACITY_MIN = 255  # Minimum opacity
ENEMY_OPACITY_MAX = 255  # Maximum opacity
ENABLE_ALLY_OPACITY = True  # Set to False to disable ally opacity
ALLY_OPACITY_MIN = 255  # Minimum opacity
ALLY_OPACITY_MAX = 255  # Maximum opacity
SHOW_BOUNDING_BOXES = False  # Set to False to hide bounding boxes
BOUNDING_BOX_SCALE = 1.0  # Scale factor to reduce bounding box size
BOUNDING_BOX_OFFSET_X = 0  # Offset for bounding box along the x-axis
BOUNDING_BOX_OFFSET_Y = 0  # Offset for bounding box along the y-axis

GENERATE_ROBUST_DATASET = True
ROTATION_NUMBER_OF_FRAMES = 15  # Total frames for rotation (0 to 360 degrees)
OPACITY_NUMBER_OF_FRAMES = 15  # Total frames for opacity from min to max value

# Calculated steps based on the number of frames
ROTATION_STEP = 360 / ROTATION_NUMBER_OF_FRAMES
OPACITY_STEP = (ENEMY_OPACITY_MAX - ENEMY_OPACITY_MIN) / OPACITY_NUMBER_OF_FRAMES

# Visibility and labeling settings
SHOW_ENEMIES = True  # Set to False to hide enemies
SHOW_ALLIES = True  # Set to False to hide allies
LABEL_ENEMIES = True  # Set to False to disable labeling of enemies
LABEL_ALLIES = True  # Set to False to disable labeling of allies
LABEL_PLAYER = True  # Set to False to disable labeling of the player

def load_and_scale_image_maintain_aspect_ratio(path, target_size, opacity=None):
    image = pygame.image.load(path).convert_alpha()
    image_rect = image.get_rect()
    width_ratio = target_size[0] / image_rect.width
    height_ratio = target_size[1] / image_rect.height
    min_ratio = min(width_ratio, height_ratio)
    new_size = (int(image_rect.width * min_ratio), int(image_rect.height * min_ratio))
    scaled_image = pygame.transform.scale(image, new_size)
    if opacity is not None:
        scaled_image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return scaled_image

def create_entity(screen_width, screen_height, target_size, min_speed, max_speed, image_path, enable_opacity=False, opacity_min=0, opacity_max=255):
    angle = random.randint(0, 360)
    speed = random.randint(min_speed, max_speed)
    dx = math.cos(math.radians(angle)) * speed
    dy = math.sin(math.radians(angle)) * speed
    opacity = None
    if enable_opacity:
        opacity = random.randint(opacity_min, opacity_max)
    image = load_and_scale_image_maintain_aspect_ratio(image_path, target_size, opacity)
    rect = image.get_rect(topleft=(random.randint(0, screen_width - target_size[0]), random.randint(0, screen_height - target_size[1])))
    return {
        'image': image,
        'rect': rect,
        'dx': dx,
        'dy': dy,
        'angle': angle,
        'opacity': opacity
    }

def get_rotated_image_and_rect(image, rect, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, rotated_rect

def main():
    ALLY_COUNT = random.randint(0, 4)
    ENEMY_COUNT = random.randint(0, 4)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    central_icon_base = load_and_scale_image_maintain_aspect_ratio(CENTRAL_ICON_PATH, (24, 24))  # Base image without rotation

    enemies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, (24, 24), MIN_SPEED, MAX_SPEED, ENEMY_IMAGE_PATH, ENABLE_ENEMY_OPACITY, ENEMY_OPACITY_MIN, ENEMY_OPACITY_MAX) for _ in range(ENEMY_COUNT)]
    allies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, (24, 24), ALLY_MIN_SPEED, ALLY_MAX_SPEED, ALLY_IMAGE_PATH, ENABLE_ALLY_OPACITY, ALLY_OPACITY_MIN, ALLY_OPACITY_MAX) for _ in range(ALLY_COUNT)]

    central_icon_rect = central_icon_base.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    clock = pygame.time.Clock()  # Create a clock object

    # Create a unique directory based on the current date and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join('screenshots', timestamp)
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    running = True
    FRAME = 0
    current_rotation_frame = 0
    current_opacity_frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        FRAME += 1
        
        ALLY_COUNT = random.randint(0, 4)
        ENEMY_COUNT = random.randint(0, 4)

        if REGENERATE_ENTITIES_EVERY_FRAME:
            enemies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, (24, 24), MIN_SPEED, MAX_SPEED, ENEMY_IMAGE_PATH, ENABLE_ENEMY_OPACITY, ENEMY_OPACITY_MIN, ENEMY_OPACITY_MAX) for _ in range(ENEMY_COUNT)]
            allies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, (24, 24), ALLY_MIN_SPEED, ALLY_MAX_SPEED, ALLY_IMAGE_PATH, ENABLE_ALLY_OPACITY, ALLY_OPACITY_MIN, ALLY_OPACITY_MAX) for _ in range(ALLY_COUNT)]

        # Generate a random background color
        background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        screen.fill(background_color)

        if ENABLE_PLAYER_ROTATION:
            central_icon, central_icon_rect = get_rotated_image_and_rect(central_icon_base, central_icon_rect, current_rotation_frame * ROTATION_STEP)
        else:
            central_icon = central_icon_base

        screen.blit(central_icon, central_icon_rect)

        annotations = []

        # Label the player (central icon)
        if LABEL_PLAYER:
            bounding_rect = central_icon_rect  # Use the exact rect of the image sprite

            x_center = (bounding_rect.centerx / SCREEN_WIDTH)
            y_center = (bounding_rect.centery / SCREEN_HEIGHT)
            width = (bounding_rect.width / SCREEN_WIDTH)
            height = (bounding_rect.height / SCREEN_HEIGHT)
            annotations.append(f"2 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

            if SHOW_BOUNDING_BOXES:
                pygame.draw.rect(screen, (0, 255, 0), bounding_rect, 1)

        # Handle enemies
        if SHOW_ENEMIES:
            for enemy in enemies:
                if ENABLE_ENEMY_MOVEMENT:
                    enemy['rect'].x += enemy['dx']
                    enemy['rect'].y += enemy['dy']

                    if enemy['rect'].left <= 0 or enemy['rect'].right >= SCREEN_WIDTH:
                        enemy['dx'] *= -1
                    if enemy['rect'].top <= 0 or enemy['rect'].bottom >= SCREEN_HEIGHT:
                        enemy['dy'] *= -1

                rotation_angle = -enemy['angle'] - 90
                rotated_enemy_image, rotated_enemy_rect = get_rotated_image_and_rect(enemy['image'], enemy['rect'], rotation_angle)
                screen.blit(rotated_enemy_image, rotated_enemy_rect)

                bounding_rect = enemy['rect']  # Use the exact rect of the image sprite

                x_center = (bounding_rect.centerx / SCREEN_WIDTH)
                y_center = (bounding_rect.centery / SCREEN_HEIGHT)
                width = (bounding_rect.width / SCREEN_WIDTH)
                height = (bounding_rect.height / SCREEN_HEIGHT)
                if LABEL_ENEMIES:
                    annotations.append(f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

                if SHOW_BOUNDING_BOXES:
                    pygame.draw.rect(screen, (0, 255, 0), bounding_rect, 1)

        # Handle allies
        if SHOW_ALLIES:
            for ally in allies:
                if ENABLE_ENEMY_MOVEMENT:
                    ally['rect'].x += ally['dx']
                    ally['rect'].y += ally['dy']

                    if ally['rect'].left <= 0 or ally['rect'].right >= SCREEN_WIDTH:
                        ally['dx'] *= -1
                    if ally['rect'].top <= 0 or ally['rect'].bottom >= SCREEN_HEIGHT:
                        ally['dy'] *= -1

                rotation_angle = -ally['angle'] - 90
                rotated_ally_image, rotated_ally_rect = get_rotated_image_and_rect(ally['image'], ally['rect'], rotation_angle)
                screen.blit(rotated_ally_image, rotated_ally_rect)

                bounding_rect = ally['rect']  # Use the exact rect of the image sprite

                x_center = (bounding_rect.centerx / SCREEN_WIDTH)
                y_center = (bounding_rect.centery / SCREEN_HEIGHT)
                width = (bounding_rect.width / SCREEN_WIDTH)
                height = (bounding_rect.height / SCREEN_HEIGHT)
                if LABEL_ALLIES:
                    annotations.append(f"1 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

                if SHOW_BOUNDING_BOXES:
                    pygame.draw.rect(screen, (0, 255, 0), bounding_rect, 1)

        pygame.display.flip()

        if SAVE_IMAGE:
            pygame.image.save(screen, os.path.join(screenshot_dir, f"Image-{FRAME}.png"))

        if SAVE_LABELS:
            with open(os.path.join(screenshot_dir, f"Image-{FRAME}.txt"), 'w') as f:
                for annotation in annotations:
                    f.write(annotation + '\n')

        if GENERATE_ROBUST_DATASET:
            if current_rotation_frame < ROTATION_NUMBER_OF_FRAMES:
                if ENABLE_PLAYER_ROTATION:
                    central_icon, central_icon_rect = get_rotated_image_and_rect(central_icon_base, central_icon_rect, current_rotation_frame * ROTATION_STEP)
                current_rotation_frame += 1
            else:
                current_rotation_frame = 0
                if current_opacity_frame < OPACITY_NUMBER_OF_FRAMES:
                    current_opacity = int(ENEMY_OPACITY_MIN + current_opacity_frame * OPACITY_STEP)
                    current_opacity_frame += 1
                    enemies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, (24, 24), MIN_SPEED, MAX_SPEED, ENEMY_IMAGE_PATH, ENABLE_ENEMY_OPACITY, current_opacity, current_opacity) for _ in range(ENEMY_COUNT)]
                else:
                    pygame.quit()
                    sys.exit()
        else:
            if FRAME == ROTATION_NUMBER_OF_FRAMES * OPACITY_NUMBER_OF_FRAMES:
                pygame.quit()
                sys.exit()

        clock.tick(20)  # Aim for 20 frames per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
