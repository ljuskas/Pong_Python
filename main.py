import pygame
import pygame_menu
import sys
from PongGame import PongGame

pygame.init()

# Configuración del menú
def start_the_game():
    pong_game.estado = 'PLAY'
    menu.disable()

pong_game = PongGame(800, 600)

menu = pygame_menu.Menu('Bienvenido', pong_game.WIDTH, pong_game.HEIGHT, theme=pygame_menu.themes.THEME_DARK)
menu.add.button('Jugar', start_the_game)
menu.add.button('Salir', pygame_menu.events.EXIT)

play = True

while play:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            if pong_game.estado == 'PLAY':
                pong_game.estado = 'PAUSED'
            elif pong_game.estado == 'PAUSED':
                pong_game.estado = 'PLAY'
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
        elif pong_game.estado == 'PAUSED':
            pong_game.draw_paused()
            pygame.display.flip()
            pong_game.clock.tick(10)
        elif pong_game.estado == 'GAME_OVER':
            pong_game.draw_game_over()
            pygame.display.flip()
            pong_game.clock.tick(10)
