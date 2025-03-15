from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()

    def draw(self):
        for sprite in self:
            self.screen.blit(sprite.image, sprite.rect)