from settings import *

class Gun(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'gun', 'gun.png'))
        self.rect = self.image.get_frect(center = pos)