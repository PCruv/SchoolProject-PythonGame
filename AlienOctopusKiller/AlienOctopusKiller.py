"""Alien Octopus Killer par Pierre CRUVEILLER et Jules FILIOT ; Projet Python 3ETI CS-DEV Groupe A"""

from tkinter import * 
from random import *
from PIL import ImageTk,Image
from tkinter import messagebox

##GESTION DU DEROULEMENT
def start(): 
   """Cettte fonction gère la mise en place de la structure du jeu (variables structurelles et création environnement)"""
   global compteur, rebond, tirs, wave, tireurs,immortal,BossHealth,alien,alienImg,score,canWave
   can.delete(logoBackground)
   creationBackGround()
   wave = 0
   tireurs = 6
   compteur = 0
   rebond = 0
   tirs = 0
   immortal=0
   BossHealth=16
   score=0
   alien=[]
   alienImg=[]
   creationCoeur()
   creationAmmo()
   creationVaisseau()
   creationScore()
   canWave=can.create_text(50,780,fill="white",font="Impact 20 bold",text="Wave "+str(wave))   
   deplacement()
   bou2["command"] = "none"
   return

def gameOver():   
   """Nettoie le terrain et affiche l'écran Game Over"""
   can.delete("all")
   bou2["text"] = "Rejouer"
   creationLogoGameOver()
   bou2["command"] = start
   popupScoreEntry()    #lance la fonction qui gere la fenetre qui demande au joueur son pseudo et affiche son score, son highscore
   return
def apropos():
   """Fenetre popup qui affiche le a propos"""
   global fenpopApropos
   fenpopApropos = Toplevel()
   fenpopApropos.wm_title("A propos du jeu")
   canApropos = Canvas(fenpopApropos, bg="black", height=700, width=700)
   canApropos.grid(column=0, row=0)
   imgApropos = Image.open("apropos.png")
   imgApropos = ImageTk.PhotoImage(imgApropos)
   canApropos.create_image(400, 400, image = imgApropos)
   boutonQuitter = Button(fenpopApropos, text = "Quitter", command = fenpopApropos.destroy)
   boutonQuitter.grid(row = 1, column = 0)
   fenpopApropos.mainloop()
   return

def creationLogoStart():   
   """Affiche le logo du jeu au démarrage (AlienOctopusKiller)"""
   global logoBackground, imgLogoStart
   imgLogoStart = Image.open("alienoctopusLOGOdark.png")
   imgLogoStart = ImageTk.PhotoImage(imgLogoStart)
   logoBackground = can.create_image(400, 400, image = imgLogoStart)
   return

def creationLogoGameOver(): 
   """Affiche l'écran Game Over"""
   global LeLogoGameOver, imgLogoGameOver
   imgLogoGameOver = Image.open("alienoctopusGAME_OVER_LOGOdark.png")
   imgLogoGameOver = ImageTk.PhotoImage(imgLogoGameOver)
   LeLogoGameOver = can.create_image(400, 400, image = imgLogoGameOver)
   return

def creationBackGround():
   """règle le fond d'écran de jeu"""
   global imageBackground, LeBackground
   imageBackground = Image.open("space.jpg")
   imageBackground = ImageTk.PhotoImage(imageBackground)
   LeBackground = can.create_image(400, 400, image=imageBackground)
   return


def creationScore():    
    """affiche le score sur l'écran (en bas à gauche)"""
    global canScore
    canScore=can.create_text(150,780,fill="white",font="Impact 15 bold",text="Score : 0")
def Score(unAlien): 
    """ajuste le score pendant le jeu selon le type d'ennemi tué"""
    global score,canScore
    typeAlien=unAlien[1]
    if typeAlien==0:
        score+=50
    elif typeAlien==1:
        score+=100
    elif typeAlien==5:
        score+=250
    else:
        score+=500
    if score%2000==0 and alien[-1][1]!=5:
        creationBonusAlien()
    can.delete(canScore)
    canScore=can.create_text(150,780,fill="white",font="Impact 15 bold",text="Score : "+str(score))
    return
    
