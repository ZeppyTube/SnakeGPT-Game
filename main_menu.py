import pygame
import sys
import subprocess
import json
pygame.init()
def load_high_scores():
    try:
        with open('high_scores.json', 'r') as file:
            scores = json.load(file)
            scores = sorted(scores, reverse=True)[:5]
            return scores
    except FileNotFoundError:
        return []
def load_settings():
    default_settings = {
        'screen_width': 1500,
        'screen_height': 1000,
        'dark_mode': True,
        'ray_tracing': False,
        'fullscreen': False, 
        'window_warp': True
    }
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
            return settings
    except FileNotFoundError:
        with open('settings.json', 'w') as f:
            json.dump(default_settings, f)
        return default_settings
settings = load_settings()
screen_width, screen_height = settings['screen_width'], settings['screen_height']
background_color = (50, 50, 50) if settings['dark_mode'] else (255, 255, 255)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game - Main Menu")
white = (255, 255, 255)
dark_gray = (50, 50, 50)
black = (0, 0, 0)
red = (255, 0, 0)
font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 28)
button_width, button_height = 200, 50
button_width2, button_height2 = 320, 50
button_width3, button_height3 = 270, 50
button_width4, button_width5, button_width6, button_width7 = 550, 270, 330, 290
button_height9 = 30
title_rect, start_game_button_rect, settings_button_rect, credits_button_rect = \
    pygame.Rect(screen_width // 2 - button_width // 2, 80, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 160, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 230, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 300, button_width, button_height)
high_score_button_rect, exit_button_rect, toggle_mode_button_rect, ray_tracing_button_rect = \
    pygame.Rect(screen_width // 2 - button_width // 2, 370, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 450, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width2 // 2, 150, button_width2, button_height2), \
    pygame.Rect(screen_width // 2 - button_width // 2, 370, button_width, button_height)
credits_background_rect, credits_background2_rect, controls_1_rect, controls_2_rect = \
    pygame.Rect(screen_width // 2 - button_width3 // 2, 250, button_width3, button_height3), \
    pygame.Rect(screen_width // 2 - button_width4 // 2, 300, button_width4, button_height), \
    pygame.Rect(screen_width // 2 - button_width7 // 2, 400, button_width7, button_height), \
    pygame.Rect(screen_width // 2 - button_width7 // 2, 450, button_width7, button_height)
controls_3_rect, controls_4_rect, controls_5_rect, size_input_title_rect = \
    pygame.Rect(screen_width // 2 - button_width7 // 2, 500, button_width7, button_height), \
    pygame.Rect(screen_width // 2 - button_width7 // 2, 550, button_width7, button_height), \
    pygame.Rect(screen_width // 2 - button_width7 // 2, 590, button_width7, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 220, button_width, button_height)
size_input_title2_rect, size_input_rect, fullscreen_button_rect, window_warp_button_rect, back_button_rect = \
    pygame.Rect(screen_width // 2 - button_width6 // 2, 270, button_width6, button_height9), \
    pygame.Rect(screen_width // 2 - button_width // 2, 300, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width // 2, 420, button_width, button_height), \
    pygame.Rect(screen_width // 2 - button_width3 // 2, 490, button_width3, button_height3), \
    pygame.Rect(screen_width // 2 - button_width // 2, 600, button_width, button_height)
size_input_text = f"{settings['screen_width']}x{settings['screen_height']}"
size_input_cursor_pos = len(size_input_text)
size_input_active = False
cursor_visible = True
last_cursor_toggle = pygame.time.get_ticks()
cursor_blink_interval = 500 
clock = pygame.time.Clock()
frame_rate = 15
def draw_button(screen, text, rect, text_color, bg_color):
    pygame.draw.rect(screen, bg_color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
def main_menu():
    screen.fill(background_color)
    draw_button(screen, "SnakeGPT", title_rect, black, white)
    draw_button(screen, "Start Game", start_game_button_rect, black, white)
    draw_button(screen, "Settings", settings_button_rect, black, white)
    draw_button(screen, "Credits/Controls", credits_button_rect, black, white)
    draw_button(screen, "Exit", exit_button_rect, black, white)
    draw_button(screen, "High Scores", high_score_button_rect, black, white)
def settings_menu():
    screen.fill(background_color)
    ray_tracing_status = 'ON' if settings['ray_tracing'] else 'OFF'
    fullscreen_status = 'ON' if settings['fullscreen'] else 'OFF'
    window_warp_status = 'ON' if settings['window_warp'] else 'OFF'
    draw_button(screen, f"Ray Tracing: {ray_tracing_status}", ray_tracing_button_rect, black, white)
    draw_button(screen, f"Fullscreen: {fullscreen_status}", fullscreen_button_rect, black, white)
    draw_button(screen, f"Window Warp: {window_warp_status}", window_warp_button_rect, black, white)
    draw_button(screen, "Back", title_rect, black, white)
    draw_button(screen, "Toggle Light/Dark Mode", toggle_mode_button_rect, black, white)
    draw_button(screen, "Screen size", size_input_title_rect, black, white)
    draw_button(screen, "(Recommended min: 700)", size_input_title2_rect, black, white)
    if settings['fullscreen']:
        pygame.draw.rect(screen, dark_gray, size_input_rect)
        text_surf = input_font.render(size_input_text, True, black)
    else:
        pygame.draw.rect(screen, white, size_input_rect)
        text_surf = input_font.render(size_input_text, True, black)
    text_rect = text_surf.get_rect(center=size_input_rect.center)
    screen.blit(text_surf, text_rect)
    if size_input_active and not settings['fullscreen']:
        cursor_x = text_rect.left + input_font.size(size_input_text[:size_input_cursor_pos])[0]
        pygame.draw.line(screen, black, (cursor_x, size_input_rect.top + 10), (cursor_x, size_input_rect.bottom - 10), 2)
def credits_menu():
    screen.fill(background_color)
    draw_button(screen, "Back", start_game_button_rect, black, white)
    draw_button(screen, "Made by: ZeppyTube.", credits_background_rect, black, white)
    draw_button(screen, "Coded by: ChatGPT and (abit of) ZeppyTube.", credits_background2_rect, black, white)
    draw_button(screen, "How to play:", controls_1_rect, black, white)
    draw_button(screen, "Arrow keys to move.", controls_2_rect, black, white)
    draw_button(screen, "Esc to exit game.", controls_3_rect, black, white)
    draw_button(screen, "Screensize changes will", controls_4_rect, black, white)
    draw_button(screen, "Restart the game.", controls_5_rect, black, white)
def load_high_scores():
    try:
        with open('high_scores.json', 'r') as file:
            scores = json.load(file)
            return [score for score in scores if score > 0]
    except (FileNotFoundError, ValueError):
        with open('high_scores.json', 'w') as file:
            json.dump([], file)
        return []
def save_high_scores(scores):
    scores = [score for score in scores if score > 0]
    with open('high_scores.json', 'w') as file:
        json.dump(scores, file)
def high_scores_menu():
    screen.fill(background_color)
    scores = load_high_scores()
    title_text = font.render("High Scores", True, black)
    title_rect = title_text.get_rect(center=(screen_width // 2, 50))
    pygame.draw.rect(screen, white, title_rect.inflate(20, 10))  
    screen.blit(title_text, title_rect.topleft)
    if not scores:
        no_scores_text = font.render("No scores yet!", True, black)
        no_scores_rect = no_scores_text.get_rect(center=(screen_width // 2, 150))
        pygame.draw.rect(screen, white, no_scores_rect.inflate(20, 10)) 
        screen.blit(no_scores_text, no_scores_rect.topleft)
    else:
        for i, score in enumerate(scores):
            score_text = font.render(f"{i+1}. Score: {score}", True, black)
            score_rect = score_text.get_rect(center=(screen_width // 2, 150 + i * 50))
            pygame.draw.rect(screen, white, score_rect.inflate(20, 10)) 
            screen.blit(score_text, score_rect.topleft)
    draw_button(screen, "Back", back_button_rect, black, white)
def toggle_mode():
    global background_color
    settings['dark_mode'] = not settings['dark_mode']
    background_color = dark_gray if settings['dark_mode'] else white
    save_settings()
def save_settings():
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
def start_game():
    settings = load_settings()
    mode = 'dark' if settings['dark_mode'] else 'light'
    cmd = f'python snake_game.py {settings['screen_width']} {settings['screen_height']} {mode}'
    try:
        game_process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        game_process.communicate()
    except Exception as e:
        pass
    game_over_process = subprocess.Popen(['python', 'game_over.py'])
    try:
        game_over_process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        game_over_process.terminate()
current_menu = "main"
running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if current_menu == "main":
                    if start_game_button_rect.collidepoint(mouse_pos):
                        start_game()
                    elif settings_button_rect.collidepoint(mouse_pos):
                        current_menu = "settings"
                    elif credits_button_rect.collidepoint(mouse_pos):
                        current_menu = "credits"
                    elif high_score_button_rect.collidepoint(mouse_pos):
                        current_menu = "high_scores"
                    elif exit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif current_menu == "high_scores":
                    if back_button_rect.collidepoint(mouse_pos):
                        current_menu = "main"
                elif current_menu == "settings":
                    if title_rect.collidepoint(mouse_pos):
                        current_menu = "main"
                    elif toggle_mode_button_rect.collidepoint(mouse_pos):
                        toggle_mode()
                        save_settings()
                    elif ray_tracing_button_rect.collidepoint(mouse_pos):
                        settings['ray_tracing'] = not settings['ray_tracing']
                        save_settings()
                    elif fullscreen_button_rect.collidepoint(mouse_pos):
                        settings['fullscreen'] = not settings['fullscreen']
                        if settings['fullscreen']:
                            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((settings['screen_width'], settings['screen_height']), pygame.RESIZABLE)
                        save_settings()
                    elif window_warp_button_rect.collidepoint(mouse_pos):
                        settings['window_warp'] = not settings['window_warp']
                        save_settings()
                    elif size_input_rect.collidepoint(mouse_pos) and not settings['fullscreen']:
                        size_input_active = True
                        size_input_cursor_pos = len(size_input_text)
                elif current_menu == "credits":
                    if start_game_button_rect.collidepoint(mouse_pos):
                        current_menu = "main"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if current_menu == "settings" and size_input_active and not settings['fullscreen']:
                if event.key is pygame.K_LEFT:
                    size_input_cursor_pos = max(0, size_input_cursor_pos - 1)
                elif event.key is pygame.K_RIGHT:
                    size_input_cursor_pos = min(len(size_input_text), size_input_cursor_pos + 1)
                elif event.key is pygame.K_BACKSPACE and size_input_cursor_pos > 0:
                    size_input_text = size_input_text[:size_input_cursor_pos - 1] + size_input_text[size_input_cursor_pos:]
                    size_input_cursor_pos -= 1
                elif event.key is pygame.K_DELETE and size_input_cursor_pos < len(size_input_text):
                    size_input_text = size_input_text[:size_input_cursor_pos] + size_input_text[size_input_cursor_pos + 1:]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    try:
                        width, height = map(int, size_input_text.split('x'))
                        if width != settings['screen_width'] or height != settings['screen_height']:
                            settings['screen_width'], settings['screen_height'] = width, height
                            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE if not settings['fullscreen'] else pygame.FULLSCREEN)
                            save_settings()
                            sys.exit(42)
                        size_input_active = False
                    except ValueError:
                        pass
                elif event.unicode.isdigit() or event.unicode in 'xX':
                    size_input_text = size_input_text[:size_input_cursor_pos] + event.unicode + size_input_text[size_input_cursor_pos:]
                    size_input_cursor_pos += 1
    if current_menu == "main":
        main_menu()
    elif current_menu == "settings":
        settings_menu()
    elif current_menu == "credits":
        credits_menu()
    elif current_menu == "high_scores":
        high_scores_menu()

    clock.tick(frame_rate)
    pygame.display.update()
pygame.quit()
sys.exit()