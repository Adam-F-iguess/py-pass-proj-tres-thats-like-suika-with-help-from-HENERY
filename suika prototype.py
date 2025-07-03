import pygame
import random
import math
import csv
import os


# Initialize Pygame
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Suika Game Prototype")


# Music settings
music_volume = 0.5
music_menu_open = False
music_button_rect = pygame.Rect(WIDTH - 60, 10, 50, 30)  # Top right corner
volume_slider_rect = pygame.Rect(WIDTH - 250, 60, 200, 20)  # Volume slider area
volume_handle_rect = pygame.Rect(WIDTH - 250 + int(200 * music_volume), 55, 10, 30)  # Volume handle
dragging_volume = False

# Update the load_music function to use the volume variable
def load_music():
    global music_volume
    try:
        music_path = os.path.join("music", "suika game music but bad yay.wav")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        print("Music loaded and playing")
    except pygame.error:
        print("Could not load music file. Make sure 'music/suika game music but bad yay.wav' exists")

def draw_music_button(screen):
    # Draw music button
    pygame.draw.rect(screen, (100, 100, 100), music_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), music_button_rect, 2)
    
    # Draw music note symbol - use a simple text character that displays properly
    note_font = pygame.font.SysFont(None, 20)
    note_text = note_font.render("Music", True, (255, 255, 255))
    screen.blit(note_text, (music_button_rect.x + 7, music_button_rect.y + 8))

def draw_music_menu(screen):
    if music_menu_open:
        # Draw menu background - made taller to prevent overlap
        menu_rect = pygame.Rect(WIDTH - 270, 50, 260, 120)  # Increased height from 100 to 120
        pygame.draw.rect(screen, (50, 50, 50), menu_rect)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2)
        
        # Draw volume label
        volume_font = pygame.font.SysFont(None, 24)
        volume_text = volume_font.render("Volume", True, (255, 255, 255))
        screen.blit(volume_text, (WIDTH - 260, 60))
        
        # Draw volume slider track - moved down slightly
        slider_rect = pygame.Rect(WIDTH - 250, 85, 200, 20)  # Moved from y=80 to y=85
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        pygame.draw.rect(screen, (255, 255, 255), slider_rect, 2)
        
        # Draw volume slider handle - update position
        handle_rect = pygame.Rect(WIDTH - 250 + int(200 * music_volume), 80, 10, 30)  # Moved from y=75 to y=80
        pygame.draw.rect(screen, (0, 200, 255), handle_rect)
        
        # Draw volume percentage - moved down
        volume_percent = int(music_volume * 100)
        percent_text = volume_font.render(f"{volume_percent}%", True, (255, 255, 255))
        screen.blit(percent_text, (WIDTH - 260, 115))  # Moved from y=90 to y=115
        
        # Draw mute button - moved down and adjusted size
        mute_rect = pygame.Rect(WIDTH - 100, 115, 80, 25)  # Moved from y=90 to y=115
        pygame.draw.rect(screen, (150, 50, 50), mute_rect)
        pygame.draw.rect(screen, (255, 255, 255), mute_rect, 2)
        mute_text = pygame.font.SysFont(None, 20).render("Mute", True, (255, 255, 255))
        screen.blit(mute_text, (mute_rect.x + 20, mute_rect.y + 5))

