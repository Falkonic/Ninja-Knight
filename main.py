import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Knight")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Spielerklasse
class Ninja(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/ninja.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Größe anpassen
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.jump_power = -15
        self.gravity = 0.8

    def update(self):
        keys = pygame.key.get_pressed()
    
        # Links/Rechts Bewegung
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5  # 5 Pixel nach links
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5  # 5 Pixel nach rechts

    # Springen
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity_y = self.jump_power
    
    # Schwerkraft
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Bodenbegrenzung
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0


# Sprite-Gruppen
all_sprites = pygame.sprite.Group()
ninja = Ninja()
all_sprites.add(ninja)

# Hauptspiel-Schleife
running = True
while running:
    clock.tick(FPS)
    
    # Events abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Logik
    all_sprites.update()

    # Zeichnen
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Bildschirm aktualisieren
    pygame.display.flip()

# Spiel beenden
pygame.quit()
sys.exit()
