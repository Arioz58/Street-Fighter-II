import pygame

# Initialiser Pygame
pygame.init()

# Définir les dimensions de la fenêtre
window_size = (800, 600)

# Initialiser la fenêtre
window = pygame.display.set_mode(window_size)

# Définir la position initiale du joueur
player_x = 100
player_y = 0

# Définir la gravité
gravity = 0.5

# Définir la vitesse initiale du saut
jump_speed = 10

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_y -= jump_speed
    
    # Appliquer la gravité
    player_y += gravity
    
    # Dessiner le joueur
    window.fill((255, 255, 255))
    pygame.draw.rect(window, (0, 0, 0), (player_x, player_y, 50, 50))
    
    # Mettre à jour l'affichage
    pygame.display.update()

# Quitter Pygame
pygame.quit()