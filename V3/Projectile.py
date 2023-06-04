import pygame as pg
from pygame.locals import *
import os

from SF_ import *

class Projectile():

    def __init__(self, orientation, x, y):
        self.x = x # coordonneés x
        self.y = y # coordonneés y
        self.reached_target = False # bool si on atteint notre cible
        self.orientation = orientation # orientation du projectile
        self.projectile_hb = pg.Rect(self.x, self.y, 100, 100) # hb
        self.damage = 20 # degat
        self.spriteCount = 0
        self.sprite = [] # image

    def launch_projectile(self, win):
        if self.orientation == "right":
            speed = 30
        elif self.orientation == "left":
            speed = -30
        self.projectile_hb.x += speed
        pg.draw.rect(win, (255,0,0), self.projectile_hb, 5)

    def display_projectile(self, win, projectile_rect):
        for file_name in os.listdir(f"V3/projectile_sprite_sheets/Hadoken"):
            self.sprite.append(pg.image.load(f"V3/projectile_sprite_sheets/Hadoken/{file_name}"))
        
        self.spriteCount += 0.40
        if self.spriteCount >= len(self.sprite):
            self.spriteCount = 0
        sprite = self.sprite[int(self.spriteCount)]
        if self.orientation == "right":
            sprite = pg.transform.scale(sprite, (sprite.get_width()*4, sprite.get_height()*4))
            win.blit(sprite, self.projectile_hb)
