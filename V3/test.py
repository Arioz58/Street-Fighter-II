self.isHadoken = True
                # hadoken_sound = pg.mixer.Sound("sound\projectile_ryu\hadoken_ryu.mp3")
                # hadoken_sound.play()
                if self.orientation == "right": #si on regare a gauche
                    pg.draw.rect(win, (255,0,0), self.projectile_hb) # on affiche le projectile
                    if not self.projectile_hb.colliderect(p2.hitbox): # tant que on a pas toucher l'adversaire
                        if self.projectile_hb.x < 1080: # tant que le projectile ne sera pas assez loin
                            self.projectile_hb.x += 10 # on fait avancer le projectile
                        else: # si le projectile est assez loin
                            self.isHadoken = False # on remets le booléen en False
                            self.projectile_hb = pg.Rect(self.hitbox.right, self.hitbox.centery - 50/2, 50, 50) #on reinitialise les coordonnée du projectile
                elif self.orientation == "left":
                    pg.draw.rect(win, (0,0,255), self.projectile_hb) # on affiche le projectile
                    if not self.projectile_hb.colliderect(p2.hitbox): # tant que on a pas toucher l'adversaire
                        if self.projectile_hb.x > 0: # tant que le projectile ne sera pas assez loin
                            self.projectile_hb.x -= 10 # on fait avancer le projectile
                        else: # si le projectile est assez loin
                            self.isHadoken = False # on remets le booléen en False
                            self.projectile_hb = pg.Rect(self.hitbox.left, self.hitbox.centery - 50/2, 50, 50) #on reinitialise les coordonnée du projectile
                if self.projectile_hb.colliderect(p2.hitbox):
                    if p2.pv > 0: #si sa vie est > 0
                        p2.pv -= self.force #alors on lui enleve de la vie
                        p2.isTouched = True
                        self.isHadoken = False # on remets le booléen en False
                        self.projectile_hb = pg.Rect(self.hitbox.right, self.hitbox.centery - 50/2, 50, 50) #on reinitialise les coordonnée du projectile