import pygame
import random
import sys
import os
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (40, 40, 40)
LIGHT_GRAY = (60, 60, 60)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)

# Fruit colors and names
FRUITS = [
    {"name": "Apple", "color": RED},
    {"name": "Banana", "color": YELLOW},
    {"name": "Orange", "color": ORANGE},
    {"name": "Strawberry", "color": RED},
    {"name": "Grape", "color": PURPLE},
    {"name": "Blueberry", "color": BLUE},
    {"name": "Watermelon", "color": RED},
    {"name": "Peach", "color": PINK},
    {"name": "Lemon", "color": YELLOW},
    {"name": "Pear", "color": GREEN}
]

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Anaconda")

# Font setup - using system fonts for better Windows compatibility
try:
    # Try to use Arial font which is common on Windows
    font = pygame.font.SysFont('arial', 36)
    title_font = pygame.font.SysFont('arial', 48)
except:
    # Fallback to default font if Arial is not available
    font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 48)

# Create a directory for fruit images if it doesn't exist
# Use os.path.join for cross-platform compatibility
fruits_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fruits')
if not os.path.exists(fruits_dir):
    os.makedirs(fruits_dir)

# Function to create a simple fruit image
def create_fruit_image(color, name):
    img = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
    
    # Draw a circle for the fruit
    pygame.draw.circle(img, color, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 2)
    
    # Add a stem
    stem_color = (0, 100, 0)  # Dark green
    pygame.draw.line(img, stem_color, (GRID_SIZE//2, 2), (GRID_SIZE//2, 6), 2)
    
    # Add a leaf
    leaf_color = (0, 150, 0)  # Light green
    leaf_points = [(GRID_SIZE//2, 2), (GRID_SIZE//2 + 5, 0), (GRID_SIZE//2 + 3, 4)]
    pygame.draw.polygon(img, leaf_color, leaf_points)
    
    # Save the image using os.path.join for cross-platform compatibility
    img_path = os.path.join(fruits_dir, f'{name.lower()}.png')
    pygame.image.save(img, img_path)
    return img

# Create and load fruit images
fruit_images = {}
fruit_names = ["Apple", "Banana", "Orange", "Strawberry", "Grape", "Blueberry", "Watermelon", "Peach", "Lemon", "Pear"]
fruit_colors = [RED, (255, 255, 0), (255, 165, 0), RED, (128, 0, 128), (0, 0, 255), RED, (255, 192, 203), (255, 255, 0), GREEN]

for i, name in enumerate(fruit_names):
    # Check if image already exists using os.path.join
    img_path = os.path.join(fruits_dir, f'{name.lower()}.png')
    if os.path.exists(img_path):
        try:
            fruit_images[name] = pygame.image.load(img_path)
        except pygame.error:
            # If loading fails, create a new image
            fruit_images[name] = create_fruit_image(fruit_colors[i], name)
    else:
        # Create and save the image
        fruit_images[name] = create_fruit_image(fruit_colors[i], name)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.last_direction = (1, 0)

    def move(self):
        current = self.positions[0]
        x, y = self.direction
        new = ((current[0] + x) % GRID_WIDTH, (current[1] + y) % GRID_HEIGHT)
        
        if new in self.positions[1:]:
            return False
        
        self.positions.insert(0, new)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        self.last_direction = self.direction
        return True

    def change_direction(self, new_direction):
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        if new_direction != opposite:
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.fruit = self.generate_fruit()

    def generate_position(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)
    
    def generate_fruit(self):
        return random.choice(fruit_names)

def draw_score(score):
    # Draw score panel background
    score_panel = pygame.Rect(10, 10, 200, 40)
    pygame.draw.rect(window, GRAY, score_panel)
    pygame.draw.rect(window, LIGHT_GRAY, score_panel, 2)
    
    # Draw score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=score_panel.center)
    window.blit(score_text, score_rect)

def draw_game_over(score):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    window.blit(overlay, (0, 0))
    
    # Draw game over panel
    panel_width = 400
    panel_height = 200
    panel = pygame.Rect((WINDOW_WIDTH - panel_width) // 2, 
                       (WINDOW_HEIGHT - panel_height) // 2,
                       panel_width, panel_height)
    pygame.draw.rect(window, GRAY, panel)
    pygame.draw.rect(window, LIGHT_GRAY, panel, 2)
    
    # Draw game over text
    game_over_text = title_font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart", True, WHITE)
    
    window.blit(game_over_text, game_over_text.get_rect(center=(panel.centerx, panel.centery - 40)))
    window.blit(score_text, score_text.get_rect(center=(panel.centerx, panel.centery)))
    window.blit(restart_text, restart_text.get_rect(center=(panel.centerx, panel.centery + 40)))

def draw_snake(snake):
    # Draw snake body segments
    for i, position in enumerate(snake.positions):
        x, y = position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        # Determine if this is the head, body, or tail
        if i == 0:  # Head
            # Draw head with eyes
            pygame.draw.rect(window, DARK_GREEN, rect)
            
            # Draw eyes based on direction
            eye_color = WHITE
            pupil_color = BLACK
            
            # Calculate eye positions based on direction
            if snake.direction == (1, 0):  # Right
                left_eye = (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5)
                right_eye = (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + GRID_SIZE - 5)
            elif snake.direction == (-1, 0):  # Left
                left_eye = (x * GRID_SIZE + 5, y * GRID_SIZE + 5)
                right_eye = (x * GRID_SIZE + 5, y * GRID_SIZE + GRID_SIZE - 5)
            elif snake.direction == (0, -1):  # Up
                left_eye = (x * GRID_SIZE + 5, y * GRID_SIZE + 5)
                right_eye = (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + 5)
            else:  # Down
                left_eye = (x * GRID_SIZE + 5, y * GRID_SIZE + GRID_SIZE - 5)
                right_eye = (x * GRID_SIZE + GRID_SIZE - 5, y * GRID_SIZE + GRID_SIZE - 5)
            
            # Draw eyes
            pygame.draw.circle(window, eye_color, left_eye, 3)
            pygame.draw.circle(window, eye_color, right_eye, 3)
            pygame.draw.circle(window, pupil_color, left_eye, 1)
            pygame.draw.circle(window, pupil_color, right_eye, 1)
            
            # Draw tongue
            tongue_color = RED
            if snake.direction == (1, 0):  # Right
                tongue_start = (x * GRID_SIZE + GRID_SIZE, y * GRID_SIZE + GRID_SIZE // 2)
                tongue_end = (x * GRID_SIZE + GRID_SIZE + 5, y * GRID_SIZE + GRID_SIZE // 2)
            elif snake.direction == (-1, 0):  # Left
                tongue_start = (x * GRID_SIZE, y * GRID_SIZE + GRID_SIZE // 2)
                tongue_end = (x * GRID_SIZE - 5, y * GRID_SIZE + GRID_SIZE // 2)
            elif snake.direction == (0, -1):  # Up
                tongue_start = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE)
                tongue_end = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE - 5)
            else:  # Down
                tongue_start = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE)
                tongue_end = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE + 5)
            
            pygame.draw.line(window, tongue_color, tongue_start, tongue_end, 2)
            
        elif i == len(snake.positions) - 1:  # Tail
            # Draw tail with a point
            pygame.draw.rect(window, GREEN, rect)
            
            # Draw tail point
            if len(snake.positions) > 1:
                prev_pos = snake.positions[i-1]
                dx = prev_pos[0] - x
                dy = prev_pos[1] - y
                
                # Calculate tail point position
                if dx == 1:  # Coming from right
                    point_x = x * GRID_SIZE
                elif dx == -1:  # Coming from left
                    point_x = x * GRID_SIZE + GRID_SIZE
                else:
                    point_x = x * GRID_SIZE + GRID_SIZE // 2
                    
                if dy == 1:  # Coming from bottom
                    point_y = y * GRID_SIZE
                elif dy == -1:  # Coming from top
                    point_y = y * GRID_SIZE + GRID_SIZE
                else:
                    point_y = y * GRID_SIZE + GRID_SIZE // 2
                
                # Draw tail point
                pygame.draw.circle(window, DARK_GREEN, (point_x, point_y), 3)
        else:  # Body
            # Draw body segment with pattern
            pygame.draw.rect(window, GREEN, rect)
            
            # Add pattern to body
            pattern_color = LIGHT_GREEN
            pattern_size = 4
            pattern_x = x * GRID_SIZE + (GRID_SIZE - pattern_size) // 2
            pattern_y = y * GRID_SIZE + (GRID_SIZE - pattern_size) // 2
            pygame.draw.rect(window, pattern_color, (pattern_x, pattern_y, pattern_size, pattern_size))

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake = Snake()
                        food = Food()
                        score = 0
                        game_over = False
                else:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))

        if not game_over:
            if not snake.move():
                game_over = True

            # Check if snake ate food
            if snake.positions[0] == food.position:
                snake.grow = True
                food.position = food.generate_position()
                food.fruit = food.generate_fruit()
                score += 1

        # Drawing
        window.fill(BLACK)
        
        # Draw grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(window, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(window, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # Draw snake with realistic appearance
        draw_snake(snake)

        # Draw food (fruit image)
        food_rect = pygame.Rect(food.position[0] * GRID_SIZE, food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        window.blit(fruit_images[food.fruit], food_rect)

        # Draw score
        draw_score(score)

        if game_over:
            draw_game_over(score)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main() 