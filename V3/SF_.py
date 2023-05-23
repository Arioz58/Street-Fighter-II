import pygame as pg
from pygame.locals import *
import os

pg.mixer.init()
class Player():
    """on créer une classe player avec tous les attribut d'un joueur
    x est la coordonnée x du joueuer
    y est la coordonnée y du joueuer
    force est les degats qu'il vas donner
    """
    def __init__(self, x, y, force, orientation, player_num = None):
        self.x = x
        self.y = y
        self.orientation = orientation # orientation du presonnage
        self.force = force # puissance de frappe de notre personnage qui varie en fonction du personnage choisie
        self.pv = 400 # les Points de Vie de notre personnage
        self.height = 350 # hauteur de notre personnage
        self.width = 200 # largeur de notre personnage
        self.player_num = player_num # initalement None
        self.idleCount = 0 
        self.walkCount = 0 #permet d'animé
        self.jumpCount = 0 #permet d'animé
        self.punchCount = 0 #permet d'animé
        self.hadokenCount = 0 #permet d'animé
        self.isMoving = False # si le joueur bouge
        self.isPunch = False #cout de poing booléen
        self.isKick = False # coute de pied booléen
        self.isCrouch = False # accroupis booléen
        self.isJump = False # saut booléen
        self.isFalling = False # si on tombe apres un coup
        self.isHadoken = False # si on lance une boule de feu
        self.isTouched = False # si on est toucher
        self.isparry = False # si on parre une attack
        self.jump_height = 10 # hauteur max du saut de notre personnage
        self.sprites = {"idle": [], "punch": [], "hit": [], "jump": [], "walk": [], "kick": [], "launch": []}
        for dire in os.listdir("V3/sprite_sheet"): #on charge toutes les images dont on a besoin
            for dire_ in os.listdir(f"V3/sprite_sheet/{dire}"):
                for file_name in os.listdir(f"V3/sprite_sheet/{dire}/{dire_}"):
                    self.sprites[str(dire)].append(pg.image.load(f"V3/sprite_sheet/{dire}/{dire_}/{file_name}"))
        self.hitbox = pg.Rect(self.x, self.y, 200, 350) #on recupere la taille de notre image et on l'appelle hitbox car pygame gere les hitbox/colisions avec les Rect
        self.hitbox.x = self.x # permet de mettre les personnages aux bons endroits (car sinon (0,0))
        self.hitbox.y = self.y # permet de mettre les personnages aux bons endroits (car sinon (0,0))
        self.punch_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery - 130, 30,60)
        self.hadoken = Projectile("right", self.hitbox.centerx, self.hitbox.centery)
        self.somme_decalage = 0

    def punch(self, p2, win):
        """enleve des degats du joueur p1 au joueur p2
        si la hitbox du coup de p1 touche la hitbox du joueur p2
        p2 : joueur adversaire instance Player
        win : las surface sur le quelle on affiche le rectangle
        """
        if self.isKick == False: #si on ne fait pas deja un coup de pied
            if self.orientation == "right": # si on regarde a droite alors la hb du poing pointe a droite
                self.punch_hb.x, self.punch_hb.y = self.hitbox.centerx, self.hitbox.centery - 130
                pg.draw.rect(win, (255,0,0), self.punch_hb, 5) #on dessine pour visualiser (a enlever une fois que le personnage sera afficher)
                if self.punch_hb.width <= 150: # si le coup n'a pas atteint sa longeur max
                    self.isPunch = True # on lance le coup
                    self.punch_hb.width += 30 # on agrandi la hb du coup
                if self.punch_hb.width > 150: # si le coup depasse le longeur max
                    self.isPunch = False # on arrete le coup
                    self.punch_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery - 130, 30,60) # on reinit la hb du coup
                if self.punch_hb.colliderect(p2.hitbox): #si la hb du coup touche la hb du joueur adverse
                    if p2.pv > 0: #si sa vie est > 0
                        p2.pv -= self.force #alors on lui enleve de la vie
                        p2.isTouched = True
                        p2.hitbox.x += 20 # on fait reculer l'adversaire
                        self.isPunch = False # on reinit
                        self.punch_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery - 130, 30,60)# on reinit
            if self.orientation == "left":# si on regarde a droite alors la hb du poing pointe a gauche
                self.isPunch = True
                self.punch_hb.x, self.punch_hb.y = self.hitbox.centerx - self.somme_decalage - 20, self.hitbox.centery - 100
                pg.draw.rect(win, (0,0,255), self.punch_hb,5)
                if self.punch_hb.width <= 150:
                    self.isPunch = True
                    self.punch_hb.width += 30
                    self.somme_decalage += 30
                    if self.somme_decalage == 150:
                        self.somme_decalage = 0
                if self.punch_hb.width > 150:
                    self.isPunch = False
                    self.punch_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery - 130, 30,60) # on reinit la hb du coup
                if self.punch_hb.colliderect(p2.hitbox): #si la hb du coup touche la hb du joueur adverse
                    if p2.pv > 0: #si sa vie est > 0
                        p2.pv -= self.force #alors on lui enleve de la vie
                        p2.isTouched = True
                        p2.hitbox.x -= 20 # on fait reculer l'adversaire
                        self.isPunch = False # on reinit
                        self.punch_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery - 130, 30,60)# on reinit

    def kick(self, p2, win):
        """enleve des degats du joueur p1 au joueur p2
        si la hitbox du coup de p1 touche la hitbox du joueur p2
        p2 : joueur adversaire instance Player
        win : las surface sur le quelle on affiche le rectangle
        """
        if not self.isPunch and not self.isMoving: # si on ne fait pas deja un coup de poing
            if self.isCrouch: # si on est accroupie
                if self.orientation == "right":
                    self.isKick = True
                    kick_hb = pg.Rect(self.hitbox.centerx, self.hitbox.centery , 200, 100) #la hb du coup de pied
                    pg.draw.rect(win, (255,0,0), kick_hb,5) # on affiche cette HB
                    if kick_hb.colliderect(p2.hitbox): # si il y a collision
                        if p2.pv > 0: # et que les PV du joueur toucher n'est pas nul
                            p2.pv -= self.force # on enleve des pv
                            p2.isTouched = True
                            p2.hitbox.x += 20
                if self.orientation == "left":# si on regarde a droite alors la hb du poing pointe a gauche
                    self.isKick = True
                    kick_hb = pg.Rect(self.hitbox.centerx - 200, self.hitbox.centery , 200, 100) #la hb du coup de pied
                    pg.draw.rect(win, (0,0,255), kick_hb,5) # on affiche cette HB
                    if kick_hb.colliderect(p2.hitbox): #si la hb du coup touche la hb du joueur adverse
                        if p2.pv > 0: #si sa vie est > 0
                            p2.pv -= self.force #alors on lui enleve de la vie
                            p2.isTouched = True
                            p2.hitbox.x -= 20
            else:
                if self.orientation == "right":
                    self.isKick = True
                    kick_hb = pg.Rect(self.hitbox.right,self.hitbox.y,100,150)
                    pg.draw.rect(win, (255,0,0), kick_hb, 5)
                    if kick_hb.colliderect(p2.hitbox):
                        if p2.pv > 0:
                            p2.pv -= self.force
                            p2.isTouched = True
                            p2.hitbox.x += 100
                elif self.orientation == "left":
                    self.isKick = True
                    kick_hb = pg.Rect(self.hitbox.left - 100, self.hitbox.y, 100, 150)
                    pg.draw.rect(win, (0,0,255), kick_hb, 5)
                    if kick_hb.colliderect(p2.hitbox):
                        if p2.pv > 0:
                            p2.pv -= self.force
                            p2.isTouched = True
                            p2.hitbox.x -= 100
        self.isKick = False # on reinitialise


    def launch_hadoken(self, p2, win):
        """lance une boule de feu, fait avancer un Rect"""
        if self.orientation == "right":
            if not self.hadoken.projectile_hb.colliderect(p2.hitbox):
                if self.isPunch == False or self.isKick == False:# si on ne fait pas deja une autre action
                    if not self.hadoken.projectile_hb.colliderect(p2.hitbox) and self.hadoken.projectile_hb.x <= 1080:
                        self.hadoken.launch_projectile(win)
                    else:
                        self.isHadoken = False
                        self.hadoken = Projectile("right", self.hitbox.centerx, self.hitbox.centery)
        if self.orientation == "left":
            if not self.hadoken.projectile_hb.colliderect(p2.hitbox):
                if self.isPunch == False or self.isKick == False:# si on ne fait pas deja une autre action
                    if not self.hadoken.projectile_hb.colliderect(p2.hitbox) and self.hadoken.projectile_hb.x > 0:
                        self.hadoken.orientation = "left"
                        self.hadoken.launch_projectile(win)
                    else:
                        self.isHadoken = False
                        self.hadoken = Projectile("left", self.hitbox.centerx, self.hitbox.centery)
        if self.hadoken.projectile_hb.colliderect(p2.hitbox):
            if p2.pv > 0: #si sa vie est > 0
                p2.pv -= self.hadoken.damage #alors on lui enleve de la vie
                p2.isTouched = True
                self.isHadoken = False # on remets le booléen en False
                self.hadoken = Projectile("right", self.hitbox.centerx, self.hitbox.centery) #on reinitialise les coordonnée du projectile
                        

    def move(self, appuyer):
        """bouge le joueur sur l'axe x,
        attend en argument le bouton appuyer get_pressed
        get_pressed : le bouton appuyer
        """
        
        x_vel = 7.5 # la velocité des joueurs
        if appuyer[K_RIGHT]:
            if self.hitbox.right < 1080:
                #print(K_RIGHT)
                #print(get_pressed[K_RIGHT])
                #print(type(get_pressed[K_RIGHT]))
                self.hitbox.x += x_vel
                self.isMoving = True
                self.walkCount += 0.40
                if int(self.walkCount) == len(self.sprites['walk']):
                    self.walkCount = 0
        elif appuyer[K_LEFT]:
            if self.hitbox.left > 0:
                self.hitbox.x -= x_vel
                self.isMoving = True
                self.walkCount -= 0.40
                if int(self.walkCount) == -len(self.sprites['walk']):
                    self.walkCount = 0
        else:
            self.isMoving = False
        
    def jump(self):
        """methode permettant au personnage de sauter"""
        
        if self.jump_height >= -10:# si on est pas a la hauteur max de notre saut
            self.isJump = True
            self.hitbox.y -= (self.jump_height * abs(self.jump_height)) #on bouge le joueur 'abs est pour les valeurs neg)
            self.jump_height -= 1 #on decremante
        else: #saut terminer reinitialisation de nos valeurs
            self.jump_height = 10
            self.isJump = False

    def crouch(self, get_pressed):
        """
        on reduit la hitbox du personnage et le personnage s'accroupis
        """
        if get_pressed[K_DOWN]:
            self.hitbox.height = 350/2 #on reduit la HB
            if self.hitbox.bottom < 520:
                self.hitbox.y += 350/2 # on descend le joueuer de la moitié de la hitobx
        else:
            self.hitbox.height = 350 #on revient a l'etat initiale
            self.hitbox.width = 200
            self.hitbox.y = 320
            self.isCrouch = False
        
    def display_HUD(self, win):
        """methode qui affiche l'interface des deux joueurs
        win : la Surface sur la quelle on souhaite afficher
        """
        player1_pv_barre = [pg.Rect(60, 50, 404, 50), pg.Rect(62, 52, 400, 46), pg.Rect(62, 52, self.pv, 46)]
        player2_pv_barre = [pg.Rect(602, 50, 404, 50), pg.Rect(602, 52, 400, 46), pg.Rect(602, 52, self.pv, 46)]
        couleur_barre_PV = [(255,255,255),(255,0,0),(255,255,0)]
        if self.player_num == 1:
            for i in range(len(player1_pv_barre)):
                pg.draw.rect(win, couleur_barre_PV[i], player1_pv_barre[i])
        elif self.player_num == 2:
            for i in range(len(player2_pv_barre)):
                pg.draw.rect(win, couleur_barre_PV[i], player2_pv_barre[i])

    
    def display(self, win, player_rect, p2):
        """methode qui affiche le joueur sur
        win : la Surface sur le quelle on souhaite afficher notre personnage
        player_rect : le Rect (hitbox) de notre personnage (optional)
        p2 : instance Player adverse (permet de changer la direction)
        """
        # si le Joueur est derriere l'adversaire leurs orientation s'inverse
        pg.draw.rect(win, (255,255,255),player_rect) # on affiche la HB des joueurs
        if self.hitbox.centerx > p2.hitbox.centerx: #si derriere l'adversaire
            self.orientation = "left"
        elif self.hitbox.centerx < p2.hitbox.centerx: # si devant l'adversaire
            self.orientation = "right"
        
        # si on est toucher alors on affiche le perso toucher
        if self.isTouched:
            if self.orientation == "right":
                touched = pg.transform.scale(self.sprites["hit"][0], ((self.width,self.height)))# on charge l'image qui est orienté de base a droite
                win.blit(touched, self.hitbox) # on affiche
            elif self.orientation == "left":
                touched = pg.transform.scale(self.sprites["hit"][0], ((self.width,self.height)))# on charge l'image qui est orienté de base a droite
                touched = pg.transform.flip(touched, True, False)# on tourne l'image a gauche
                win.blit(touched, self.hitbox) # on affiche l'image
            self.isTouched = False # on reinitialise isTouched

        #l'affichage du coup
        elif self.isPunch and self.isMoving == False:# si on mets un coup et ne bouge pas
            self.punchCount += 0.30 # on incremente (rapidité de l'animation)
            if int(self.punchCount) == len(self.sprites["punch"]): # si l'entier est egale a la longeur max de l'animation
                self.punchCount = 0 #on reinit
            punch = self.sprites["punch"][int(self.punchCount)] # notre image est l'indice punchCount
            if self.orientation == "right": #si on regarde a droite
                punch = pg.transform.scale(punch, (240, self.height))
                win.blit(punch, self.hitbox.topleft)
            elif self.orientation == "left": #si on regarde a gauche 
                punch = pg.transform.scale(punch, (400, self.height))
                punch = pg.transform.flip(punch, True, False)
                win.blit(punch, self.hitbox.topleft)

        # animation Hadoken
        elif self.isHadoken:
            #on affiche idle en fonction de l'orientation
            self.hadokenCount += 0.40
            if self.hadokenCount > len(self.sprites["launch"]):
                self.hadokenCount = 0
            launch = self.sprites["launch"][int(self.hadokenCount)]
            if self.orientation == "right": #si l'orientation est droite on affiche l'image qui regarde a droite
                launch = pg.transform.scale(launch, (launch.get_width() * 5,launch.get_height() * 4.7))
                win.blit(launch, self.hitbox)
            elif self.orientation == "left": #si l'orientation est gauche on affiche l'image qui regarde a gauche
                launch = pg.transform.scale(launch, (self.width,self.height))
                launch = pg.transform.flip(launch, True, False)
                win.blit(launch, self.hitbox.top)
        
        # si on ne bouge pas on affiche le perso Idle dans la HB
        elif self.isMoving == False and self.isJump == False:
            #on affiche idle en fonction de l'orientation
            self.idleCount += 0.30
            if self.idleCount > len(self.sprites["idle"]):
                self.idleCount = 0
            idle = self.sprites["idle"][int(self.idleCount)]
            if self.orientation == "right": #si l'orientation est droite on affiche l'image qui regarde a droite
                idle = pg.transform.scale(idle, (self.width,self.height))
                win.blit(idle, self.hitbox)
            elif self.orientation == "left": #si l'orientation est gauche on affiche l'image qui regarde a gauche
                idle = pg.transform.scale(idle, (self.width,self.height))
                idle = pg.transform.flip(idle, True, False)
                win.blit(idle, self.hitbox)
            
        # si le perso avance on affiche le perso entrain de bouger dans la HB
        elif self.isMoving and self.isJump == False:
            walk = self.sprites["walk"][int(self.walkCount)]
            if self.orientation == "right":
                walk = pg.transform.scale(walk, (self.width,self.height))
                win.blit(walk, self.hitbox)
            elif self.orientation == "left":
                walk = pg.transform.scale(walk, (self.width,self.height))
                walk = pg.transform.flip(walk, True, False)
                win.blit(walk, self.hitbox)
        
        #l'affichage du saut
        elif self.isJump:
            self.jumpCount += 0.4
            if int(self.jumpCount) == len(self.sprites["jump"]):
                self.jumpCount = 0
            jump = self.sprites["jump"][int(self.jumpCount)]
            if self.orientation == "right":
                jump = pg.transform.scale(jump, (self.width, self.height))
                win.blit(jump, self.hitbox)
            elif self.orientation == "left":
                jump = pg.transform.scale(jump, (self.width, self.height))
                jump = pg.transform.flip(jump, True, False)
                win.blit(jump, self.hitbox)

class Projectile():

    def __init__(self, orientation, x, y):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.projectile_hb = pg.Rect(self.x, self.y, 50, 50)
        self.damage = 20
        self.sprite = []

    def launch_projectile(self, win):
        if self.orientation == "right":
            speed = 30
        elif self.orientation == "left":
            speed = -30
        self.projectile_hb.x += speed
        pg.draw.rect(win, (255,0,0), self.projectile_hb, 5)

    def display_projectile(self, win, projectile_rect):
        pass