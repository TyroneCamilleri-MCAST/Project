import pygame
import random
import sys
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
BG_COLOR = (100, 100, 140)  # Grayish blue background

# Paths
CENTRAL_ICON_PATH = 'data/Icons/player24.png'
ENEMY_IMAGE_PATH = 'data/Icons/player24_red.png'
ALLY_IMAGE_PATH = 'data/Icons/player24_blue.png'

# General Settings
SAVE_IMAGE = False
SAVE_LABELS = False

# Enemy settings
ENEMY_COUNT = random.randint(1, 2)
ENEMY_SIZE = (24, 24)  # Size for enemies
MIN_SPEED = 2  # Minimum speed
MAX_SPEED = 5  # Maximum speed

# Ally settings
ALLY_COUNT = random.randint(1, 1)
ALLY_SIZE = (24, 24)  # Size for allies
ALLY_MIN_SPEED = 1  # Minimum speed
ALLY_MAX_SPEED = 3  # Maximum speed

# Game settings
INFINITE_RUN = True
ROTATE_CENTER_ICON = False
ENABLE_PLAYER_ROTATION = True
ENABLE_ENEMY_MOVEMENT = True
ENABLE_ALLY_MOVEMENT = True
ENABLE_ENEMY_OPACITY = True
ENEMY_OPACITY_MIN = 255
ENEMY_OPACITY_MAX = 255
ENABLE_ALLY_OPACITY = True
ALLY_OPACITY_MIN = 255
ALLY_OPACITY_MAX = 255
SHOW_BOUNDING_BOXES = False
BOUNDING_BOX_SCALE = 0.8
BOUNDING_BOX_OFFSET_X = -1
BOUNDING_BOX_OFFSET_Y = -1

GENERATE_ROBUST_DATASET = False
ROTATION_NUMBER_OF_FRAMES = 15
OPACITY_NUMBER_OF_FRAMES = 15

ROTATION_STEP = 360 / ROTATION_NUMBER_OF_FRAMES
OPACITY_STEP = (ENEMY_OPACITY_MAX - ENEMY_OPACITY_MIN) / OPACITY_NUMBER_OF_FRAMES

SHOW_ENEMIES = True
SHOW_ALLIES = True
LABEL_ENEMIES = False
LABEL_ALLIES = False
LABEL_PLAYER = False

def load_and_scale_image(path, size, opacity=None):
    image = pygame.image.load(path).convert_alpha()
    scaled_image = pygame.transform.scale(image, size)
    if opacity is not None:
        scaled_image.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return scaled_image

def create_entity(screen_width, screen_height, size, min_speed, max_speed, enable_opacity=False, opacity_min=0, opacity_max=255):
    rect = pygame.Rect(random.randint(0, screen_width - size[0]), random.randint(0, screen_height - size[1]), *size)
    speed = random.uniform(min_speed, max_speed)
    target = (random.randint(0, screen_width - size[0]), random.randint(0, screen_height - size[1]))
    opacity = None
    if enable_opacity:
        opacity = random.randint(opacity_min, opacity_max)
    return {
        'rect': rect,
        'speed': speed,
        'target': target,
        'opacity': opacity
    }

def move_towards_target(entity):
    entity_center = entity['rect'].center
    target_center = entity['target']
    angle = math.atan2(target_center[1] - entity_center[1], target_center[0] - entity_center[0])
    dx = math.cos(angle) * entity['speed']
    dy = math.sin(angle) * entity['speed']
    new_center = (entity_center[0] + dx, entity_center[1] + dy)
    entity['rect'].center = new_center

    if math.hypot(target_center[0] - new_center[0], target_center[1] - new_center[1]) < entity['speed']:
        entity['target'] = (random.randint(0, SCREEN_WIDTH - entity['rect'].width), random.randint(0, SCREEN_HEIGHT - entity['rect'].height))

