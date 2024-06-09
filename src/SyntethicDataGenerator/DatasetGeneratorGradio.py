import pygame
import random
import sys
import os
from datetime import datetime
import math
import gradio as gr

pygame.init()

SCREEN_SIZE = (256, 256)
PATHS = {
    "central_icon": ['assets/icons/player24.png'],
    "enemy_images": ['assets/Icons/player24_red.png'],
    "ally_images": ['assets/icons/player24_blue.png'],
    "background_folder": r'C:\Users\Abzsorb\Desktop\Mini-mapObjectDetection\assets\images\Background\CallOfDutyMap'
}
SAVE_SETTINGS = {"image": True, "labels": True}
ENTITY_SETTINGS = {
    "size": (24, 24),
    "enemy_count_range": (0, 4),
    "ally_count_range": (0, 4),
    "speed_range": {"enemies": (2, 5), "allies": (1, 3)}
}
FRAME_SETTINGS = {"regen_every_frame": True, "number_of_frames": 50}
BACKGROUND = {
    "custom": True,
    "color_range": {"min": 100, "max": 200}
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

def create_entity(screen_dims, size, speed_range, opacity_settings, image_paths):
    angle, speed = random.randint(0, 360), random.randint(*speed_range)
    opacity = random.randint(opacity_settings["min"], opacity_settings["max"]) if opacity_settings["enable"] else None
    return {
        'rect': pygame.Rect(random.randint(0, screen_dims[0] - size[0]), random.randint(0, screen_dims[1] - size[1]), *size),
        'dx': math.cos(math.radians(angle)) * speed,
        'dy': math.sin(math.radians(angle)) * speed,
        'angle': angle,
        'opacity': opacity,
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

def run_simulation(custom_background, regen_every_frame, number_of_frames,
                   enemy_count_range_min, enemy_count_range_max,
                   ally_count_range_min, ally_count_range_max,
                   enemy_speed_min, enemy_speed_max, ally_speed_min, ally_speed_max,
                   player_visible, enemies_visible, allies_visible,
                   player_movement, enemies_movement, allies_movement,
                   player_opacity_enable, player_opacity_min, player_opacity_max,
                   enemies_opacity_enable, enemies_opacity_min, enemies_opacity_max,
                   allies_opacity_enable, allies_opacity_min, allies_opacity_max,
                   label_player, label_enemies, label_allies,
                   rot_opac_enable, rot_opac_frames, rot_opac_min, rot_opac_max,
                   color_range_min, color_range_max, bounding_box_inflate_x, bounding_box_inflate_y,
                   bounding_box_move_x, bounding_box_move_y):
    
    global BACKGROUND, FRAME_SETTINGS, ENTITY_SETTINGS, VISIBLE, MOVEMENT, OPACITY, LABEL, ROT_OPAC_SETTINGS

    BACKGROUND["custom"] = custom_background
    BACKGROUND["color_range"]["min"] = color_range_min
    BACKGROUND["color_range"]["max"] = color_range_max
    FRAME_SETTINGS["regen_every_frame"] = regen_every_frame
    FRAME_SETTINGS["number_of_frames"] = number_of_frames

    ENTITY_SETTINGS["enemy_count_range"] = (enemy_count_range_min, enemy_count_range_max)
    ENTITY_SETTINGS["ally_count_range"] = (ally_count_range_min, ally_count_range_max)
    ENTITY_SETTINGS["speed_range"]["enemies"] = (enemy_speed_min, enemy_speed_max)
    ENTITY_SETTINGS["speed_range"]["allies"] = (ally_speed_min, ally_speed_max)

    VISIBLE["player"] = player_visible
    VISIBLE["enemies"] = enemies_visible
    VISIBLE["allies"] = allies_visible

    MOVEMENT["player"] = player_movement
    MOVEMENT["enemies"] = enemies_movement
    MOVEMENT["allies"] = allies_movement

    OPACITY["player"]["enable"] = player_opacity_enable
    OPACITY["player"]["min"] = player_opacity_min
    OPACITY["player"]["max"] = player_opacity_max

    OPACITY["enemies"]["enable"] = enemies_opacity_enable
    OPACITY["enemies"]["min"] = enemies_opacity_min
    OPACITY["enemies"]["max"] = enemies_opacity_max

    OPACITY["allies"]["enable"] = allies_opacity_enable
    OPACITY["allies"]["min"] = allies_opacity_min
    OPACITY["allies"]["max"] = allies_opacity_max

    LABEL["player"] = label_player
    LABEL["enemies"] = label_enemies
    LABEL["allies"] = label_allies

    ROT_OPAC_SETTINGS["enable"] = rot_opac_enable
    ROT_OPAC_SETTINGS["frames"] = rot_opac_frames
    ROT_OPAC_SETTINGS["step_rot"] = 360 / rot_opac_frames
    ROT_OPAC_SETTINGS["min_opac"] = rot_opac_min
    ROT_OPAC_SETTINGS["max_opac"] = rot_opac_max
    ROT_OPAC_SETTINGS["step_opac"] = (rot_opac_max - rot_opac_min) / rot_opac_frames

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    if BACKGROUND["custom"]:
        backgrounds = load_backgrounds(PATHS["background_folder"])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_dir = os.path.join('dataset/object_detection', timestamp)
    os.makedirs(screenshot_dir, exist_ok=True)

    frame = rotation_frame = 0

    while frame < FRAME_SETTINGS["number_of_frames"]:
        frame += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if FRAME_SETTINGS["regen_every_frame"]:
            base_image_path = random.choice(PATHS["central_icon"])
            base_image = load_image(base_image_path, ENTITY_SETTINGS["size"])
            central_icon_rect = base_image.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
            enemies = []
            allies = []
            if VISIBLE["enemies"]:
                enemy_count = random.randint(*ENTITY_SETTINGS["enemy_count_range"])
                enemies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], ENTITY_SETTINGS["speed_range"]["enemies"], OPACITY["enemies"], PATHS["enemy_images"]) for _ in range(enemy_count)]
            if VISIBLE["allies"]:
                ally_count = random.randint(*ENTITY_SETTINGS["ally_count_range"])
                allies = [create_entity(SCREEN_SIZE, ENTITY_SETTINGS["size"], ENTITY_SETTINGS["speed_range"]["allies"], OPACITY["allies"], PATHS["ally_images"]) for _ in range(ally_count)]

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

        annotations = []

        def process_entity(entity, label):
            entity_type = 'enemies' if label == 0 else 'allies'
            if MOVEMENT[entity_type]:
                entity['rect'].x += entity['dx']
                entity['rect'].y += entity['dy']
                if entity['rect'].left <= 0 or entity['rect'].right >= SCREEN_SIZE[0]:
                    entity['dx'] *= -1
                if entity['rect'].top <= 0 or entity['rect'].bottom >= SCREEN_SIZE[1]:
                    entity['dy'] *= -1

            opacity = entity['opacity']
            img = load_image(entity['image_path'], ENTITY_SETTINGS["size"], opacity)
            img, img_rect = rotate_image(img, entity['rect'], -entity['angle'] - 90)
            screen.blit(img, img_rect)
            bounding_rect = entity['rect'].inflate(bounding_box_inflate_x, bounding_box_inflate_y).move(bounding_box_move_x, bounding_box_move_y)
            pygame.draw.rect(screen, (0, 255, 0) if entity_type == 'enemies' else (0, 0, 255), bounding_rect, 1)  # Draw bounding box
            x_center, y_center = bounding_rect.centerx / SCREEN_SIZE[0], bounding_rect.centery / SCREEN_SIZE[1]
            width, height = bounding_rect.width / SCREEN_SIZE[0], bounding_rect.height / SCREEN_SIZE[1]
            annotations.append(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")


        if VISIBLE["player"]:
            screen.blit(central_icon_rotated, central_icon_rect)
            bounding_rect = central_icon_rect.inflate(bounding_box_inflate_x, bounding_box_inflate_y).move(bounding_box_move_x, bounding_box_move_y)
            pygame.draw.rect(screen, (255, 0, 0), bounding_rect, 1)  # Draw bounding box

        if LABEL["player"]:
            x_center, y_center = bounding_rect.centerx / SCREEN_SIZE[0], bounding_rect.centery / SCREEN_SIZE[1]
            width, height = bounding_rect.width / SCREEN_SIZE[0], bounding_rect.height / SCREEN_SIZE[1]
            annotations.append(f"2 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

        for entity in enemies:
            process_entity(entity, 0)
        for entity in allies:
            process_entity(entity, 1)

        pygame.display.flip()
        save_frame(screen, annotations, frame, screenshot_dir)
        clock.tick(20)

    # Convert the final frame to a numpy array
    frame_array = pygame.surfarray.array3d(screen)
    frame_array = frame_array.swapaxes(0, 1)

    pygame.quit()
    return f"Simulation completed. Frames saved in {screenshot_dir}", frame_array


def launch_gradio_interface():
    interface = gr.Interface(
        fn=run_simulation,
        inputs=[
            gr.Checkbox(label="Custom Background", value=BACKGROUND["custom"]),
            gr.Checkbox(label="Regen Every Frame", value=FRAME_SETTINGS["regen_every_frame"]),
            gr.Slider(label="Number of Frames", minimum=10, maximum=100, step=1, value=FRAME_SETTINGS["number_of_frames"]),
            gr.Slider(label="Enemy Count Range Min", minimum=0, maximum=10, step=1, value=ENTITY_SETTINGS["enemy_count_range"][0]),
            gr.Slider(label="Enemy Count Range Max", minimum=0, maximum=10, step=1, value=ENTITY_SETTINGS["enemy_count_range"][1]),
            gr.Slider(label="Ally Count Range Min", minimum=0, maximum=10, step=1, value=ENTITY_SETTINGS["ally_count_range"][0]),
            gr.Slider(label="Ally Count Range Max", minimum=0, maximum=10, step=1, value=ENTITY_SETTINGS["ally_count_range"][1]),
            gr.Slider(label="Enemy Speed Min", minimum=1, maximum=10, step=1, value=ENTITY_SETTINGS["speed_range"]["enemies"][0]),
            gr.Slider(label="Enemy Speed Max", minimum=1, maximum=10, step=1, value=ENTITY_SETTINGS["speed_range"]["enemies"][1]),
            gr.Slider(label="Ally Speed Min", minimum=1, maximum=10, step=1, value=ENTITY_SETTINGS["speed_range"]["allies"][0]),
            gr.Slider(label="Ally Speed Max", minimum=1, maximum=10, step=1, value=ENTITY_SETTINGS["speed_range"]["allies"][1]),
            gr.Checkbox(label="Player Visible", value=VISIBLE["player"]),
            gr.Checkbox(label="Enemies Visible", value=VISIBLE["enemies"]),
            gr.Checkbox(label="Allies Visible", value=VISIBLE["allies"]),
            gr.Checkbox(label="Player Movement", value=MOVEMENT["player"]),
            gr.Checkbox(label="Enemies Movement", value=MOVEMENT["enemies"]),
            gr.Checkbox(label="Allies Movement", value=MOVEMENT["allies"]),
            gr.Checkbox(label="Player Opacity Enable", value=OPACITY["player"]["enable"]),
            gr.Slider(label="Player Opacity Min", minimum=0, maximum=255, step=1, value=OPACITY["player"]["min"]),
            gr.Slider(label="Player Opacity Max", minimum=0, maximum=255, step=1, value=OPACITY["player"]["max"]),
            gr.Checkbox(label="Enemies Opacity Enable", value=OPACITY["enemies"]["enable"]),
            gr.Slider(label="Enemies Opacity Min", minimum=0, maximum=255, step=1, value=OPACITY["enemies"]["min"]),
            gr.Slider(label="Enemies Opacity Max", minimum=0, maximum=255, step=1, value=OPACITY["enemies"]["max"]),
            gr.Checkbox(label="Allies Opacity Enable", value=OPACITY["allies"]["enable"]),
            gr.Slider(label="Allies Opacity Min", minimum=0, maximum=255, step=1, value=OPACITY["allies"]["min"]),
            gr.Slider(label="Allies Opacity Max", minimum=0, maximum=255, step=1, value=OPACITY["allies"]["max"]),
            gr.Checkbox(label="Label Player", value=LABEL["player"]),
            gr.Checkbox(label="Label Enemies", value=LABEL["enemies"]),
            gr.Checkbox(label="Label Allies", value=LABEL["allies"]),
            gr.Checkbox(label="Rotation and Opacity Enable", value=ROT_OPAC_SETTINGS["enable"]),
            gr.Slider(label="Rotation Frames", minimum=1, maximum=60, step=1, value=ROT_OPAC_SETTINGS["frames"]),
            gr.Slider(label="Rotation Opacity Min", minimum=0, maximum=255, step=1, value=ROT_OPAC_SETTINGS["min_opac"]),
            gr.Slider(label="Rotation Opacity Max", minimum=0, maximum=255, step=1, value=ROT_OPAC_SETTINGS["max_opac"]),
            gr.Slider(label="Color Range Min", minimum=0, maximum=255, step=1, value=BACKGROUND["color_range"]["min"]),
            gr.Slider(label="Color Range Max", minimum=0, maximum=255, step=1, value=BACKGROUND["color_range"]["max"]),
            gr.Slider(label="Bounding Box Inflate X", minimum=-10, maximum=10, step=1, value=0),
            gr.Slider(label="Bounding Box Inflate Y", minimum=-10, maximum=10, step=1, value=0),
            gr.Slider(label="Bounding Box Move X", minimum=-10, maximum=10, step=1, value=0),
            gr.Slider(label="Bounding Box Move Y", minimum=-10, maximum=10, step=1, value=0),
        ],
        outputs=[
            gr.Textbox(label="Simulation Output"),
            gr.Image(label="Simulation Output Image")
        ],
        title="Simulation Settings",
        description="Adjust the settings for the simulation and click submit to run."
    )

    demo = gr.TabbedInterface([interface], ["Run Simulation"])
    demo.launch()

if __name__ == "__main__":
    launch_gradio_interface()