def AjoutScoreboard(pseudo, ScoreDuJoueur):
   """Actualise le highscore d'un joueur, si le joueur n'avait jamais jouer la fonction crée une entrée avec son nom et son score"""
   file = open("scoreboard.txt", "r")
   Lscore = file.readlines()
   for indiceLigne in range(len(Lscore)):
       ligne = Lscore[indiceLigne]     #ligne qu'on observe d'indice: indiceLigne dans la liste Lscore
       ligne = ligne[:-1]
       Ljoueur = ligne.split(":")  #liste avec pseudo d'un joueur en indice 0 et son score en indice 1
       if Ljoueur[0] == pseudo:
           if int(Ljoueur[1]) < int(ScoreDuJoueur):    #on teste si le joueur a réaliser son highscore personnel
               LaNewLigne = Ljoueur[0] + ":" + str(ScoreDuJoueur) + "\n"
               Lscore[indiceLigne] = LaNewLigne    #on remplace l'ancienne ligne avec la nouvelle qui contient le score mis à jour dans la liste qui contient toutes les lignes
               file.close()
               file = open("scoreboard.txt", "w")
               for UneLigne in Lscore:
                   file.write(UneLigne)
               file.close()
               return
           elif int(Ljoueur[1]) >= int(ScoreDuJoueur): #si le score du joueur est inférieur au précédent on sort de la fonction
               return
   #ici on ajoute une nouvelle ligne au fichier texte avec le pseudo et le score du joueur si on ne l'a pas trouvé dans le fichier
   UneNouvelleLigne = pseudo + ":" + str(ScoreDuJoueur) + "\n"
   file.close()
   file = open("scoreboard.txt", "a")
   file.write(UneNouvelleLigne)
   file.close()
   return
def RechercheHighScore():
   """Recherche le highscore global dans le fichier des scores"""
   file = open("scoreboard.txt", "r")
   Lscore = file.readlines()
   highscore = 0
   joueur = ""
   for ligne in Lscore:
       ligne = ligne[:-1]
       Ljoueur = ligne.split(":")
       if int(Ljoueur[1]) > highscore:
           highscore = int(Ljoueur[1])
           joueur = Ljoueur[0]
   return highscore, joueur
def RechercheHighScoreJoueur(pseudo):
   """Recherche le highscore d'un joueur en particulier (donc pas le global)"""
   file = open("scoreboard.txt", "r")
   Lscore = file.readlines()
   for ligne in Lscore:
       ligne = ligne[:-1]
       Ljoueur = ligne.split(":")
       if Ljoueur[0] == pseudo:
           return int(Ljoueur[1])
   return False
# def RechercheTop5Highscore():         ##Fonction en cours de création pour afficher les 5 meilleurs score du jeu
#     """Recherche dans le fichier score les 5 meilleurs score"""
#     file = open("scoreboard.txt", "r")
#     Lscore = file.readlines()
#     LscoreOptimale = []  #liste sous forme [[pseudo, score], [pseudo, score]]
#     Lhighscores = []
#     JoueurARetirerDeLscore = ""
#     highscore = 0
#     for ligne in Lscore:
#         ligne = ligne[:-2]
#         Ljoueur = ligne.split(":")
#         LscoreOptimale.append(Ljoueur)
#     for indiceScoreEnRecherche in range(0, 5):
#         for UnJoueur in LscoreOptimale:
#             if int(UnJoueur[1]) > highscore:
#                 highscore = int(UnJoueur[1])
#                 JoueurARetirerDeLscore = UnJoueur
#         Lhighscores.append(highscore)
#         LscoreOptimale.remove(JoueurARetirerDeLscore)
#         highscore = 0
#     print(Lhighscores)
#     return Lhighscores
def GestionScoreGameOver(pseudo):
   """Gère le score du joueur à la fin de la partie: l'ajoute au fichier avec son pseudo et lui affiche le score de la partie qu'il vient de réaliser et son highscore"""
   scoreJoueur = int(score)
   AjoutScoreboard(pseudo, scoreJoueur)
   highscoreJoueur = RechercheHighScoreJoueur(pseudo)
   popupInfoScore(pseudo, scoreJoueur, highscoreJoueur)
   return
