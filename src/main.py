import pygame
import pygame_menu
import sys
from PongGame import PongGame

pygame.init()


# Configuración del menú
def start_the_game():
    pong_game.joystick  = initialize_joystick()
    pong_game.estado = 'PLAY'
    print("Inicia juego con ", pong_game.players, " jugador/es")
    menu.disable()

# Función para actualizar la cantidad de jugadores
def set_players(value, number):
    pong_game.players = number
    
# Función para detectar si existe un joystick conectado
def initialize_joystick():
    if pygame.joystick.get_count() == 0:
        return False
    else:
        print("Joystick detectados : " + str(pygame.joystick.get_count()))
        pong_game.joystick = pygame.joystick # Obtén el primer joystick disponible
        pong_game.joystick.init()
        
pong_game = PongGame(800, 600)

menu = pygame_menu.Menu('Bienvenido', pong_game.WIDTH, pong_game.HEIGHT, theme=pygame_menu.themes.THEME_DARK)
selector = menu.add.selector('Cant. Jugadores: ', [('Un jugador', 1), ('Dos jugadores', 2)], onchange=set_players)
menu.add.button('Jugar', start_the_game)
menu.add.button('Salir', pygame_menu.events.EXIT)

def check_estado():
    if pong_game.estado == 'PLAY':
        pong_game.estado = 'PAUSED'
    elif pong_game.estado == 'PAUSED':
        pong_game.estado = 'PLAY'
        
play = True

while play:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            check_estado()
        elif event.type == pygame.JOYBUTTONDOWN:
            print(event.bnutton)
        elif pong_game.estado == 'GAME_OVER' and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pong_game.estado = 'PLAY'
            pong_game.reset_game()
        elif pong_game.estado == 'GAME_OVER' and event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            play = False

    if pong_game.estado == 'MENU':
        menu.draw(pong_game.screen)
        menu.update(events)
        pygame.display.flip()
    else:
        if pong_game.estado == 'PLAY':
            pong_game.update()
        elif pong_game.estado == 'COUNTDOWN':
            pong_game.draw_countdown()
            pygame.display.flip()
            pong_game.clock.tick(10)
        elif pong_game.estado == 'PAUSED':
            pong_game.draw_paused()
            pygame.display.flip()
            pong_game.clock.tick(10)
        elif pong_game.estado == 'GAME_OVER':
            pong_game.draw_game_over()
            pygame.display.flip()
            pong_game.clock.tick(10)
