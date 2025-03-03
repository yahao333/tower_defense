import pygame
from tower import Tower
from enemy import Enemy

class Game:
    def spawn_enemies(self):
        for i in range(5):
            self.enemies.append(Enemy((-50 - i * 50, 300)))

    def __init__(self, screen):
        self.screen = screen
        self.towers = []
        self.enemies = []
        self.money = 100
        self.lives = 20
        self.wave = 1
        self.path = [(0, 300), (800, 300)]  # 简单的直线路径
        self.attack_lines = []
        
        # 初始化敌人
        self.spawn_enemies()
        
    def update(self):
        self.attack_lines = []  # 清空上一帧的攻击线条
        
        # 更新敌人
        for enemy in self.enemies[:]:
            enemy.move(self.path)
            if enemy.reached_end():
                self.enemies.remove(enemy)
                self.lives -= 1
            elif enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += 10
        
        # 更新防御塔
        for tower in self.towers:
            target = tower.update(self.enemies)  # 获取攻击目标
            if target:  # 如果有攻击目标，记录攻击线条
                self.attack_lines.append((tower.pos, (target.pos[0], target.pos[1])))
        
        # 检查是否需要生成新的一波敌人
        if not self.enemies:
            self.wave += 1
            self.spawn_enemies()
    
    def draw(self):
        # 绘制背景
        self.screen.fill((200, 255, 200))
        
        # 绘制路径
        pygame.draw.line(self.screen, (150, 150, 150), self.path[0], self.path[1], 40)
        
        # 绘制防御塔
        for tower in self.towers:
            tower.draw(self.screen)
        
        # 绘制攻击线条
        for start, end in self.attack_lines:
            pygame.draw.line(self.screen, (255, 255, 0), start, end, 2)
        
        # 绘制敌人
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # 绘制UI
        font = pygame.font.Font(None, 36)
        money_text = font.render(f"Money: {self.money}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        wave_text = font.render(f"Wave: {self.wave}", True, (0, 0, 0))
        
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(wave_text, (10, 90))

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click
                pos = pygame.mouse.get_pos()
                if self.money >= 50:  # Check if enough money
                    self.towers.append(Tower(pos))
                    self.money -= 50