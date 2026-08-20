import pygame


class GreenInsect(pygame.sprite.Sprite):
    def __init__(self, screen, pos, blocks, player):
        super().__init__()
        self.screen = screen
        # Load images
        self.image = pygame.transform.scale(pygame.image.load("assets/enemies/green insect/move/move-0.png"), (31, 20))
        self.move_images = [pygame.transform.scale(pygame.image.load("assets/enemies/green insect/move/move-0.png"),
                                                   (31, 20)),
                            pygame.transform.scale(pygame.image.load("assets/enemies/green insect/move/move-1.png"),
                                                   (31, 20))]
        self.rect = self.image.get_rect(bottomleft=pos)
        # Initialize velocity and other attributes
        self.velocity_y = 0
        self.platforms = pygame.sprite.Group()
        self.blocks = blocks
        self.keys = pygame.key.get_pressed()
        self.on_ground = False
        self.speed = 4
        self.frame = 0
        self.gravity = 0.8
        self.player = player
        self.jump_block = self.player
        self.empty_line = []
        self.empty_line_y = []
        self.empty_find()
        self.old_dis = 0
        self.target_y = 0

    def update(self, player, platforms, blocks):
        # Update references
        self.blocks = blocks
        self.platforms = platforms
        self.player = player
        self.keys = pygame.key.get_pressed()

        # Apply gravity and check collisions
        self.gravity_effect()
        self.check_collision_y()
        self.check_collision()
        self.rect.y += self.velocity_y
        self.move()

        # Draw the insect
        self.draw()

    def check_collision(self):
        # Check collision with player bullets
        for bullet in self.player.bullets:
            if self.rect.colliderect(bullet.rect):
                bullet.finish()
                self.player.exp += 1
                self.kill()

    def gravity_effect(self):
        # Apply gravity if not on ground
        if not self.on_ground:
            if self.velocity_y < 10:
                self.velocity_y += self.gravity

    def jump(self):
        # Jump if on ground or close to it
        if self.on_ground or self.rect.bottom > 510:
            self.velocity_y = -14
            self.rect.bottom -= 5
            self.on_ground = False

    def check_collision_y(self):
        # Check collision with blocks in the y-axis
        self.on_ground = False
        for block in self.blocks:
            if block.rect.top > 0:
                if self.rect.colliderect(block.rect):
                    if (self.rect.centery > block.rect.bottom and not block.space
                            and not self.rect.bottom < block.rect.top + 1):
                        if self.rect.centerx < block.rect.left:
                            self.rect.right = block.rect.left - 1
                        elif self.rect.centerx > block.rect.right:
                            self.rect.left = block.rect.right + 1
                        else:
                            self.rect.top = block.rect.bottom
                            self.velocity_y = 0
                    if (self.rect.centery < block.rect.centery and not block.space
                            and not self.rect.top > block.rect.bottom - 1):
                        self.rect.bottom = block.rect.top
                        self.velocity_y = 0
                        self.on_ground = True

        if self.rect.bottom >= 599:  # Adjust this according to your screen height
            self.rect.bottom = 600
            self.on_ground = True
            self.velocity_y = 0

    def empty_find(self):
        # Move towards player and animate
        self.empty_line_y = []
        self.empty_line = []

        if self.player.rect.bottom < 310:

            if self.rect.bottom > 510:
                self.target_y = 510
            elif self.rect.bottom > 410:
                self.target_y = 410
            elif self.rect.bottom > 310:
                self.target_y = 310
            else:
                self.target_y = 0

        elif self.player.rect.bottom < 410:

            if self.rect.bottom > 510:
                self.target_y = 510
            elif self.rect.bottom > 410:
                self.target_y = 410
            elif self.rect.bottom < 310:
                self.target_y = 310
            else:
                self.target_y = 0

        elif self.player.rect.bottom < 510:

            if self.rect.bottom > 510:
                self.target_y = 510
            elif self.rect.bottom < 310:
                self.target_y = 310
            elif self.rect.bottom < 410:
                self.target_y = 410
            else:
                self.target_y = 0

        elif self.player.rect.bottom > 510:

            if self.rect.bottom < 310:
                self.target_y = 310
            elif self.rect.bottom < 410:
                self.target_y = 410
            elif self.rect.bottom < 510:
                self.target_y = 510
            else:
                self.target_y = 0

        for block in self.blocks:
            if self.rect.topleft == (-100, -100):
                self.empty_line.append(block)
            if block.space:
                self.empty_line.append(block)

        for block in self.empty_line:
            if block.rect.top < self.target_y < block.rect.bottom:
                self.jump_block = block
                self.empty_line_y.append(block.rect.centery)

        if self.rect.top - 20 < self.player.rect.centery < self.rect.bottom and self.target_y == 0:

            self.jump_block = self.player

    def move(self):

        if self.old_dis != self.rect.centery - self.player.rect.centery:
            self.empty_find()
        if (abs(self.rect.centerx - self.jump_block.rect.centerx) <= 10 and
                self.rect.bottom - 70 > self.jump_block.rect.bottom):
            self.jump()
        self.old_dis = self.rect.centery - self.player.rect.centery

        self.move_animation()
        if self.rect.centerx > self.jump_block.rect.centerx:
            self.rect.left -= self.speed
        else:
            self.rect.right += self.speed
            self.image = pygame.transform.flip(self.image, True, False)

    def move_animation(self):
        # Animate movement
        self.frame += 1
        if self.frame >= len(self.move_images):
            self.frame = 0
        self.image = self.move_images[self.frame]

    def draw(self):
        # Draw the insect
        self.screen.blit(self.image, self.rect)
