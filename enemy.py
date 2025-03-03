import pygame
import math

class Enemy:
    def __init__(self, pos, health=100, speed=2):
        self.pos = list(pos)
        self.speed = speed
        self.health = health
        self.max_health = health
        self.radius = 15
        self.path_index = 0
    
    def reached_end(self):
        # 修改判断条件：当敌人到达路径终点时返回True
        return self.path_index >= 1 and self.pos[0] >= 800
    
    def move(self, path):
        target = path[min(self.path_index + 1, len(path) - 1)]
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(path) - 1:
                return
        
        if distance != 0:
            self.pos[0] += (dx/distance) * self.speed
            self.pos[1] += (dy/distance) * self.speed
    
    def take_damage(self, damage):
        self.health -= damage
    
    def draw(self, screen):
        # 绘制起点和终点
        start_pos = (0, 300)
        end_pos = (800, 300)
        pygame.draw.circle(screen, (0, 255, 0), start_pos, 25)  # 绿色起点
        pygame.draw.circle(screen, (255, 0, 0), end_pos, 25)    # 红色终点
        
        # 绘制敌人
        pygame.draw.circle(screen, (255, 0, 0), 
                         (int(self.pos[0]), int(self.pos[1])), self.radius)
        
        # 绘制血条
        health_ratio = self.health / self.max_health
        health_bar_length = 30
        health_bar_height = 5
        health_bar_pos = (int(self.pos[0] - health_bar_length/2),
                         int(self.pos[1] - self.radius - 10))
        
        pygame.draw.rect(screen, (255, 0, 0),
                        (*health_bar_pos, health_bar_length, health_bar_height))
        pygame.draw.rect(screen, (0, 255, 0),
                        (*health_bar_pos, health_bar_length * health_ratio, 
                         health_bar_height))