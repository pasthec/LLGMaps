import pygame
from queue import *

pygame.init()

ecran = pygame.display.set_mode((720, 600),pygame.RESIZABLE)
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
N=50
H=4
#hauteur en pixels d'un niveau
h = 50		
grille = [ [ [0]*N for _ in range(N)] for z in range(H) ]

""" Système de représentation sur 5 bits:

    1er bit -> mur droit
    2e 		-> mur gauche
    3e		-> escalier vers le bas
    4e		-> escalier vers le haut
    5e		-> présence d'une tuile
"""

htuile, ltuile = 6, 10

losange = [(ltuile//2,0),(ltuile,htuile//2),(ltuile//2,htuile),(0,htuile//2)]
MUR_G = [(ltuile//2,0), (ltuile//2,h), (0,h+htuile//2), (0, htuile//2)]
MUR_D = [(0,0), (ltuile//2,htuile//2), (ltuile//2,h+htuile//2), (0,h)]

def voisins(position):
	z,x,y = position
	vois=[]
	for direction in [(1,0),(-1,0),(0,1),(0,-1)]:
		dx, dy= direction[0], direction[1]
		nx, ny = x+dx, y+dy
		if nx>=0 and nx<N and ny>=0 and ny<N:
			if (grille[z][nx][ny]//2**4)%2==1:
				vois.append((z,nx,ny))
	if z>0:
		if (grille[z][x][y]//(2**2))%2 == 1 and  (grille[z-1][x][y]//(2**4))%2 == 1: #Si il y a un escalier vers le bas qui mène sur une case
			vois.append((z-1,x,y))
	if z<H-1:
		if (grille[z][x][y]//(2**3))%2 == 1 and  (grille[z+1][x][y]//(2**4))%2 == 1: #Si il y a un escalier vers le haut qui mène sur une case
			vois.append((z+1,x,y))
	return vois

def BFS(x1,y1,z1, x2,y2,z2):
	file = Queue()
	posDepart = (z1,x1,y1)
	arrivee = (z2,x2,y2)
	print("Arrivee : ",arrivee)
	prec = [ [ [(-1,-1,-1)]*N for _ in range(N)] for z in range(H) ]
	prec[z1][x1][y1] = (z1,x1,y1)
	file.put(posDepart)
	trouve = False
	while not file.empty():
		curPos = file.get()
		print("curPos : {}".format(curPos))
		if curPos == arrivee:
			trouve = True
			break
		print("Voisins :")
		for vois in voisins(curPos):
			print(vois)
			if prec[vois[2]][vois[0]][vois[1]] == (-1,-1,-1):
				prec[vois[2]][vois[0]][vois[1]] = curPos
				file.put(vois)
	if not trouve:
		print("Chemin impossible :'(")
	else:
		chemin = []
		pos = arrivee
		chemin.append(arrivee)
		while pos!=posDepart:
			pos = prec[pos[2]][pos[0]][pos[1]]
			chemin.append(pos)
		return chemin[::-1]
	return []

def rendu():
	for z in range(H):
		for x in range(N):
			for y in range(N):
				if (grille[z][x][y]//2**4)%2==1:
					los = pygame.Surface((ltuile+2,htuile+2),pygame.SRCALPHA)
					pygame.draw.polygon(los, NOIR+(255,), losange, 3)
					pygame.draw.polygon(los, couleur[z] +(200,), losange)
					pos = [324, 150-z*h]
					pos[0] += htuile*(x - y)
					pos[1] += ltuile//2*(x + y)
					ecran.blit(los, pos)
				if (grille[z][x][y]//2) % 2 == 1:
					dessinerMurGauche(x,y,z)
				if grille[z][x][y]%2 == 1:
					dessinerMurDroit(x,y,z)
				pygame.display.flip()

def dessinerRectangle(x1,y1,x2,y2,z):
	if x1>=N or x2>=N or y1>=N or y2>=N:
		return
	for x in range(min(x1,x2), max(x1,x2)+1):
		for y in range(min(y1,y2), max(y1,y2)+1):
			changerTuile(x,y,z,1)

def dessinerMurGauche(x,y,z):
	mur = pygame.Surface((28, 32+h), pygame.SRCALPHA)
	#pygame.draw.polygon(mur, NOIR+(255,), MUR_G, 6)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR_G)
	pos = [324, 150-z*h - h]
	pos[0] += htuile*(x - y)
	pos[1] += ltuile*(x + y)
	ecran.blit(mur, pos)

def dessinerMurDroit(x,y,z):
	mur = pygame.Surface((28, 32+h), pygame.SRCALPHA)
	#pygame.draw.polygon(mur, NOIR+(255,), MUR_D, 6)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR_D)
	pos = [324, 150-z*h - h]
	pos[0] += htuile*(x - y) + ltuile//2
	pos[1] += ltuile*(x + y)
	ecran.blit(mur, pos)

def changerMurGauche(x,y,z, a):
	#a = -1 pour enlever, 1 pour ajouter
	if a==1 and (grille[z][x][y]//2) % 2 != 1:
		grille[z][x][y] += 2
	elif a==-1 and (grille[z][x][y]//2) %2 ==1:
		grille[z][x][y] -=2

def changerMurDroit(x,y,z, a):
	if a==1 and grille[z][x][y]%2 != 1:
		grille[z][x][y] += 1
	if a==-1 and grille[z][x][y]%2 == 1:
		grille[z][x][y] -= 1

def changerTuile(x,y,z, a):
	if a==1 and (grille[z][x][y]//(2**4))%2 != 1:
		grille[z][x][y] += (2**4)
	if a==-1 and (grille[z][x][y]//(2**4))%2 == 1:
		grille[z][x][y] -= (2**4)

def changerEscalierH(x,y,z, a):
	if a==1 and (grille[z][x][y]//(2**3))%2 != 1:
		grille[z][x][y] += (2**3)
	if a==-1 and (grille[z][x][y]//(2**3))%2 == 1:
		grille[z][x][y] -= (2**3)

def changerEscalierB(x,y,z, a):
	if a==1 and (grille[z][x][y]//(2**2))%2 != 1:
		grille[z][x][y] += 2**2
	if a==-1 and (grille[z][x][y]//(2**2))%2 == 1:
		grille[z][x][y] -= 2**2

grille[0][0][0] = 2**4
grille[1][0][0] = 2**4
grille[2][0][0] = 2**4
grille[3][0][0] = 2**4
grille[0][0][1] = 2**4
grille[0][0][2], grille[0][0][3], grille[0][1][3] = 2**4,2**4,2**4
grille[0][0][11] = 2**4
grille[0][11][0] = 2**4
grille[0][11][11] = 2**4

dessinerRectangle(3,5,8,6,0)
dessinerRectangle(2,2,6,2,1)
changerMurGauche(0,0,0,1)
changerMurDroit(0,0,0,1)
dessinerRectangle(0,0,30,30,0)
dessinerRectangle(0,0,30,3,1)
dessinerRectangle(0,0,3,30,1)

## RdC VH

dessinerRectangle(0,0,21,15,0)   
dessinerRectangle(6,16,21,27,0) """Sol de la cours + salles de cours"""
dessinerRectangle(3,16,5,17) """Escalier vers N3"""
dessinerRectangle(18,28,19,31,0) """Escalier HX1/4"""
dessinerLigneMurGauche(18,28,18,31,0) """ mur Escalier HX1/4"""
dessinerLigneMurGauche(20,28,20,31,0) """idem"""
dessinerLigneMurDroit(0,0,21,0,0) '''Mur exterieur derriere VH0xx'''
dessinerLigneMurDroit(0,2,21,2,0) '''Mur des VH Oxx'''
for k in range(6): '''mur inter-salle'''
    dessinerLigneMurGauche(3+3*k,0,3+3*k,1,0)
dessinerLigneMurGauche(0,0,0,31,0) '''Mur exterieur derriere amphi/wc'''
dessinerLigneMurGauche(3,3,3,17,0) '''mur devant wc/gymnase'''
dessinerMurGauche(4,7,0) '''Pilier RdC début'''
dessinerMurGauche(4,11,0)
dessinerMurDroit(6,3,0)
dessinerMurDroit(10,3,0)
dessinerMurDroit(14,3,0) '''fin pilier'''
dessinerLigneMurGauche(19,0,19,1,0) '''mur escalier/parloir'''
dessinerLigneMurGauche(19,3,19,14,0) '''mur chapelle -> CPE'''
dessinerLigneMurGauche(19,16,19,18,0) '''mur escalier anglais'''
dessinerLigneMurGauche(19,20,19,27,0) '''mur cafet -> musique'''    
dessinerMurDroit(19,3,0) '''Mur chapelle'''
dessinerMurDroit(21,3,0)
dessinerLigneMurDroit(19,10,21,10,0) '''Tous les murs du coté chapelle'''
dessinerLigneMurDroit(19,13,21,13,0)
dessinerLigneMurDroit(19,15,21,15,0)
dessinerLigneMurDroit(20,16,21,16,0)
dessinerLigneMurDroit(20,19,21,19,0)
dessinerLigneMurDroit(20,20,21,20,0)
dessinerLigneMurDroit(19,24,21,24,0)
dessinerLigneMurDroit(19,26,21,26,0)
dessinerLigneMurDroit(19,28,21,28,0) '''fin mur coté chapelle'''
dessinerLigneMurDroit(17,28,6,28,0) '''Mur ECS'''
dessinerLigneMurGauche(6,16,6,27,0) '''mur amphi'''
dessinerLigneMurDroit(4,16,5,16,0) '''Mur escalier vers N3 début''' 
dessinerLigneMurDroit(3,18,5,18,0)
dessinerMurDroit(3,17,0) '''fin mur ...'''

changerMurGauche(3,14,0, -1) '''debut portes'''
changerMurGauche(3,11,0, -1)
changerMurGauche(3,9,0, -1)
for k in range(3):
    changerMurGauche(6+3*k,0,0, -1)
changerMurGauche(19,12,0, -1)
changerMurGauche(19,13,0, -1)
changerMurGauche(19,25,0, -1)
changerMurGauche(19,26,0, -1)

changerMurDroit(1,2,0, -1)
changerMurDroit(3,2,0, -1)
changerMurDroit(6,2,0, -1)
changerMurDroit(11,2,0, -1)
changerMurDroit(14,2,0, -1)
changerMurDroit(18,2,0, -1)
changerMurDroit(20,2,0, -1) '''fin portes'''


## Fin RdC VH


rendu()

#print(*BFS(0,0,0,1,3,0))


continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            continuer = False

pygame.quit()
