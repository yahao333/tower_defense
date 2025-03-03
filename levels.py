LEVELS = {
    1: {
        'enemies': 5,
        'enemy_health': 100,
        'enemy_speed': 2,
        'spawn_interval': 50,  # 敌人生成间隔
        'path': [(0, 300), (800, 300)]
    },
    2: {
        'enemies': 8,
        'enemy_health': 150,
        'enemy_speed': 2.5,
        'spawn_interval': 40,
        'path': [(0, 200), (400, 200), (400, 400), (800, 400)]
    },
    3: {
        'enemies': 12,
        'enemy_health': 200,
        'enemy_speed': 3,
        'spawn_interval': 30,
        'path': [(0, 100), (200, 100), (200, 500), (600, 500), (600, 300), (800, 300)]
    }
}