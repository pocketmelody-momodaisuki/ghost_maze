import pygame
import random
import sys
import heapq

# -----------------------------
# 設定
# -----------------------------
CELL_SIZE = 24
MAZE_WIDTH = 31
MAZE_HEIGHT = 21

SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE

COLOR_WALL = (30, 30, 60)
COLOR_PATH = (220, 220, 240)
COLOR_GOAL = (255, 180, 80)
COLOR_TEXT = (255, 255, 255)
COLOR_BG = (10, 10, 20)

# -----------------------------
# Prim法で迷路生成
# -----------------------------
def generate_maze(width, height):
    maze = [[0 for _ in range(width)] for _ in range(height)]

    start_x, start_y = 1, 1
    maze[start_y][start_x] = 1

    walls = []
    walls.append((start_x + 1, start_y))
    walls.append((start_x - 1, start_y))
    walls.append((start_x, start_y + 1))
    walls.append((start_x, start_y - 1))

    while walls:
        wx, wy = random.choice(walls)
        walls.remove((wx, wy))

        paths = 0
        if wx > 0 and maze[wy][wx - 1] == 1:
            paths += 1
        if wx < width - 1 and maze[wy][wx + 1] == 1:
            paths += 1
        if wy > 0 and maze[wy - 1][wx] == 1:
            paths += 1
        if wy < height - 1 and maze[wy + 1][wx] == 1:
            paths += 1

        if paths == 1:
            maze[wy][wx] = 1

            if wx + 1 < width - 1 and maze[wy][wx + 1] == 0:
                walls.append((wx + 1, wy))
            if wx - 1 > 0 and maze[wy][wx - 1] == 0:
                walls.append((wx - 1, wy))
            if wy + 1 < height - 1 and maze[wy + 1][wx] == 0:
                walls.append((wx, wy + 1))
            if wy - 1 > 0 and maze[wy - 1][wx] == 0:
                walls.append((wx, wy - 1))

    return maze

# -----------------------------
# 広場を追加する
# -----------------------------
def add_open_area(maze, width, height, size=5):
    x = random.randint(2, width - size - 2)
    y = random.randint(2, height - size - 2)

    for iy in range(y, y + size):
        for ix in range(x, x + size):
            maze[iy][ix] = 1

    return maze

# -----------------------------
# プレイヤー移動
# -----------------------------
def move_player(maze, player_pos, dx, dy):
    x, y = player_pos
    nx, ny = x + dx, y + dy
    if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
        if maze[ny][nx] == 1:
            return (nx, ny)
    return player_pos

# -----------------------------
# A* アルゴリズム
# -----------------------------
def astar(maze, start, goal):
    sx, sy = start
    gx, gy = goal

    open_list = []
    heapq.heappush(open_list, (0, (sx, sy)))

    came_from = {}
    cost = { (sx, sy): 0 }

    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    while open_list:
        _, current = heapq.heappop(open_list)
        cx, cy = current

        if current == goal:
            break

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
                if maze[ny][nx] == 1:
                    new_cost = cost[(cx, cy)] + 1

                    if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                        cost[(nx, ny)] = new_cost
                        priority = new_cost + abs(nx - gx) + abs(ny - gy)
                        heapq.heappush(open_list, (priority, (nx, ny)))
                        came_from[(nx, ny)] = (cx, cy)

    if (gx, gy) not in came_from:
        return start

    path = []
    current = (gx, gy)
    while current != (sx, sy):
        path.append(current)
        current = came_from[current]
    path.reverse()

    if len(path) > 0:
        return path[0]
    else:
        return start

