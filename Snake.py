from pygame.locals import *
import random
import pygame as pg

# Definição das variáveis gerais
Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Screen_Height = 300
Screen_Width = 300
clock = pg.time.Clock()
score = 0

# Funções auxiliares
def grid_random():  # Define as posições aleatórias da maçã
    x = random.randint(0, 29)  # Dimensões da janela menos 1
    y = random.randint(0, 29)
    return (x * 10, y * 10)  # Dimensões totais da maçã


def collision(c1, c2):  # Detecta colisões da cobra e as maçãs
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


# Teclas para movimento
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
my_direction = LEFT


# Cobra
snake = [(180, 200), (190, 200), (200, 200)]  # Segmentos que formam a cobra
snake_skin = pg.Surface((10, 10))  # Tamanho e largura da superfície
snake_skin.fill((Green))  # Cor RGB verde

# Maçã
apple_pos = grid_random()  # Função abaixo
apple = pg.Surface((10, 10))
apple.fill(Red)

# Janela vazia
pg.init()  # Inicia uma janela
screen = pg.display.set_mode(
    (Screen_Height, Screen_Width)
)  # Define as dimensões dessa janela
pg.display.set_caption("Snake")  # Define o nome da janela
font = pg.font.Font("freesansbold.ttf", 18)  # Fonte do texto da pontuação
bite_sound = pg.mixer.Sound("Music/BITE.wav")
gameover_sound = pg.mixer.Sound("Music/Pacman.wav")
music = pg.mixer.music.load("Music/Music.wav")
pg.mixer.music.play(-1)

game_over = False  # Define o estado de game over
while not game_over:
    clock.tick(
        10
    )  # Reduz a velocidade do movimento da cobra, ajustando a framerate da janela

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:  # Definindo movimentos da cobra
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT
            if event.key == K_a:
                apple_pos = grid_random()
            if event.key == K_ESCAPE:
                game_over = True
                break

    if collision(snake[0], apple_pos):  # Cobra comeu a maçã
        apple_pos = grid_random()  # Nova posição da maçã
        snake.append((0, 0))  # Novo bloco adicionado a cobra
        score += 1  # Jogador ganha um ponto
        pg.mixer.Sound.play(bite_sound)  # Cobra morde a maçã
    # Determinando se a cobra colidiu com as bordas da janela
    if (
        snake[0][0] == Screen_Height
        or snake[0][1] == Screen_Width
        or snake[0][0] < 0
        or snake[0][1] < 0
    ):
        game_over = True
        break

    # Determinando se a cobra colidiu consigo mesma
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            game_over = True
    if game_over:
        break

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    if my_direction == UP:  # Movimentação da cobra
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((Black))  # Tela preta
    screen.blit(apple, apple_pos)  # Renderizando a maçã

    for x in range(0, Screen_Width, 10):
        pg.draw.line(
            screen, (40, 40, 40), (x, 0), (x, Screen_Width)
        )  # Desenhando linhas horizontais
    for y in range(0, Screen_Height, 10):
        pg.draw.line(
            screen, (40, 40, 40), (0, y), (Screen_Height, y)
        )  # Desenhando linhas verticais

    # Definindo pontuação do jogador
    score_font = font.render(f"Pontuação {score} ", True, (White))
    score_rect = score_font.get_rect()
    score_rect.topleft = (Screen_Height - 150, 10)
    screen.blit(score_font, score_rect)

    for pos in snake:
        screen.blit(snake_skin, pos)  # Renderizando a cobra

    pg.display.update()

while True:
    game_over_font = pg.font.Font("freesansbold.ttf", 30)
    game_over_screen = game_over_font.render("Game Over", True, (Red))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (Screen_Height / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pg.mixer.music.stop()
    pg.mixer.Sound.play(gameover_sound)
    pg.display.update()
    pg.time.wait(500)
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
