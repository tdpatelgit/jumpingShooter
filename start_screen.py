import pygame


class StartScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.start_button = pygame.Rect(300, 200, 200, 50)
        self.quit_button = pygame.Rect(300, 300, 200, 50)
        self.game = game

    def update(self, game):

        self.game = game
        self.handle_events()
        self.draw()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(pygame.mouse.get_pos()):
                    self.game.scene = "game"
                elif self.quit_button.collidepoint(pygame.mouse.get_pos()):
                    self.game.scene = "quit"

    def draw(self):
        self.screen.fill((0, 128, 0))  # Green background

        # Start button
        pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)  # Green button
        start_text = self.font.render("Start", True, (0, 0, 0))
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        self.screen.blit(start_text, start_text_rect)

        # Quit button
        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)  # Red button
        quit_text = self.font.render("Quit", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)