def get_rotated_image_and_rect(image, rect, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, rotated_rect

def draw_bounding_box(screen, rect, scale, offset_x, offset_y, color=(0, 255, 0)):
    scaled_width = int(rect.width * scale)
    scaled_height = int(rect.height * scale)
    scaled_rect = pygame.Rect(
        rect.left + offset_x,
        rect.top + offset_y,
        scaled_width,
        scaled_height
    )
    pygame.draw.rect(screen, color, scaled_rect, 2)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    central_icon_base = load_and_scale_image(CENTRAL_ICON_PATH, ENEMY_SIZE)  # Base image without rotation

    enemies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, MIN_SPEED, MAX_SPEED, ENABLE_ENEMY_OPACITY, ENEMY_OPACITY_MIN, ENEMY_OPACITY_MAX) for _ in range(ENEMY_COUNT)]
    allies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, ALLY_SIZE, ALLY_MIN_SPEED, ALLY_MAX_SPEED, ENABLE_ALLY_OPACITY, ALLY_OPACITY_MIN, ALLY_OPACITY_MAX) for _ in range(ALLY_COUNT)]

    central_icon_rect = central_icon_base.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    clock = pygame.time.Clock()  # Create a clock object

    running = True
    FRAME = 0
    current_rotation_frame = 0
    current_opacity_frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        FRAME += 1

        screen.fill(BG_COLOR)

        if ENABLE_PLAYER_ROTATION:
            central_icon = pygame.transform.rotate(central_icon_base, current_rotation_frame * ROTATION_STEP)
        else:
            central_icon = central_icon_base

        screen.blit(central_icon, central_icon_rect)

        # Draw bounding box for central icon
        if SHOW_BOUNDING_BOXES:
            draw_bounding_box(screen, central_icon_rect, BOUNDING_BOX_SCALE, BOUNDING_BOX_OFFSET_X, BOUNDING_BOX_OFFSET_Y)

        # Handle enemies
        if SHOW_ENEMIES:
            for enemy in enemies:
                if ENABLE_ENEMY_MOVEMENT:
                    move_towards_target(enemy)

                rotation_angle = -math.degrees(math.atan2(enemy['target'][1] - enemy['rect'].centery, enemy['target'][0] - enemy['rect'].centerx)) - 90
                enemy_image = load_and_scale_image(ENEMY_IMAGE_PATH, ENEMY_SIZE, enemy['opacity']) if ENABLE_ENEMY_OPACITY else load_and_scale_image(ENEMY_IMAGE_PATH, ENEMY_SIZE)
                rotated_enemy_image, rotated_enemy_rect = get_rotated_image_and_rect(enemy_image, enemy['rect'], rotation_angle)
                screen.blit(rotated_enemy_image, rotated_enemy_rect)

                # Draw bounding box for enemy
                if SHOW_BOUNDING_BOXES:
                    draw_bounding_box(screen, rotated_enemy_rect, BOUNDING_BOX_SCALE, BOUNDING_BOX_OFFSET_X, BOUNDING_BOX_OFFSET_Y)

        # Handle allies
        if SHOW_ALLIES:
            for ally in allies:
                if ENABLE_ALLY_MOVEMENT:
                    move_towards_target(ally)

                rotation_angle = -math.degrees(math.atan2(ally['target'][1] - ally['rect'].centery, ally['target'][0] - ally['rect'].centerx)) - 90
                ally_image = load_and_scale_image(ALLY_IMAGE_PATH, ALLY_SIZE, ally['opacity']) if ENABLE_ALLY_OPACITY else load_and_scale_image(ALLY_IMAGE_PATH, ALLY_SIZE)
                rotated_ally_image, rotated_ally_rect = get_rotated_image_and_rect(ally_image, ally['rect'], rotation_angle)
                screen.blit(rotated_ally_image, rotated_ally_rect)

                # Draw bounding box for ally
                if SHOW_BOUNDING_BOXES:
                    draw_bounding_box(screen, rotated_ally_rect, BOUNDING_BOX_SCALE, BOUNDING_BOX_OFFSET_X, BOUNDING_BOX_OFFSET_Y)

        pygame.display.flip()
        
        if not INFINITE_RUN:
            if GENERATE_ROBUST_DATASET:
                if current_rotation_frame < ROTATION_NUMBER_OF_FRAMES:
                    if ENABLE_PLAYER_ROTATION:
                        central_icon = pygame.transform.rotate(central_icon_base, current_rotation_frame * ROTATION_STEP)
                    current_rotation_frame += 1
                else:
                    current_rotation_frame = 0
                    if current_opacity_frame < OPACITY_NUMBER_OF_FRAMES:
                        current_opacity = int(ENEMY_OPACITY_MIN + current_opacity_frame * OPACITY_STEP)
                        current_opacity_frame += 1
                        enemies = [create_entity(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, MIN_SPEED, MAX_SPEED, ENABLE_ENEMY_OPACITY, current_opacity, current_opacity) for _ in range(ENEMY_COUNT)]
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
