import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
score = 0

# Constantes pour les types de cellules et les valeurs initiales
G = 1000  # Valeur pour les murs
M = 100   # Valeur initiale pour les cases accessibles

#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]);
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1
   return GUM
            
GUM = PlacementsGUM()   
   
   
      

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange"] )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan"  ]   )
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red"   ]     )         



##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche, score

   # Afficher le score
   canvas.create_text(screeenWidth // 2, 30, text = f"Score: {score}", fill="yellow", font=PoliceTexte)

   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3

   # Afficher le score
   canvas.create_text(screeenWidth // 2, 30, text = f"Score: {score}", fill="yellow", font=PoliceTexte)

  # Afficher le message de pause uniquement si le jeu n'est pas en pause
   if not PAUSE_FLAG:
      canvas.create_text(screeenWidth // 2, screenHeight - 50, text="PAUSE : PRESS SPACE", fill="yellow", font=PoliceTexte)
   else:
      canvas.create_text(screeenWidth // 2, screenHeight - 50, text="", fill="yellow", font=PoliceTexte)

   canvas.create_text(screeenWidth // 2, screenHeight - 20, text=message, fill="yellow", font=PoliceTexte)

       
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

      
def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 2 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 2 ): L.append((-1,0))
   return L


def initialize_distance_grid():
    distance_grid = np.full(TBL.shape, M, dtype=np.int32)
    distance_grid[TBL == 1] = G
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GUM[x][y] == 1:
                distance_grid[x][y] = 0  # Définir la distance à 0 où il y a des pac-gommes
    return distance_grid

def update_distance_grid(grid, distance_grid):
    changes = False
    for x in range(1, LARGEUR - 1):
        for y in range(1, HAUTEUR - 1):
            if grid[x][y] == 0:  # Seulement les cases accessibles
                current_value = distance_grid[x][y]
                # Calculer le minimum des voisins + 1
                new_value = 1 + min(
                    distance_grid[x + 1][y], distance_grid[x - 1][y],
                    distance_grid[x][y + 1], distance_grid[x][y - 1]
                )
                # Mettre à jour si une meilleure valeur est trouvée
                if new_value < current_value:
                    distance_grid[x][y] = new_value
                    changes = True
    return changes

# Créer et mettre à jour la grille des distances
distance_grid = initialize_distance_grid()
while update_distance_grid(TBL, distance_grid):
    pass  # Continuer jusqu'à ce qu'il n'y ait plus de changements


   
def IAPacman():
   global PacManPos, GUM, score
   # Déplacement Pacman
   possible_moves = PacManPossibleMove()
   # Sélectionner le mouvement qui minimise la distance à la pac-gomme la plus proche
   best_move = min(possible_moves, key=lambda move: distance_grid[PacManPos[0] + move[0]][PacManPos[1] + move[1]])
   new_x, new_y = PacManPos[0] + best_move[0], PacManPos[1] + best_move[1]

   # Mange la pac-gomme si présente
   if GUM[new_x][new_y] == 1:
      GUM[new_x][new_y] = 0  # Supprime la pac-gomme
      score += 100  # Augmente le score de 100


   # Met à jour la position de Pacman
   PacManPos[0] = new_x
   PacManPos[1] = new_y
   
   # juste pour montrer comment on se sert de la fonction SetInfo1
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         info = x
         if   x % 3 == 1 : info = "+∞"
         elif x % 3 == 2 : info = ""
         SetInfo1(x,y,info)
   
 
   
def IAGhosts():
   #deplacement Fantome
   for F in Ghosts:
      L = GhostsPossibleMove(F[0],F[1])
      choix = random.randrange(len(L))
      F[0] += L[choix][0]
      F[1] += L[choix][1]
      
  
 

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
   global iteration
   
   if not PAUSE_FLAG : 
      iteration += 1
      if iteration % 2 == 0 :   IAPacman()
      else:                     IAGhosts()
   
   Affiche(PacmanColor = "yellow", message = "message")  
 
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()

 
   
   
    
   
   