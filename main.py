import pygame
import sys

# Initialisierung
pygame.init()

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
        self.rect.x = 50  # Start links
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 0.8

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity_y = self.jump_power

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

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

# Funktion: Level starten
def start_level(level):
    all_sprites = pygame.sprite.Group()
    pirates = pygame.sprite.Group()

    ninja = Ninja()
    all_sprites.add(ninja)

    start_x = 400
    piraten_abstand = 200
    piraten_pro_reihe = 4  # Neue Reihe nach 4 Piraten

    for i in range(level):
        x = start_x + (i % piraten_pro_reihe) * piraten_abstand
        y_offset = (i // piraten_pro_reihe) * 100  # jede neue Reihe 100 Pixel höher
        base_y = SCREEN_HEIGHT  # Start ganz unten
        y_position = base_y - y_offset

        if y_position < 100:
            y_position = 100  # Begrenzung: nicht zu hoch!

        movement_range = 100 + i * 20
        speed = 2 + i * 0.2
        pirate = Pirate(x, movement_range, speed)
        pirate.rect.bottom = y_position

        all_sprites.add(pirate)
        pirates.add(pirate)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Updates
        all_sprites.update()

        # Kollisionen prüfen
        if pygame.sprite.spritecollide(ninja, pirates, False):
            return False  # Game Over

        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Level geschafft, wenn Ninja ganz rechts rausläuft
        if ninja.rect.left > SCREEN_WIDTH:
            return True

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
        max_levels = 10

        while level <= max_levels:
            print(f"Level {level} beginnt...")
            success = start_level(level)
            if success:
                print(f"Level {level} geschafft!")
                level += 1
            else:
                print(f"Game Over in Level {level}!")
                break

        if level > max_levels:
            print("Herzlichen Glückwunsch! Du hast Ninja Knight durchgespielt!")

        playing = game_over_screen()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
