import random
from typing import Any, Dict, List, Tuple

import pygame

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [BLACK, WHITE, GRAY, RED, GREEN, BLUE]

# Dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

# Initialize Pygame
pygame.init()

font = pygame.font.SysFont(None, 25)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Tetris")

# Define the shapes of the blocks: Zero means the part does not exist
SHAPE_I = [[1, 1, 1, 1]]
SHAPE_J = [[1, 1, 1], [0, 0, 1]]
SHAPE_L = [[1, 1, 1], [1, 0, 0]]
SHAPE_O = [[1, 1], [1, 1]]
SHAPE_S = [[0, 1, 1], [1, 1, 0]]
SHAPE_T = [[1, 1, 1], [0, 1, 0]]
SHAPE_Z = [[1, 1, 0], [0, 1, 1]]
SHAPES = [SHAPE_I, SHAPE_J, SHAPE_L, SHAPE_O, SHAPE_S, SHAPE_T, SHAPE_Z]


def draw_screen(grid, block, level, score):
    screen.fill(BLACK)
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col:
                rect = pygame.Rect(
                    x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                )
                pygame.draw.rect(screen, COLORS[col], rect)
    draw_block(block)
    pygame.draw.rect(
        screen, WHITE, pygame.Rect(SCREEN_WIDTH - 100, 0, 100, SCREEN_HEIGHT)
    )
    level_text = font.render(f"Level: {level}", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(level_text, (SCREEN_WIDTH - 90, 10))
    screen.blit(score_text, (SCREEN_WIDTH - 90, 50))


def draw_block(block):
    for y, row in enumerate(block["shape"]):
        for x, col in enumerate(row):
            if col:
                rect = pygame.Rect(
                    (block["x"] + x) * BLOCK_SIZE,
                    (block["y"] + y) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE,
                )
                pygame.draw.rect(screen, COLORS[block["color"]], rect)


def new_block():
    shape = random.choice(SHAPES)
    color = random.randint(1, len(COLORS) - 1)
    block = {
        "shape": shape,
        "color": color,
        "x": int(GRID_WIDTH / 2) - int(len(shape[0]) / 2),
        "y": 0,
    }
    return block


def is_out_of_bounds(grid: List[List[int]], block: Dict[str, Any]) -> bool:
    for y, row in enumerate(block["shape"]):
        for x, col in enumerate(row):
            if not col:
                continue
            if block["y"] + y < 0:
                return True
            if len(grid) <= block["y"] + y:
                return True
            if len(grid[block["y"] + y]) <= block["x"] + x:
                return True
            if block["x"] + x < 0:
                return True
    return False


def has_colission(grid: List[List[int]], block: Dict[str, Any]) -> bool:
    return any(
        [
            grid[block["y"] + y][block["x"] + x]
            for y, row in enumerate(block["shape"])
            for x, col in enumerate(row)
            if col
        ]
    )


def write_block_to_grid(grid: List[List[int]], block: Dict[str, Any]):
    for y, row in enumerate(block["shape"]):
        for x, col in enumerate(row):
            if col:
                grid[block["y"] + y][block["x"] + x] = block["color"]
    return grid


def clear_completed_rows(
    grid: List[List[int]], score: int
) -> Tuple[List[List[int]], int]:
    for y, row in enumerate(grid):
        if all(row):
            grid.pop(y)
            grid.insert(0, [0 for x in range(GRID_WIDTH)])
            score += 100
    return grid, score


def rotate_block(block, direction):
    new_shape = [
        [block["shape"][y][x] for y in range(len(block["shape"]))]
        for x in range(len(block["shape"][0]))
    ]
    if direction == "clockwise":
        new_shape.reverse()
    else:
        for row in new_shape:
            row.reverse()
    if not any(
        [
            grid[block["y"] + y][block["x"] + x]
            for y, row in enumerate(new_shape)
            for x, col in enumerate(row)
            if col
        ]
    ):
        block["shape"] = new_shape
    return block


def is_gameover(grid) -> bool:
    return any(grid[0])


# Define the grid
grid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

# Define the game loop
game_over = False
score = 0
level = 1
block = new_block()
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN or pygame.key.get_pressed():
            if event.type == pygame.KEYDOWN:
                keys = [event.key]
            else:
                keys = pygame.key.get_pressed()
                if pygame.K_SPACE in keys:
                    continue
            if pygame.K_LEFT in keys:
                block["x"] -= 1
                if is_out_of_bounds(grid, block) or has_colission(grid, block):
                    block["x"] += 1
            elif pygame.K_RIGHT in keys:
                block["x"] += 1
                if is_out_of_bounds(grid, block) or has_colission(grid, block):
                    block["x"] -= 1
            elif pygame.K_UP in keys:
                block = rotate_block(block, "clockwise")
            elif pygame.K_DOWN in keys:
                block["y"] += 1
                if is_out_of_bounds(grid, block) or has_colission(grid, block):
                    block["y"] -= 1
            elif pygame.K_SPACE in keys:
                while not is_out_of_bounds(grid, block) and not has_colission(
                    grid, block
                ):
                    block["y"] += 1
                block["y"] -= 1
                grid = write_block_to_grid(grid, block)
                if is_gameover(grid):
                    game_over = True
                block = new_block()
                score += 10

    # Move the block down
    block["y"] += 1
    if is_out_of_bounds(grid, block) or has_colission(grid, block):
        block["y"] -= 1
        grid = write_block_to_grid(grid, block)
        if is_gameover(grid):
            game_over = True
        block = new_block()
        score += 10

    grid, score = clear_completed_rows(grid, score)
    level = score // 1000 + 1

    draw_screen(grid, block, level, score)
    pygame.display.flip()
    clock.tick(3 * level)

print(f"Final Score: {score} (level {level})")
