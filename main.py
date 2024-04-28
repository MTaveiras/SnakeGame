import pygame
import random

# pygame setup
pygame.init()
square_width = 1000
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True

# Function to generate a random starting position for the snake or food
def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return [random.randrange(*position_range), random.randrange(*position_range)]

# Function to reset the game state
def reset():
    global snake, snake_direction, snake_length
    snake_pixel.center = generate_starting_position()
    snake = [snake_pixel.copy()]
    snake_direction = (0, 0)
    snake_length = 1
    return snake_pixel.copy()

# Function to check if the snake is out of bounds
def isOutOfBounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 or snake_pixel.left < 0 or snake_pixel.right > square_width

# Function to check if the snake's head collides with any part of its body
def checkCollision():
    return any(snake_part.colliderect(snake_pixel) for snake_part in snake[1:])  # Check collision with all snake parts except the head

# snake setup
snake_pixel = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1

# food setup
food = pygame.rect.Rect([0, 0, pixel_width - 2, pixel_width - 2])
food.center = generate_starting_position()

# Font setup for displaying score
score_font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # Reset the game if snake is out of bounds or collides with itself
    if isOutOfBounds() or checkCollision():
        snake_pixel = reset()

    # Generate new food if snake eats the existing one
    if snake_pixel.colliderect(food):
        food.center = generate_starting_position()
        snake_length += 1
    else:
        snake.pop()  # Remove the tail if no food is eaten

    # Handle user input to change snake direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and snake_direction != (0, pixel_width):
        snake_direction = (0, -pixel_width)
    if keys[pygame.K_s] and snake_direction != (0, -pixel_width):
        snake_direction = (0, pixel_width)
    if keys[pygame.K_a] and snake_direction != (pixel_width, 0):
        snake_direction = (-pixel_width, 0)
    if keys[pygame.K_d] and snake_direction != (-pixel_width, 0):
        snake_direction = (pixel_width, 0)

    # Move the snake according to its direction
    snake_pixel.move_ip(snake_direction)
    snake.insert(0, snake_pixel.copy())

    # Draw the snake and food on the screen
    for snake_part in snake:
        pygame.draw.rect(screen, "green", snake_part)

    pygame.draw.rect(screen, "red", food)

    # Display the current score (snake length)
    score_text = score_font.render(f"Score: {snake_length}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(10)

pygame.quit()