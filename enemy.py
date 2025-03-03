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
        # 检查敌人是否到达最后一个路径点
        return self.path_index >= len(self.current_path) - 1
    
    def move(self, path):
        self.current_path = path  # 保存当前路径以供 reached_end 使用
        target = path[min(self.path_index + 1, len(path) - 1)]
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance < self.speed:
            self.path_index += 1
            if self.path_index >= len(path) - 1:
                return True  # 到达终点
        
        if distance != 0:
            self.pos[0] += (dx/distance) * self.speed
            self.pos[1] += (dy/distance) * self.speed
        
        return False  # 未到达终点
    
    def take_damage(self, damage):
        self.health -= damage
    
    def draw(self, screen):
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