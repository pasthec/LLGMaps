import pygame

pygame.init()

ecran = pygame.display.set_mode((700, 400),pygame.RESIZABLE)

lycee = pygame.image.load("lycee_ext.jpg").convert_alpha()
lycee = pygame.transform.scale(lycee, (700,400))
ecran.blit(lycee, (0,0))


cour = pygame.image.load("cour_d'honneur.jpg").convert()
cour = pygame.transform.scale(cour, (256, 182))
cour = pygame.transform.rotate(cour, 45)
cour.set_alpha(80)
ecran.blit(cour, (150, 100))

losange = pygame.Surface((200,200),pygame.SRCALPHA)
losange.fill((255,255,255,0))
pygame.draw.polygon(losange, (100,0,0,100), [(50,50),(100,75),(50,100),(0,75)], 10)
#losange.set_alpha(0)
ecran.blit(losange,(0,0))
pygame.display.flip()

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

pygame.quit()