# -----------------------------
# メイン
# -----------------------------
def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ghost Maze Escape - Sound Edition")

    ghost_imgs = [
        pygame.transform.scale(pygame.image.load("ghost_walk1.png").convert_alpha(), (CELL_SIZE, CELL_SIZE)),
        pygame.transform.scale(pygame.image.load("ghost_walk2.png").convert_alpha(), (CELL_SIZE, CELL_SIZE))
    ]

    enemy_img = pygame.transform.scale(
        pygame.image.load("enemy.png").convert_alpha(),
        (CELL_SIZE, CELL_SIZE)
    )

    # -----------------------------
    # 音読み込み
    # -----------------------------
    walk_sound = pygame.mixer.Sound("walk.wav")
    clear_sound = pygame.mixer.Sound("clear.wav")
    gameover_sound = pygame.mixer.Sound("gameover.wav")

    ghost_frame = 0
    ghost_anim_counter = 0

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)

    for _ in range(5):
        maze = add_open_area(maze, MAZE_WIDTH, MAZE_HEIGHT, size=5)

    player_pos = (1, 1)

    goal_pos = None
    for y in range(MAZE_HEIGHT - 2, 0, -1):
        for x in range(MAZE_WIDTH - 2, 0, -1):
            if maze[y][x] == 1:
                goal_pos = (x, y)
                break
        if goal_pos:
            break

    enemy_positions = []
    for _ in range(4):
        while True:
            x = random.randint(1, MAZE_WIDTH - 2)
            y = random.randint(1, MAZE_HEIGHT - 2)
            if maze[y][x] == 1 and (x, y) != player_pos and (x, y) != goal_pos:
                enemy_positions.append((x, y))
                break

    enemy_move_counter = 0
    enemy_move_interval = 18

    game_clear = False
    game_over = False

    # -------------------------
    # メインループ
    # -------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over and event.key == pygame.K_RETURN:
                    return main()

                if game_clear or game_over:
                    continue

                moved = False

                if event.key == pygame.K_UP:
                    new_pos = move_player(maze, player_pos, 0, -1)
                    moved = new_pos != player_pos
                    player_pos = new_pos
                elif event.key == pygame.K_DOWN:
                    new_pos = move_player(maze, player_pos, 0, 1)
                    moved = new_pos != player_pos
                    player_pos = new_pos
                elif event.key == pygame.K_LEFT:
                    new_pos = move_player(maze, player_pos, -1, 0)
                    moved = new_pos != player_pos
                    player_pos = new_pos
                elif event.key == pygame.K_RIGHT:
                    new_pos = move_player(maze, player_pos, 1, 0)
                    moved = new_pos != player_pos
                    player_pos = new_pos

                if moved:
                    walk_sound.play()
                    ghost_anim_counter += 1

        if player_pos == goal_pos:
            if not game_clear:
                clear_sound.play()
            game_clear = True

        for pos in enemy_positions:
            if pos == player_pos:
                if not game_over:
                    gameover_sound.play()
                game_over = True

        if not game_over and not game_clear:
            enemy_move_counter += 1
            if enemy_move_counter >= enemy_move_interval:
                for i in range(len(enemy_positions)):
                    enemy_positions[i] = astar(maze, enemy_positions[i], player_pos)
                enemy_move_counter = 0

        if ghost_anim_counter > 0:
            ghost_anim_counter = 0
            ghost_frame = (ghost_frame + 1) % len(ghost_imgs)

        screen.fill(COLOR_BG)

        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(screen, COLOR_PATH, rect)

        gx, gy = goal_pos
        pygame.draw.rect(screen, COLOR_GOAL, (gx * CELL_SIZE, gy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for ex, ey in enemy_positions:
            screen.blit(enemy_img, (ex * CELL_SIZE, ey * CELL_SIZE))

        px, py = player_pos
        screen.blit(ghost_imgs[ghost_frame], (px * CELL_SIZE, py * CELL_SIZE))

        if game_clear:
            text = font.render("CLEAR!", True, COLOR_TEXT)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))

        if game_over:
            text = font.render("GAME OVER", True, (255, 50, 50))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))

            retry_text = font.render("Press ENTER to Retry", True, COLOR_TEXT)
            screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
