import pygame
import player
import game_platform
import plank
import green_insect
import random


class Level1:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.transform.scale(pygame.image.load("assets/background/Background.png"), (1200, 600))
        self.ground = pygame.surface.Surface((1200, 200))
        self.ground.fill("green")
        self.ground_rect = self.ground.get_rect(topleft=(0, 600))
        self.platforms = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.ground_list = [self.ground_rect]
        self.player = player.Player(self.screen, self.ground_list, self.blocks)
        self.enemies = pygame.sprite.Group()
        self.max_enemies = 3
        self.total_enemies_spawned = 0

        self.generate_platform()

    def generate_platform(self):
        self.platforms = pygame.sprite.Group()
        not_x_list = []
        for y in range(0, 3):
            not_x = random.randint(0, 28)
            not_x_list.append(not_x - 1)
            not_x_list.append(not_x)
            not_x_list.append(not_x + 1)
            for x in range(0, 3):
                platform = game_platform.Platform((x * 400, 500 - (y * 100)), self.screen)
                self.ground_list.append(platform.rect)
                self.platforms.add(platform)
            for x in range(-1, 31):
                if x != not_x and x != not_x + 1:
                    block = plank.Plank(self.screen, (x * 40, 500 - (y * 100)))
                    self.blocks.add(block)
                else:
                    block = plank.Plank(self.screen, (x * 40, 500 - (y * 100)), True)
                    self.blocks.add(block)

    def enemy_spawner(self):
        spawn_positions = [(0, 300), (1240, 400), (0, 400), (0, 500)]
        if len(self.enemies) < self.max_enemies:
            self.enemies.add(green_insect.GreenInsect(self.screen,
                                                      spawn_positions[random.randrange(len(spawn_positions))],
                                                      self.blocks, self.player))
            self.total_enemies_spawned += 1
        if self.total_enemies_spawned // 10 > self.max_enemies:
            self.max_enemies += 1

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.platforms.update()
        self.player.update(self.blocks)
        self.enemy_spawner()
        self.enemies.update(self.player, self.blocks, self.blocks)
        self.blocks.update(self.player)
        self.screen.blit(self.ground, self.ground_rect)
        pygame.display.update()