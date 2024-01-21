import pygame
import sys
import os
import math
import random

class Player:
    def __init__(self, x, y, speed, max_ammo, reload_time, max_health, kills):
        self.x = x
        self.y = y
        self.speed = 7
        self.width = 100
        self.height = 160
        self.ammo = max_ammo
        self.max_ammo = max_ammo
        self.reload_time = 1000
        self.last_shot_time = 0
        self.max_health = max_health
        self.health = max_health
        self.kills = kills

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
        if self.health <= 0:
            self.health = 0
            save_to_leaderboard()
            print("Game Over! You ran out of health.")
            pygame.quit()
            sys.exit()

    def regenerate_health(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 3000:
            self.health += 1100
            if self.health > self.max_health:
                self.health = self.max_health
            self.last_shot_time = current_time

class Bullet:
    def __init__(self, x, y, angle, damage):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 25
        self.width = 35
        self.height = 30
        self.damage_dealt = False
        self.damage = damage
        self.image = pygame.image.load(os.path.join("images", "Bullet.png")).convert()
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, -self.angle)

    def check_collision(self, new_x, new_y):
        for robot in small_robots:
            bullet_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            robot_rect = pygame.Rect(robot.x, robot.y, robot.width, robot.height)
            bullet.speed = 50

            if bullet_rect.colliderect(robot_rect):
                return True
        return False

    def move(self):
        global last_key
        radians = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(radians)
        new_y = self.y - self.speed * math.sin(radians)
        self.x = new_x
        self.y = new_y


        if not self.check_collision(new_x, new_y):
            self.x, self.y = new_x, new_y

    def hit_small_robot(self, robot):
        if not self.damage_dealt:
            bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            robot_rect = pygame.Rect(robot.x, robot.y, robot.width, robot.height)

            if bullet_rect.colliderect(robot_rect):
                self.damage_dealt = True
                return True
        return False