def popupInfoScore(pseudo, scoreJoueur, highscoreJoueur):
   """Fenetre popup qui affiche le score réalisé par le joueur et son highscore"""
   fenpop2 = Toplevel()
   fenpop2.wm_title("Info Score")
   textpseudo = Label(fenpop2, text = pseudo)
   textpseudo.grid(row = 0, column =0)
   textinfo1 = Label(fenpop2, text = "Votre score à cette partie : ")
   textinfo1.grid(row = 1, column = 0)
   affichageinfo1 = Label(fenpop2, text = scoreJoueur)
   affichageinfo1.grid(row = 1, column = 1)
   textinfo2 = Label(fenpop2, text = "Votre highscore : ")
   textinfo2.grid(row = 2, column = 0)
   affichageinfo2 = Label(fenpop2, text = highscoreJoueur)
   affichageinfo2.grid(row = 2, column = 1)
   boutonQuitter = Button(fenpop2, text = "OK", command = fenpop2.destroy)
   boutonQuitter.grid(row = 3, column = 0)
   return
def popupScoreEntry():
   """Fenetre popup qui demande au joueur d'entrer son pseudo"""
   global fenpop, entryPseudo
   fenpop = Toplevel()
   fenpop.wm_title("Entrez votre pseudo")
   entryPseudoText = Label(fenpop, text = "Entrez votre pseudo (4 caractères max) : ")
   entryPseudoText.grid(row = 0, column = 0)
   entryPseudo = Entry(fenpop, bd = 2)
   entryPseudo.grid(row = 0, column = 1)
   boutonQuitter = Button(fenpop, text = "Valider", command = lambda : popupGetPseudoEtQuitter())
   boutonQuitter.grid(row = 1, column = 0)
   return
def popupGetPseudoEtQuitter():
   """Récupère le pseudo du joueur et quitte la fenetre"""
   pseudo = entryPseudo.get()
   if isPseudoOk(pseudo):
       GestionScoreGameOver(pseudo)
       fenpop.destroy()
       return
   elif not isPseudoOk(pseudo):
       fenpop.destroy()
       popupScoreEntry()
       messagebox.showwarning("Pseudo Invalide", "Veuillez entrer un pseudo valide svp !")
       return
   return
def isPseudoOk(LePseudo):
   """Test si le pseudo est de forme valide (pas composé uniquement d'espaces et pas vide et pas plus de 4 caractères"""
   if len(LePseudo) > 4 or len(LePseudo) == 0:
       return False
   else:
       compteurSpaces = 0
       for caractere in LePseudo:
           if caractere == " ":
               compteurSpaces += 1
       if compteurSpaces == len(LePseudo):
           return False
   return True


    
def creationCoeur(): 
    """crée les vies du joueur et les affiche"""
    global vies, imgC
    imgC = Image.open("heart.png")
    imgC = ImageTk.PhotoImage(imgC)
    coeur1 = can.create_image(350, 780, anchor=CENTER, image=imgC)
    coeur2 = can.create_image(400, 780, anchor=CENTER, image=imgC)
    coeur3 = can.create_image(450, 780, anchor=CENTER, image=imgC)
    vies = [coeur1, coeur2, coeur3]
    return

def LifeFill(): 
    """remplit la vie du joueur"""
    for coeur in vies:
        can.delete(vies[-1])
        del vies[-1]
    creationCoeur()
    return

def creationAmmo(): 
    """crée le système de munitions du joueur et les affiche"""
    global ammo, imgAmmo, txtAmmo
    imgAmmo = Image.open("ammo.png")
    imgAmmo = ImageTk.PhotoImage(imgAmmo)
    txtAmmo = can.create_image(550, 780, anchor=CENTER, image=imgAmmo)
    ammo1 = can.create_oval(590, 770, 600, 790, width=1, fill="yellow", outline="lightyellow")
    ammo2 = can.create_oval(610, 770, 620, 790, width=1, fill="yellow", outline="lightyellow")
    ammo3 = can.create_oval(630, 770, 640, 790, width=1, fill="yellow", outline="lightyellow")
    ammo = [ammo1, ammo2, ammo3]
    return

