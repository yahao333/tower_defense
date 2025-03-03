import pygame
from tower import Tower
from enemy import Enemy
from levels import LEVELS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.towers = []
        self.enemies = []
        self.money = 100
        self.lives = 20
        self.wave = 1
        self.current_level = LEVELS[1]  # 从第一关开始
        self.path = self.current_level['path']
        self.spawn_timer = 0
        self.enemies_spawned = 0
        
    def spawn_enemies(self):
        if self.spawn_timer <= 0 and self.enemies_spawned < self.current_level['enemies']:
            self.enemies.append(Enemy(
                pos=(-50, self.path[0][1]),
                health=self.current_level['enemy_health'],
                speed=self.current_level['enemy_speed']
            ))
            self.enemies_spawned += 1
            self.spawn_timer = self.current_level['spawn_interval']
        self.spawn_timer -= 1
    
    def update(self):
        self.attack_lines = []
        
        # 生成敌人
        self.spawn_enemies()
        
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
            target = tower.update(self.enemies)
            if target:
                self.attack_lines.append((tower.pos, (target.pos[0], target.pos[1])))
        
        # 检查是否需要进入下一关
        if not self.enemies and self.enemies_spawned >= self.current_level['enemies']:
            if self.wave < len(LEVELS):  # 检查是否还有下一关
                self.wave += 1
                # 清理当前关卡的内容
                self.towers = []
                self.enemies = []
                self.attack_lines = []
                self.money += 100
                
                # 加载新关卡
                self.current_level = LEVELS[self.wave]
                self.path = self.current_level['path']
                self.enemies_spawned = 0
                self.spawn_timer = 0
    
    def draw(self):
        # 绘制背景
        self.screen.fill((200, 255, 200))
        
        # 绘制路径和起终点
        for i in range(len(self.path) - 1):
            pygame.draw.line(self.screen, (150, 150, 150), 
                           self.path[i], self.path[i + 1], 40)
        
        # 只绘制当前关卡的起终点
        start_pos = self.current_level['path'][0]
        end_pos = self.current_level['path'][-1]
        pygame.draw.circle(self.screen, (0, 255, 0), start_pos, 25)  # 绿色起点
        pygame.draw.circle(self.screen, (255, 0, 0), end_pos, 25)    # 红色终点
        
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