def handle_music_menu_events(event):
    global music_menu_open, dragging_volume, music_volume, volume_handle_rect
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if music_button_rect.collidepoint(event.pos):
            music_menu_open = not music_menu_open
        elif music_menu_open:
            # Updated slider rect for collision detection
            slider_rect = pygame.Rect(WIDTH - 250, 85, 200, 20)
            # Check if clicking on volume slider
            if slider_rect.collidepoint(event.pos):
                dragging_volume = True
                # Calculate new volume based on click position
                relative_x = event.pos[0] - slider_rect.x
                new_volume = relative_x / slider_rect.width
                set_music_volume(new_volume)
            # Check if clicking on mute button - updated position
            elif pygame.Rect(WIDTH - 100, 115, 80, 25).collidepoint(event.pos):
                if music_volume > 0:
                    set_music_volume(0)
                else:
                    set_music_volume(0.5)
            # Close menu if clicking outside - updated menu rect
            elif not pygame.Rect(WIDTH - 270, 50, 260, 120).collidepoint(event.pos):
                music_menu_open = False
    
    elif event.type == pygame.MOUSEBUTTONUP:
        dragging_volume = False
    
    elif event.type == pygame.MOUSEMOTION and dragging_volume:
        # Update volume while dragging - updated slider rect
        slider_rect = pygame.Rect(WIDTH - 250, 85, 200, 20)
        if slider_rect.collidepoint(event.pos):
            relative_x = event.pos[0] - slider_rect.x
            new_volume = relative_x / slider_rect.width
            set_music_volume(new_volume)

def set_music_volume(volume):
    global music_volume, volume_handle_rect
    music_volume = max(0.0, min(1.0, volume))
    pygame.mixer.music.set_volume(music_volume)
    # Update handle position with new slider position
    volume_handle_rect = pygame.Rect(WIDTH - 250 + int(200 * music_volume), 80, 10, 30)
    
# Load music at startup
load_music()

# Load sprites
def load_sprite(filename):
    try:
        sprite_path = os.path.join("sprites", filename)
        return pygame.image.load(sprite_path).convert_alpha()
    except pygame.error:
        print(f"Could not load {filename}")
        return None

def center_sprite(sprite):
    """Centers the sprite by cropping to its non-transparent bounding box"""
    if not sprite:
        return None
    
    # Get the bounding rect of non-transparent pixels
    mask = pygame.mask.from_surface(sprite)
    bounding_rect = mask.get_bounding_rects()
    
    if not bounding_rect:
        return sprite  # Return original if no non-transparent pixels found
    
    # Get the tightest bounding box
    min_x = min(rect.left for rect in bounding_rect)
    min_y = min(rect.top for rect in bounding_rect)
    max_x = max(rect.right for rect in bounding_rect)
    max_y = max(rect.bottom for rect in bounding_rect)
    
    # Crop to the bounding box
    cropped_width = max_x - min_x
    cropped_height = max_y - min_y
    
    # Create a new surface with the cropped size
    cropped_sprite = pygame.Surface((cropped_width, cropped_height), pygame.SRCALPHA)
    cropped_sprite.blit(sprite, (0, 0), (min_x, min_y, cropped_width, cropped_height))
    
    return cropped_sprite

# Load cherry sprite
cherry_sprite = load_sprite("cherry.png")
if cherry_sprite:
    cherry_sprite = center_sprite(cherry_sprite)  # Only center, don't scale

strawberry_sprite = load_sprite("strawberry.png")
if strawberry_sprite:
    strawberry_sprite = center_sprite(strawberry_sprite)  # Only center, don't scale

grape_sprite = load_sprite("grape.png")
if grape_sprite:  # Fix: was checking cherry_sprite instead of grape_sprite
    grape_sprite = center_sprite(grape_sprite)  # Only center, don't scale

dekopon_sprite = load_sprite("dekopon.png")
if dekopon_sprite:
    dekopon_sprite = center_sprite(dekopon_sprite)  # Only center, don't scale

persimmon_sprite = load_sprite("persimmon.png")
if persimmon_sprite:
    persimmon_sprite = center_sprite(persimmon_sprite)  # Only center, don't scale

apple_sprite = load_sprite("apple.png")
if apple_sprite:
    apple_sprite = center_sprite(apple_sprite)  # Only center, don't scale

peach_sprite = load_sprite("peach.png")
if peach_sprite:
    peach_sprite = center_sprite(peach_sprite)  # Only center, don't scale

pineapple_sprite = load_sprite("pineapple.png")
if pineapple_sprite:
    pineapple_sprite = center_sprite(pineapple_sprite)  # Only center, don't scale

melon_sprite = load_sprite("melon.png")
if melon_sprite:
    melon_sprite = center_sprite(melon_sprite)  # Only center, don't scale

