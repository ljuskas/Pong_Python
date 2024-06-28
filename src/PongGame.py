import pygame
import time

class PongGame:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('PONG PY')
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        
        self.winner_score = 10
        self.left_score = 0
        self.right_score = 0
        self.score_checker= 1
        self.speed_incremen = 0.1
        self.font = pygame.font.SysFont(None, 36)
        
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 10, 100
        self.paddle_speed = 10
        self.left_paddle = pygame.Rect(30, (self.HEIGHT - self.PADDLE_HEIGHT) // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.right_paddle = pygame.Rect(self.WIDTH - 40, (self.HEIGHT - self.PADDLE_HEIGHT) // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        
        self.BALL_SIZE = 20
        self.ball_speed_x = 7
        self.ball_speed_y = 7
        self.ball = pygame.Rect(self.WIDTH // 2, self.HEIGHT // 2, self.BALL_SIZE, self.BALL_SIZE)
        
        self.winner_font_size = 48
        self.winner_font = pygame.font.SysFont(None, self.winner_font_size)
        
        self.info_font_size = 24
        self.info_font  = pygame.font.SysFont(None, self.info_font_size)
        
        self.estado     = 'MENU'
        self.players    = 1
        self.winner     = None
        self.hits       = 0
        self.countdown   = 2
        self.auto_paddle_speed = 6.5
        self.last_time = pygame.time.get_ticks()
        self.joystick = None
        

    def move_paddles(self, keys):
        if(self.players == 2):
            self.move_paddles_2p(keys)
        elif(self.players == 1):
            self.move_paddle_1p(keys)

    def move_joystick_paddle_1p(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:  
                    print("Botón 1 presionado!")
                    self.right_paddle.y -= self.paddle_speed 
                elif event.button == 2:  
                    print("Botón 3 presionado!")
                    self.right_paddle.y += self.paddle_speed 
            
    def move_paddle_1p(self, keys):
        self.move_automatic_paddle()
        if keys[pygame.K_UP] and self.right_paddle.top > 0:
            self.right_paddle.y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.right_paddle.bottom < self.HEIGHT:
            self.right_paddle.y += self.paddle_speed
    
    def move_paddles_2p(self, keys):
            if keys[pygame.K_w] and self.left_paddle.top > 0:
                self.left_paddle.y -= self.paddle_speed
            if keys[pygame.K_s] and self.left_paddle.bottom < self.HEIGHT:
                self.left_paddle.y += self.paddle_speed
            if keys[pygame.K_UP] and self.right_paddle.top > 0:
                self.right_paddle.y -= self.paddle_speed
            if keys[pygame.K_DOWN] and self.right_paddle.bottom < self.HEIGHT:
                self.right_paddle.y += self.paddle_speed
    
    def move_automatic_paddle(self):
        if self.ball.centery < self.left_paddle.centery:
            self.left_paddle.y -= self.auto_paddle_speed
        elif self.ball.centery > self.left_paddle.centery:
            self.left_paddle.y += self.auto_paddle_speed
        self.left_paddle.y = max(self.left_paddle.y, 0) 
        self.left_paddle.y = min(self.left_paddle.y, self.HEIGHT - self.left_paddle.height)  
    
    def move_ball(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.ball_speed_y = -self.ball_speed_y

        if self.ball.left <= 0:
            self.right_score += 1
            self.score_checker += 1
            self.estado = 'COUNTDOWN'
            self.reset_ball()
        elif self.ball.right >= self.WIDTH:
            self.left_score += 1
            self.score_checker += 1
            self.estado = 'COUNTDOWN'
            self.reset_ball()

        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.hits += 1
            print("Hits!", self.hits)
            self.ball_speed_x = -self.ball_speed_x
        
        self.check_score()
        
    def check_hits(self):
        if self.hits == 4:
            print(f"Incrementamos velocidad (x hit): X={self.ball_speed_x}, Y={self.ball_speed_y}")
            self.ball_speed_x = self._increase_speed(self.ball_speed_x)
            self.ball_speed_y = self._increase_speed(self.ball_speed_y)
            self.hits = 0
            
    def check_score(self):
        if self.score_checker % 2 == 0:
            self.score_checker = 1
            print(f"Incrementamos velocidad (x score): X={self.ball_speed_x}, Y={self.ball_speed_y}")
            self.ball_speed_x = self._increase_speed(self.ball_speed_x)
            self.ball_speed_y = self._increase_speed(self.ball_speed_y)

    def _increase_speed(self, speed):
        if speed > 0:
            return speed + self.speed_incremen
        else:
            return speed - self.speed_incremen
        
    def reset_ball(self):
        self.ball.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.ball_speed_x *= -1
        self.ball_speed_y *= -1

    def reset_game(self):
        self.left_score = 0
        self.right_score = 0
        self.left_paddle = pygame.Rect(30, (self.HEIGHT - self.PADDLE_HEIGHT) // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.right_paddle = pygame.Rect(self.WIDTH - 40, (self.HEIGHT - self.PADDLE_HEIGHT) // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = pygame.Rect(self.WIDTH // 2, self.HEIGHT // 2, self.BALL_SIZE, self.BALL_SIZE)
        self.ball_speed_x = 7
        self.ball_speed_y = 7

    def draw_game(self):
        self.screen.fill(self.BLACK)
        pygame.draw.rect(self.screen, self.WHITE, self.left_paddle)
        pygame.draw.rect(self.screen, self.WHITE, self.right_paddle)
        pygame.draw.ellipse(self.screen, self.WHITE, self.ball)
        pygame.draw.aaline(self.screen, self.WHITE, (self.WIDTH // 2, 0), (self.WIDTH // 2, self.HEIGHT))
        left_score_text = self.font.render(f'Left: {self.left_score}', True, self.WHITE)
        right_score_text = self.font.render(f'Right: {self.right_score}', True, self.WHITE)
        self.screen.blit(left_score_text, (20, 20))
        self.screen.blit(right_score_text, (self.WIDTH - right_score_text.get_width() - 20, 20))

    def check_winner(self):
        if self.left_score == self.winner_score or self.right_score == self.winner_score:
            self.winner = "LEFT PLAYER" if self.left_score == self.winner_score else "RIGHT PLAYER"
            self.estado = 'GAME_OVER'

    def draw_paused(self):
        pause_text = self.winner_font.render("PAUSED", True, self.WHITE)
        self.screen.blit(pause_text, (self.WIDTH // 2 - pause_text.get_width() // 2, self.HEIGHT // 2 - pause_text.get_height() // 2))

    def draw_countdown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:  
            self.countdown -= 1
            self.last_time = current_time

        mins, secs = divmod(self.countdown, 60)  
        countdown_text = self.font.render(f'Atentos...', True, self.WHITE)
        if(self.countdown != 0):
            self.screen.fill(self.BLACK)
            self.screen.blit(countdown_text, (self.WIDTH // 2 - countdown_text.get_width() // 2, self.HEIGHT // 2 - countdown_text.get_height() // 2))
        if self.countdown == 0:
            self.screen.fill(self.BLACK)
            go_text= self.font.render('¡YA!', True, self.WHITE)
            self.screen.blit(go_text, (self.WIDTH // 2 - go_text.get_width() // 2, self.HEIGHT // 2 - go_text.get_height() // 2))
            self.estado = 'PLAY'
            self.countdown = 2
        
    def draw_game_over(self):
        self.screen.fill(self.BLACK)
        winner_text = self.font.render(f'WINNER {self.winner}', True, self.WHITE)
        info_text = self.font.render('Presion tecla "r" para reiniciar o "x" para cerrar', True, self.WHITE)
        self.screen.blit(winner_text, (self.WIDTH // 2 - winner_text.get_width() // 2, self.HEIGHT // 2.5 - winner_text.get_height() // 2))
        self.screen.blit(info_text, (self.WIDTH // 3 - winner_text.get_width() // 2, self.HEIGHT // 2 - winner_text.get_height() // 2))
        

    def update(self):
        keys = pygame.key.get_pressed()
        self.move_paddles(keys)
        self.move_ball()
        self.draw_game()
        self.check_winner()
        self.check_hits()
        pygame.display.flip()
        self.clock.tick(self.FPS)
