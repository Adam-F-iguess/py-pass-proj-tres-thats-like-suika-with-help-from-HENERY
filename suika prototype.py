import pygame
import random
import math
import csv
import os

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suika Game Prototype")

# Jar dimensions
JAR_LEFT = 100
JAR_TOP = 150
JAR_WIDTH = 400
JAR_HEIGHT = 600
JAR_RIGHT = JAR_LEFT + JAR_WIDTH
JAR_BOTTOM = JAR_TOP + JAR_HEIGHT
STATE_MENU = 0
STATE_PLAYING = 1
STATE_LEADERBOARD = 2
STATE_GAME_OVER = 3
LEADERBOARD_FILE = "leaderboard.csv"

# Fruit definitions: (radius, color, weight)
FRUITS = [
    (10, (220, 0, 0), 1),        # Cherry (red, tiny)
    (11, (255, 80, 80), 2),      # Strawberry (lighter red, tiny)
    (22, (160, 60, 200), 3),     # Grape (purple, small)
    (23, (255, 220, 60), 4),     # Dekopon (yellow, small)
    (34, (255, 140, 0), 6),      # Persimmon (orange, medium)
    (44, (200, 0, 0), 8),        # Apple (red, medium)
    (60, (255, 170, 200), 11),   # Peach (pink, large)
    (70, (255, 230, 80), 14),    # Pineapple (yellow, large)
    (80, (60, 200, 60), 18),     # Melon (green, very large)
    (100, (20, 80, 40), 25),      # Watermelon (dark green, M A S S I V E)
]

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

class Fruit:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.radius, self.color, self.weight = FRUITS[kind]
        self.hitbox_radius = self.radius + 1  # Reduced hitbox size to 1 pixel
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.merged = False
        self.landed = False

    def update(self, fruits):
        self.vy += 0.7  # Increased gravity for quicker gameplay
        self.x += self.vx
        self.y += self.vy

        # Floor collision (jar bottom)
        if self.y + self.radius > JAR_BOTTOM:
            self.y = JAR_BOTTOM - self.radius
            self.vy = 0
            self.landed = True
            self.vx *= 0.98  # Slightly less damping for quicker movements
        else:
            # Check if supported by another fruit
            if is_supported(self, fruits):
                self.vy = 0
                self.landed = True
                self.vx *= 0.98  # Only slip if not blocked horizontally
            else:
                self.landed = False
                self.vx = 0  # No sliding in the air

        # Wall collision (jar sides)
        if self.x - self.radius < JAR_LEFT:
            self.x = JAR_LEFT + self.radius
            self.vx = -self.vx * 0.6 if self.y + self.radius >= JAR_BOTTOM else 0
        if self.x + self.radius > JAR_RIGHT:
            self.x = JAR_RIGHT - self.radius
            self.vx = -self.vx * 0.6 if self.y + self.radius >= JAR_BOTTOM else 0

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)
 
       
def resolve_collision(f1, f2):
    dx = f2.x - f1.x
    dy = f2.y - f1.y
    dist = math.hypot(dx, dy)
    overlap = f1.hitbox_radius + f2.hitbox_radius - dist
    if overlap > 0 and dist != 0:
        nx = dx / dist
        ny = dy / dist

        # Weight-based push: heavier fruits move less
        total_weight = f1.weight + f2.weight
        move1 = (f2.weight / total_weight) * overlap * 0.4  # Reduced adjustment magnitude for smoother collisions
        move2 = (f1.weight / total_weight) * overlap * 0.4

        # Adjust positions to prevent clipping
        f1.x -= nx * move1
        f1.y -= ny * move1
        f2.x += nx * move2
        f2.y += ny * move2

        # Dampen velocity changes
        f1.vx *= 0.92  # Slightly less damping for quicker gameplay
        f1.vy *= 0.92
        f2.vx *= 0.92
        f2.vy *= 0.92

        # Clamp positions inside the jar
        for f in (f1, f2):
            if f.x - f.radius < JAR_LEFT:
                f.x = JAR_LEFT + f.radius
                f.vx = -f.vx * 0.5
            if f.x + f.radius > JAR_RIGHT:
                f.x = JAR_RIGHT - f.radius
                f.vx = -f.vx * 0.5
            if f.y + f.radius > JAR_BOTTOM:
                f.y = JAR_BOTTOM - f.radius
                f.vy = 0
                f.landed = True

