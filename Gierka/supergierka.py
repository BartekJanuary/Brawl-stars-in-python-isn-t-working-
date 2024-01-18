import pygame
import sys
import os
import math

class Player:
    def __init__(self, x, y, speed, max_ammo, reload_time, max_health):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 100
        self.height = 160
        self.ammo = max_ammo
        self.max_ammo = max_ammo
        self.reload_time = 1000
        self.last_shot_time = 0
        self.max_health = max_health
        self.health = max_health

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

    def update_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

class Bullet:
    def __init__(self, x, y, angle, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 2
        self.width = 30
        self.height = 30
        self.damage = damage
        self.image = pygame.image.load(os.path.join("images", "Bullet.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.angle)  # Obróć obrazek w kierunku strzału

    def move(self):
        global last_key
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y -= self.speed * math.sin(radians)

    def hit_player(self, player):
        return player.x < self.x < player.x + player.width and player.y < self.y < player.y + player.height

class SmallRobot:
    def __init__(self, x, y, rotation_speed):
        self.x = x
        self.y = y
        self.rotation_speed = rotation_speed
        self.width = 50
        self.height = 50
        self.image_original = pygame.image.load(os.path.join("images", "small_robot.png")).convert()
        self.image_original.set_colorkey((0, 0, 0))
        self.image = self.image_original.copy()
        self.angle = 0

    def rotate(self):
        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.image_original, self.angle)

    def hit_bullet(self, bullet):
        return self.x < bullet.x < self.x + self.width and self.y < bullet.y < self.y + self.height

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
player = Player(window_width // 2 - player_width // 2, window_height - player_height + 5, 0.8, 3, 450, 6000)  # max_ammo=3, reload_time=450, max_health=6000

# Lista przechowująca obiekty pocisków
bullets = []

# Lista przechowująca obiekty small_robot
small_robots = [SmallRobot(300, 300, 1)]

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
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 90, 50))  # W
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 100, 50))  # W_UP_LEFT
                        bullets.append(Bullet(player.x + player_width // 2, player.y, 80, 50))  # W_UP_RIGHT
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'S':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 270, 50))  # S
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 260, 50))  # S_DOWN_LEFT
                        bullets.append(Bullet(player.x + player_width // 2, player.y + player_height, 280, 50))  # S_DOWN_RIGHT
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'A':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 180, 50))  # A
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 190, 50))  # A_LEFT_UP
                        bullets.append(Bullet(player.x, player.y + player_height // 2, 170, 50))  # A_LEFT_DOWN
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()
                elif last_key == 'D':
                    if player.ammo > 0:
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 0, 50))  # D
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 10, 50))  # D_RIGHT_UP
                        bullets.append(Bullet(player.x + player_width, player.y + player_height // 2, 350, 50))  # D_RIGHT_DOWN
                        player.ammo -= 1
                        player.last_shot_time = pygame.time.get_ticks()

    player.reload_ammo()

    # Pobierz stan klawiszy
    keys = pygame.key.get_pressed()

    # Aktualizacja pozycji gracza
    player.move(keys)

    # Aktualizacja pozycji pocisków
    for bullet in bullets:
        bullet.move()

        # Sprawdzenie, czy pocisk trafił w gracza
        if bullet.hit_player(player):
            player.update_health(bullet.damage)
            bullets.remove(bullet)

    # Aktualizacja pozycji small_robot
    for robot in small_robots:
        robot.rotate()

        # Sprawdzenie, czy jakiś pocisk trafił w small_robot
        for bullet in bullets:
            if robot.hit_bullet(bullet):
                # Zmiana koloru na czerwony przez 0.2 sekundy
                robot.image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
                pygame.time.delay(200)
                robot.image = pygame.transform.scale(robot.image, (robot.width, robot.height))

    # Usuwanie pocisków, które opuściły ekran
    bullets = [bullet for bullet in bullets if 0 <= bullet.y <= window_height and 0 <= bullet.x <= window_width]

    # Rysowanie tła
    screen.fill(background_color)

    # Rysowanie obrazka gracza
    screen.blit(player_image, (player.x, player.y))

    # Rysowanie pocisków
    for bullet in bullets:
        screen.blit(bullet.image, (bullet.x, bullet.y))

    # Rysowanie small_robot
    for robot in small_robots:
        screen.blit(robot.image, (robot.x, robot.y))

    # Rysowanie paska zdrowia
    health_bar_width = 100
    health_bar_height = 10
    pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y - health_bar_height - 5, health_bar_width, health_bar_height))  # Czerwony prostokąt (maksymalne zdrowie)
    pygame.draw.rect(screen, (0, 255, 0), (player.x, player.y - health_bar_height - 5, health_bar_width * (player.health / player.max_health), health_bar_height))  # Zielony prostokąt (aktualne zdrowie)

    # Rysowanie ilości amunicji
    font = pygame.font.Font(None, 36)
    ammo_text = font.render(f"Ammo: {player.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, window_height - 40))

    # Aktualizacja ekranu
    pygame.display.flip()
