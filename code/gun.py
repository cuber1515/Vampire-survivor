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
        rEct = self.image.get_frect(center = pos)
        self.gunPos = pygame.Vector2(rEct.centerx + 100, rEct.centery)
        self.rect = self.image.get_frect(center = self.gunPos)

    def update(self, dt):
        pass