def Wave():  
    """gère le renouvellement des vagues d'alien et des niveaux Boss"""
    global wave,tireurs,canWave
    can.delete(canWave)
    canWave=can.create_text(50,780,fill="white",font="Impact 15 bold",text="Wave  "+str(wave))
    if wave==0:
            creationMur()
            creationRemparts()
    if not alien:
        wave+=1
        tireurs+=1
        if wave%3==0:
            for UnMur in murs:
                can.delete(UnMur)
            for UnRempart in remparts:
                can.delete(UnRempart)
            creationMur()
            creationRemparts()
            BossLevel()
        else:
            creationAlien()
    return

##GESTION DES BOSS
def BossLevel(): 
    """Choisit aléatoirement l'un des 3 Boss pour le niveau Boss concerné"""
    global bosslifebar
    bosslifebar=can.create_rectangle(100,10,700,30,fill="green")   #Génère la barre de vie du boss
    choixBoss=randint(1,3)
    if choixBoss==1:
        BossUbik()
    elif choixBoss==2:
        BossCapone()
    else:
        BossBizarro()
    return

def BossUbik():  
    """Génère le Boss appelé Ubik"""
    global imgUbik,BossTitle
    BossTitle=can.create_text(150,50,fill="white",font="Impact 20 bold",text="Boss Ubik")
    imgUbik=Image.open("bossUbik.png")
    imgUbik=ImageTk.PhotoImage(imgUbik)
    Ubik=can.create_rectangle(200,250,600,300,outline="")
    UbikImg=can.create_image(400,200,anchor=CENTER,image=imgUbik)
    alien.append((Ubik,2))
    alienImg.append(UbikImg)
    return
    
def BossCapone():  
    """Génère le Boss appelé Capone"""
    global imgCapone,BossTitle
    BossTitle=can.create_text(150,50,fill="white",font="Impact 20 bold",text="Boss Capone")
    imgCapone=Image.open("bossCapone.png")
    imgCapone=ImageTk.PhotoImage(imgCapone)
    Capone=can.create_rectangle(310,100,490,300,outline="")
    CaponeImg=can.create_image(400,200,anchor=CENTER,image=imgCapone)
    alien.append((Capone,3))
    alienImg.append(CaponeImg)
    return
    
def BossBizarro(): 
    """Génère le Boss appelé Bizarro et ses trois soldats Bizarrini"""
    global imgBizarro,BossTitle,imgBizarrini
    BossTitle=can.create_text(150,50,fill="white",font="Impact 20 bold",text="Boss Bizarro")
    imgBizarrini=Image.open("Bizarrini.png")
    imgBizarrini=ImageTk.PhotoImage(imgBizarrini)
    for i in range(3):
        alien.append((can.create_rectangle(i*200+90,240,i*200+180,295,outline=""),6))
        alienImg.append(can.create_image(i*200+135, 265, anchor=CENTER, image=imgBizarrini))
    imgBizarro=Image.open("bossBizarro.png")
    imgBizarro=ImageTk.PhotoImage(imgBizarro)
    Bizarro=can.create_rectangle(30,70,170,170,outline="")
    BizarroImg=can.create_image(100,100,anchor=CENTER,image=imgBizarro)
    alien.append((Bizarro,4))
    alienImg.append(BizarroImg)
    return

def BossLifeBar(laBarre): 
    """Gère la barre de vie d'un Boss, il faut lui tirer dessus 18 fois pour le tuer"""
    global BossHealth,BossTitle
    if BossHealth>=2:
            BossHealth-=1
            coords=can.coords(laBarre)
            can.delete(laBarre)
            laBarre=can.create_rectangle(coords[0],coords[1],coords[2]-37.5,coords[3],fill="red")
    else:  #détruit la barre de vie et tue le boss
            Score(alien[0])
            for i in range(len(alien)):
                can.delete(alien[i][0])
                can.delete(alienImg[i])
                del alien[i]
                del alienImg[i]
            can.delete(laBarre)
            laBarre=can.create_rectangle(0,0,0,0,outline="")
            BossHealth=16
            LifeFill()
            can.delete(BossTitle)
    return laBarre
            
