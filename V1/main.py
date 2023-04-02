import pygame as pg
from pygame.locals import *
from SF_ import *
from PARAMETRE import *

pg.init()

f = pg.display.set_mode((RESOLUTION
))
pg.display.set_caption("Street Fighter")
timer = pg.time.Clock()

player1 = Player(0,0/2,10,"Droite")

jump = False
y_vel = 5
while True:

    pg.display.flip()

    timer.tick(FPS)

    f.fill((0,0,0))

    perso = pg.Rect(player1.x, player1.y, 100, 200)

    obstacles = [pg.Rect(0,700,1080,20)]
    
    for elem in obstacles:
        pg.draw.rect(f, (200,200,200), elem)
    
    if perso.collidelist(obstacles) != -1:
        player1.y = obstacles[perso.collidelist(obstacles)].y - 200

    if perso.collidelist(obstacles) == -1:
        player1.y += GRAVITY

    pg.draw.rect(f,(255,255,255), perso)

    

    #pour ne pas sortir de l'ecran
    if player1.x + 100 > 1080 :#droite
        player1.x = 1080-100
    elif player1.x < 0: #gauche
        player1.x = 0

    #gestion des evenements
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()

    bouton_appuyer = pg.key.get_pressed()
    if bouton_appuyer[K_ESCAPE]:
        pg.quit()
    if bouton_appuyer[K_RIGHT] or bouton_appuyer[K_LEFT]:
        player1.move(bouton_appuyer)
    if bouton_appuyer[K_DOWN]:
        player1.crouche(bouton_appuyer)
    if bouton_appuyer[K_UP]:
        jump = True
        player1.saut(jump)
        
