import pygame as pg
from pygame.locals import *

class Player():
    """on créer une classe player avec tous les attribut d'un joueur
    x est la coordonnée x du joueuer
    y est la coordonnée y du joueuer
    force est les degats qu'il vas donner
    """
    def __init__(self, x, y, force, orientation ):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.force = force
        self.vie = 300

    def frape(self, p2):
        """enleve des degats du joueur p1 au joueur p2"""
        p2.vie -= self.force

    def move(self, get_pressed):
        """
        bouge le joueur sur l'axe x,
        attend en argument le bouton appuyer get_pressed
        """
        x_vel = 0.65
        if get_pressed[K_RIGHT]:
            self.x += x_vel
        if get_pressed[K_LEFT]:
            self.x -= x_vel
    
    def saut(self,jump):
        """
        bouge le joueur sur l'axe y pour sauter
        attend en argument un booléen jump
        """
        y_vel = 1
        if jump:
            self.y -= y_vel
            y_vel -= 1
            if y_vel == 0:
                jump = False
                y_vel = 1

    def crouche(self, get_pressed):
        """
        on reduit la hitbox du personnage et le personnage s'accroupis
        """
        y_vel = 0.65
        if get_pressed[K_DOWN]:
            self.y += y_vel

    