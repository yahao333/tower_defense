import pygame
import math

class Tower:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 20
        self.range = 150
        self.damage = 80
        self.cooldown = 30
        self.cooldown_timer = 0
    
    def update(self, enemies):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
            return None
            
        # 寻找最近的敌人
        closest_enemy = None
        min_dist = float('inf')
        
        for enemy in enemies:
            dist = math.sqrt((enemy.pos[0] - self.pos[0])**2 + 
                           (enemy.pos[1] - self.pos[1])**2)
            if dist < self.range and dist < min_dist:
                closest_enemy = enemy
                min_dist = dist
        
        # 攻击敌人
        if closest_enemy:
            closest_enemy.take_damage(self.damage)
            self.cooldown_timer = self.cooldown
            return closest_enemy  # 返回攻击目标
        
        return None
    
    def draw(self, screen):
        pygame.draw.circle(screen, (100, 100, 255), self.pos, self.radius)
        # 绘制攻击范围（半透明）
        range_surface = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA)
        pygame.draw.circle(range_surface, (100, 100, 255, 50), 
                         (self.range, self.range), self.range)
        screen.blit(range_surface, 
                   (self.pos[0] - self.range, self.pos[1] - self.range))