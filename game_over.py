import pygame
import time
import os

try:
    pygame.init()
    print("Pygame initialized successfully")
except Exception as e:
    print("Failed to initialize Pygame:", e)

def show_message():
    screen = pygame.display.set_mode((300, 200))
    pygame.display.set_caption("Game Over")
    font = pygame.font.Font(None, 36)
    text = font.render("Thanks for playing!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(150, 100))
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        screen.blit(text, text_rect)
        pygame.display.update()
        time.sleep(1)
        running = False

    pygame.quit()

while True:
    if os.path.exists('game_over_signal.txt'):
        print("Signal file found. Displaying message.")
        show_message()
        os.remove('game_over_signal.txt')
        break
    else:
        print("Signal file not found. Checking again...")
    time.sleep(0.5)
