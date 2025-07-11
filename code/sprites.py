from settings import *
from math import atan2, degrees
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):

    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        # player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(0,1)

        # sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos- player_pos).normalize()

    def rotate_gun(self):
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)
        

    def update(self, _, __):
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

class Bullet(pygame.sprite.Sprite):
    def __init__(self, surf, pos, direction, groups, collision_sprites):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20, -20)

        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 1000

        self.direction = direction
        self.speed =  1200
        self.collision_sprites = collision_sprites

    def collision(self):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                self.kill()

    def update(self, dt, _):
        self.collision()
        self.hitbox_rect.center += self.direction * self.speed * dt
        self.rect.center = self.hitbox_rect.center

        if pygame.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # randomizing the mob
        random = randint(1,3)
        if random == 1:
            self.mob = 'bat'
        elif random == 2:
            self.mob = 'blob'
        elif random == 3:
            self.mob = 'skeleton'

        # set up image
        self.frame_index = 0
        self.load_images()
        self.image = pygame.image.load(join('images', 'enemies', self.mob, '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -60)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 350
        self.collision_sprites = collision_sprites
        self.goal = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

    def load_images(self):
        self.frames = []
        self.folder_path = join('images', 'enemies', self.mob)
        for file in range(4):
            name = f'{file}.png'
            full_path = join(self.folder_path, name)
            surf = pygame.image.load(full_path).convert_alpha()
            self.frames.append(surf)
    
    def track(self, pos):
        self.direction.x = -self.rect.centerx + pos[0]
        self.direction.y = -self.rect.centery + pos[1]
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
    
    def animate(self, dt):
        self.frame_index = self.frame_index + 10 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt, pos):
        self.animate(dt)
        self.track(pos)
        self.move(dt)