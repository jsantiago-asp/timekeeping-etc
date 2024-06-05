# 5 June 2024
# jsantiago@asparis.fr
# simple countdown timer with pygame with abstract art
# just type how many minutes you want and then press enter

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FONT_SIZE = 60
BACKGROUND_COLOR = (255, 255, 255)  # White background
TEXT_COLOR = (0, 0, 0)  # Black text color
INPUT_CIRCLE_COLOR = (200, 200, 200)  # Light gray for input circle
CIRCLE_RADIUS = 50

# Mondrian colors and rectangles
RECT_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 0, 0)]  # Red, Blue, Yellow, Black
RECTANGLES = [
    (50, 50, 150, 150),
    (250, 50, 100, 300),
    (400, 50, 150, 150),
    (50, 250, 150, 150),
    (250, 400, 300, 50)
]

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Countdown Timer")

# Load font
font = pygame.font.SysFont(None, FONT_SIZE)
input_font = pygame.font.SysFont(None, 40)

# Function to draw the Mondrian style background
def draw_mondrian_background():
    screen.fill(BACKGROUND_COLOR)
    for color, rect in zip(RECT_COLORS, RECTANGLES):
        pygame.draw.rect(screen, color, rect)

# Function to get user input for the timer
def get_user_input():
    user_input = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        draw_mondrian_background()
        input_circle_pos = (CIRCLE_RADIUS + 10, CIRCLE_RADIUS + 10)
        pygame.draw.circle(screen, INPUT_CIRCLE_COLOR, input_circle_pos, CIRCLE_RADIUS)
        input_surface = input_font.render(user_input, True, TEXT_COLOR)
        text_rect = input_surface.get_rect(center=input_circle_pos)
        screen.blit(input_surface, text_rect)
        pygame.display.flip()

    return int(user_input)

# Get the countdown time from the user
countdown_minutes = get_user_input()
cdowntime = countdown_minutes * 60 * 1000  # Convert to milliseconds

# Initialize timer
start_ticks = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the number of milliseconds since the program started
    elapsed_ticks = pygame.time.get_ticks() - start_ticks

    # Calculate the remaining time
    remaining_time = cdowntime - elapsed_ticks
    minutes = remaining_time // (60 * 1000)
    seconds = (remaining_time % (60 * 1000)) // 1000

    # Render the timer
    timer_text = f"{int(minutes):02}:{int(seconds):02}"
    text_surface = font.render(timer_text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))

    # Clear screen and draw Mondrian style background
    draw_mondrian_background()

    # Draw timer text
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    # If the countdown is over, end the loop
    if remaining_time <= 0:
        break

# Display a message saying the time is up and wait for a few seconds
time_up_text = "Time's up!"
text_surface = font.render(time_up_text, True, TEXT_COLOR)
text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
screen.fill(BACKGROUND_COLOR)
for color, rect in zip(RECT_COLORS, RECTANGLES):
    pygame.draw.rect(screen, color, rect)
screen.blit(text_surface, text_rect)
pygame.display.flip()
pygame.time.wait(5000)

pygame.quit()
