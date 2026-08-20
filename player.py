import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, platforms, blocks):
        super().__init__()

        # Initialize player attributes
        self.mouse = pygame.mouse
        self.keys = pygame.key.get_pressed()
        self.image = pygame.transform.scale(pygame.image.load("assets/player/move-frame-0.png").convert_alpha(),
                                            (31, 31))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 584
        self.speed = 7
        self.gravity = 0.8
        self.jump_power = -14
        self.velocity_y = 0
        self.on_ground = False
        self.screen = screen
        self.platforms = platforms
        self.blocks = blocks
        self.frame = 0
        self.move_images = [pygame.transform.scale(pygame.image.load("assets/player/move-frame-0.png"), (31, 31)),
                            pygame.transform.scale(pygame.image.load("assets/player/move-frame-1.png"), (31, 31))]
        self.health = 100
        self.exp = 0
        self.next_level = 100

        # Gun attributes
        self.gun_image = pygame.transform.scale(pygame.image.load("assets/Gun/gun.png").convert_alpha(), (31, 31))
        self.gun_rect = self.gun_image.get_rect(center=self.rect.center)

        # Shooting attributes
        self.shoot_delay = 100  # in milliseconds
        self.last_shot = pygame.time.get_ticks()

        # Group for bullets
        self.bullets = pygame.sprite.Group()

    def update(self, blocks):
        # Update player attributes and behaviors

        self.blocks = blocks
        self.mouse = pygame.mouse
        self.keys = pygame.key.get_pressed()

        self.check_collision_y()
        self.gravity_effect()
        self.move()
        self.jump()
        self.rect.y += self.velocity_y

        self.update_gun()
        if self.mouse.get_pressed()[0]:
            self.shoot()
        self.bullets.update()
        self.draw()

    def gravity_effect(self):
        # Apply gravity effect if player is not on ground

        if not self.on_ground:
            if self.velocity_y < 10:
                self.velocity_y += self.gravity

    def jump(self):
        # Make player jump when space bar is pressed and player is on ground

        if self.on_ground and self.keys[pygame.K_SPACE]:
            self.velocity_y = self.jump_power

    def check_collision_y(self):
        # Check collision with platforms and blocks in the y-axis

        self.on_ground = False

        for platform in self.platforms:
            if self.rect.colliderect(platform) and self.rect.bottom <= platform.top + 10:
                if not (self.keys[pygame.K_s] or self.keys[pygame.K_LSHIFT]):
                    if self.velocity_y >= 0:
                        self.rect.bottom = platform.top + 1
                        self.velocity_y = 0
                        self.on_ground = True
                        return

        for block in self.blocks:
            if block.rect.top > 0 and not block.space:
                if self.rect.colliderect(block.rect):
                    if self.rect.centery > block.rect.centery:
                        self.rect.top = block.rect.bottom
                        self.velocity_y = 0
                    if self.rect.centery < block.rect.centery:
                        self.rect.bottom = block.rect.top
                        self.velocity_y = 0

        if self.rect.bottom >= 600:  # Adjust this according to your screen height
            self.rect.bottom = 600
            self.on_ground = True
            self.velocity_y = 0

    def move(self):
        # Move player left or right

        if self.keys[pygame.K_a]:
            self.rect.centerx -= self.speed
            self.move_animation()
        if self.keys[pygame.K_d]:
            self.rect.centerx += self.speed
            self.move_animation()
            self.image = pygame.transform.flip(self.image, False, True)

    def update_gun(self):
        # Update gun position and angle

        mouse_pos = self.mouse.get_pos()

        dx = mouse_pos[0] - (self.rect.x + self.rect.width / 2)
        dy = mouse_pos[1] - (self.rect.y + self.rect.height / 2)
        angle = math.degrees(math.atan2(-dy, dx))
        self.gun_image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("assets/Gun/gun.png").convert_alpha(), (31, 31)), angle)
        self.gun_rect = self.gun_image.get_rect(center=self.rect.center)

    def shoot(self):
        # Make player shoot bullets

        now = pygame.time.get_ticks()

        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.mouse.get_pos()[0], self.mouse.get_pos()[1])
            self.bullets.add(bullet)

    def draw(self):
        # Draw player, gun, and bullets

        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.gun_image, self.gun_rect)
        self.bullets.draw(self.screen)

    def move_animation(self):
        # Animate player movement
        self.frame += 1
        if self.frame >= len(self.move_images):
            self.frame = 0
        self.image = self.move_images[self.frame]


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):

        super().__init__()

        # Initialize bullet attributes
        self.image = pygame.transform.scale(pygame.image.load("assets/Gun/bullet.png").convert_alpha(), (3, 1))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - self.rect.centerx, my - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.speed = 10
        self.dx = target_x - x
        self.dy = target_y - y
        distance = (self.dx ** 2 + self.dy ** 2) ** 0.5
        self.dx /= distance
        self.dy /= distance
        self.health = 10

    def update(self):
        # Move bullet towards target

        if 0 < self.rect.y < 600 and 0 < self.rect.x < 1200:
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
        else:
            self.kill()

    def finish(self):
        # Reduce bullet health and kill if health is zero

        self.health -= 1
        if self.health <= 0:
            self.kill()