watermelon_sprite = load_sprite("watermelon.png")
if watermelon_sprite:
    watermelon_sprite = center_sprite(watermelon_sprite)  # Only center, don't scale



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
STATE_HOWTO = 4
STATE_CREDITS = 5
LEADERBOARD_FILE = "leaderboard.csv"

# Fruit definitions: (radius, color, weight)
FRUITS = [
    (10, (220, 0, 0), 1, cherry_sprite),        # Cherry (red, tiny, with sprite)
    (11, (255, 80, 80), 2, strawberry_sprite),      # Strawberry (lighter red, tiny)
    (22, (160, 60, 200), 3, grape_sprite),     # Grape (purple, small)
    (23, (255, 220, 60), 4, dekopon_sprite),     # Dekopon (yellow, small)
    (34, (255, 140, 0), 6, persimmon_sprite),      # Persimmon (orange, medium)
    (44, (200, 0, 0), 8, apple_sprite),        # Apple (red, medium)
    (66, (255, 170, 200), 11, peach_sprite),   # Peach (pink, large)
    (75, (255, 230, 80), 14, pineapple_sprite),    # Pineapple (yellow, large)
    (90, (60, 200, 60), 18, melon_sprite),     # Melon (green, very large)
    (120, (20, 80, 40), 25, watermelon_sprite),      # Watermelon (dark green, M A S S I V E)
]


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 48)

