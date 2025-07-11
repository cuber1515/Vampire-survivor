from settings import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)


        random = randint(1,3)
        if random == 1:
            self.mob = 'bat'
        elif random == 2:
            self.mob = 'blob'
        elif random == 3:
            self.mob = 'skeleton'

        self.frame_index = 0
        self.load_images()
        self.image = pygame.image.load(join('images', 'enemies', self.mob, '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = []
        self.folder_path = join('images', 'enemies', self.mob)
        for file in range(4):
            name = f'{file}.png'
            full_path = join(self.folder_path, name)
            surf = pygame.image.load(full_path).convert_alpha()
            self.frames.append(surf)

    def animate(self, dt):
        self.frame_index = self.frame_index + 10 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)