##GESTION DES ALIENS
        
def creationAlien():    
    """création de l'armée alien"""
    global nbNonTireurs,nbTireurs,imgA,imgA2
    imgA = Image.open("Poulpe1.png")
    imgA = ImageTk.PhotoImage(imgA)
    imgA2 = Image.open("Poulpe2.png")
    imgA2 = ImageTk.PhotoImage(imgA2)
    nbNonTireurs=0
    nbTireurs=0
    for i in range(6):
        for j in range(3):
            if Tireur(): #la fonction tireur décide aléatoirement si on place un tireur ou non
                nbTireurs+=1
                alien.append((can.create_rectangle(i*100+100,50+j*100,i*100+170,80+j*100,outline=""),1))
                alienImg.append(can.create_image(i*100+135, 65+j*100, anchor=CENTER, image=imgA2))

            else:
                nbNonTireurs+=1
                alien.append((can.create_rectangle(i*100+100,50+j*100,i*100+170,80+j*100,outline=""),0))
                alienImg.append(can.create_image(i*100+135, 65+j*100, anchor=CENTER, image=imgA))
    return

def creationBonusAlien():
    """création de l'alien bonus lorsque tous les tireurs ont été tués ou lorsque le score est un multiple de 2000"""
    global imgBA
    imgBA=Image.open("ufo.png")
    imgBA=ImageTk.PhotoImage(imgBA)
    alien.append(((can.create_rectangle(85,200,215,240,outline="")),5))
    alienImg.append(can.create_image(150, 185, anchor=CENTER, image=imgBA))

def Tireur():  
    """randomise le placement des aliens tireurs dans l'armée"""
    global tireurs
    if nbTireurs<tireurs:
        n=randint(1,18)
        if n<tireurs or nbNonTireurs>=18-tireurs:
            return True
    else:
        return False

def deplacement():   
    """Gestion du deplacement des aliens"""
    global dx,dy,compteur,rebond,dxb
    Wave()
    if compteur==0:         #condition pour le premier lancement de l'alien
        dx=2
        dxb=2.2*dx
    compteur+=1
    dy=0
    if rebond!=0 and rebond%2==0:   #fait descendre l'armée tous les 2 rebonds
        dy=20
        rebond=0
    contactAlienVaisseau()   #détruit le vaisseau si les aliens entrent en contact avec
    for i in range (len(alien)):     
        if can.coords(alien[i][0])[2]>800 or can.coords(alien[i][0])[0]<0:
            if alien[i][1]==5 or alien[i][1]==4:
                dxb=-1*dxb
            else:
                dx= -1 * dx
                rebond+=1
            break
    BonusAlien=1
    for i in range(len(alien)):  #teste le type de l'alien et le fait agir en conséquence
        if alien[i][1]!=0:
            BonusAlien=0
        if alien[i][1]==1:
            TirAlien(alien[i][0])                
        if alien[i][1]==2:
            TirUbik(alien[i][0])
        if alien[i][1]==3:
            TirCapone(alien[i][0])
        if alien[i][1]==6:
            dy=0
            TirBizarrini(alien[i][0])
        if alien[i][1]==5:
            TirAlienBonus(alien[i][0])
            can.move(alien[i][0],dxb,-0.01)
            can.move(alienImg[i],dxb,-0.01)
            break
        if alien[i][1]==4:
            if len(alien)==1:
                TirBizarrini(alien[i][0])
            can.move(alien[i][0],dxb,-0.01)
            can.move(alienImg[i],dxb,-0.01)
            break
        can.move(alien[i][0],dx,dy)
        can.move(alienImg[i],dx,dy)
    if BonusAlien==1:
        creationBonusAlien()


    fen.after(10,deplacement)
    return

def TirAlien(unAlien):  
    """fait tirer l'alien aléatoirement"""
    n=randint(1,20*len(alien))
    if n==1:
            AlienBullet=can.create_oval(can.coords(unAlien)[0]+30,can.coords(unAlien)[1]+25,can.coords(unAlien)[2]-30,can.coords(unAlien)[3]+25,width=1,fill="red",outline="lightpink",tags="bullet")
            deplacementTirAlien(AlienBullet)
    return
    
