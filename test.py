import pygame
from queue import *

pygame.init()
ecran = pygame.display.set_mode((600, 600),pygame.RESIZABLE)
logo = pygame.image.load('textures/logo_fenetre.jpg').convert_alpha()
pygame.display.set_icon(logo)
pygame.display.set_caption('LLGMaps')
ecran.fill((255,255,255))

#Couleurs
NOIR = (0,0,0)
BLANC = (255, 255, 255)
BLEU_CLAIR = (47,225,252)
ORANGE = (252, 136, 35)
VERT = (21, 216, 47)
ROSE = (223, 102, 232)


couleur = [ORANGE, BLEU_CLAIR, VERT, ROSE] #Pour plus de clarté chaque niveau sera représenté par une couleur


#Dimensions du la grille : N pour x,y; H pour z
N=35
H=3
#hauteur en pixels d'un niveau
h = 35	
grille = [ [ [0]*N for _ in range(N)] for z in range(H) ]
col = [ [ [(BLANC)]*N for _ in range(N)] for z in range(H) ]

for z in range(H):
	for x in range(N):
		for y in range(N):
			col[z][x][y] = couleur[z]
""" Système de représentation sur 5 bits:

    1er bit -> mur droit
    2e 		-> mur gauche
    3e		-> escalier vers le bas
    4e		-> escalier vers le haut
    5e		-> présence d'une tuile
"""

htuile, ltuile = 10, 16

