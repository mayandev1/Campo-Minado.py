import pygame
import random

# Configurações do jogo
GRID_SIZE = 10  # Redefinido para 10x10
CELL_SIZE = 40  # Tamanho de cada célula
NUM_BOMBAS = 15  # Quantidade de bombas

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE))
pygame.display.set_caption("Campo Minado")
font = pygame.font.Font(None, 36)

# Criar tabuleiro
board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Distribuir bombas
bomb_positions = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_BOMBAS)
for pos in bomb_positions:
    row, col = divmod(pos, GRID_SIZE)
    board[row][col] = -1

# Calcular números ao redor das bombas
def count_bombs(row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            r, c = row + i, col + j
            if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == -1:
                count += 1
    return count

for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        if board[row][col] == -1:
            continue
        board[row][col] = count_bombs(row, col)

# Revelar células recursivamente
def reveal_cells(row, col):
    if revealed[row][col] or flags[row][col]:
        return
    revealed[row][col] = True
    if board[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                r, c = row + i, col + j
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    reveal_cells(r, c)

def check_victory():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] != -1 and not revealed[row][col]:
                return False
    return True

# Loop principal
game_over = False
victory = False
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = y // CELL_SIZE, x // CELL_SIZE
            if event.button == 1:  # Clique esquerdo
                if board[row][col] == -1:
                    game_over = True
                else:
                    reveal_cells(row, col)
                if check_victory():
                    victory = True
                    game_over = True
            elif event.button == 3:  # Clique direito para bandeira
                flags[row][col] = not flags[row][col]
    
    # Desenhar tabuleiro
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREY, rect, 0 if revealed[row][col] else 1)
            if revealed[row][col]:
                if board[row][col] == -1:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 4)
                elif board[row][col] > 0:
                    text = font.render(str(board[row][col]), True, BLUE)
                    screen.blit(text, text.get_rect(center=rect.center))
            elif flags[row][col]:
                pygame.draw.polygon(screen, YELLOW, [(col * CELL_SIZE + 10, row * CELL_SIZE + 30),
                                                      (col * CELL_SIZE + 30, row * CELL_SIZE + 20),
                                                      (col * CELL_SIZE + 10, row * CELL_SIZE + 10)])
    
    if game_over:
        message = "Você venceu!" if victory else "Game Over!"
        text = font.render(message, True, GREEN if victory else RED)
        screen.blit(text, (GRID_SIZE * CELL_SIZE // 4, GRID_SIZE * CELL_SIZE // 2))
    
    pygame.display.flip()
pygame.quit()