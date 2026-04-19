import pygame
import sys
import random

# --- INITIALIZATION ---
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Kombat")
clock = pygame.time.Clock()

# --- COLORS ---
BG_COLOR = (30, 30, 30)
P1_COLOR = (0, 255, 255)  # Cyan
AI_COLOR = (255, 50, 50)   # Red
ATTACK_COLOR = (255, 255, 0) # Yellow
HP_BG = (100, 100, 100)
HP_FILL = (0, 255, 0)

# --- FIGHTER CLASS ---
class Fighter:
    def __init__(self, x, y, color, is_ai=False):
        self.rect = pygame.Rect(x, y, 50, 100) # (x, y, width, height)
        # TO ADD REAL 2D CHARACTERS: 
        # self.image = pygame.image.load('player_sprite.png')
        # self.image = pygame.transform.scale(self.image, (50, 100))
        
        self.color = color
        self.is_ai = is_ai
        self.hp = 100
        
        # Physics
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 1
        self.speed = 5
        self.is_jumping = False
        
        # Actions
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_rect = None
        
        # Dodge
        self.is_dodging = False
        self.dodge_timer = 0

    def move(self, keys, target):
        dx = 0
        
        if not self.is_ai:
            # --- PLAYER CONTROLS ---
            if keys[pygame.K_a]:
                dx = -self.speed
            if keys[pygame.K_d]:
                dx = self.speed
            if keys[pygame.K_w] and not self.is_jumping:
                self.vel_y = self.jump_power
                self.is_jumping = True
            if keys[pygame.K_s] and self.dodge_timer == 0:
                self.is_dodging = True
                self.dodge_timer = 30 # Frames of invincibility
            if keys[pygame.K_SPACE] and self.attack_timer == 0 and not self.is_dodging:
                self.attack(target)
        else:
            # --- SMART AI LOGIC ---
            if self.attack_timer == 0 and not self.is_dodging:
                dist = target.rect.centerx - self.rect.centerx
                # Move towards player
                if dist > 60:
                    dx = self.speed - 1 # slightly slower than player
                elif dist < -60:
                    dx = -(self.speed - 1)
                else:
                    # Close enough to attack
                    if random.random() < 0.05: # 5% chance per frame to attack
                        self.attack(target)
                
                # Randomly jump or dodge if player attacks
                if target.is_attacking and random.random() < 0.03:
                    if not self.is_jumping:
                        self.vel_y = self.jump_power
                        self.is_jumping = True
                elif target.is_attacking and random.random() < 0.02 and self.dodge_timer == 0:
                    self.is_dodging = True
                    self.dodge_timer = 30

        # Apply Dodge logic
        if self.is_dodging:
            self.dodge_timer -= 1
            self.rect.height = 50 # Shrink to dodge high attacks
            self.rect.y = HEIGHT - 50 # Snap to floor
            if self.dodge_timer <= 0:
                self.is_dodging = False
                self.rect.height = 100
                self.rect.y = HEIGHT - 100

        # Apply Gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Floor Collision
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0
            self.is_jumping = False

        # Screen boundaries
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > WIDTH:
            dx = WIDTH - self.rect.right

        self.rect.x += dx

        # Handle Attack Duration
        if self.is_attacking:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_rect = None

    def attack(self, target):
        self.is_attacking = True
        self.attack_timer = 15 # Attack lasts 15 frames
        
        # Determine direction of attack
        direction = 1 if target.rect.centerx > self.rect.centerx else -1
        
        # Create Attack Hitbox
        self.attack_rect = pygame.Rect(self.rect.centerx + (20 * direction), self.rect.y + 20, 40, 20)
        
        # Check Collision (if target is not dodging)
        if self.attack_rect.colliderect(target.rect) and not target.is_dodging:
            target.hp -= 10
            target.rect.x += 20 * direction # Knockback

    def draw(self, surface):
        # Draw Character (Replace with self.image if using sprites)
        if self.is_dodging:
            pygame.draw.rect(surface, (100, 100, 100), self.rect) # Grey out when dodging
        else:
            pygame.draw.rect(surface, self.color, self.rect)

        # Draw Attack Hitbox
        if self.is_attacking and self.attack_rect:
            # TO ADD ATTACK ANIMATIONS:
            # Draw your fireball/punch png here using self.attack_rect coordinates
            pygame.draw.rect(surface, ATTACK_COLOR, self.attack_rect)

def draw_health_bar(hp, x, y):
    pygame.draw.rect(screen, HP_BG, (x, y, 300, 30))
    pygame.draw.rect(screen, HP_FILL, (x, y, max(0, hp * 3), 30))

# --- MAIN GAME LOOP ---
player = Fighter(200, HEIGHT - 100, P1_COLOR)
ai = Fighter(550, HEIGHT - 100, AI_COLOR, is_ai=True)

running = True
game_over = False

while running:
    clock.tick(60) # 60 FPS
    screen.fill(BG_COLOR)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # Move & Update Logic
        player.move(keys, ai)
        ai.move(keys, player)

        # Draw Fighters
        player.draw(screen)
        ai.draw(screen)

        # Draw Health Bars
        draw_health_bar(player.hp, 50, 20)
        draw_health_bar(ai.hp, WIDTH - 350, 20)

        # Win/Lose Condition
        if player.hp <= 0 or ai.hp <= 0:
            game_over = True

    else:
        # Game Over Screen
        font = pygame.font.Font(None, 74)
        if player.hp <= 0:
            text = font.render("YOU LOSE!", True, (255, 0, 0))
        else:
            text = font.render("YOU WIN!", True, (0, 255, 0))
        
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()

