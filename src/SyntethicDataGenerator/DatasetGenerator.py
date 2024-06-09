import pygame
import random
import sys
import os
from datetime import datetime
import math

pygame.init()

SCREEN_SIZE = (256, 256)
DRAW_BOUNDING_BOXES = False  # Global parameter to control bounding box drawing
PATHS = {
    "central_icon": ['assets/icons/player24.png', 'assets/icons/Player.png',],
    "enemy_images": ['assets/Icons/player24_red.png', 'assets/icons/Enemy.png'],
    "ally_images": ['assets/icons/player24_blue.png', 'assets/icons/Ally.png'],
    "background_folder": r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\assets\images\GameMap'
}
SAVE_SETTINGS = {"image": True, "labels": True}
ENTITY_SETTINGS = {
    "size": (24, 24),
    "enemy_count_range": (0, 4),
    "ally_count_range": (0, 4),
    "player_count_range": (1, 3)  # Added for multiple players
}
FRAME_SETTINGS = {"regen_every_frame": True, "number_of_frames": 50}
BACKGROUND = {
    "custom": True,
    "color_range": {"min": 30, "max": 200}
}
LABEL = {"player": True, "enemies": True, "allies": True}
OPACITY = {
    "player": {"enable": False, "min": 255, "max": 255},
    "enemies": {"enable": False, "min": 100, "max": 255},
    "allies": {"enable": False, "min": 100, "max": 255}
}
VISIBLE = {"player": True, "enemies": True, "allies": True}
ROTATE_ANGLE = random.randint(0,360)

def load_image(path, size, opacity=None):
    img = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
    if opacity is not None:
        img.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return img

def load_backgrounds(folder_path):
    return [pygame.image.load(os.path.join(folder_path, f)).convert() for f in os.listdir(folder_path) if f.endswith(('png', 'jpg'))]

def create_entity(screen_dims, size, image_paths):
    angle = random.randint(0, 360)
    return {
        'rect': pygame.Rect(random.randint(0, screen_dims[0] - size[0]), random.randint(0, screen_dims[1] - size[1]), *size),
        'angle': angle,
        'image_path': random.choice(image_paths)
    }

def rotate_image(image, rect, angle):
    rotated = pygame.transform.rotate(image, angle)
    return rotated, rotated.get_rect(center=rect.center)

def generate_random_pastel_color(color_range):
    return (random.randint(color_range["min"], color_range["max"]),
            random.randint(color_range["min"], color_range["max"]),
            random.randint(color_range["min"], color_range["max"]))

def save_frame(screen, annotations, frame, dir_path):
    if SAVE_SETTINGS["image"]:
        pygame.image.save(screen, os.path.join(dir_path, f"Image-{frame}.png"))
    if SAVE_SETTINGS["labels"]:
        with open(os.path.join(dir_path, f"Image-{frame}.txt"), 'w') as f:
            f.write('\n'.join(annotations))

def get_aabb(mask, rect):
    mask_rects = mask.get_bounding_rects()
    if not mask_rects:
        return rect  # Return the original rect if no bounding rects found
    mask_rect = mask_rects[0]
    for r in mask_rects[1:]:
        mask_rect.union_ip(r)
    mask_rect.move_ip(rect.topleft)
    return mask_rect

def annotate_entity(rect, label, annotations):
    x_center, y_center = rect.centerx / SCREEN_SIZE[0], rect.centery / SCREEN_SIZE[1]
    width, height = rect.width / SCREEN_SIZE[0], rect.height / SCREEN_SIZE[1]
    annotations.append(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    print(f"Annotation - Label: {label}, X: {x_center}, Y: {y_center}, Width: {width}, Height: {height}")

def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if BACKGROUND["custom"]:
        backgrounds = load_backgrounds(PATHS["background_folder"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join('dataset/object_detection', timestamp)
    os.makedirs(screenshot_dir, exist_ok=True)

    frame = 0

    while True:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if FRAME_SETTINGS["regen_every_frame"]:
            ROTATE_ANGLE = random.randint(0,360)
            player_count = random.randint(*ENTITY_SETTINGS["player_count_range"])
            players = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], PATHS["central_icon"]) for _ in range(player_count)]
            enemies = []
            allies = []
            if VISIBLE["enemies"]:
                enemy_count = random.randint(*ENTITY_SETTINGS["enemy_count_range"])
                enemies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], PATHS["enemy_images"]) for _ in range(enemy_count)]
            if VISIBLE["allies"]:
                ally_count = random.randint(*ENTITY_SETTINGS["ally_count_range"])
                allies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], PATHS["ally_images"]) for _ in range(ally_count)]

        if BACKGROUND["custom"]:
            screen.blit(pygame.transform.scale(random.choice(backgrounds), SCREEN_SIZE), (0, 0))
        else:
            screen.fill(generate_random_pastel_color(BACKGROUND["color_range"]))

        annotations = []

        for player in players:
            base_image = load_image(player['image_path'], ENTITY_SETTINGS["size"])
            player_rotated, player_rect = rotate_image(base_image, player['rect'], ROTATE_ANGLE)
            screen.blit(player_rotated, player_rect.topleft)
            if LABEL["player"]:
                mask = pygame.mask.from_surface(player_rotated)
                aabb = get_aabb(mask, player_rect)
                annotate_entity(aabb, 2, annotations)
                if DRAW_BOUNDING_BOXES:
                    pygame.draw.rect(screen, (255, 0, 0), aabb, 2)  # Draw bounding box if enabled
                print(f"Player AABB: {aabb}")

        for entities, label in [(enemies, 0), (allies, 1)]:
            for ent in entities:
                img = load_image(ent['image_path'], ENTITY_SETTINGS["size"])
                img, img_rect = rotate_image(img, ent['rect'], ent['angle'])
                screen.blit(img, img_rect.topleft)
                if LABEL["enemies"] or LABEL["allies"]:
                    mask = pygame.mask.from_surface(img)
                    aabb = get_aabb(mask, img_rect)
                    annotate_entity(aabb, label, annotations)
                    if DRAW_BOUNDING_BOXES:
                        pygame.draw.rect(screen, (255, 0, 0), aabb, 2)  # Draw bounding box if enabled
                    print(f"Entity AABB: {aabb}")

        pygame.display.flip()
        save_frame(screen, annotations, frame, screenshot_dir)

        if frame == FRAME_SETTINGS["number_of_frames"]:
            pygame.quit()
            sys.exit()
        clock.tick(20)

if __name__ == "__main__":
    main()