class SmallRobot:
    def __init__(self, index, rotation_speed, hp_small_robot):
        self.index = index
        self.rotation_speed = rotation_speed
        self.width = 300
        self.height = 168
        self.hp_small_robot = hp_small_robot
        self.image_original = pygame.image.load(os.path.join("images", "small_robot.png")).convert()
        self.image_original.set_colorkey((0, 0, 0))
        self.image = self.image_original.copy()
        self.angle = 0
        self.cooldown = 3000
        self.last_attack_time = 0

    def spawn(self):
        self.x = random.randint(0, window_width - self.width)
        self.y = random.randint(0, window_height - self.height)

    def rotate(self, player):
        angle = math.degrees(math.atan2(player.y - self.y, player.x - self.x))
        self.angle = (angle + 360) % 360
        self.image = pygame.transform.rotate(self.image_original, self.angle)

    def move_towards_player(self, player):
        radians = math.radians(self.angle)
        new_x = self.x + 1.5 * math.cos(radians)
        new_y = self.y + 1.5 * math.sin(radians)

        distance_to_player = math.sqrt((player.x - new_x)**2 + (player.y - new_y)**2)
        if distance_to_player > 20:
            self.x = new_x
            self.y = new_y

    def attack_player(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.cooldown:
            player.update_health(1100)
            self.last_attack_time = current_time

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.input_font = pygame.font.Font(None, 48)
        self.input_active = False
        self.input_text = ''
        self.input_rect = pygame.Rect(200, 300, 300, 50)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    player_name = self.input_text.strip()
                    if player_name:
                        return player_name
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def update(self):
        width = max(200, self.input_rect.width + 10)
        self.input_rect.w = width
        self.color = self.color_active if self.active else self.color_inactive

    def draw(self, screen):
        txt_surface = self.font.render("Enter your name:", True, self.color)
        width = max(400, txt_surface.get_width()+10)
        self.input_rect.w = width
        screen.blit(txt_surface, (self.input_rect.x+5, self.input_rect.y-25))
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
        txt_surface = self.input_font.render(self.input_text, True, (255, 255, 255))
        width = max(200, txt_surface.get_width()+10)
        self.input_rect.w = width
        screen.blit(txt_surface, (self.input_rect.x+5, self.input_rect.y+5))

def save_to_leaderboard(player_name, player_kills):
    leaderboard_path = os.path.join("leaderstats", "Leaderboards.txt")
    leaderboards = []

    if os.path.exists(leaderboard_path):
        with open(leaderboard_path, 'r') as file:
            leaderboards = [line.strip() for line in file.readlines()]

    leaderboards.append(f"{player_name}: {player_kills} kills")
    leaderboards.sort(reverse=True, key=lambda x: int(x.split(":")[1].split()[0]))

    with open(leaderboard_path, 'w') as file:
        file.write('\n'.join(leaderboards[:10]))

pygame.init()

# Ustawienia okna
window_width, window_height = 1500, 780
title = "strzelanko"
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(title)

# Ustawienia menu
menu_font = pygame.font.Font(None, 50)
input_font = pygame.font.Font(None, 36)
input_rect = pygame.Rect(450, 300, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('gray15')
color = color_passive
input_active = False
text = ''
clock = pygame.time.Clock()

# Początkowy stan programu
current_state = "menu"  # Dostępne stany: "menu", "game", "game_over"
player_name = ""
leaderboard = []

# Last key char
last_key = 'D'

# Początkowe wymiary gracza
player_width, player_height = 100, 160
health_reload = 3

# Ścieżka do obrazka gracza
image_path = os.path.join("images", "Shelly.png")
player_image = pygame.image.load(image_path).convert()
player_image.set_colorkey((0, 0, 0))
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Początkowa pozycja gracza
player = Player(window_width // 2 - player_width // 2, window_height - player_height + 5, 0.8, 3, 450, 6000, 0)

# Lista przechowująca obiekty pocisków
bullets = []

# Lista przechowująca obiekty small_robot
small_robots = []

# Pętla główna
clock = pygame.time.Clock()
last_robot_spawn_time = 0

# Licznik indeksu dla małych robotów
robot_index_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Obsługa zdarzeń w zależności od aktualnego stanu
        if current_state == "menu":
            background_color = (0, 0, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_state = "game"
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = not input_active
                else:
                    input_active = False
            color = color_active if input_active else color_passive

        elif current_state == "game":
            background_color = (255, 255, 0)
            # Kod obsługujący rozgrywkę
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Kod obsługujący strzały gracza
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

        elif current_state == "game_over":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_state = "menu"
                    player_name = ""
                    text = ""

    # Rysowanie tła
    screen.fill(background_color)

    # Rysowanie w zależności od aktualnego stanu
    if current_state == "menu":
        menu_text = menu_font.render("Press Enter to Start", True, (255, 255, 255))
        screen.blit(menu_text, (500, 200))

        input_surf = input_font.render(text, True, (255, 255, 255))
        width = max(200, input_surf.get_width() + 10)
        input_rect.w = width
        pygame.draw.rect(screen, color, input_rect)
        screen.blit(input_surf, (input_rect.x + 5, input_rect.y + 5))
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)

    elif current_state == "game":
        # Kod obsługujący rozgrywkę
        player.reload_ammo()
        player.regenerate_health()

        keys = pygame.key.get_pressed()
        player.move(keys)

        for bullet in bullets:
            bullet.move()

        bullets = [bullet for bullet in bullets if 0 <= bullet.y <= window_height and 0 <= bullet.x <= window_width]

        for robot in small_robots:
            robot.rotate(player)
            robot.move_towards_player(player)
            distance_to_player = math.sqrt((player.x - robot.x)**2 + (player.y - robot.y)**2)

            if distance_to_player < 50:
                robot.attack_player(player)

        bullets_to_remove = []
        for bullet in bullets:
            for i, robot in enumerate(small_robots):
                if bullet.hit_small_robot(robot):
                    distance = math.sqrt((robot.x - bullet.x)**2 + (robot.y - bullet.y)**2)
                    print(f"Bullet hit small robot! Distance: {distance}, Robot HP: {robot.hp_small_robot}")
                    damage = max(1000, min(2300, 2300 - distance * 5))
                    print(f"Inflicted damage: {damage}")
                    robot.hp_small_robot -= damage
                    print(f"Robot HP after damage: {robot.hp_small_robot}")
                    bullets_to_remove.append(bullet)
                    if robot.hp_small_robot <= 0:
                        small_robots.pop(i)
                        player.kills += 1
                        print("Small robot defeated!")
                    break

        bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]

        current_time = pygame.time.get_ticks()
        if current_time - last_robot_spawn_time > random.randint(1000, 2000):
            robot_index_counter += 1
            new_robot = SmallRobot(robot_index_counter, 1, 3300)
            new_robot.spawn()
            small_robots.append(new_robot)
            last_robot_spawn_time = current_time

        # Rysowanie obrazka gracza
        screen.blit(player_image, (player.x, player.y))

        # Rysowanie pocisków
        for bullet in bullets:
            screen.blit(bullet.image, (bullet.x, bullet.y))

        # Rysowanie small_robot
        for robot in small_robots:
            screen.blit(robot.image, (robot.x, robot.y))

        # Rysowanie paska zdrowia gracza
        health_bar_width = 100
        health_bar_height = 30
        pygame.draw.rect(screen, (255, 0, 0), (player.x, player.y - health_bar_height - 5, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (player.x, player.y - health_bar_height - 5, health_bar_width * (player.health / player.max_health), health_bar_height))

        # Rysowanie ilości amunicji i zabitych small_robotów
        font1 = pygame.font.Font(None, 36)
        font2 = pygame.font.Font(None, 27)
        ammo_text = font1.render(f"Ammo: {player.ammo}", True, (0, 0, 0))
        kills_text = font1.render(f"Kills: {player.kills}", True, (0, 0, 0))
        health_text = font2.render(f"{player.health}/{player.max_health}", True, (0, 0, 0))
        screen.blit(health_text, (player.x + 5, player.y - health_bar_height))
        screen.blit(ammo_text, (10, window_height - 80))
        screen.blit(kills_text, (10, window_height - 40))

    elif current_state == "game_over":
        save_to_leaderboard(pla)

        game_over_text = menu_font.render("Game Over! Press Enter to return to Menu", True, (255, 255, 255))
        screen.blit(game_over_text, (350, 200))

    pygame.display.flip()
    clock.tick(60)