class Fruit:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.radius, self.color, self.weight, self.sprite = FRUITS[kind]
        
        # Scale sprite to match fruit radius if it exists
        if self.sprite:
            sprite_size = self.radius * 2  # Diameter = radius * 2
            self.sprite = pygame.transform.scale(self.sprite, (sprite_size, sprite_size))
            self.original_sprite = self.sprite.copy()  # Keep original for rotation
        else:
            self.original_sprite = None
        
        # Hitbox is 1px larger than visual radius for better collision detection
        self.hitbox_radius = self.radius + 1  # 1px larger than visual
        
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.merged = False
        self.landed = False
        self.rotation = 0  # Add rotation angle
        self.rolling = False  # Track if fruit is in rolling state

    def update(self, fruits):
        self.vy += 0.7  # Increased gravity for quicker gameplay
        self.x += self.vx
        self.y += self.vy

        # Check if fruit is colliding with others to enter rolling state
        was_rolling = self.rolling
        self.rolling = False
        
        for other in fruits:
            if other is not self and collide(self, other):
                self.rolling = True
                break
        
        # Only rotate when rolling (colliding with other fruits)
        if self.rolling:
            # Much slower visual rotation based on horizontal velocity when rolling
            if abs(self.vx) > 0.05:  # Higher threshold for rotation
                self.rotation += self.vx * 0.3  # Much slower rotation speed (was 0.8)
                self.rotation = self.rotation % 360  # Keep angle within 0-360 degrees
            
            # Tiny collision-based rotation for natural movement
            collision_rotation = random.uniform(-0.05, 0.05)  # Much smaller (was -0.1, 0.1)
            self.rotation += collision_rotation
            self.rotation = self.rotation % 360
        
        # If fruit was rolling but isn't anymore, gradually slow rotation
        elif was_rolling and not self.rolling:
            # Gradually slow down rotation when no longer rolling
            self.rotation += self.vx * 0.1  # Much slower (was 0.2)
            self.rotation = self.rotation % 360

        # Floor collision (jar bottom) - use hitbox_radius for collision detection
        if self.y + self.hitbox_radius > JAR_BOTTOM:
            self.y = JAR_BOTTOM - self.hitbox_radius
            self.vy = 0
            self.landed = True
            self.vx *= 0.85  # More friction (was 0.88)
        else:
            # Check if supported by another fruit
            if is_supported(self, fruits):
                self.vy = 0
                self.landed = True
                self.vx *= 0.85  # More friction (was 0.88)
                
                # Much reduced rolling physics when on top of other fruits
                for other in fruits:
                    if other is not self and self.y < other.y:  # This fruit is above the other
                        dx = abs(self.x - other.x)
                        dy = abs(self.y - other.y)
                        if dx < self.hitbox_radius + other.hitbox_radius and dy < self.hitbox_radius + other.hitbox_radius:
                            # Calculate slope for rolling - much reduced force
                            if self.x > other.x:
                                self.vx += 0.08  # Much reduced rolling force (was 0.15)
                            else:
                                self.vx -= 0.08  # Much reduced rolling force (was 0.15)
            else:
                self.landed = False
                self.vx *= 0.93  # More air resistance (was 0.95)

        # Wall collision (jar sides) - use hitbox_radius for collision detection
        if self.x - self.hitbox_radius < JAR_LEFT:
            self.x = JAR_LEFT + self.hitbox_radius
            self.vx = -self.vx * 0.4  # Much less bouncy (was 0.6)
        if self.x + self.hitbox_radius > JAR_RIGHT:
            self.x = JAR_RIGHT - self.hitbox_radius
            self.vx = -self.vx * 0.4  # Much less bouncy (was 0.6)

    def draw(self, surf):
        if self.sprite and self.original_sprite:
            # Rotate sprite based on rotation angle
            rotated_sprite = pygame.transform.rotate(self.original_sprite, self.rotation)
            sprite_rect = rotated_sprite.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(rotated_sprite, sprite_rect)
        elif self.sprite:
            # Fallback for sprites without original
            sprite_rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(self.sprite, sprite_rect)

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
        move1 = (f2.weight / total_weight) * overlap * 0.52  # Increased from 0.5 to reduce clipping
        move2 = (f1.weight / total_weight) * overlap * 0.52  # Increased from 0.5 to reduce clipping

        # Adjust positions to prevent clipping
        f1.x -= nx * move1
        f1.y -= ny * move1
        f2.x += nx * move2
        f2.y += ny * move2

        # Set both fruits to rolling state when they collide
        f1.rolling = True
        f2.rolling = True

        # Much reduced rolling physics based on collision
        if abs(dx) > 0.1:  # Horizontal collision
            # Transfer much less velocity for rolling
            velocity_transfer = 0.08  # Much reduced (was 0.15)
            if f1.x > f2.x:
                f1.vx += velocity_transfer
                f2.vx -= velocity_transfer
            else:
                f1.vx -= velocity_transfer
                f2.vx += velocity_transfer

        # Tiny rotation effect from collision
        if f1.rolling:
            collision_force = overlap * 0.005  # Much further reduced (was 0.01)
            f1.rotation += collision_force * random.uniform(-0.1, 0.1)  # Much smaller range (was -0.2, 0.2)
        
        if f2.rolling:
            collision_force = overlap * 0.005  # Much further reduced (was 0.01)
            f2.rotation += collision_force * random.uniform(-0.1, 0.1)  # Much smaller range (was -0.2, 0.2)

        # Much more velocity damping for less slippery physics
        f1.vx *= 0.85  # Much increased damping (was 0.90)
        f1.vy *= 0.85  # Much increased damping (was 0.90)
        f2.vx *= 0.85  # Much increased damping (was 0.90)
        f2.vy *= 0.85  # Much increased damping (was 0.90)

        # Improved boundary clamping to prevent clipping
        for f in (f1, f2):
            # More aggressive boundary enforcement
            if f.x - f.hitbox_radius < JAR_LEFT:
                f.x = JAR_LEFT + f.hitbox_radius + 1  # Added +1 buffer
                f.vx = -f.vx * 0.3  # Much less bouncy (was 0.5)
            if f.x + f.hitbox_radius > JAR_RIGHT:
                f.x = JAR_RIGHT - f.hitbox_radius - 1  # Added -1 buffer
                f.vx = -f.vx * 0.3  # Much less bouncy (was 0.5)
            if f.y + f.hitbox_radius > JAR_BOTTOM:
                f.y = JAR_BOTTOM - f.hitbox_radius - 1  # Added -1 buffer
                f.vy = 0
                f.landed = True

