import random
import pygame
import player
import game_platform
import plank
import green_insect


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Jumper Shooter")

        self.screen_width = 1200
        self.screen_height = 700
        self.pause_menu_width = self.screen_width - 100
        self.pause_menu_height = self.screen_height - 40

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
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
        self.running = True
        self.total_enemies_spawned = 0
        self.scene = "start"

        self.pause_menu_background = pygame.surface.Surface((self.pause_menu_width, self.pause_menu_height))
        self.pause_menu_background.fill(pygame.color.Color(255, 255, 255))
        self.pause_menu_background.set_alpha(200)
        
        self.resume_button = pygame.image.load("assets/buttons/resume.png")
        self.start_button = pygame.image.load("assets/buttons/start.png")
        self.quit_button = pygame.image.load("assets/buttons/quit.png")
        self.menu_button = pygame.image.load("assets/buttons/menu.png")

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

    def start_screen(self):
        start_button = pygame.Rect(self.screen_width // 2 - 100, 200, 200, 50)
        quit_button = pygame.Rect(self.screen_width // 2 - 100, 300, 200, 50)
        font = pygame.font.Font(None, 36)

        while self.scene == "start":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.scene = "game"
                    elif quit_button.collidepoint(event.pos):
                        self.scene = "false"
                        self.running = False

            self.screen.fill((0, 128, 0))  # Green background

            self.screen.blit(self.start_button, start_button)

            self.screen.blit(self.quit_button, quit_button)

            pygame.display.flip()
            self.clock.tick(30)

    def pause_menu(self):

        resume_button = pygame.Rect(self.screen_width // 2 - 100,
                                    40, 200, 50)
        quit_button = pygame.Rect(self.screen_width // 2 - 100,
                                  110, 200, 50)
        menu_button = pygame.Rect(self.screen_width // 2 - 100,
                                  180, 200, 50)

        font = pygame.font.Font(None, 36)

        self.screen.blit(self.pause_menu_background, (self.screen_width // 2 - self.pause_menu_width // 2,
                                                      self.screen_height // 2 - self.pause_menu_height // 2))

        self.screen.blit(self.quit_button, quit_button)

        self.screen.blit(self.resume_button, resume_button)

        self.screen.blit(self.menu_button, menu_button)

        while self.scene == "pause":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.scene = "false"
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.collidepoint(event.pos):
                        self.scene = "game"
                    elif quit_button.collidepoint(event.pos):
                        self.scene = "false"
                        self.running = False
                    elif menu_button.collidepoint(event.pos):
                        self.scene = "start"

            pygame.display.flip()
            self.clock.tick(30)

    def start(self):
        while self.running:
            if self.scene == "start":
                self.start_screen()
            elif self.scene == "game":
                self.game_loop()
            elif self.scene == "pause":
                self.pause_menu()

        pygame.quit()

    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.scene = "pause"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the pause button is clicked
                    pause_button = pygame.Rect(self.screen_width - 50, 10, 40, 40)
                    if pause_button.collidepoint(event.pos):
                        self.scene = "pause"  # Set scene to "pause" to display the pause menu

        self.screen.blit(self.background, (0, 0))
        self.platforms.update()
        self.player.update(self.blocks)
        self.enemy_spawner()
        self.enemies.update(self.player, self.blocks, self.blocks)
        self.blocks.update(self.player)
        self.screen.blit(self.ground, self.ground_rect)

        # Pause button
        pause_button = pygame.Rect(self.screen_width - 50, 10, 40, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), pause_button)
        pygame.draw.lines(self.screen, (0, 0, 0), True,
                          [(self.screen_width - 35, 20), (self.screen_width - 15, 30), (self.screen_width - 35, 40)], 2)

        pygame.display.flip()
        self.clock.tick(30)


game = Game()
game.start()
