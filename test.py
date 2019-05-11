import pygame

pygame.init()

ecran = pygame.display.set_mode((700, 550),pygame.RESIZABLE)
ecran.fill((255,255,255))

#Couleurs
NOIR = (0,0,0)
BLANC = (255, 255, 255)
BLEU_CLAIR = (47,225,252)
ORANGE = (252, 136, 35)
VERT = 21, 216, 47

couleur = [ORANGE, BLEU_CLAIR, VERT]


"""
lycee = pygame.image.load("lycee_ext.jpg").convert_alpha()
lycee = pygame.transform.scale(lycee, (700,400))
ecran.blit(lycee, (0,0))
"""

#colo slate

"""
cour = pygame.image.load("cour_d'honneur.jpg").convert_alpha()
cour = pygame.transform.scale(cour, (256, 182))
cour = pygame.transform.rotate(cour, 45)
cour.set_alpha(180)
ecran.blit(cour, (150, 100))
"""

losange = [(27,0),(54,16),(27,32),(0,16)]

N=12
H=3
h = 50
grille = [ [ [0]*N for _ in range(N)] for z in range(H) ]



def rendu():
	for z in range(H):
		for x in range(N):
			for y in range(N):
				if grille[z][x][y] > 0:
					los = pygame.Surface((55,40),pygame.SRCALPHA)
					pygame.draw.polygon(los, NOIR+(255,), losange, 6)
					pygame.draw.polygon(los, couleur[z] +(200,), losange)
					pos = [324, 150-z*h]
					pos[0] += 27*(x - y)
					pos[1] += 16*(x + y)
					ecran.blit(los, pos)
					pygame.display.flip()

def dessinerRectangle(x1,y1,x2,y2,z):
	if x1>=N or x2>=N or y1>=N or y2>=N:
		return
	for x in range(min(x1,x2), max(x1,x2)+1):
		for y in range(min(y1,y2), max(y1,y2)+1):
			grille[z][x][y] = 1
	return

grille[0][0][0] = 1
grille[1][0][0] = 1
grille[2][0][0] = 1
grille[0][0][1] = 1
grille[0][0][2], grille[0][0][3], grille[0][1][3] = 1,1,1
grille[0][0][11] = 1
grille[0][11][0] = 1
grille[0][11][11] = 1

dessinerRectangle(3,5,8,6,0)
dessinerRectangle(2,2,6,2,1)
rendu()

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            continuer = False

pygame.quit()
