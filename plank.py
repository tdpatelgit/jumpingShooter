import pygame


class Plank(pygame.sprite.Sprite):
    def __init__(self, screen, pos, space=False):
        super().__init__()
        # Initialize attributes
        self.screen = screen
        self.player = None
        self.image = pygame.transform.scale(pygame.image.load("assets/platform/plank.png"), (40, 20))
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.name = "plank"
        self.space = space
        if self.space:
            self.health = 0
        else:
            self.health = 10
        self.show = 100

    def check_collision(self):
        # Check collision with bullets if the plank is visible and not a space plank
        if not self.space:
            for bullet in self.player.bullets:
                if self.show == 100:
                    if self.rect.colliderect(bullet.rect):
                        bullet.finish()
                        self.health -= 1
                        if self.health <= 0:
                            self.show = 0
                            self.rect.center = (-100, -100)

    def update(self, player):
        # Update plank's state
        self.player = player
        if not self.space:
            if self.show == 100:
                # Reset position and draw if visible
                self.rect = self.image.get_rect(topleft=self.pos)
                self.draw()
                self.check_collision()
            else:
                # Increment counter to show the plank again
                self.show += 1

    def draw(self):
        # Draw the plank on the screen
        self.screen.blit(self.image, self.pos)
