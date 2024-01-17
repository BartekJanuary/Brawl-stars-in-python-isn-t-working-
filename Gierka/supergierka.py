import pygame
import sys
import os
import math

class Player:
    def __init__(self, x, y, speed, max_ammo, reload_time):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 100
        self.height = 160
        self.ammo = max_ammo
        self.max_ammo = max_ammo
        self.reload_time = 1000
        self.last_shot_time = 0

    def move(self, keys):
        global last_key
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            last_key = 'A'
        if keys[pygame.K_d] and self.x < window_width - self.width:
            self.x += self.speed
            last_key = 'D'
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
            last_key = 'W'
        if keys[pygame.K_s] and self.y < window_height - self.height:
            self.y += self.speed
            last_key = 'S'

    def reload_ammo(self):
        if self.ammo < self.max_ammo:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.reload_time:
                self.ammo += 1
                self.last_shot_time = current_time

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 1.5
        self.width = 20
        self.height = 20
        self.image = pygame.image.load(os.path.join("images", "Bullet.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.angle)  # Obróć obrazek w kierunku strzału

    def move(self):
        global last_key
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y -= self.speed * math.sin(radians)

# Inicjalizacja Pygame
pygame.init()
# last_key char
last_key = 'D'
# Ustawienia okna
window_width, window_height = 1500, 780
title = "strzelanko"

# Inicjalizacja okna
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)

# Kolor tła
background_color = (0, 255, 0)

# Początkowe wymiary gracza
player_width, player_height = 100, 160

# Ścieżka do obrazka gracza
image_path = os.path.join("images", "Shelly.png")  # Zmień na poprawną ścieżkę do pliku obrazka

# Wczytaj obrazek gracza
player_image = pygame.image.load(image_path).convert()
player_image.set_colorkey((0, 0, 0))
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Początkowa pozycja obrazka
player = Player(window_width // 2 - player_width // 2, window_height - player_height + 5, 0.8, 3, 450)  # max_ammo=3, reload_time=450

# Lista przechowująca obiekty pocisków
bullets = []

# Pętla główna
while True:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Dodaj trzy nowe kule przy każdym strzelaniu
                if last_key == 'W':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 90))  # W
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 100))  # W_UP_LEFT
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 80))  # W_UP_RIGHT
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'S':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 270))  # S
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 260))  # S_DOWN_LEFT
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 280))  # S_DOWN_RIGHT
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'A':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 180))  # A
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 190))  # A_LEFT_UP
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 170))  # A_LEFT_DOWN
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'D':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 0))  # D
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 10))  # D_RIGHT_UP
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 350))  # D_RIGHT_DOWN
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()

            # Przeładowanie amunicji po naciśnięciu R

    player.reload_ammo()

    # Pobierz stan klawiszy
    keys = pygame.key.get_pressed()

    # Aktualizacja pozycji gracza
    player.move(keys)

    # Aktualizacja pozycji pocisków
    for bullet in bullets:
        bullet.move()

    # Usuwanie pocisków, które opuściły ekran
    bullets = [bullet for bullet in bullets if 0 <= bullet.y <= window_height and 0 <= bullet.x <= window_width]

    # Rysowanie tła
    screen.fill(background_color)

    # Rysowanie obrazka gracza
    screen.blit(player_image, (player.x, player.y))

    # Rysowanie pocisków
    for bullet in bullets:
        screen.blit(bullet.image, (bullet.x, bullet.y))

    # Rysowanie ilości amunicji
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, window_height - 40))

    # Aktualizacja ekranu
    pygame.display.flip()