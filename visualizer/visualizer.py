import sys, pygame, json, glob, os
from renderer import Renderer

pygame.init()
size = 800, 740
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Football Visualizer")
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.

history = json.loads(open("pts_history.json", "r").read())
renderer = Renderer(screen, history, padding=(10, 40, 10, 10))

matchday = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                matchday -= 1
                if matchday < 0: matchday = 0
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                matchday += 1
                if matchday >= len(history): matchday = len(history)-1 
    screen.fill((72, 73, 77))

    renderer.update()
    renderer.renderChart(history[matchday])

    pygame.display.flip()

pygame.quit()