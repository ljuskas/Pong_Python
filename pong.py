import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Velocidad del juego
FPS = 60
clock = pygame.time.Clock()

# Puntuaciones
winner_score = 2
left_score = 0
right_score = 0
font = pygame.font.SysFont(None, 36)

# Configuración de las paletas
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 10
left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Configuración de la pelota
BALL_SIZE = 20
ball_speed_x = 7
ball_speed_y = 7
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)

# Función para mover las paletas
def move_paddles(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

# Función para mover la pelota
def move_ball(ball, ball_speed_x, ball_speed_y, left_paddle, right_paddle):
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    if ball.left <= 0:
        # Puntuación para el jugador derecho
        global right_score
        right_score += 1
        reset_ball()
    elif ball.right >= WIDTH:
        # Puntuación para el jugador izquierdo
        global left_score
        left_score += 1
        reset_ball()

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

    return ball_speed_x, ball_speed_y

# Función para reiniciar la posición de la pelota
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= -1
    ball_speed_y *= -1
    
# Volvemos el juego a cero
def reset_game():
    global left_score, right_score, left_paddle, right_paddle, ball, ball_speed_x, ball_speed_y
    left_score = 0
    right_score = 0
    left_paddle = pygame.Rect(30, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 40, (HEIGHT - PADDLE_HEIGHT) // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_SIZE, BALL_SIZE)
    ball_speed_x = 7
    ball_speed_y = 7


# Define el tamaño de la fuente del texto del ganador
winner_font_size = 48
winner_font = pygame.font.SysFont(None, winner_font_size)

estados_juego = ['PLAY', 'PAUSED', 'GAME_OVER'] 
estado = estados_juego[0]
winner: str

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Presiona la tecla "p" para pausar o reanudar el juego
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if estado == estados_juego[0]:
                estado = estados_juego[1] # PAUSED
            else:
                estado = estados_juego[0] # PLAY
        elif event.type == pygame.KEYDOWN:
            if estado == estados_juego[2]:  # Solo restablecer el juego si está en GAME_OVER
                estado = estados_juego[0] # PLAY
                reset_game()

    if estado == estados_juego[0]:
        keys = pygame.key.get_pressed()
        move_paddles(keys, left_paddle, right_paddle)
        ball_speed_x, ball_speed_y = move_ball(ball, ball_speed_x, ball_speed_y, left_paddle, right_paddle)

        # Dibujar todo
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Mostrar puntajes
        left_score_text = font.render(f'Left: {left_score}', True, WHITE)
        right_score_text = font.render(f'Right: {right_score}', True, WHITE)
        screen.blit(left_score_text, (20, 20))
        screen.blit(right_score_text, (WIDTH - right_score_text.get_width() - 20, 20))

        # Verificar si hay un ganador
        if left_score == winner_score or right_score == winner_score:
            if left_score == winner_score:
                winner = "LEFT PLAYER"
            else: 
                winner = "RIGHT PLAYER"
            estado = estados_juego[2] #GAME OVER 

        pygame.display.flip()
        clock.tick(FPS)
        
    elif estado == estados_juego[1]:
        # Dibuja un mensaje de pausa en la pantalla
        pause_text = winner_font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
        pygame.display.flip()
        clock.tick(10)  # Limita la tasa de actualización para reducir el uso de CPU
        
    elif estado == estados_juego[2]:
        screen.fill(BLACK)
        winner_text = font.render(f'WINNER {winner}', True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
        pygame.display.flip()
        clock.tick(10)

