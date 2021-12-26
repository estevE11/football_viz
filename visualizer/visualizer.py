import sys, pygame, json, glob, os
from renderer import Renderer

pygame.init()
size = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Football Visualizer")
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
renderer = Renderer(screen, padding=(10, 10, 10, 10))

history = json.loads(open("pts_history.json", "r").read())

matchday = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                matchday -= 1
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                matchday += 1

    screen.fill((72, 73, 77))

    renderer.renderChart(history[matchday])

    pygame.display.flip()

pygame.quit()