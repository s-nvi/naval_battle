import random
from colorama import Fore, Style        # permet une visualisation plus simple lors de l'affichage textuel du jeu
import time    # crée une pause pendant le temps de jeu de l'IA
# random.seed(4)     # sert à avoir le même tirage pour l'IA (utile pendants les phases de test)

Dico = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4 , 'F':5, 'G':6, 'H':7, 'I':8, 'J':9}
Dico_2 = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J'}
Dico_bateaux = {5 : 'Porte Avion', 4 : 'Croiseur', 3 : 'Contre torpilleur', 2 : 'Torpilleur'}

# ------------------------------ création des grilles de jeu -----------------------------------------------------------------------------------------------------------------

# fonction qui renvoie une grille n par m remplis de 0 
def Grille (n:int, m:int)->list:
    return [[0 for _ in range(n)] for _ in range(m)]
    
   
# Fonction d'affichage d'une grille quelconque ( sans censure )
def affichage(grille:list)->None:
    print("     ", end='')
    x = len(grille)
    m=0
    while m < x :
        for i in range(x):
            print(Dico_2[i], end='   ')
            m+=1
    print('\n')
    n=0
    for i in grille:
        print(n,'  ', end ='')
        for j in i:
            if j == 0:
                print(".   ", end= '')
            else:
                print("X   ", end= '')
        print('\n')
        n += 1   
        
 
 
# Renvoie la liste des valeurs à côté de la positon (c,l) 
#(si il y a un 1 dans la liste renvoyée on peut en deduire qu'il y a un bateau dans la zone)
def regles(grille:list, c:int ,l:int)->list:
    ''' la fonction verifie que le nouveau bateau en CL puisse se mettre là '''
    verif =[]
    # point A0
    if l==0 and c==0 :
        x = grille[0:2]
        for i in x:
            liste = i[0 : 2]
            for e in liste:
                verif.append(e)
    # la ligne 0
    elif l == 0 :
        x = grille[0:2]
        for i in x:
            liste = i[c-1 : c+2]
            for e in liste:
                verif.append(e)
    # la colonne A
    elif c == 0 :
        x = grille[l-1 : l+2]
        for i in x :
            liste = i[0:2]
            for e in liste:
                verif.append(e)
    # le centre de la grille
    else:
        x = grille[l-1 : l+2]
        for i in x :
            liste = i[c-1 : c+2]
            for e in liste:
                verif.append(e)
    return verif
        

# Verifie si l'emplacement proposé pour le nouveau bateau est valable
def verif(grille:list, liste_bateaux:list, new_bateau:list, direction:str)-> bool:
    rep = True 
    
    if direction == 'H':
        # verifie si ça sort de la grille
        if ( new_bateau[0][0] + len(new_bateau) ) > 10:
            print("--- Le bateau sort de la grille ---")
            return  False
            
    if direction == 'V':
        # verifie si ça sort de la grille
        if ( new_bateau[0][1] +  len(new_bateau) ) > 10:
            print("--- Le bateau sort de la grille ---")
            return False
                    
    for e in new_bateau:
        for i in liste_bateaux:
            # verifie si ça se superpose avec un bateau déjà placé
            if e in i :
                print("--- Le bateau se superpose avec un autre bateau ---")
                return False
                    
            verif = regles(grille,e[0],e[1])
            if 1 in verif:
                print("--- le bateau est à côté d'un autre bateau ---")
                return False
    return rep
    
    
# Place un bateau de taille n dans la grille du joueur 
def placer_bateau(grille:list, liste_bateaux:list, n:int)->list:
    bon_emplacement = False
    while not bon_emplacement:
        nom = Dico_bateaux[n]
        bateau = input(f"Entrez l'emplacement de votre {nom} ({n} cases) : ").upper()
        c = int(Dico[bateau[0]])
        l = int(bateau[1])
        direction = input("definir sa direction (H ou V) : ").upper()
        new_bateau = []
        for e in range(n):
            if direction == 'H':
                new_bateau.append((c+e,l))
            else:
                new_bateau.append((c,l+e))
        bon_emplacement = verif(grille, liste_bateaux, new_bateau, direction)  
        if bon_emplacement == True :
            for e in new_bateau:
                grille[e[1]][e[0]] = 1
    return new_bateau
    
    
# Place un bateau de taille n dans la grille de jeu de l'IA
def placer_bateau_IA(grille:list, direction:str, n:int, c:int, l:int)->list:
    new_bateau = []
    for e in range(n):
        if direction == 'H':
            new_bateau.append((c+e,l))
        else:
            new_bateau.append((c,l+e))  
    for e in new_bateau:
        grille[e[1]][e[0]] = 1
    return new_bateau
    
    
