import pygame
import random
import sys
import os
from datetime import datetime
import math

pygame.init()

SCREEN_SIZE = (256, 256)
PATHS = {
    "central_icon": 'data/Icons/player24.png',
    "enemy_image": 'data/Icons/player24_red.png',
    "ally_image": 'data/Icons/player24_blue.png',
    "background_folder": r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\data\images\Background\CallOfDutyMap'
}
SAVE_SETTINGS = {"image": True, "labels": True}
ENTITY_SETTINGS = {
    "size": (24, 24),
    "enemy_count_range": (0, 4),
    "ally_count_range": (0, 4),
    "speed_range": {"enemies": (2, 5), "allies": (1, 3)}
}
FRAME_SETTINGS = {"regen_every_frame": True, "number_of_frames": 5000}
BACKGROUND = {
    "custom": True,
    "color_range": {"min": 200, "max": 255}
}
LABEL = {"player": True, "enemies": True, "allies": True}
MOVEMENT = {"player": False, "enemies": False, "allies": False}
OPACITY = {
    "player": {"enable": False, "min": 255, "max": 255},
    "enemies": {"enable": False, "min": 100, "max": 255},
    "allies": {"enable": False, "min": 100, "max": 255}
}
VISIBLE = {"player": True, "enemies": True, "allies": True}
ROT_OPAC_SETTINGS = {
    "enable": True,
    "frames": 15,
    "step_rot": 360 / 15,
    "step_opac": (255 - 100) / 15,
    "min_opac": 100,
    "max_opac": 255
}

def load_image(path, size, opacity=None):
    img = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
    if opacity is not None:
        img.fill((255, 255, 255, opacity), None, pygame.BLEND_RGBA_MULT)
    return img

def load_backgrounds(folder_path):
    return [pygame.image.load(os.path.join(folder_path, f)).convert() for f in os.listdir(folder_path) if f.endswith(('png', 'jpg'))]

def create_entity(screen_dims, size, speed_range, opacity_settings):
    angle, speed = random.randint(0, 360), random.randint(*speed_range)
    opacity = random.randint(opacity_settings["min"], opacity_settings["max"]) if opacity_settings["enable"] else None
    return {
        'rect': pygame.Rect(random.randint(0, screen_dims[0] - size[0]), random.randint(0, screen_dims[1] - size[1]), *size),
        'dx': math.cos(math.radians(angle)) * speed,
        'dy': math.sin(math.radians(angle)) * speed,
        'angle': angle,
        'opacity': opacity
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

def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if BACKGROUND["custom"]:
        backgrounds = load_backgrounds(PATHS["background_folder"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join('dataset/object_detection', timestamp)
    os.makedirs(screenshot_dir, exist_ok=True)

    base_image = load_image(PATHS["central_icon"], ENTITY_SETTINGS["size"])
    central_icon_rect = base_image.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))

    frame = rotation_frame = 0

    while True:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if FRAME_SETTINGS["regen_every_frame"]:
            enemy_count = random.randint(*ENTITY_SETTINGS["enemy_count_range"])
            ally_count = random.randint(*ENTITY_SETTINGS["ally_count_range"])
            enemies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], ENTITY_SETTINGS["speed_range"]["enemies"], OPACITY["enemies"]) for _ in range(enemy_count)]
            allies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], ENTITY_SETTINGS["speed_range"]["allies"], OPACITY["allies"]) for _ in range(ally_count)]

        if BACKGROUND["custom"]:
            screen.blit(pygame.transform.scale(random.choice(backgrounds), SCREEN_SIZE), (0, 0))
        else:
            screen.fill(generate_random_pastel_color(BACKGROUND["color_range"]))

        if ROT_OPAC_SETTINGS["enable"]:
            rotation_angle = rotation_frame * ROT_OPAC_SETTINGS["step_rot"]
            central_icon_rotated, central_icon_rect = rotate_image(base_image, central_icon_rect, rotation_angle)
            rotation_frame = (rotation_frame + 1) % ROT_OPAC_SETTINGS["frames"]
        else:
            central_icon_rotated = base_image

        if VISIBLE["player"]:
            screen.blit(central_icon_rotated, central_icon_rect)

        annotations = []
        if LABEL["player"]:
            x_center, y_center = central_icon_rect.centerx / SCREEN_SIZE[0], central_icon_rect.centery / SCREEN_SIZE[1]
            width, height = central_icon_rect.width / SCREEN_SIZE[0], central_icon_rect.height / SCREEN_SIZE[1]
            annotations.append(f"2 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        for entities, img_path, label in [(enemies, PATHS["enemy_image"], 0), (allies, PATHS["ally_image"], 1)]:
            entity_type = "enemies" if label == 0 else "allies"
            if VISIBLE[entity_type]:
                for ent in entities:
                    if MOVEMENT[entity_type]:
                        ent['rect'].x += ent['dx']
                        ent['rect'].y += ent['dy']
                        if ent['rect'].left <= 0 or ent['rect'].right >= SCREEN_SIZE[0]:
                            ent['dx'] *= -1
                        if ent['rect'].top <= 0 or ent['rect'].bottom >= SCREEN_SIZE[1]:
                            ent['dy'] *= -1

                    opacity = ent['opacity']
                    img = load_image(img_path, ENTITY_SETTINGS["size"], opacity)
                    img, img_rect = rotate_image(img, ent['rect'], -ent['angle'] - 90)
                    screen.blit(img, img_rect)
                    x_center, y_center = ent['rect'].centerx / SCREEN_SIZE[0], ent['rect'].centery / SCREEN_SIZE[1]
                    width, height = ent['rect'].width / SCREEN_SIZE[0], ent['rect'].height / SCREEN_SIZE[1]
                    annotations.append(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        pygame.display.flip()
        save_frame(screen, annotations, frame, screenshot_dir)

        if frame == FRAME_SETTINGS["number_of_frames"]:
            pygame.quit()
            sys.exit()
        clock.tick(20)

if __name__ == "__main__":
    main()