def TirUbik(unAlien): 
    """crée les triple-tirs du Boss Ubik"""
    n=randint(1,40)
    if n==1:
            UbikBullet1=can.create_oval(can.coords(unAlien)[0]+195,can.coords(unAlien)[1]+75,can.coords(unAlien)[2]-195,can.coords(unAlien)[3]+55,width=1,fill="red",outline="lightpink",tags="bullet")
            UbikBullet2=can.create_oval(can.coords(unAlien)[0]+385,can.coords(unAlien)[1]+45,can.coords(unAlien)[2]-5,can.coords(unAlien)[3]+25,width=1,fill="red",outline="lightpink",tags="bullet")
            UbikBullet3=can.create_oval(can.coords(unAlien)[0]+5,can.coords(unAlien)[1]+45,can.coords(unAlien)[2]-385,can.coords(unAlien)[3]+25,width=1,fill="red",outline="lightpink",tags="bullet")

            deplacementTirAlien(UbikBullet1)
            deplacementTirAlien(UbikBullet2)
            deplacementTirAlien(UbikBullet3)
    return
    
def TirCapone(unAlien): 
    """crée les tirs du Boss Capone"""
    n=randint(1,40)
    if n==1:
        CaponeBullet=can.create_oval(can.coords(unAlien)[0]+82,can.coords(unAlien)[3],can.coords(unAlien)[2]-82,can.coords(unAlien)[3]+20,width=1,fill="white",outline="black",tags=("bullet","Caponebullet"))
        deplacementTirAlien(CaponeBullet)
    return
def TirBizarrini(unAlien): 
    """crée les tirs des soldats du boss Bizarro"""
    n=randint(1,20*len(alien))
    if n==1:
        BizarriniBullet=can.create_oval(can.coords(unAlien)[0]+50,can.coords(unAlien)[1]+55,can.coords(unAlien)[2]-50,can.coords(unAlien)[3]+25,width=1,fill="lightblue",outline="white",tags=("bullet","Bizarrinibullet"))
        deplacementTirAlien(BizarriniBullet)
    return
def TirAlienBonus(unAlien): 
    """crée les tirs de l'alien bonus"""
    n=randint(1,20*len(alien))
    if n==1:
            AlienBullet=can.create_oval(can.coords(unAlien)[0]+70,can.coords(unAlien)[1]+55,can.coords(unAlien)[2]-70,can.coords(unAlien)[3]+35,width=1,fill="green",outline="lightgreen",tags="bullet")
            deplacementTirAlien(AlienBullet)
    return
    
def deplacementTirAlien(AlienBullet): 
    """gère le déplacement des tirs aliens"""
    global sx,sy,murs
    sx=0
    sy=6
    if can.coords(AlienBullet)[3]>can.coords(vaisseau)[1] and (can.coords(vaisseau)[2]>can.coords(AlienBullet)[0]+5>can.coords(vaisseau)[0]):
            can.delete(AlienBullet)
            Vies() #enlève une vie au joueur s'il est touché
            return
    elif can.coords(AlienBullet)[3]>790:
        can.delete(AlienBullet)
        return
    elif can.coords(AlienBullet)[3]>640: #gère les impacts sur les murs
        if can.coords(murs[0])[0]<can.coords(AlienBullet)[0]<can.coords(murs[0])[2]:
            can.delete(AlienBullet)
            murs[0]=destructionMur(murs[0])
            return
        elif can.coords(murs[1])[0]<can.coords(AlienBullet)[0]<can.coords(murs[1])[2]:
            can.delete(AlienBullet)
            murs[1]=destructionMur(murs[1])
            return
        elif can.coords(murs[2])[0]<can.coords(AlienBullet)[0]<can.coords(murs[2])[2]:
            can.delete(AlienBullet)
            murs[2]=destructionMur(murs[2])
            return
    for i in range(len(remparts)): #gère les impacts sur les remparts
        if destructionRempart(remparts[i], AlienBullet):
            can.delete(AlienBullet)
            can.delete(remparts[i])
            del remparts[i]
            return
    if "Caponebullet" in can.gettags(AlienBullet): #teste si c'est une balle de Capone
        MagieCaponeBullet(AlienBullet)
    elif "Bizarrinibullet" in can.gettags(AlienBullet): #teste si c'est une balle de Bizarrini
        sx=BizarreBullets()
    can.move(AlienBullet,sx,sy)
    fen.after(10,lambda:deplacementTirAlien(AlienBullet))  
    return

