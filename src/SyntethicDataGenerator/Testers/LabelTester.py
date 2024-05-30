import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

# Paths
SCREENSHOT_DIR = 'screenshots'

def draw_bounding_box(screen, label, color):
    """Draws a bounding box on the screen based on the YOLO label."""
    cls, x_center, y_center, width, height = map(float, label.split())
    x_center *= SCREEN_WIDTH
    y_center *= SCREEN_HEIGHT
    width *= SCREEN_WIDTH
    height *= SCREEN_HEIGHT

    x = x_center - width / 2
    y = y_center - height / 2

    pygame.draw.rect(screen, color, pygame.Rect(x, y, width, height), 2)

def main():
    # List all .png files and corresponding .txt files
    files = os.listdir(SCREENSHOT_DIR)
    images = sorted([f for f in files if f.endswith('.png')])
    labels = sorted([f for f in files if f.endswith('.txt')])

    # Ensure each image has a corresponding label file
    image_label_pairs = [(img, img.replace('.png', '.txt')) for img in images if img.replace('.png', '.txt') in labels]

    if not image_label_pairs:
        print("No matching image-label pairs found.")
        return

    clock = pygame.time.Clock()
    index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    index = (index + 1) % len(image_label_pairs)
                elif event.key == pygame.K_LEFT:
                    index = (index - 1) % len(image_label_pairs)

        # Load image and label
        image_path, label_path = image_label_pairs[index]

        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        image = pygame.image.load(os.path.join(SCREENSHOT_DIR, image_path))
        screen.blit(image, (0, 0))

        with open(os.path.join(SCREENSHOT_DIR, label_path), 'r') as f:
            labels = f.readlines()
            for label in labels:
                color = (0, 255, 0) if label.startswith('0') else (0, 0, 255)
                draw_bounding_box(screen, label, color)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
