import pygame
import random
import sys
import os
import json
from collections import deque

pygame.init()

def load_high_scores():
    try:
        with open('high_scores.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, ValueError):
        with open('high_scores.json', 'w') as file:
            json.dump([], file)
        return []

def save_high_scores(scores):
    with open('high_scores.json', 'w') as file:
        json.dump(scores, file)

def update_high_scores(current_score, scores):
    scores.append(current_score)
    scores.sort(reverse=True)
    return scores[:5]

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except (FileNotFoundError, KeyError, ValueError):
        settings = {'screen_width': 1000, 'screen_height': 1000, 'dark_mode': False, 'ray_tracing': False, 'fullscreen': False, 'window_warp': True}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    default_settings = {'screen_width': 1000, 'screen_height': 1000, 'dark_mode': False, 'ray_tracing': False, 'fullscreen': False, 'window_warp': True}
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    return settings

settings = load_settings()
fullscreen_enabled = settings.get('fullscreen', False)
screen_width = int(settings.get('screen_width', 1000))
screen_height = int(settings.get('screen_height', 1000))
dark_mode_enabled = settings.get('dark_mode', False)
ray_tracing_enabled = settings.get('ray_tracing', False)

background_color = (50, 50, 50) if dark_mode_enabled else (255, 255, 255)

if fullscreen_enabled:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
else:
    screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption('Snake Game')

score = 0
high_scores = load_high_scores()
font = pygame.font.SysFont(None, 36)

SNAKE_SIZE = 20
FOOD_SIZE = 20
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def draw_block(color, position):
    block = pygame.Rect((position[0], position[1], SNAKE_SIZE, SNAKE_SIZE))
    pygame.draw.rect(screen, color, block)

def apply_glow_and_edge():
    glow_color_base = (255, 215, 0)
    glow_radius = 20
    snake_glow_intensity = 120
    food_glow_intensity = 140

    glow_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)

    for position in snake + [food]:
        glow_intensity = snake_glow_intensity if position in snake else food_glow_intensity
        pygame.draw.circle(glow_surface, glow_color_base + (glow_intensity,), (position[0] + SNAKE_SIZE // 2, position[1] + SNAKE_SIZE // 2), glow_radius)

    for i in range(len(snake) - 1):
        start = snake[i]
        end = snake[i + 1]
        num_inter_points = 5

        if abs(start[0] - end[0]) > SNAKE_SIZE * num_inter_points or abs(start[1] - end[1]) > SNAKE_SIZE * num_inter_points:
            continue

        for j in range(1, num_inter_points):
            interp_x = start[0] + (end[0] - start[0]) * j / num_inter_points
            interp_y = start[1] + (end[1] - start[1]) * j / num_inter_points

            pygame.draw.circle(glow_surface, glow_color_base + (snake_glow_intensity,), (int(interp_x) + SNAKE_SIZE // 2, int(interp_y) + SNAKE_SIZE // 2), glow_radius)

    if ray_tracing_enabled:
        pass
    screen.blit(glow_surface, (0, 0))

def random_food_position(snake):
    while True:
        x = random.randint(0, (screen_width - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        y = random.randint(0, (screen_height - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE
        if (x, y) not in snake:
            return (x, y)

snake = [(500, 500)]
food = random_food_position(snake)
direction_queue = deque(['RIGHT'])

clock = pygame.time.Clock()
base_speed = 10
speed_increase_interval = 60000
last_speed_increase = pygame.time.get_ticks()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            current_direction = direction_queue[-1]
            new_direction = None
            if event.key == pygame.K_UP and current_direction != 'DOWN':
                new_direction = 'UP'
            elif event.key == pygame.K_DOWN and current_direction != 'UP':
                new_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and current_direction != 'RIGHT':
                new_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and current_direction != 'LEFT':
                new_direction = 'RIGHT'
            if new_direction:
                direction_queue.append(new_direction)

    if len(direction_queue) > 1:
        direction_queue.popleft()
    direction = direction_queue[0]

    head_x, head_y = snake[0]
    if direction == 'UP':
        head_y -= SNAKE_SIZE
    elif direction == 'DOWN':
        head_y += SNAKE_SIZE
    elif direction == 'LEFT':
        head_x -= SNAKE_SIZE
    elif direction == 'RIGHT':
        head_x += SNAKE_SIZE

    if settings['window_warp']:
        head_x %= screen.get_width()
        head_y %= screen.get_height()
    else:
        if head_x < 0 or head_x >= screen.get_width() or head_y < 0 or head_y >= screen.get_height():
            running = False

    new_head = (head_x, head_y)

    if new_head in snake:
        running = False

    snake.insert(0, new_head)
    if new_head == food:
        food = random_food_position(snake)
        score += 1
    else:
        snake.pop()

    screen.fill(background_color)
    for part in snake:
        draw_block(RED, part)
    draw_block(GREEN, food)

    if ray_tracing_enabled:
        apply_glow_and_edge()

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(base_speed)

high_scores = update_high_scores(score, high_scores)
save_high_scores(high_scores)

with open('game_over_signal.txt', 'w') as f:
    f.write('GameOver')

pygame.quit()