def MagieCaponeBullet(AlienBullet): 
    """gère les déplacements téléportés et rebondissants des balles du boss Capone"""
    global dx
    if can.coords(AlienBullet)[0]<30:
        can.move(AlienBullet,740,0)
    elif can.coords(AlienBullet)[2]>770:
        can.move(AlienBullet,-740,0)
    can.move(AlienBullet,-3*dx,-3)

def BizarreBullets(): 
    """gère les trajectoires imprévisibles des balles des Bizarrini"""
    sx=4*randint(-1,1)
    return sx
    
def contactAlienVaisseau():   
   """Teste si le vaisseau et l'alien entrent en contact, si c'est le cas détruit le vaisseau et la partie est perdue"""
   for i in range(len(alien)):
       if can.coords(alien[i][0])[3]>650:
           gameOver()
           return
       return

##Gestion des tirs du vaisseau
def deplacementTir(bullet): 
    """gère le déplacement des tirs du joueur"""
    global sx,sy,alien,tirs,bosslifebar
    sx=0
    sy=-6
    if can.coords(bullet)[1]<10:
        can.delete(bullet)
        tirs-=1
        AddAmmo()
        return
    if can.coords(bullet)[1]<650 and ((can.coords(murs[0])[0] < can.coords(bullet)[0] < can.coords(murs[0])[2]) or (can.coords(murs[1])[0] < can.coords(bullet)[0] < can.coords(murs[1])[2]) or (can.coords(murs[2])[0] < can.coords(bullet)[0] < can.coords(murs[2])[2])):
        can.delete(bullet) #les balles disparaissent si on tire dans les murs
        tirs-=1
        AddAmmo()
        return
    for i in range(len(alien)): #teste si une balle touche un alien
        if can.coords(alien[i][0])[3]>can.coords(bullet)[1]>can.coords(alien[i][0])[1] and can.coords(alien[i][0])[0]<can.coords(bullet)[0]+5<can.coords(alien[i][0])[2]:
            can.delete(bullet)
            tirs-=1
            AddAmmo()
            if wave%3==0 and alien[i][1]!=6:
                bosslifebar=BossLifeBar(bosslifebar) #si l'alien est un boss il faut le toucher 18 fois
                return
            elif alien[i][1]==5 and len(alien)>1: #l'alien bonus ne meure pas tant que les autres n'ont pas été tués
                return
            elif alien[i][1]==6: #les soldats Bizarrini sont immortels, il faut tuer leur chef(le boss Bizarro)
                return
            else:
                Score(alien[i]) #détruit l'alien et augmente le score
                can.delete(alien[i][0])
                can.delete(alienImg[i])
                del alien[i]
                del alienImg[i]
            return
    can.move(bullet,sx,sy)
    fen.after(10,lambda:deplacementTir(bullet))
    return

##GESTION DU VAISSEAU
def creationVaisseau(): 
    """crée le vaisseau et l'affiche"""
    global vaisseau, vaisseauImg, imgV
    vaisseau = can.create_rectangle(350, 700, 450, 755, outline="")
    imgV = Image.open("vaisseau.png")
    imgV = ImageTk.PhotoImage(imgV)
    vaisseauImg = can.create_image(408, 650, anchor=CENTER, image=imgV)
    return
def droite(event): 
    """déplace le vaisseau à droite"""
    if can.coords(vaisseau)[2]<=800:    
        can.move(vaisseau,40,0)
        can.move(vaisseauImg,40,0)
        return
def gauche(event): 
    """déplace le vaisseau à gauche"""
    if can.coords(vaisseau)[0]>=0:
        can.move(vaisseau,-40,0) 
        can.move(vaisseauImg,-40,0)
        return