def merge(f1, f2):
    # If not the last fruit, merge up as normal
    if f1.kind < len(FRUITS) - 1:
        return Fruit(f1.kind + 1, (f1.x + f2.x) / 2, (f1.y + f2.y) / 2)
    # If both are watermelons, merging returns nothing (they disappear)
    return None

def collide(f1, f2):
    dist = math.hypot(f1.x - f2.x, f1.y - f2.y)
    return dist < f1.hitbox_radius + f2.hitbox_radius

def is_supported(fruit, fruits):
    if abs(fruit.y + fruit.radius - JAR_BOTTOM) < 1:
        return True
    for other in fruits:
        if other is fruit:
            continue
        dx = abs(fruit.x - other.x)
        dy = (fruit.y + fruit.hitbox_radius) - (other.y - other.hitbox_radius)
        if dx < fruit.hitbox_radius + other.hitbox_radius - 2 and 0 <= dy < 2:
            return True
    return False

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, newline='') as f:
        reader = csv.reader(f)
        return [(row[0], int(row[1])) for row in reader]

def save_score(name, score):
    scores = load_leaderboard()
    scores.append((name, score))
    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    # Save back
    with open(LEADERBOARD_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        for entry in scores:
            writer.writerow(entry)
    return scores

fruits = []
# When spawning a new fruit, drop it above the jar
next_kind = random.randint(0, 4)
current_kind = random.randint(0, 4)
current_fruit = Fruit(current_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
game_over = False
score = 0
drop_cooldown = 2000  # milliseconds (1 seconds)
last_drop_time = pygame.time.get_ticks() - drop_cooldown  # allow immediate first drop

state = STATE_MENU
running = True

while running:
    if state == STATE_MENU:
        # --- MENU SCREEN ---
        screen.fill((30, 30, 30))
        title = big_font.render("Suika Game", True, (255, 255, 0))
        play_btn = font.render("1. Play", True, (255, 255, 255))
        lb_btn = font.render("2. Leaderboard", True, (255, 255, 255))
        quit_btn = font.render("3. Quit", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(play_btn, (WIDTH // 2 - play_btn.get_width() // 2, 320))
        screen.blit(lb_btn, (WIDTH // 2 - lb_btn.get_width() // 2, 370))
        screen.blit(quit_btn, (WIDTH // 2 - quit_btn.get_width() // 2, 420))
        pygame.display.flip()

        menu_waiting = True
        while menu_waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu_waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        state = STATE_PLAYING
                        menu_waiting = False
                    elif event.key == pygame.K_2:
                        state = STATE_LEADERBOARD
                        menu_waiting = False
                    elif event.key == pygame.K_3 or event.key == pygame.K_ESCAPE:
                        running = False
                        menu_waiting = False

    elif state == STATE_LEADERBOARD:
        # --- LEADERBOARD SCREEN ---
        scores = load_leaderboard()
        top10 = scores[:10]
        screen.fill((30, 30, 30))
        lb_title = big_font.render("Leaderboard (Top 10)", True, (255, 255, 255))
        screen.blit(lb_title, (WIDTH // 2 - lb_title.get_width() // 2, 100))
        for i, entry in enumerate(top10):
            entry_msg = font.render(f"{i+1}. {entry[0]} - {entry[1]}", True, (255, 255, 255))
            screen.blit(entry_msg, (WIDTH // 2 - entry_msg.get_width() // 2, 180 + i * 40))
        back_msg = font.render("Press any key to return to menu", True, (200, 200, 200))
        screen.blit(back_msg, (WIDTH // 2 - back_msg.get_width() // 2, 650))
        pygame.display.flip()
        lb_waiting = True
        while lb_waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    lb_waiting = False
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    lb_waiting = False

    elif state == STATE_PLAYING:
        # --- GAME SETUP ---
        fruits = []
        next_kind = random.randint(0, 4)
        current_kind = random.randint(0, 4)
        current_fruit = Fruit(current_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
        game_over = False
        score = 0
        drop_cooldown = 2000
        last_drop_time = pygame.time.get_ticks() - drop_cooldown

        # --- GAME LOOP ---
        while not game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_fruit.x -= 20
                        if current_fruit.x - current_fruit.radius < JAR_LEFT:
                            current_fruit.x = JAR_LEFT + current_fruit.radius
                    if event.key == pygame.K_RIGHT:
                        current_fruit.x += 20
                        if current_fruit.x + current_fruit.radius > JAR_RIGHT:
                            current_fruit.x = JAR_RIGHT - current_fruit.radius
                    if event.key == pygame.K_SPACE:
                        now = pygame.time.get_ticks()
                        if now - last_drop_time >= drop_cooldown:
                            fruits.append(current_fruit)
                            vx = random.uniform(-2, 2)
                            current_fruit = Fruit(next_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
                            current_fruit.vx = vx
                            next_kind = random.randint(0, 4)  # Only allow cherry to persimmon
                            last_drop_time = now

            # --- MERGE LOGIC ---
            merged_indices = set()
            new_fruits = []
            for i in range(len(fruits)):
                for j in range(i + 1, len(fruits)):
                    if i in merged_indices or j in merged_indices:
                        continue
                    if fruits[i].kind == fruits[j].kind and collide(fruits[i], fruits[j]):
                        # Merge fruits regardless of velocity or landed status
                        new_fruit = merge(fruits[i], fruits[j])
                        if new_fruit:
                            new_fruits.append(new_fruit)
                            merged_indices.add(i)
                            merged_indices.add(j)
                            score += 10 * (new_fruit.kind + 1)

            # Remove merged fruits and add new ones
            for idx in sorted(merged_indices, reverse=True):
                del fruits[idx]
            fruits.extend(new_fruits)

            # --- PRIORITY LOOP: walls -> collisions ---
            max_priority_passes = 5
            priority_pass = 0
            while priority_pass < max_priority_passes:
                # 1. Resolve wall collisions
                wall_bounced = False
                for fruit in fruits:
                    if fruit.x - fruit.radius < JAR_LEFT:
                        fruit.x = JAR_LEFT + fruit.radius
                        fruit.vx = -fruit.vx * 0.7  # Reduced bounce damping for quicker gameplay
                        wall_bounced = True
                    if fruit.x + fruit.radius > JAR_RIGHT:
                        fruit.x = JAR_RIGHT - fruit.radius
                        fruit.vx = -fruit.vx * 0.7
                        wall_bounced = True
                if wall_bounced:
                    priority_pass += 1
                    continue  # After wall bounce, check collisions again

                # 2. Resolve fruit-to-fruit collisions
                collision_happened = False
                fruits_copy = fruits[:]
                for i in range(len(fruits_copy)):
                    for j in range(i + 1, len(fruits_copy)):
                        if i >= len(fruits) or j >= len(fruits):
                            break
                        before = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                        resolve_collision(fruits[i], fruits[j])
                        after = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                        if before != after:
                            collision_happened = True
                if collision_happened:
                    priority_pass += 1
                    continue  # After collision, check walls again

                break  # If nothing happened, exit the loop

            # Update fruits
            for fruit in fruits:
                fruit.update(fruits)

            # --- GAME OVER CHECK ---
            for fruit in fruits:
                if fruit.landed and fruit.y - fruit.radius < JAR_TOP + 10:
                    game_over = True

            # Draw everything
            screen.fill((30, 30, 30))

            # Draw jar (rectangle and top)
            pygame.draw.rect(screen, (60, 60, 60), (JAR_LEFT, JAR_TOP, JAR_WIDTH, JAR_HEIGHT), 0)
            pygame.draw.rect(screen, (200, 200, 200), (JAR_LEFT, JAR_TOP, JAR_WIDTH, JAR_HEIGHT), 5)
            pygame.draw.rect(screen, (255, 100, 100), (JAR_LEFT, JAR_TOP, JAR_WIDTH, 10))  # visual top

            # Draw fruits
            for fruit in fruits:
                fruit.draw(screen)
            current_fruit.draw(screen)

            # Draw cooldown indicator (to the right of jar, near top)
            now = pygame.time.get_ticks()
            cooldown_ratio = min(1, (now - last_drop_time) / drop_cooldown)
            indicator_radius = 30
            indicator_center = (JAR_RIGHT + 60, JAR_TOP + 40)
            pygame.draw.circle(screen, (100, 100, 100), indicator_center, indicator_radius, 3)
            if cooldown_ratio < 1:
                # Draw cooldown fill (arc)
                end_angle = -math.pi / 2 + 2 * math.pi * cooldown_ratio
                pygame.draw.arc(
                    screen,
                    (0, 200, 255),
                    (indicator_center[0] - indicator_radius, indicator_center[1] - indicator_radius, indicator_radius * 2, indicator_radius * 2),
                    -math.pi / 2,
                    end_angle,
                    8
                )
            else:
                # Ready: draw full circle
                pygame.draw.circle(screen, (0, 255, 0), indicator_center, indicator_radius - 6, 0)

            # Draw "Next" fruit preview under cooldown
            next_label = font.render("Next", True, (255, 255, 255))
            screen.blit(next_label, (indicator_center[0] - next_label.get_width() // 2, indicator_center[1] + indicator_radius + 50))
            next_fruit_y = indicator_center[1] + indicator_radius + 90  # Increased offset
            pygame.draw.circle(
                screen,
                FRUITS[next_kind][1],
                (indicator_center[0], next_fruit_y),
                FRUITS[next_kind][0]
            )

            score_text = font.render(f"Score: {score}", True, (255, 255, 0))
            screen.blit(score_text, (20, 20))

            pygame.display.flip()
            clock.tick(60)

        if running:
            state = STATE_GAME_OVER

    elif state == STATE_GAME_OVER:
        # --- GAME OVER SCREEN ---
        # Prompt for player name (simple input box)
        import tkinter as tk
        from tkinter import simpledialog
        root = tk.Tk()
        root.withdraw()
        player_name = simpledialog.askstring("Name", "Enter your name for the leaderboard:")
        if not player_name:
            player_name = "Anonymous"
        root.destroy()
        scores = save_score(player_name, score)
        rank = [i+1 for i, entry in enumerate(scores) if entry[0] == player_name and entry[1] == score][0]
        top10 = scores[:10]
        screen.fill((30, 30, 30))
        msg = big_font.render("Game Over!", True, (255, 80, 80))
        score_msg = font.render(f"Final Score: {score}", True, (255, 255, 0))
        rank_msg = font.render(f"Your Rank: {rank}", True, (0, 255, 255))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 60))
        screen.blit(score_msg, (WIDTH // 2 - score_msg.get_width() // 2, 120))
        screen.blit(rank_msg, (WIDTH // 2 - rank_msg.get_width() // 2, 160))
        lb_title = font.render("Leaderboard (Top 10)", True, (255, 255, 255))
        screen.blit(lb_title, (WIDTH // 2 - lb_title.get_width() // 2, 220))
        for i, entry in enumerate(top10):
            entry_msg = font.render(f"{i+1}. {entry[0]} - {entry[1]}", True, (255, 255, 255))
            screen.blit(entry_msg, (WIDTH // 2 - entry_msg.get_width() // 2, 260 + i * 30))
        back_msg = font.render("Press any key to return to menu", True, (200, 200, 200))
        screen.blit(back_msg, (WIDTH // 2 - back_msg.get_width() // 2, 650))
        pygame.display.flip()
        go_waiting = True
        while go_waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    go_waiting = False
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    go_waiting = False

pygame.quit()