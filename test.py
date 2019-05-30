import pygame

pygame.init()

ecran = pygame.display.set_mode((700, 550),pygame.RESIZABLE)
ecran.fill((255,255,255))

#Couleurs
NOIR = (0,0,0)
BLANC = (255, 255, 255)
BLEU_CLAIR = (47,225,252)
ORANGE = (252, 136, 35)
VERT = (21, 216, 47)
ROSE = (223, 102, 232)


couleur = [ORANGE, BLEU_CLAIR, VERT, ROSE] #Pour plus de clarté chaque niveau sera représenté par une couleur


"""
lycee = pygame.image.load("lycee_ext.jpg").convert_alpha()
lycee = pygame.transform.scale(lycee, (700,400))
ecran.blit(lycee, (0,0))
"""

"""
cour = pygame.image.load("cour_d'honneur.jpg").convert_alpha()
cour = pygame.transform.scale(cour, (256, 182))
cour = pygame.transform.rotate(cour, 45)
cour.set_alpha(180)
ecran.blit(cour, (150, 100))
"""
#Dimensions du la grille : N pour x,y; H pour z
N=12
H=4
#hauteur en pixels d'un niveau
h = 50
grille = [ [ [0]*N for _ in range(N)] for z in range(H) ]

""" Système de représentation sur 5 bits:

    1er bit -> existence du mur
    2e 		-> escalier vers le haut
    3e		-> escalier vers le bas
    4e		-> mur gauche
    5e		-> mur droit
"""

losange = [(27,0),(54,16),(27,32),(0,16)]
MUR = [(0,13+h), (27,h-3), (27,0), (0, 16)]

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
			changerTuile(x,y,z,1)

def dessinerMurGauche(x,y,z):
	mur = pygame.Surface((28, 32+h), pygame.SRCALPHA)
	pygame.draw.polygon(mur, NOIR+(255,), MUR, 6)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR)
	pos = [324, 150-z*h - h]
	pos[0] += 27*(x - y)
	pos[1] += 16*(x + y)
	ecran.blit(mur, pos)
	pygame.display.flip()

def dessinerMurGauche(x,y,z):
	mur = pygame.Surface((28, 32+h), pygame.SRCALPHA)
	pygame.draw.polygon(mur, NOIR+(255,), MUR, 6)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR)
	pos = [324, 150-z*h - h]
	pos[0] += 27*(x - y)
	pos[1] += 16*(x + y)
	ecran.blit(mur, pos)
	pygame.display.flip()

def changerMurGauche(x,y,z, a):
	#a = -1 pour enlever, 1 pour ajouter
	grille[z][x][y] += 2*a

def changerMurDroit(x,y,z, a):
	grille[z][x][y] += a

def changerTuile(x,y,z, a):
	grille[z][x][y] += (2**4)*a

def changerEscalierH(x,y,z, a):
	grille[z][x][y] += (2**3)*a

def changerEscalierB(x,y,z, a):
	grille[z][x][y] += (2**2)*a

grille[0][0][0] = 1
grille[1][0][0] = 1
grille[2][0][0] = 1
grille[3][0][0] = 1
grille[0][0][1] = 1
grille[0][0][2], grille[0][0][3], grille[0][1][3] = 1,1,1
grille[0][0][11] = 1
grille[0][11][0] = 1
grille[0][11][11] = 1

dessinerRectangle(3,5,8,6,0)
dessinerRectangle(2,2,6,2,1)
rendu()
dessinerMurGauche(0,0,0)

continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            continuer = False

pygame.quit()