def tir(event): 
    """crée un tir du vaisseau si une munition est disponible"""
    global tirs
    if tirs<3:
        tirs+=1
        DelAmmo()
        bullet=can.create_oval(can.coords(vaisseau)[0]+45,can.coords(vaisseau)[1]-35,can.coords(vaisseau)[2]-45,can.coords(vaisseau)[3]-75,width=1,fill="yellow",outline="lightyellow",tags="bullet")
        deplacementTir(bullet)
    return
def Vies(): 
    """enlève une vie au joueur s'il est touché et gère le cheat Immortalité"""
    global vies
    if immortal!=1:
        can.delete(vies[-1])
        del vies[-1]
        if len(vies)==0:
            gameOver()
    return
def CheatImmortality(event): 
    """rend le joueur immortel"""
    global immortal
    if immortal==1 :   
        immortal=0
    else:
        immortal=1
    return
def DelAmmo(): 
    """supprime une munition quand on tire"""
    global ammo
    if len(ammo)!=0:
        can.delete(ammo[-1])
        del ammo[-1]
    return
def AddAmmo(): 
    """ajoute une munition lorsqu'une balle se détruit"""
    global ammo
    i=len(ammo)
    ammo.append(can.create_oval(590+i*20,770,600+i*20,790,width=1,fill="yellow",outline="lightyellow"))
    return
##GESTION DES MURS
def creationMur(): 
    """crée et affiche les murs qui se réduisent en longeur"""
    global murs
    mur1 = can.create_rectangle(0, 640, 150, 650, fill="lightgrey")
    mur2 = can.create_rectangle(325, 640, 475, 650, fill="lightgrey")
    mur3 = can.create_rectangle(650, 640, 800, 650, fill="lightgrey")
    murs = [mur1, mur2, mur3]
    return
def destructionMur(UnMur): 
    """réduit les murs en longueur"""
    coords=can.coords(UnMur)
    can.delete(UnMur)
    if coords[2]-20>=coords[0]+20:
        UnMur=can.create_rectangle(coords[0]+20,coords[1],coords[2]-20,coords[3],fill="lightgrey")
    else:
        UnMur=can.create_rectangle(0,0,0,0,outline="")
    return UnMur

def creationRemparts():   
    """crée et affiche les remparts qui se détruisent petit à petit"""
    global remparts
    remparts=[]
    for i in range(3):
        remparts.append(can.create_rectangle(0+i*50,600,50+i*50,620,fill="lightyellow"))
        remparts.append(can.create_rectangle(0+i*50,620,50+i*50,640,fill="lightyellow"))

        remparts.append(can.create_rectangle(325+i*50,600,375+i*50,620,fill="lightyellow"))
        remparts.append(can.create_rectangle(325+i*50,620,375+i*50,640,fill="lightyellow"))
        
        remparts.append(can.create_rectangle(650+i*50,600,700+i*50,620,fill="lightyellow"))
        remparts.append(can.create_rectangle(650+i*50,620,700+i*50,640,fill="lightyellow"))
    return
def destructionRempart(unRempart,AlienBullet): 
    """détruit le bout de rempart touché"""
    if can.coords(unRempart)[1]<can.coords(AlienBullet)[3]:        
        if can.coords(unRempart)[0]<can.coords(AlienBullet)[0]+5<can.coords(unRempart)[2]:
            return True
    else:
        return False

##Création des objets Tkinter
fen=Tk()
fen.title('AlienOctopusKiller')

can=Canvas(fen,bg="navy",height=800,width=800)

can.grid(column=0,row=0)

bou1=Button(fen,text='Quitter',command=fen.destroy)
bou1.grid(column=0,row=2)
bou2=Button(fen,text='Jouer',command=start)
bou2.grid(column=0,row=1)
bou3=Button(fen,text='A propos',command=apropos)
bou3.grid(column=0,row=3)

creationLogoStart()
##Association des touches
can.bind_all('<Right>',droite)
can.bind_all('<Left>',gauche)
can.bind_all('<space>',tir)
can.bind_all('<i>',CheatImmortality)

fen.mainloop()


