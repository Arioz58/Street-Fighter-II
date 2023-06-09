import pygame as pg
from pygame.locals import *

from PARAMETRE import * #PARAMETRE est le fichier contenant toutes les constantes
from SF_ import *


pg.init()
pg.mixer.init()
#surface de la fenetre
f = pg.display.set_mode((RESOLUTION))

#Titre de la fenetre
pg.display.set_caption("Street Fighter")

#couleur
rouge = (255, 0, 0)
vert = (0, 255, 0)
bleu = (0, 0, 255)
blanc_mate = (200, 200, 200)
blanc = (255, 255, 255)
noir = (0, 0, 0)
jaune = (255, 255, 0)
marron = (175, 50, 0)

#init timer
timer = pg.time.Clock()

#init mixer
pg.mixer.init(44100, -16, 2, 2048)

#initialisation des instance Player/joueurs
player1 = Player(70,320,10,"right", 1)
player2 = Player(810, 320, 10, "left", 2)
            
def play():
    msecond = 0
    
    while True:
        pg.display.flip()

        f.fill(noir)
        timer.tick(FPS)
        # print(timer)

        msecond = msecond + 1
        supr = msecond // 24

        # on affiche nos personnages
        player1.display(f, player1.hitbox, player2)
        player2.display(f, player2.hitbox, player1)
        
        # on affiche
        player1.display_HUD(f)
        player2.display_HUD(f)

        # punch
        if player1.isPunch:
            player1.punch(player2, f)

        # cout de pieds
        if player1.isKick:
            player1.kick(player2, f)

        # Hadoken/projectile
        if player1.isHadoken:
            player1.launch_hadoken(player2, f)

        # saut
        if player1.isJump: # si saut
            player1.jump()

        #accroupis
        if player1.isCrouch:
            player1.crouch(bouton_appuyer)

        #pour ne pas sortir de l'ecran
        if player1.x + 200 > 1080 :#droite
            player1.x = 1080-200
        elif player1.x < 0: #gauche
            player1.x = 0

        #gestion des evenements
        for event in pg.event.get():
            if event.type == QUIT: #pour la crois de la fenetre
                pg.quit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    player1.isPunch = True
                if event.key == K_s:
                    player1.isKick = True

        bouton_appuyer = pg.key.get_pressed() #on recupere la touche appuyer
        if bouton_appuyer[K_ESCAPE]:
            pg.quit()
        player1.move(bouton_appuyer)
        if bouton_appuyer[K_DOWN]:
            player1.isCrouch = True
        if bouton_appuyer[K_UP]:
            player1.isJump = True
        if bouton_appuyer[K_d]:
            player1.isHadoken = True
        if bouton_appuyer[K_r]:
            player2.isParry = True
        else:
            player2.isParry = False
        # player2.isParry = True
        # print(bouton_appuyer)
play()