def merge(f1, f2):
    # If not the last fruit, merge up as normal
    if f1.kind < len(FRUITS) - 1:
        new_fruit = Fruit(f1.kind + 1, (f1.x + f2.x) / 2, (f1.y + f2.y) / 2)
        # Much reduced merge rotation (was ±30 and ±45)
        if random.choice([True, False]):
            new_fruit.rotation = f1.rotation + random.uniform(-10, 10)
        else:
            new_fruit.rotation = f2.rotation + random.uniform(-10, 10)
        
        # Reduced merge spin effect (was ±45)
        new_fruit.rotation += random.uniform(-15, 15)
        new_fruit.rotation = new_fruit.rotation % 360
        
        return new_fruit
    return None

def collide(f1, f2):
    dist = math.hypot(f1.x - f2.x, f1.y - f2.y)
    return dist < f1.hitbox_radius + f2.hitbox_radius

def is_supported(fruit, fruits):
    if abs(fruit.y + fruit.hitbox_radius - JAR_BOTTOM) < 2:  # Increased tolerance
        return True
    for other in fruits:
        if other is fruit:
            continue
        dx = abs(fruit.x - other.x)
        dy = (fruit.y + fruit.hitbox_radius) - (other.y - other.hitbox_radius)
        # More precise support detection
        if dx < fruit.hitbox_radius + other.hitbox_radius - 3 and 0 <= dy < 3:  # Adjusted tolerances
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
game_over_triggered = False
game_over_time = 0
score = 0
drop_cooldown = 2000
last_drop_time = pygame.time.get_ticks() - drop_cooldown

state = STATE_MENU
running = True