losange = [(ltuile//2,0),(ltuile,htuile//2),(ltuile//2,htuile),(0,htuile//2)]
MUR_G = [(ltuile//2,0), (ltuile//2,h), (0,h+htuile//2), (0, htuile//2)]
MUR_G_C = [(ltuile//2,0), (0, htuile//2)]
MUR_D = [(0,0), (ltuile//2,htuile//2), (ltuile//2,h+htuile//2), (0,h)]
MUR_D_C = [(0,0), (ltuile//2,htuile//2)]

def voisins(position):
	z,x,y = position
	vois=[]
	if x<N-1 and (grille[z][x+1][y]//(2**4))%2 == 1 and (grille[z][x+1][y]//2)%2==0:	#Si il y a une case à droite et pas de mur entre les deux
		vois.append((z,x+1,y))
	if x>0 and  (grille[z][x-1][y]//(2**4))%2 == 1 and (grille[z][x][y]//2)%2==0:		#Si il y a une case à gauche et pas de mur entre les deux
		vois.append((z,x-1,y))
	if y<N-1 and (grille[z][x][y+1]//(2**4))%2 == 1 and (grille[z][x][y+1])%2==0:    #Si une case en bas et pas de mur entre les deux
		vois.append((z,x,y+1))
	if y>0 and (grille[z][x][y-1]//(2**4))%2 == 1 and (grille[z][x][y])%2==0:        #Si une case en haut et pas de mur entre les deux
		vois.append((z,x,y-1))
	#Pour aller en diagonale bas
	# Si c'est une case et qu'aucun mur ne les sépare
	if x<N-1 and y<N-1 and (grille[z][x+1][y+1]//(2**4))%2 == 1 and \
	(grille[z][x+1][y]//2)%2==0 and (grille[z][x+1][y+1]%2==0) and (grille[z][x][y+1])%2==0 and (grille[z][x+1][y+1]//2)%2==0:
		vois.append((z,x+1,y+1))
	#Diagonale droite
	if x<N-1 and y>0 and (grille[z][x+1][y+1]//(2**4))%2 == 1 and \
	(grille[z][x+1][y]//2)%2==0 and (grille[z][x+1][y]%2==0) and (grille[z][x][y])%2==0 and (grille[z][x+1][y-1]//2)%2==0:
		vois.append((z,x+1,y-1))
	#Diagonale haut
	if x>0 and y>0 and (grille[z][x-1][y-1]//(2**4))%2 == 1 and \
	(grille[z][x][y]//2)%2==0 and grille[z][x][y]%2==0 and (grille[z][x][y-1]//2)%2==0 and grille[z][x-1][y]%2==0:
		vois.append((z,x-1,y-1))
	#Diagonale gauche
	if x>0 and y<N-1 and (grille[z][x-1][y+1]//(2**4))%2 == 1 and \
	(grille[z][x][y]//2)%2==0 and (grille[z][x][y+1]//2)%2==0 and grille[z][x][y+1]%2==0 and grille[z][x-1][y+1]%2==0:
		vois.append((z,x-1,y+1))

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
		#print("curPos : {}".format(curPos))
		if curPos == arrivee:
			trouve = True
			break
		#print("Voisins :")
		for vois in voisins(curPos):
			#print(vois)
			if prec[vois[0]][vois[1]][vois[2]] == (-1,-1,-1):
				prec[vois[0]][vois[1]][vois[2]] = curPos
				file.put(vois)
	if not trouve:
		print("Chemin impossible :'(")
	else:
		print("On a trouvé le chemin vers les citées d'or !")
		chemin = []
		pos = arrivee
		chemin.append(arrivee)
		while pos!=posDepart:
			pos = prec[pos[0]][pos[1]][pos[2]]
			chemin.append(pos)
		return chemin[::-1]
	return []

def rendu():
	ecran.fill((255,255,255))
	for z in range(H):
		print(z)
		for x in range(N):
			for y in range(N):
				if (grille[z][x][y]//2**4)%2==1:
					los = pygame.Surface((ltuile+2,htuile+2),pygame.SRCALPHA)
					pygame.draw.polygon(los, NOIR+(255,), losange, 4)
					pygame.draw.polygon(los, col[z][x][y] +(200,), losange)
					pos = [324, 150-z*h]
					pos[0] += (htuile-1)*(x - y)
					pos[1] += (ltuile//2-1)*(x + y)
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
	mur = pygame.Surface((ltuile, htuile+h), pygame.SRCALPHA)
	pygame.draw.polygon(mur, BLANC+(255,), MUR_G, 4)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR_G)
	pos = [324, 150-z*h - h]
	pos[0] += (htuile-1)*(x - y)
	pos[1] += (ltuile//2-1)*(x + y)
	ecran.blit(mur, pos)

def dessinerMurDroit(x,y,z):
	mur = pygame.Surface((ltuile, htuile+h), pygame.SRCALPHA)
	pygame.draw.polygon(mur, BLANC+(255,), MUR_D, 4)
	pygame.draw.polygon(mur, couleur[z] +(200,), MUR_D)
	pos = [324, 150-z*h - h]
	pos[0] += (htuile-1)*(x - y) + ltuile//2
	pos[1] += (ltuile//2-1)*(x + y)
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

def dessinerLigneMurGauche(x1,y1,x2,y2,z):
	if x1>=N or x2>=N or y1>=N or y2>=N:
		return
	if y2 < y1:
		y1, y2 = y2, y1
	if x2 < x1:
		x1, x2 = x2, x1
	for i in range(y2-y1+1):
		for j in range(x2-x1+1):
			changerMurGauche(x1+j,y1+i,z,1)

def dessinerLigneMurDroit(x1,y1,x2,y2,z):
	if x1>=N or x2>=N or y1>=N or y2>=N:
		return
	if x2 < x1:
		x1, x2 = x2, x1
	for i in range(y2-y1+1):
		for j in range(x2-x1+1):
			changerMurDroit(x1+j,y1+i,z,1)

def dessinerChemin(chemin):
	"""
	for pos in chemin:
		z,x,y = pos
		col[z][x][y] = VERT
	"""
	print("rendu ... ")
	rendu()
	print("terminé")
	for pos in chemin:
		z,x,y = pos
		los = pygame.Surface((ltuile+2,htuile+2),pygame.SRCALPHA)
		pygame.draw.polygon(los, NOIR+(255,), losange, 4)
		pygame.draw.polygon(los, VERT +(200,), losange)
		pos = [324, 150-z*h]
		pos[0] += (htuile-1)*(x - y)
		pos[1] += (ltuile//2-1)*(x + y)
		ecran.blit(los, pos)
	pygame.display.flip()

## RdC VH

dessinerRectangle(0,0,21,15,0)   
dessinerRectangle(6,16,21,27,0)
"""Sol de la cours + salles de cours"""
dessinerRectangle(3,16,5,17,0) 
"""Escalier vers N3"""
dessinerRectangle(18,28,19,31,0) 
"""Escalier HX1/4"""
dessinerLigneMurGauche(18,28,18,31,0) 
""" mur Escalier HX1/4"""
dessinerLigneMurGauche(20,28,20,31,0) 
"""idem"""
dessinerLigneMurDroit(0,0,21,0,0) 
'''Mur exterieur derriere VH0xx'''
dessinerLigneMurDroit(0,2,21,2,0) 
'''Mur des VH Oxx'''

'''mur inter-salle'''
for k in range(6):
	dessinerLigneMurGauche(3+3*k,0,3+3*k,1,0)

dessinerLigneMurGauche(0,0,0,15,0) 
dessinerLigneMurDroit(3,18,5,18,0) 
'''Mur exterieur derriere amphi/wc'''
dessinerLigneMurGauche(3,3,3,17,0) 
'''mur devant wc/gymnase'''
changerMurGauche(4,7,0,1) 
'''Pilier RdC début'''
changerMurGauche(4,11,0,1)
changerMurDroit(6,3,0,1)
changerMurDroit(10,3,0,1)
changerMurDroit(14,3,0,1) 
'''fin pilier'''
dessinerLigneMurGauche(19,0,19,1,0) 
'''mur escalier/parloir'''
dessinerLigneMurGauche(19,3,19,14,0) 
'''mur chapelle -> CPE'''
dessinerLigneMurGauche(19,16,19,18,0) 
'''mur escalier anglais'''
dessinerLigneMurGauche(19,20,19,27,0) 
'''mur cafet -> musique'''    
dessinerMurDroit(19,3,0) 
'''Mur chapelle'''
dessinerMurDroit(21,3,0)
dessinerLigneMurDroit(19,10,21,10,0) 
'''Tous les murs du coté chapelle'''
dessinerLigneMurDroit(19,13,21,13,0)
dessinerLigneMurDroit(19,15,21,15,0)
dessinerLigneMurDroit(20,16,21,16,0)
dessinerLigneMurDroit(20,19,21,19,0)
dessinerLigneMurDroit(20,20,21,20,0)
dessinerLigneMurDroit(19,24,21,24,0)
dessinerLigneMurDroit(19,26,21,26,0)
dessinerLigneMurDroit(19,28,21,28,0) 
'''fin mur coté chapelle'''
dessinerLigneMurDroit(17,28,6,28,0) 
'''Mur ECS'''
dessinerLigneMurGauche(6,16,6,27,0)
'''mur amphi'''
dessinerLigneMurDroit(4,16,5,16,0) 
'''Mur escalier vers N3 début''' 
dessinerLigneMurDroit(3,18,5,18,0)
dessinerMurDroit(3,17,0) 
'''fin mur ...'''

changerMurGauche(3,14,0, -1) 
'''debut portes'''
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
changerMurDroit(20,2,0, -1) 
'''fin portes'''

"""Escalier"""
changerEscalierH(20,17,0,1)
changerEscalierH(4,16,0,1)
changerEscalierH(4,17,0,1)
changerEscalierH(0,0,0,1)
changerEscalierH(18,1,0,1)
changerEscalierH(9,28,0,1)
changerEscalierH(19,31,0,1)

## Fin RdC VH


## Debut Etage1 VH

dessinerRectangle(0,0,3,15,1)
"""sol VH14X"""
dessinerRectangle(4,0,18,2,1)
"""sol VH orthog. 141"""
dessinerRectangle(3,16,5,17,1)
"""escalier vers N3"""
dessinerRectangle(1,18,5,28,1)
dessinerRectangle(1,29,3,29,1)
dessinerRectangle(5,28,17,30,1)
dessinerRectangle(18,28,21,31,1)
dessinerRectangle(19,10,21,27,1)
"""Sol 1er etage"""
dessinerLigneMurGauche(0,0,0,15,1)
dessinerLigneMurGauche(3,4,3,17,1)
dessinerLigneMurDroit(0,0,18,0,1)
dessinerLigneMurDroit(0,2,17,2,1)
dessinerLigneMurDroit(4,3,18,3,1)
for k in range(6):
	dessinerLigneMurGauche(3+3*k,0,3+3*k,1,1)
dessinerLigneMurGauche(19,0,19,27,1)	
dessinerLigneMurDroit(0,3,2,3,1)
dessinerLigneMurDroit(1,6,2,6,1)
dessinerLigneMurDroit(1,10,2,10,1)
dessinerLigneMurDroit(1,13,2,13,1)
dessinerLigneMurDroit(0,16,2,16,1)
"""Murs haut droit"""
dessinerLigneMurDroit(4,16,5,16,1)
dessinerLigneMurGauche(6,16,6,27,1)
"""murs escalier N3/SdC"""
dessinerLigneMurDroit(1,18,3,18,1)
dessinerLigneMurDroit(1,22,3,22,1)
dessinerLigneMurDroit(1,26,3,26,1)
dessinerLigneMurGauche(1,18,1,29,1)
dessinerLigneMurDroit(1,30,3,30,1)
dessinerLigneMurGauche(4,19,4,20,1)
dessinerLigneMurGauche(4,23,4,24,1)
dessinerLigneMurGauche(4,27,4,28,1)
dessinerLigneMurGauche(5,22,5,23,1)
changerMurGauche(5,18,1,1)
changerMurGauche(5,27,1,1)
changerMurGauche(20,28,1,1)
changerMurGauche(21,28,1,1)
changerMurGauche(20,14,1,1)
changerMurDroit(5,18,1,1)
changerMurDroit(5,20,1,1)
changerMurDroit(5,21,1,1)
changerMurDroit(5,23,1,1)
changerMurDroit(5,25,1,1)
changerMurDroit(5,26,1,1)
changerMurDroit(4,29,1,1)
dessinerLigneMurDroit(5,28,18,28,1)
dessinerLigneMurDroit(6,30,7,30,1)
dessinerLigneMurDroit(6,30,7,30,1)
dessinerLigneMurGauche(9,28,9,29,1)
dessinerLigneMurGauche(10,28,10,29,1)
dessinerLigneMurGauche(12,28,12,29,1)
dessinerLigneMurGauche(14,28,14,29,1)
dessinerLigneMurDroit(19,10,21,10,1)
dessinerLigneMurDroit(20,13,21,13,1)
dessinerLigneMurDroit(20,15,21,15,1)
dessinerLigneMurDroit(20,16,21,16,1)
dessinerLigneMurDroit(20,19,21,19,1)
dessinerLigneMurDroit(20,20,21,20,1)
dessinerLigneMurDroit(20,28,21,28,1)
dessinerLigneMurGauche(20,30,20,31,1)
dessinerLigneMurGauche(21,30,21,31,1)
changerMurDroit(21,30,1,1)
changerMurGauche(18,28,1,1)
changerMurGauche(18,30,1,1)



changerMurGauche(3,3,1,-1)
changerMurGauche(3,6,1,-1)
changerMurGauche(3,10,1,-1)
changerMurGauche(3,13,1,-1)
for k in range(6):
	changerMurDroit(1+3*k,2,1,-1)

"""Escalier etage1"""

changerEscalierB(4,16,1,1)
changerEscalierH(4,16,1,1)
changerEscalierB(4,17,1,1)
changerEscalierH(4,17,1,1)
changerEscalierB(0,0,1,1)
changerEscalierH(0,0,1,1)
changerEscalierB(18,1,1,1)
changerEscalierH(18,1,1,1)
changerEscalierB(9,28,1,1)
changerEscalierH(9,28,1,1)
changerEscalierB(19,31,1,1)
changerEscalierH(19,31,1,1)
changerEscalierB(20,17,1,1)
changerEscalierH(20,17,1,1)
##Fin Etage1 VH

## Debut Etage2 VH

dessinerRectangle(0,0,3,17,2)
"""sol VH14X"""
dessinerRectangle(4,0,18,2,2)
"""sol VH orthog. 141"""
dessinerRectangle(3,16,5,17,2)
dessinerRectangle(4,15,4,15,2)
"""escalier vers N3"""
dessinerRectangle(1,18,5,28,2)
dessinerRectangle(1,29,3,29,2)
dessinerRectangle(5,28,17,30,2)
dessinerRectangle(18,28,19,31,2)
dessinerRectangle(19,14,21,18,2)
dessinerRectangle(19,2,19,2,2)
dessinerRectangle(20,2,21,3,2)
"""Sol 2e etage"""
dessinerLigneMurGauche(0,0,0,17,2)
dessinerLigneMurGauche(3,3,3,17,2)
dessinerLigneMurDroit(0,0,18,0,2)
for k in range(6):
	dessinerLigneMurGauche(3+3*k,0,3+3*k,1,2)
for k in range(5):
	dessinerLigneMurDroit(4+3*k,2,5+3*k,2,2)
dessinerLigneMurGauche(19,0,19,1,2)	
changerMurGauche(3,20,2,1)
dessinerLigneMurDroit(4,20,4,21,2)

"""Pilier 2e début"""
changerMurGauche(4,7,2,1) 
changerMurGauche(4,11,2,1)
changerMurDroit(6,3,2,1)
changerMurDroit(10,3,2,1)
changerMurDroit(14,3,2,1) 
"""fin pilier"""
"""Murs haut droit"""

dessinerLigneMurDroit(4,16,5,16,2)
changerMurDroit(4,15,2,1)
changerMurGauche(5,15,2,1)
dessinerLigneMurGauche(6,16,6,27,2)
"""murs escalier N3/SdC"""
dessinerLigneMurDroit(1,18,3,18,2)
dessinerLigneMurDroit(1,22,3,22,2)
dessinerLigneMurDroit(1,26,3,26,2)
dessinerLigneMurGauche(1,18,1,29,2)
dessinerLigneMurDroit(1,30,3,30,2)
dessinerLigneMurGauche(4,19,4,20,2)
dessinerLigneMurGauche(4,23,4,24,2)
dessinerLigneMurGauche(4,27,4,28,2)
dessinerLigneMurGauche(5,22,5,23,2)
changerMurGauche(5,18,1,2)
changerMurGauche(5,27,1,2)
changerMurDroit(5,18,1,2)
changerMurDroit(5,20,1,2)
changerMurDroit(5,21,1,2)
changerMurDroit(5,23,1,2)
changerMurDroit(5,25,1,2)
changerMurDroit(5,26,1,2)
changerMurDroit(4,29,1,2)
dessinerLigneMurDroit(5,28,19,28,2)
dessinerLigneMurDroit(6,30,7,30, 2)
dessinerLigneMurGauche(9,28,9,29,2)
dessinerLigneMurGauche(10,28,10,29,2)
dessinerLigneMurGauche(12,28,12,29,2)
dessinerLigneMurGauche(14,28,14,29,2)
changerMurGauche(3,4,2,-1)
changerMurGauche(3,7,2,-1)
changerMurGauche(3,10,2,-1)
changerMurGauche(3,13,2,-1)

dessinerLigneMurDroit(19,14,21,14,2)
dessinerLigneMurDroit(20,16,21,16,2)
dessinerLigneMurDroit(19,19,21,19,2)
dessinerLigneMurGauche(19,14,19,18,2)
dessinerLigneMurGauche(18,29,18,31,2)
dessinerLigneMurGauche(20,28,20,31,2)

changerEscalierB(20,17,2,1)
changerEscalierH(20,17,2,1)
changerEscalierB(4,16,2,1)
changerEscalierH(4,16,2,1)
changerEscalierB(4,17,2,1)
changerEscalierH(4,17,2,1)
changerEscalierB(0,0,2,1)
changerEscalierH(0,0,2,1)
changerEscalierB(18,1,2,1)
changerEscalierB(9,28,2,1)
changerEscalierB(19,31,2,1)
changerEscalierH(20,3,2,1)


##Fin Etage2 VH
rendu()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_g:			
				print("Où êtes vous ?")
				x1, y1, z1 = map(int,input().split())
				print("Où allez vous ?")
				x2, y2, z2 = map(int,input().split())
				dessinerChemin(BFS(x1,y1,z1,x2,y2,z2))
