from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.down_frames = [pygame.image.load(join('images', 'player', 'down', f'{i}.png')).convert_alpha() for i in range(4)]
        self.left_frames = [pygame.image.load(join('images', 'player', 'left', f'{i}.png')).convert_alpha() for i in range(4)]
        self.right_frames = [pygame.image.load(join('images', 'player', 'right', f'{i}.png')).convert_alpha() for i in range(4)]
        self.up_frames = [pygame.image.load(join('images', 'player', 'up', f'{i}.png')).convert_alpha() for i in range(4)]

        self.left_index, self.right_index, self.down_index, self.up_index = 0, 0, 0, 0

        self.image = self.down_frames[self.down_index]
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.direction = pygame.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.animate_speed = 201

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
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
        if self.direction.x > 0: 
            self.right_index += int(self.animate_speed * dt)
            self.image = self.right_frames[self.right_index % 4]
        elif self.direction.x < 0:
            self.left_index += int(self.animate_speed * dt)
            self.image = self.left_frames[self.left_index % 4]
        elif self.direction.y > 0:
            self.down_index += int(self.animate_speed * dt)
            self.image = self.down_frames[self.down_index % 4]
        elif self.direction.y < 0:
            self.up_index += int(self.animate_speed * dt)
            self.image = self.up_frames[self.up_index % 4]

                
    def update (self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)