# Repertorie tous les emplacements valides suivant la grille en construction de l'IA
def possible(grille:list, direction:str, taille:int)->list:
    liste_verif = []
    if direction == 'H':
        for  i in range(len(grille)):
            for j in range(len(grille[i])):
                if j + taille <= 10 :
                    liste = []
                    for x in range(taille):
                        verif = regles(grille, j+x, i)
                        liste = liste + verif
                    if 1 not in liste:
                        liste_verif.append((j,i))
                        
    if direction == 'V':
        for  i in range(len(grille)):
            for j in range(len(grille[i])):
                if i + taille <= 10 :
                    liste = []
                    for x in range(taille):
                        verif = regles(grille, j, i+x)
                        liste = liste + verif
                    if 1 not in liste:
                        liste_verif.append((j,i))
    return liste_verif
    



# ------------------------------- deviner la grille de l'adverser ---------------------------------------------------------------------------------------
    
 
# Fonction crée une grille remplis de ""
def Grille_Mys(n:int ,m:int)->list:
    '''   crée la grille de jeu  '''
    return [["" for _ in range(n)] for _ in range(m)]
    

# Affiche les elemnts decouverts de l'Humain sur une grille inconnu
def affichage_Devine(grille:list)->None:
    print("     ", end='')
    x = len(grille)
    m=0
    while m < x :
        for i in range(x):
            print(Dico_2[i], end='   ')
            m+=1
    print('\n')
    n=0
    for i in grille:
        print(n,' ', end ='')
        for j in i:
            if j == 0:
                print("°   ", end= '')
            elif j == 1:                
                print(Fore.GREEN + 'X   ', end = '')
                print(Style.RESET_ALL, end = '')
            else : 
                print(".   ", end= '')
        print('\n')
        n += 1


# Affiche les decouvertes de l'IA dans la grille du joueur Humain
def affichage_IA(G_mystere:list, G_reponse:list, place:tuple)->None:
    print("    ", end='')
    x = len(G_reponse)
    m=0
    while m < x :
        for i in range(x):
            print(Dico_2[i], end='   ')
            m+=1
    print('\n')
    n=0
    for i in range(x):
        print(n,'  ', end ='')
        for j in range(len(G_reponse[i])):
            # met d'une certaine couleur ce qui vient d'être jouée par l'ia
            if i == place[0] and j == place[1] :
                if G_reponse[i][j]==1:
                    print(Fore.MAGENTA + 'X   ', end = '')
                    print(Style.RESET_ALL, end = '')
                else:
                    print(Fore.MAGENTA  +"°   ", end= '')
                    print(Style.RESET_ALL, end = '')

            elif G_reponse[i][j]==1 and G_mystere[i][j]==1 :
                print(Fore.RED + 'X   ', end = '')
                print(Style.RESET_ALL, end = '')
            elif G_reponse[i][j] == 0 and G_mystere[i][j]==0 :
                print(Fore.BLUE + "°   ", end= '')
                print(Style.RESET_ALL, end = '')
            elif G_reponse[i][j] == 0:
                print(".   ", end= '')
            else:
                print("X   ", end= '')
        print('\n')
        n += 1
  
  
# Renvoie True si un bout de bateau se trouve en c (colonne) ,l (ligne)  
def verif_tire(grille_reponse:list, grille_mystere:list, c:int, l:list)->bool:   
    if grille_reponse[l][c]== 1:
        grille_mystere[l][c] = 1
        return True
    else:
        grille_mystere[l][c]=0
    return False


# Renvoie True si tous les beteaux de l'adversaire ont été trouvés
def tout_trouvee(liste:list)->bool:
    nombre = 0
    for i in liste:
        for j in i:
            if j == 1:
                nombre += 1
    if nombre == 17 :
        return True
    return False


# Renvoie True si un bateau en entier à été trouvé
def bateau_trouvee(liste_bateaux_2:list, c:int, l:int)-> bool:
    for x in range(len(liste_bateaux_2)):
        if (c,l) in liste_bateaux_2[x]:
            L = liste_bateaux_2[x]
            indice = L.index((c,l))
            liste_bateaux_2[x][indice]=1
        
            rep = 0
            for e in L:
                if e == 1:
                    rep += 1
            if rep == len(L):
                print("--- touché coulé ---")
                return True

            else:
                print("--- touché ---")
                return False
               

