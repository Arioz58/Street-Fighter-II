import pygame as pg
pg.init()
debut = pg.time.get_ticks()
for i in range(4):
    print(str(debut)+ "-"+str(pg.time.get_ticks()))
    print(pg.time.get_ticks()- debut)