from settings import *

class Bat(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.image = pygame.image.load(join('images', 'enemies', 'bat', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.last_spawn = pygame.time.get_ticks()
        self.spawn_time = 2000

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites

    def load_images(self):
        self.frames = []
        self.folder_path = join('images', 'enemies', 'bat')
        for file in range(4):
            name = f'{file}.png'
            full_path = join(self.folder_path, name)
            surf = pygame.image.load(full_path).convert_alpha()
            self.frames.append(surf)
            print(full_path)