# la decouverte d'un bateau cré des changements:
# Indique dans la grille de jeu que tout autour de ce bateau il n'y en a pas 
def decouverte(jeu:list, bateau:list)->list:
    ''' la fonction verifie que le nouveau bateau en CL puisse se mettre là '''
    for t in bateau:
        for elem in t:
            c = t[0]
            l = t[1]
        if c == 0 and l == 0:
            x = jeu[0:2]
            ligne = 0
            for i in x:
                for e in range(0,2):
                    jeu[ligne][e] = 0
                ligne = ligne + 1
        
        elif c == (len(jeu[0]) - 1) and l == 0 :
            x = jeu[0:2]
            ligne = 0
            for i in x:
                for e in range(c-1,c+1):
                    jeu[ligne][e] = 0
                ligne = ligne + 1
                
        elif l == 0 :
            x = jeu[0 : 2]
            ligne = 0
            for i in x:
                for e in range(c-1 , c+2):
                    jeu[ligne][e] = 0
                ligne += 1   
                
        elif c == 0 :
            x = jeu[l-1 : l+2]
            ligne = l-1
            for i in x:
                for e in range(0,2):
                    jeu[ligne][e] = 0
                ligne = ligne + 1   
        
        elif c == (len(jeu[0]) - 1):
            x = jeu[l-1 : l+2]
            ligne = l-1
            for i in x:
                for e in range(c-1,c+1):
                    jeu[ligne][e] = 0
                ligne = ligne + 1 
                
        else : 
            x = jeu[l-1 : l+2]
            ligne = l-1
            for i in x:
                for e in range(c-1,c+2):
                    jeu[ligne][e] = 0
                ligne = ligne + 1
    for t in bateau:
        for elem in t:
            jeu[t[1]][t[0]] =1
    return jeu                 
       
    
# trie dans l'ordre coissant une liste de tuples (x, y) en regardant y                                              VERIFIER QUE CE NE SOIT PAS X
def Sort_Tuple(tup):
    lst = len(tup)
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j+1]
                tup[j + 1] = temp
    return tup

 
 
# Liste repertoriant les endroits où l'IA peut proposer de toucher un bateau,  IA level1                                      REFORMULER
def choix_possible_IA_1(grille_mystere:list, proposition:list, LB_en_cours:list)->list:
    possible = []
    for i in range(len(grille_mystere)):
        for j in range(len(grille_mystere)):
            if (j,i) not in proposition:
                possible.append((j,i))
    return possible


# Verifie si (C, L) peut être proposé, IA level2
def toujoursplus(grille_mystere:list, C:int , L:int, proposition:list)-> bool:
    # c,l n'a pas déjà été proposé
    if (C,L) not in proposition:
        # c,l appartient à la grille
        if 0 <= C <= 9 and 0 <= L <= 9 :
            # pas déjà au courent qu'il n'y a pas de bateau
            if grille_mystere[L][C] != 0:
                return True
    return False        
    
 
# Liste repertoriant les endroits où l'IA peut proposer de toucher un bateau,  IA level2 
def choix_possible_IA_2(grille_mystere:list, proposition:list, LB_en_cours:list)->list:
    possible = []
    taille = len(LB_en_cours)
    
    if taille == 1:
        for t in LB_en_cours:
            c = t[0]
            l = t[1]
        if toujoursplus(grille_mystere, c+1, l, proposition) == True :
            possible.append((c+1,l)) 
        if toujoursplus(grille_mystere, c-1, l, proposition) == True :
            possible.append((c-1,l))
        if toujoursplus(grille_mystere, c, l-1, proposition) == True :
            possible.append((c,l-1))
        if toujoursplus(grille_mystere, c, l+1, proposition) == True :
            possible.append((c,l+1))
    
    elif taille > 1 :
        # bateau horizontale
        if LB_en_cours[0][1] == LB_en_cours[1][1]:
            LB_en_cours = sorted(LB_en_cours)
            l = LB_en_cours[0][1]
            if toujoursplus(grille_mystere, LB_en_cours[0][0]-1, l, proposition) == True: 
                possible.append((LB_en_cours[0][0]-1, l))
            if toujoursplus(grille_mystere, LB_en_cours[taille-1][0] + 1 , l, proposition) == True: 
                possible.append((LB_en_cours[taille-1][0] + 1 , l))

        elif LB_en_cours[0][0] == LB_en_cours[1][0]:
            Sort_Tuple(LB_en_cours)
            c = LB_en_cours[0][0]
            if toujoursplus(grille_mystere, c , LB_en_cours[0][1]-1, proposition) == True: 
                possible.append((c, LB_en_cours[0][1]-1))
            if  toujoursplus(grille_mystere, c , LB_en_cours[taille-1][1]+1, proposition) == True: 
                possible.append((c, LB_en_cours[taille-1][1]+1 ))
    
    else:
        for i in range(len(grille_mystere)):
            for j in range(len(grille_mystere)):
                if toujoursplus(grille_mystere, j, i, proposition) == True :
                    possible.append((j,i))

    return possible
              
               
