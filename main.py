import pygame
import sys

# Initialisierung
pygame.init()

# Mixer initialisieren für Sound
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("assets/sounds/jump.mp3")

# Fenster auf Vollbild setzen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
pygame.display.set_caption("Ninja Knight")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Spielerklasse
class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/ninja.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.on_ground = False  # Steht der Ninja?

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            jump_sound.play()

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

# Piratenklasse
class Pirate(pygame.sprite.Sprite):
    def __init__(self, x, movement_range, speed):
        super().__init__()
        self.image = pygame.image.load("assets/images/pirate.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = SCREEN_HEIGHT
        self.start_x = x
        self.movement_range = movement_range
        self.speed = speed
        self.direction = 1

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) >= self.movement_range:
            self.direction *= -1

# Plattformklasse
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height=20):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Grau
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Funktion: Level starten
def start_level(level, lives):
    all_sprites = pygame.sprite.Group()
    pirates = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    ninja = Ninja()
    all_sprites.add(ninja)

    start_x = 400
    piraten_abstand = 200
    piraten_pro_reihe = 4

    for i in range(level):
        x = start_x + (i % piraten_pro_reihe) * piraten_abstand
        y_offset = (i // piraten_pro_reihe) * 100
        base_y = SCREEN_HEIGHT
        y_position = base_y - y_offset

        if y_position < 100:
            y_position = 100

        movement_range = 100 + i * 20
        speed = 2 + i * 0.2
        pirate = Pirate(x, movement_range, speed)
        pirate.rect.bottom = y_position

        all_sprites.add(pirate)
        pirates.add(pirate)

    # Plattformen hinzufügen ab Level 6
    if level >= 6:
        plat_width = 200
        plat_y = SCREEN_HEIGHT - 100  # Höhe wie zweite Piratenreihe

        platform1 = Platform(SCREEN_WIDTH // 3 - plat_width // 2, plat_y, plat_width)
        platform2 = Platform(2 * SCREEN_WIDTH // 3 - plat_width // 2, plat_y, plat_width)

        all_sprites.add(platform1, platform2)
        platforms.add(platform1, platform2)

    font = pygame.font.Font(None, 48)

    running = True
    hit_cooldown = 0  # Damit man nach einem Treffer kurz unverwundbar ist

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        
        # Updates
        all_sprites.update()

        # Kollisionslogik
        ninja.on_ground = False  # Standardmäßig erstmal: nicht auf Boden oder Plattform

        if level >= 6:
            ninja.rect.y += 5
            hits = pygame.sprite.spritecollide(ninja, platforms, False)
            ninja.rect.y -= 5

            if hits:
                if ninja.velocity_y > 0:
                    ninja.rect.bottom = hits[0].rect.top
                    ninja.velocity_y = 0
                    ninja.on_ground = True

        if ninja.rect.bottom >= SCREEN_HEIGHT:
            ninja.rect.bottom = SCREEN_HEIGHT
            ninja.velocity_y = 0
            ninja.on_ground = True

        # Treffer durch Piraten
        if hit_cooldown == 0 and pygame.sprite.spritecollide(ninja, pirates, False):
            lives -= 1
            hit_cooldown = 60  # 1 Sekunde Immunität
            if lives <= 0:
                return False, lives  # Game Over

        if hit_cooldown > 0:
            hit_cooldown -= 1

        # Bildschirm zeichnen
        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Levelanzeige
        level_text = font.render(f"Level {level}", True, BLACK)
        lives_text = font.render(f"Leben: {lives}", True, RED)
        screen.blit(level_text, (20, 20))
        screen.blit(lives_text, (20, 70))

        pygame.display.flip()

        # Level geschafft
        if ninja.rect.left > SCREEN_WIDTH:
            return True, lives

# Game Over Screen
def game_over_screen():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill(WHITE)

        game_over_text = font.render("GAME OVER", True, RED)
        retry_text = small_font.render("Drücke R für Neustart oder Q zum Beenden", True, BLACK)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False

# Hauptspiel
def main():
    playing = True
    while playing:
        level = 1
        lives = 3  # NEU: Starte mit 3 Leben
        max_levels = 10

        while level <= max_levels and lives > 0:
            print(f"Level {level} beginnt...")
            success, lives = start_level(level, lives)
            if success:
                print(f"Level {level} geschafft!")
                level += 1
            else:
                print(f"Game Over in Level {level}!")

        if level > max_levels:
            print("Herzlichen Glückwunsch! Du hast Ninja Knight durchgespielt!")

        playing = game_over_screen()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