while running:
    if state == STATE_MENU:
        # --- MENU SCREEN ---
        menu_waiting = True
        while menu_waiting:
            # Move the drawing code inside the loop for continuous updates
            screen.fill((30, 30, 30))
            title = big_font.render("Suika Game", True, (255, 255, 0))
            play_btn = font.render("1. Play", True, (255, 255, 255))
            howto_btn = font.render("2. How to Play", True, (255, 255, 255))
            lb_btn = font.render("3. Leaderboard", True, (255, 255, 255))
            credits_btn = font.render("4. Credits", True, (255, 255, 255))
            quit_btn = font.render("5. Quit", True, (255, 255, 255))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
            screen.blit(play_btn, (WIDTH // 2 - play_btn.get_width() // 2, 270))
            screen.blit(howto_btn, (WIDTH // 2 - howto_btn.get_width() // 2, 320))
            screen.blit(lb_btn, (WIDTH // 2 - lb_btn.get_width() // 2, 370))
            screen.blit(credits_btn, (WIDTH // 2 - credits_btn.get_width() // 2, 420))
            screen.blit(quit_btn, (WIDTH // 2 - quit_btn.get_width() // 2, 470))
            
            # Draw music controls
            draw_music_button(screen)
            draw_music_menu(screen)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    menu_waiting = False
                
                # Handle music menu events
                handle_music_menu_events(event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        state = STATE_PLAYING
                        menu_waiting = False
                    elif event.key == pygame.K_2:
                        state = STATE_HOWTO
                        menu_waiting = False
                    elif event.key == pygame.K_3:
                        state = STATE_LEADERBOARD
                        menu_waiting = False
                    elif event.key == pygame.K_4:
                        state = STATE_CREDITS
                        menu_waiting = False
                    elif event.key == pygame.K_5 or event.key == pygame.K_ESCAPE:
                        running = False
                        menu_waiting = False
            
            clock.tick(60)  # Add frame rate control

    elif state == STATE_HOWTO:
        # --- HOW TO PLAY SCREEN ---
        howto_waiting = True
        while howto_waiting:
            screen.fill((30, 30, 30))
            title = big_font.render("How to Play", True, (255, 255, 0))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        
            # Instructions text (blank for you to edit)
            instructions = [
                "",  # Add your instructions here
                "",
                "",
                "",
                "",
            ]
            
            y_offset = 120
            for instruction in instructions:
                if instruction:
                    text = font.render(instruction, True, (255, 255, 255))
                    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 35
            
            # Show merge order with sprites
            merge_title = font.render("Merge Order:", True, (255, 255, 255))
            screen.blit(merge_title, (WIDTH // 2 - merge_title.get_width() // 2, y_offset + 20))
            
            # Display fruits in merge order with much better spacing
            start_x = 60  # Adjusted for better centering
            start_y = y_offset + 70
            sprite_spacing = 110  # Increased spacing to prevent overlap
            
            for i, (radius, color, weight, sprite) in enumerate(FRUITS):
                x = start_x + (i % 5) * sprite_spacing
                y = start_y + (i // 5) * sprite_spacing * 1.8  # Increased vertical spacing more
                
                if sprite:
                    # Scale sprite for display - smaller scale to prevent overlap
                    max_display_size = 40  # Maximum display size to prevent overlap
                    display_size = min(radius * 1.2, max_display_size)  # Cap the size
                    display_sprite = pygame.transform.scale(sprite, (int(display_size), int(display_size)))
                    sprite_rect = display_sprite.get_rect(center=(x, y))
                    screen.blit(display_sprite, sprite_rect)
                else:
                    # Draw as circle with capped size
                    display_radius = min(radius // 2, 20)  # Cap circle size too
                    pygame.draw.circle(screen, color, (x, y), display_radius)
                
                # Draw arrow if not the last fruit and not at end of row
                if i < len(FRUITS) - 1 and (i + 1) % 5 != 0:
                    # Fixed arrow positioning - use consistent spacing
                    arrow_start = (x + 25, y)  # Fixed distance from center
                    arrow_end = (x + sprite_spacing - 25, y)  # Fixed distance to next
                    pygame.draw.line(screen, (255, 255, 255), arrow_start, arrow_end, 2)
                    # Arrow head
                    pygame.draw.polygon(screen, (255, 255, 255), [
                        arrow_end,
                        (arrow_end[0] - 8, arrow_end[1] - 4),
                        (arrow_end[0] - 8, arrow_end[1] + 4)
                    ])
                
                # Draw down arrow for end of first row (fruit 4 -> fruit 5)
                if i == 4:  # End of first row
                    arrow_start = (x, y + 25)  # Fixed distance below
                    arrow_end = (start_x, y + sprite_spacing * 1.8 - 25)  # Point to start of next row
                    pygame.draw.line(screen, (255, 255, 255), arrow_start, arrow_end, 2)
                    # Arrow head pointing down-left
                    pygame.draw.polygon(screen, (255, 255, 255), [
                        arrow_end,
                        (arrow_end[0] + 6, arrow_end[1] - 6),
                        (arrow_end[0] + 6, arrow_end[1] + 2)
                    ])
            
            back_msg = font.render("Press any key to return to menu", True, (200, 200, 200))
            screen.blit(back_msg, (WIDTH // 2 - back_msg.get_width() // 2, 650))
        
            # Draw music controls
            draw_music_button(screen)
            draw_music_menu(screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    howto_waiting = False
                handle_music_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    howto_waiting = False
            
            clock.tick(60)


    elif state == STATE_CREDITS:
        # --- CREDITS SCREEN ---
        credits_waiting = True
        while credits_waiting:
            screen.fill((30, 30, 30))
            title = big_font.render("Credits", True, (255, 255, 0))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))  # Moved higher
            
            # Credits text (blank for you to edit)
            credits = [
                "Original Game: Aladdin X",
                "Code (98.52%): Github Copilot",
                "Code (1.48%): Adam Faseeh",
                "Sprites: Adam Faseeh",
                "Music:",
                "   -Suika Game theme (original): tibita",
                "   -Suika Game theme (recorder (originally flute arrangement)): Sourced off MuseScore",
                "from the user ccruz21",
                "   -Suika Game theme (piano arrangement): Sourced off MuseScore", 
                "from the user Scarnaval",
                "Support: Henry Sun",
                "Who you need to sub to: Henry's Lego Armoury",
                "Probably did something idk go ask him: Tim Kaempf"
            ]
            
            y_offset = 100  # Start higher
            for credit in credits:
                if credit:
                    # Use smaller font for longer lines
                    if len(credit) > 60:  # Reduced threshold
                        small_font = pygame.font.SysFont(None, 20)  # Even smaller font
                        text = small_font.render(credit, True, (255, 255, 255))
                    else:
                        text = font.render(credit, True, (255, 255, 255))
                    
                    # Center text but check if it fits
                    text_x = WIDTH // 2 - text.get_width() // 2
                    if text.get_width() > WIDTH - 40:  # If text is too wide
                        text_x = 20  # Align to left with padding
                    
                    screen.blit(text, (text_x, y_offset))
                y_offset += 30  # Reduced spacing
            
            back_msg = font.render("Press any key to return to menu", True, (200, 200, 200))
            screen.blit(back_msg, (WIDTH // 2 - back_msg.get_width() // 2, 700))
            
            # Draw music controls
            draw_music_button(screen)
            draw_music_menu(screen)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    credits_waiting = False
                
                handle_music_menu_events(event)
                
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    credits_waiting = False
            
            clock.tick(60)  # Add frame rate control

    elif state == STATE_LEADERBOARD:
        # --- LEADERBOARD SCREEN ---
        lb_waiting = True
        while lb_waiting:
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
            
            # Draw music controls
            draw_music_button(screen)
            draw_music_menu(screen)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    lb_waiting = False
                handle_music_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    lb_waiting = False
            
            clock.tick(60)

    elif state == STATE_PLAYING:
        # --- GAME SETUP ---
        fruits = []
        next_kind = random.randint(0, 4)
        current_kind = random.randint(0, 4)
        current_fruit = Fruit(current_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
        game_over = False
        game_over_triggered = False
        game_over_time = 0
        score = 0
        drop_cooldown = 2000
        last_drop_time = pygame.time.get_ticks() - drop_cooldown

        # --- GAME LOOP ---
        while not game_over and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                handle_music_menu_events(event)
                if event.type == pygame.KEYDOWN and not game_over_triggered:
                    if event.key == pygame.K_LEFT:
                        current_fruit.x -= 20
                        if current_fruit.x - current_fruit.hitbox_radius < JAR_LEFT:
                            current_fruit.x = JAR_LEFT + current_fruit.hitbox_radius
                    if event.key == pygame.K_RIGHT:
                        current_fruit.x += 20
                        if current_fruit.x + current_fruit.hitbox_radius > JAR_RIGHT:
                            current_fruit.x = JAR_RIGHT - current_fruit.hitbox_radius
                    if event.key == pygame.K_SPACE:
                        now = pygame.time.get_ticks()
                        if now - last_drop_time >= drop_cooldown:
                            fruits.append(current_fruit)
                            current_fruit = Fruit(next_kind, JAR_LEFT + JAR_WIDTH // 2, JAR_TOP - 40)
                            current_fruit.vx = 0
                            next_kind = random.randint(0, 4)  # Only allow cherry to persimmon
                            last_drop_time = now

            # Only update game logic if not in game over freeze
            if not game_over_triggered:
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
                                score += 10 * (new_fruit.kind + 1)

                            merged_indices.add(i)
                            merged_indices.add(j)

                # Remove merged fruits and add new ones
                for idx in sorted(merged_indices, reverse=True):
                    del fruits[idx]
                fruits.extend(new_fruits)

                # --- PRIORITY LOOP: walls -> collisions ---
                max_priority_passes = 8  # Increased from 5 to handle more complex collisions
                priority_pass = 0
                while priority_pass < max_priority_passes:
                    # 1. Resolve wall collisions - use hitbox_radius
                    wall_bounced = False
                    for fruit in fruits:
                        # More aggressive wall collision detection
                        if fruit.x - fruit.hitbox_radius <= JAR_LEFT:
                            fruit.x = JAR_LEFT + fruit.hitbox_radius + 1
                            fruit.vx = -fruit.vx * 0.4  # Much less bouncy (was 0.6)
                            wall_bounced = True
                        if fruit.x + fruit.hitbox_radius >= JAR_RIGHT:
                            fruit.x = JAR_RIGHT - fruit.hitbox_radius - 1
                            fruit.vx = -fruit.vx * 0.4  # Much less bouncy (was 0.6)
                            wall_bounced = True
                        if fruit.y + fruit.hitbox_radius >= JAR_BOTTOM:
                            fruit.y = JAR_BOTTOM - fruit.hitbox_radius - 1
                            fruit.vy = 0
                            fruit.landed = True
                            wall_bounced = True
                    if wall_bounced:
                        priority_pass += 1
                        continue

                    # 2. Resolve fruit-to-fruit collisions
                    collision_happened = False
                    fruits_copy = fruits[:]
                    for i in range(len(fruits_copy)):
                        for j in range(i + 1, len(fruits_copy)):
                            if i >= len(fruits) or j >= len(fruits):
                                break
                            if collide(fruits[i], fruits[j]):
                                before = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                                resolve_collision(fruits[i], fruits[j])
                                after = (fruits[i].x, fruits[i].y, fruits[j].x, fruits[j].y)
                                if before != after:
                                    collision_happened = True
                    if collision_happened:
                        priority_pass += 1
                        continue

                    break

                # Update fruits
                for fruit in fruits:
                    fruit.update(fruits)

                # --- GAME OVER CHECK ---
                for fruit in fruits:
                    if fruit.landed and fruit.y - fruit.hitbox_radius < JAR_TOP + 10:
                        game_over_triggered = True
                        game_over_time = pygame.time.get_ticks()
                        break

            # Check if 5 seconds have passed since game over was triggered
            if game_over_triggered:
                if pygame.time.get_ticks() - game_over_time >= 5000:  # 5 seconds
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
            if not game_over_triggered:
                current_fruit.draw(screen)

            # Draw cooldown indicator (to the right of jar, near top) - only if not game over
            if not game_over_triggered:
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
                
                # Draw next fruit with sprite if available
                next_label = font.render("Next", True, (255, 255, 255))
                next_label_y = indicator_center[1] + indicator_radius + 50
                screen.blit(next_label, (indicator_center[0] - next_label.get_width() // 2, next_label_y))
                
                # Position next fruit to not overlap with text
                next_fruit_y = next_label_y + next_label.get_height() + 20  # Dynamic positioning
                
                # Draw next fruit with sprite if available
                next_radius, next_color, next_weight, next_sprite = FRUITS[next_kind]
                if next_sprite:
                    # Scale sprite for next fruit preview
                    preview_sprite = pygame.transform.scale(next_sprite, (next_radius * 2, next_radius * 2))
                    sprite_rect = preview_sprite.get_rect(center=(indicator_center[0], next_fruit_y))
                    screen.blit(preview_sprite, sprite_rect)
                else:
                    # Draw as circle for fruits without sprites
                    pygame.draw.circle(
                        screen,
                        next_color,
                        (indicator_center[0], next_fruit_y),
                        next_radius
                    )

            # Draw game over warning if triggered
            if game_over_triggered:
                warning_text = big_font.render("GAME OVER!", True, (255, 0, 0))
                screen.blit(warning_text, (WIDTH // 2 - warning_text.get_width() // 2, HEIGHT // 2 - 50))
                time_left = 5 - (pygame.time.get_ticks() - game_over_time) // 1000
                countdown_text = font.render(f"Continuing in {time_left}...", True, (255, 255, 255))
                screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 + 20))

            score_text = font.render(f"Score: {score}", True, (255, 255, 0))
            screen.blit(score_text, (20, 20))
            draw_music_button(screen)
            draw_music_menu(screen)
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
        go_waiting = True
        while go_waiting:
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
            draw_music_button(screen)
            draw_music_menu(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    go_waiting = False
                handle_music_menu_events(event)
                if event.type == pygame.KEYDOWN:
                    state = STATE_MENU
                    go_waiting = False

            clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()