# ------------------------------ fonctions principales ---------------------------------------------------------------------------------------------------------------------------               

# l'Humain créé sa grille de jeu     
def CH(grille:list)->list:
    L =  [5,4,3,3,2]
    liste_bateaux = []
    for x in L:
        affichage(grille)
        liste_bateaux.append(placer_bateau(grille,liste_bateaux,x))
    affichage(grille)
    return liste_bateaux
    
    
# L'IA créé sa grille de jeu (totalement au hasard)
def CIA(grille:list)->list:
    L =  [5,4,3,3,2]
    liste_bateaux = []
    for x in L:
        L_direction = ['H','V']
        vers = random.randint(0,1)
        direction = L_direction[vers]
        # direction = 'H'                # test
        position = random.choice(possible(grille, direction, x))
        liste_bateaux.append(placer_bateau_IA(grille, direction, x , position[0], position[1]))
    return liste_bateaux


# renvoie la liste des proposition qu'a donné l'Humain
# tout en effectuant des des changements, c'est la fonction qui represente le tour de jeu d'un humain
def tour_humain(grille_mystere:list, grille_reponse:list, proposition:list, liste_bateaux_2:list, liste_indepandante:list, tour:int)->list:
    new_proposition = False
    affichage_Devine(grille_mystere)
    while not new_proposition:
        lieu = input(f"Viser un bateau ({tour}) : ").upper()
        c = int(Dico[lieu[0]])
        l = int(lieu[1])
        
        if (c,l) not in proposition:
            proposition.append((c,l))
            new_proposition = True
            if verif_tire(grille_reponse, grille_mystere, c, l) == True:
                bateau_trouvee(liste_bateaux_2, c, l)
                
                
                for ligne in range(len(liste_bateaux_2)):
                    rep = 0
                    for e in liste_bateaux_2[ligne]:
                        if e == 1:
                            rep += 1
                        if rep == len(liste_bateaux_2[ligne]):      #signifie que tous les bouts du bateau à était trouvé
                            decouverte(grille_mystere, liste_indepandante[ligne])
            else:
                print("--- à l'eau ---")
        else:
            print("--- vous avec déjà proposé cette emplacement ---")
    return proposition


# renvoie la liste du bateau quiest en train d'être trouvé (utile pour l'IA level2)
# tout en effectuant des des changements, c'est la fonction qui represente le tour de jeu d'une IA
def tour_IA(grille_mystere:list, grille_reponse:list, liste_bateaux_a_trouve:list, proposition:list, LB_en_cours:list, version)->None:
    if version == "1":
        choix = choix_possible_IA_1(grille_mystere,proposition,LB_en_cours)
    else:
        choix = choix_possible_IA_2(grille_mystere,proposition,LB_en_cours)
    place = random.choice(choix) 
    c = place[0]
    l = place[1]
    proposition.append((c,l))
    if verif_tire(grille_reponse, grille_mystere, c, l) == True:
        LB_en_cours.append((c,l))
        verif = bateau_trouvee(liste_bateaux_a_trouve, c, l)
        # remet les conteurs à zero quand un bateau à etait trouvé en entier
        if verif == True:
            decouverte(grille_mystere, LB_en_cours)
            LB_en_cours = []
    affichage_IA(grille_mystere, grille_reponse, (l,c))
    return LB_en_cours


# --------------------- Programme principale ------------------------------------------------------------------------------------------------------------------------------

