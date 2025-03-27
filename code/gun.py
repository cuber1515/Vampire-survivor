from settings import *

class Gun(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'gun', 'gun.png'))
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500

    
    def move(self, pos):
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        pass