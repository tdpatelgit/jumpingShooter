import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        # Load platform image
        self.image = pygame.transform.scale(pygame.image.load("assets/platform/platform.png"), (400, 20))
        # Create mask for collision detection
        self.mask = pygame.surface.Surface((400, 20))
        self.mask.fill(pygame.Color(100, 100, 100))  # Fill mask with a gray color
        self.mask.set_alpha(200)  # Set alpha transparency to 200 (0 is fully transparent, 255 is fully opaque)
        # Set position of the platform
        self.rect = self.image.get_rect(topleft=pos)
        self.screen = screen

    def update(self):
        # Draw platform
        self.draw()

    def draw(self):
        # Draw platform and mask on the screen
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.mask, self.rect)