def Jeu():
    grille_joueur_1 = Grille(10,10)
    grille_joueur_2 = Grille(10,10)
    grille_mystere_J1 = Grille_Mys(10,10)
    grille_mystere_J2 = Grille_Mys(10,10)

    J1 = input('joueur 1 (H ou IA) : ').upper()
    J2 = input('joueur 1 (H ou IA) : ').upper()
    tour = 0
    fin_partie = False
    if J1 == J2:
        # IA vs IA 
        if J1 == 'IA':
            # choisir la version de l'IA1 et de L'IA2 
            version_J1 = input("choisir la version de l'IA_1 (1 ou 2)")
            version_J2 = input("choisir la version de l'IA_2 (1 ou 2)")
            bateau_IA_1 = CIA(grille_joueur_1)
            bateau_IA_2 = CIA(grille_joueur_2)
            
            LB_en_cours_IA_1 = []
            proposition_IA_1 = []
            LB_en_cours_IA_2 = []
            proposition_IA_2 = []
            
            while not fin_partie:
                tour += 1
                LB_en_cours_IA_1 = tour_IA(grille_mystere_J1, grille_joueur_2, bateau_IA_2, proposition_IA_1, LB_en_cours_IA_1,version_J1)
                if tout_trouvee(bateau_IA_2) == True:
                    fin_partie = True
                    print(f"L'IA_1 a gagné en {tour} coups")


                else:
                    LB_en_cours_IA_2 = tour_IA(grille_mystere_J2, grille_joueur_1, bateau_IA_1, proposition_IA_2, LB_en_cours_IA_2,version_J2)
                    if tout_trouvee(bateau_IA_1) == True:
                        fin_partie = True
                        print(f"L'IA_2 a gagné en {tour}coups")
        # Humain vs Humain                 
        else :
            continuer = input("Voulez vous vraiment jouer dans ce mode de jeu ? (oui ou non) ").upper()
            if continuer == 'OUI':
                print("--- joueur 1 veuillez faire votre grille ---")
                bateaux_H1 = CH(grille_joueur_1)
                proposition_J1 =[]
                liste_indepandante_J1 = []
                print("--- C'est maintenant au joueur 2 de faire votre grille ---")
                bateaux_H2 = CH(grille_joueur_2)
                proposition_J2 = []
                liste_indepandante_J2 = []
                
                while not fin_partie:
                    tour += 1
                    print("--- tour Joueur 1 ---\n")
                    tour_humain(grille_mystere_J1, grille_joueur_2, proposition_J1, bateaux_H2, liste_indepandante_J1, tour)
                    if tout_trouvee(bateaux_H2) == True:
                        fin_partie = True
                        print('   --- fin de partie ---')
                        print(f"Le joueur 1 a gagné en {tour} coups")
                    else:
                        print("--- tour Joueur 2 ---\n")
                        tour_humain(grille_mystere_J2, grille_joueur_1, proposition_J2, bateaux_H1, liste_indepandante_J2, tour)
                        if tout_trouvee(bateaux_H1) == True:
                            fin_partie = True
                            print('   --- fin de partie ---')
                            print(f"Le joueur 2 a gagné en {tour} coups")
            else:
                print("--- Relancez un partie pour choisir un nouveau mode :) ---")
            
            
            
    else:
        # Humain vs IA (1 ou 2)

        bateaux_IA = CIA(grille_joueur_2)
        version = input("la version de l'IA contre laquel vous voulez jouer (1 ou 2)")
        print("--- l'ia à crée sa grille\n")     
        time.sleep(1)
        print("--- à vous de créer votre grille de jeu : ")
        #grille_joueur_1 = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]]
        #bateaux_H = [[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], [(6, 3), (6, 4), (6, 5), (6, 6)], [(8, 1), (8, 2), (8, 3)], [(2, 7), (3, 7), (4, 7)], [(5, 9), (6, 9)]]

        bateaux_H = CH(grille_joueur_1)
        proposition_H = []
        LB_en_cours_IA = []
        proposition_IA = []
        liste_indepandante = []
        for e in bateaux_IA:
            liste_indepandante.append(e.copy())
            
            
        while not fin_partie:
            tour += 1
            print("--- votre tour ---\n")
            tour_humain(grille_mystere_J1, grille_joueur_2, proposition_H, bateaux_IA, liste_indepandante, tour)
            if tout_trouvee(bateaux_IA) == True:
                fin_partie = True
                print('   --- fin de partie ---')
                print(f"vous avez gagné en {tour} coups")
            else:
                print("--- tour de l'ia ---\n")
                time.sleep(2)
                LB_en_cours_IA = tour_IA(grille_mystere_J2, grille_joueur_1, bateaux_H, proposition_IA, LB_en_cours_IA, version)
                if tout_trouvee(bateaux_H) == True:
                    fin_partie = True
                    print('   --- fin de partie ---')
                    print(f"L'IA a gagné en {tour} coups")
                    print("--- voici la grille que vous diviez deviner ---")
                    affichage(grille_joueur_2)


Jeu()
        
 