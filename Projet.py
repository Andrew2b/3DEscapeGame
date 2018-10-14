1.01
#sys.stdout.flush()

#----------- IMPLANTATIONS ------------------------------

import pygame
import random
import math
import time
import sys
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import os, inspect
from pygame.transform import scale
from pygame.locals import *
from sys import platform as _platform
import socket
from objloader import *

if _platform == "win32":
    scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
    scriptDIR  = os.path.dirname(scriptPATH)

#----------- FIN DES IMPLANTATIONS ------------------------------






##################################  CREATION DE FONCTIONS ###############################################################



def InitReseau():
  global MySocket
  MySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  MySocket.bind((MyIP, portIDstart+PlayerID))
  MySocket.setblocking(0)


def LitMessage():
    try:
        data, address = MySocket.recvfrom(1024)
        data = str(data.decode())
        return data
    except:
        pass

    return ''



def EnvoiMessage(list_infos):
    msg  = ''
    for i in range(len(list_infos)):
       msg += str(list_infos[i]) + ' '
    msg = msg.rstrip() #retire le dernier espace

    # on envoie à tous les joueurs sur les 4 ports
    for IP in IPplayers:
       for i in range(4):
           sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           sent = sock.sendto(msg.encode(), ( IP, portIDstart+i))
           sock.close()


def DecodeMessage(msg):
    global lastbouton
    valeurs = msg.split(' ')
    ID_joueur = int(valeurs[0])
    list_player[ID_joueur][0] = int(valeurs[1])/10**5
    list_player[ID_joueur][1] =(int(valeurs[2])/10**5)-0.8
    list_player[ID_joueur][2] = int(valeurs[3])/10**5
    list_player[ID_joueur][3] = int(valeurs[4])/10**5
    list_player[ID_joueur][4] = int(valeurs[5])/10**5
    if int(valeurs[6])==1 and int(valeurs[20]) == 1 :
        Room[0]["Bouton"]["Pressed"][0] = True
    if int(valeurs[7])==1 and int(valeurs[20]) == 1 :
        Room[1]["Bouton"]["Pressed"][0] = True
    if int(valeurs[8])==1 and int(valeurs[20]) == 1 :
        Room[2]["Bouton"]["Pressed"][0] = True

    if (int(valeurs[9]) == 1 or int(valeurs[10]) == 1 or int(valeurs[11]) == 1 or int(valeurs[12]) == 1 or int(valeurs[13]) == 1 or int(valeurs[14]) == 1 or int(valeurs[15]) == 1 ) and int(valeurs[20]) == 1 :
        for i in range (7) :
            if (int(valeurs[9+i]) == 1) :
                Room[6]["Bouton"]["Pressed"][i] = True

    if int(valeurs[19]) == 1 :
        Room[3]["Box1"]["Rotate"] = int(valeurs[16])
        Room[3]["Box2"]["Rotate"] = int(valeurs[17])
        Room[3]["Box3"]["Rotate"] = int(valeurs[18])
    if int(valeurs[20]) == 1 and int(valeurs[21])!= -1 :
        lastbouton = int(valeurs[21])
    play[ID_joueur]= int(valeurs[22])
    skin_joueur[ID_joueur]= int(valeurs[23])
    if int(valeurs[33]) == 1 :
        Room[7]["Signs"]["Rotate"][0]= int(valeurs[24])
        Room[7]["Signs"]["Rotate"][1]= int(valeurs[25])
        Room[7]["Signs"]["Rotate"][2]= int(valeurs[26])
        Room[7]["Signs"]["Rotate"][3]= int(valeurs[27])
        Room[7]["Signs"]["Rotate"][4]= int(valeurs[28])
        Room[7]["Signs"]["Rotate"][5]= int(valeurs[29])
        Room[7]["Signs"]["Rotate"][6]= int(valeurs[30])
        Room[7]["Signs"]["Rotate"][7]= int(valeurs[31])
        Room[7]["Signs"]["Rotate"][8]= int(valeurs[32])
    if int(valeurs[45])==1 :
        Room[3]["Key"]["Taken"]= True
    if int(valeurs[46])==1 :
        Room[6]["Key"]["Taken"]= True
    if int(valeurs[47])==1 :
        Room[7]["Key"]["Taken"]= True
    if int(valeurs[48])==1 :
        Room[10]["Key"]["Taken"]= True
    list_player[ID_joueur][5] = int(valeurs[49])



def OpenGLColor(Couleur):
    (R,V,B) = Couleur
    return (R/255,V/255,B/255)

def Aim():
    glBegin(GL_QUADS)
    glColor3f(1,1,1)
    glVertex2f((Screen_x/2)-2, (Screen_y/2)-2)
    glVertex2f((Screen_x/2)+2, (Screen_y/2)-2)
    glVertex2f((Screen_x/2)+2, (Screen_y/2)+2)
    glVertex2f((Screen_x/2)-2, (Screen_y/2)+2)

    glEnd()

def Face(Couleur,A,u,v):
    (Ax,Ay,Az) = A
    (ux,uy,uz) = u
    (vx,vy,vz) = v
    A1 = A
    A2 = (Ax+ux,Ay+uy,Az+uz)
    A3 = (Ax+ux+vx,Ay+uy+vy,Az+uz+vz)
    A4 = (Ax+vx,Ay+vy,Az+vz)
    glBegin(GL_QUADS)
    glColor3fv(OpenGLColor(Couleur))
    glVertex3fv( A1 )
    glVertex3fv( A2 )
    glVertex3fv( A3 )
    glVertex3fv( A4  )
    glEnd()


def Lines(Couleur,P1,P2):
    glBegin(GL_LINES)
    glColor3fv(Couleur)
    glVertex3fv(P1)
    glVertex3fv(P2)
    glEnd()


def AxesRepere(longueur):
    L = longueur
    P = (.1,.1,.1)
    Lines(RED,P,(L,0,0))
    Lines(GREEN,P,(0,L,0))
    Lines(BLUE,P,(0,0,L))


def OpenGLRepereCamera(): #ne pas toucher
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix();
    glRotatef(list_player[PlayerID][4], 1,0,0)#math.cos(math.pi/2 + math.radians(list_player[PlayerID][3]))
    glRotatef(list_player[PlayerID][3], 0, 1, 0)
    glTranslatef(list_player[PlayerID][0], -list_player[PlayerID][1], list_player[PlayerID][2])

def RotatingCube():
    glPushMatrix(); # cree un sous repère
    theta = (time.time()*10)%360
    h =  (time.time())%10
    glTranslatef(-1,h,-10)     # translation par rapport au repère parent
    glRotatef(theta, 0, 1, 0)  # rotation autours de l'axe Y du repère parent
    glScale(2,2,2)             # zoom autours des axes du repere parent
    Cube()
    AxesRepere(2)              # desine les axes du repere local
    glPopMatrix();             # revient au repère parent et oublie le repère courant

def Cube():
    Face(YELLOW, (0,0,0),ix,iz)
    Face(GREEN, (0,0,0),ix,iy)
    Face(BLUE,  (0,0,0),iy,iz)
    Face(RED,   (1,1,1),mix,miz)
    Face(BROWN, (1,1,1),mix,miy)
    Face(YELLOW,(1,1,1),miy,miz)


def TupleChange(x):
    ix = ()
    for i in range(0,len(x)):
        ix = ix + (x[i]*(-1),)
    return ix

def Rect(x,y,z, a,b,c,d,e,f, Couleur):
    ix = TupleChange(x)
    iy = TupleChange(y)
    iz = TupleChange(z)
    Face(Couleur, (a,b,c),x,z)
    Face(Couleur, (a,b,c),x,y)
    Face(Couleur, (a,b,c),y,z)
    Face(Couleur, (d,e,f),ix,iz)
    Face(Couleur, (d,e,f),ix,iy)
    Face(Couleur, (d,e,f),iy,iz)


def loadTexture(nomdetexture):
    textureSurface = pygame.image.load(nomdetexture)
    textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
    width1 = textureSurface.get_width()
    height1 = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width1, height1,0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid

def affichageimage(nomdetexture,x,y,taillex,tailley) :
    loadTexture(nomdetexture)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex2f(x,y)
    glTexCoord2f(1.0, 0.0)
    glVertex2f(x+taillex, y)
    glTexCoord2f(1.0, 1.0)
    glVertex2f(x+taillex, y+tailley)
    glTexCoord2f(0.0, 1.0)
    glVertex2f(x, y+tailley)
    glEnd()

def Stair(x,y,z,Nb):
    for i in range(len(x)):
        glPushMatrix();
        glColor3fv((255,255,255))

        glTranslatef(-x[i],y,-z[i])
        glRotatef(-90, 1, 0, 0)
        if Nb[i] == 1 :
            glCallList(objhauteur1.gl_list)
        elif Nb[i] == 2 :
            glCallList(objhauteur2.gl_list)
        elif Nb[i] == 3 :
            glCallList(objhauteur3.gl_list)
        elif Nb[i] == 4 :
            glCallList(objhauteur4.gl_list)
        elif Nb[i] == 5 :
            glCallList(objhauteur5.gl_list)
        elif Nb[i] == 6 :
            glCallList(objhauteur6.gl_list)
        else :
            glCallList(objhauteur7.gl_list)
        glPopMatrix();

def Sign(x,y,z,Nb,Rotate):
    for i in range(len(x)):
        glPushMatrix(); # cree un sous repère
        glColor3fv((255,255,255))
        glTranslatef(-x[i],y,-z[i])     # translation par rapport au repère parent
        glRotatef(-90 * Rotate[i], 0, 1, 0)
        glRotatef(-90, 1, 0, 0)  # rotation autours de l'axe Y du repère parent
        if Nb[i] == 1 :
            glCallList(objsigne1.gl_list)
        elif Nb[i] == 2 :
            glCallList(objsigne2.gl_list)
        elif Nb[i] == 3 :
            glCallList(objsigne3.gl_list)
        elif Nb[i] == 4 :
            glCallList(objsigne4.gl_list)
        elif Nb[i] == 5 :
            glCallList(objsigne5.gl_list)
        elif Nb[i] == 6 :
            glCallList(objsigne6.gl_list)
        elif Nb[i] == 7 :
            glCallList(objsigne7.gl_list)
        elif Nb[i] == 8 :
            glCallList(objsigne8.gl_list)
        elif Nb[i] == 9 :
            glCallList(objsigne9.gl_list)
        glPopMatrix();             # revient au repère parent et oublie le repère courant

def Box(x,y,z,Nb,Black):
    glPushMatrix(); # cree un sous repère
    glColor3fv((255,255,255))

    glTranslatef(-x,y,-z)     # translation par rapport au repère parent


    glRotatef(-90-90*Nb, 0,1, 0)  # rotation autours de l'axe Y du repère parent
    glRotatef(-90, 1, 0, 0)  # rotation autours de l'axe Y du repère parent
    if Black != True :
        NbRotate = Room[now]["Box"+str(Nb)]["Rotate"]
        glRotatef(-90 * NbRotate, 1, 0, 0)
        glTranslatef(0, -rotation_depl[NbRotate][1],- rotation_depl[NbRotate][0])     # translation par rapport au repère parent
    if Black == True :
        glCallList(objblackbox.gl_list)
    elif Nb == 1 :
        glCallList(objcube1.gl_list)
    elif Nb == 2 :
        glCallList(objcube2.gl_list)
    elif Nb == 3 :
        glCallList(objcube3.gl_list)

    glPopMatrix();             # revient au repère parent et oublie le repère courant

def Platform(x,y,z):
    for i in range(len(x)):
        glPushMatrix();
        glColor3fv((255,255,255))

        glTranslatef(-x[i],y[i],-z[i])
        glRotatef(-90, 1, 0, 0)

        glCallList(objplatforme.gl_list)
        glPopMatrix();

def Furniture(x,y,z,Nb,Rotate):
    for i in range(len(x)):
        glPushMatrix(); # cree un sous repère
        glColor3fv((255,255,255))

        glTranslatef(-x[i],y[i],-z[i])     # translation par rapport au repère parent

        if Rotate[i]==True:
            glRotatef(-180, 0, 1, 0)  # rotation autours de l'axe Y du repère parent
        elif(Nb[i] == 1):
                glTranslatef(0,0,4)     # translation par rapport au repère parent
        glRotatef(-90, 1, 0, 0)  # rotation autours de l'axe Y du repère parent
        if Nb[i] == 1:
            glCallList(objarmoire1.gl_list)
        elif Nb[i] == 2 :
            glCallList(objarmoire2.gl_list)
        elif Nb[i] == 3 :
            glCallList(objarmoire3.gl_list)
        elif Nb[i] == 4 :
            glCallList(objarmoire4.gl_list)
        else :
            glCallList(objarmoire5.gl_list)

        glPopMatrix();             # revient au repère parent et oublie le repère courant

def nbTeam():
    team1  = 0
    team2 = 0
    for i in range(4) :
        if list_player[i][5]==1 or list_player[i][5]==3 or list_player[i][5]==5 or list_player[i][5]==7:
            team1 +=1
        if list_player[i][5]==2 or list_player[i][5]==4 or list_player[i][5]==6 or list_player[i][5]==8:
            team2 +=1
    return (team1,team2)
    

def draw(i):
    glPushMatrix()
    glColor3fv((255,255,255))
    glTranslatef(-list_player[i][0],list_player[i][1],-list_player[i][2])     # translation par rapport au repère parent
    glRotatef(-list_player[i][3], 0, 1, 0)
    glRotatef(-list_player[i][4]-90, 1, 0, 0)
    glCallList(skin[skin_joueur[i]].gl_list)
    glPopMatrix()

def drawPlayers():
    for i in range(len(play)):
        if(play[i]==1 and PlayerID != i) :
            draw(i)


def RoomCreate(x,y,z,RoomNb):
    glPushMatrix(); # cree un sous repère
    glColor3fv((255,255,255))

    glTranslatef(-x,y,-z)     # translation par rapport au repère parent
    if(RoomNb == 10):
        glRotatef(-90, 0, 1, 0)  # rotation autours de l'axe Y du repère parent
    glRotatef(-90, 1, 0, 0)  # rotation autours de l'axe Y du repère parent
    glRotatef(-90, 0, 0, 1)  # rotation autours de l'axe Y du repère parent

#    AxesRepere(2)              # desine les axes du repere local
    glCallList(roomlist[RoomNb].gl_list)
    glPopMatrix();             # revient au repère parent et oublie le repère courant

def Door(x,y,z,rotation,Open):
    for i in range(len( Room[now]["Porte"]["x"])):
        glPushMatrix(); # cree un sous repère
        glColor3fv((255,255,255))

        glTranslatef(-Room[now]["Porte"]["x"][i],Room[now]["Porte"]["y"][i],-Room[now]["Porte"]["z"][i])
        glRotatef(-90*rotation[i] ,0,1,0)
        if rotation[i] != -1 :
            glRotatef(-90, 1, 0, 0)
        if Open[i] == 1 :
            glCallList(objdooropen.gl_list)
        elif Open[i] == 0 :
            glCallList(objdoorclose.gl_list)
        elif Open[i] == -1:
            glCallList(objbackdoor.gl_list)
        elif Open[i] == -2 :
            glCallList(objtp.gl_list)
        elif Open[i] == 2 :
            glCallList(objfinaldoor.gl_list)
        elif Open[i] == 3 :
            glCallList(objbegindoor.gl_list)
        elif Open[i] == 4 :
            glCallList(objbeginopen.gl_list)
        glPopMatrix();   # revient au repère parent et oublie le repère courant

def Prison(x,y,z,rotate):
    for i in range(len(x)):
        glPushMatrix();
        glColor3fv((255,255,255))

        glTranslatef(-x[i],y,-z[i])
        glRotatef(-90*rotate[i],0,1,0)
        glRotatef(-90, 1, 0, 0)

        glCallList(objcell.gl_list)
        glPopMatrix();

def Table(x,y,z):
    for i in range(len(x)):
        glPushMatrix();
        glColor3fv((255,255,255))

        glTranslatef(-x[i],y,-z[i])
        glRotatef( 90, 0, 1, 0)
        glRotatef(-90, 1, 0, 0)

        glCallList(objtable.gl_list)
        glPopMatrix();


def testtouche() :
    k=-5
    for i in range (len(codetoucheclavier)):
        if pygame.key.get_pressed()[codetoucheclavier[i]]:
            k=i
    return k

def Arbre2(a,b,c): #y,z,x
    Rect((1,0,0),(0,2,0),(0,0,1),a+1,b,c+1,a+2,b+2,c+2,BROWN)
    Rect((2,0,0),(0,3,0),(0,0,2),a,b+2,c+1,a+2,b+5,c+3,GREEN)
    Rect((2,0,0),(0,1,0),(0,0,4),a,b+3,c,a+2,b+4,c+4,GREEN)
    Rect((4,0,0),(0,1,0),(0,0,2),a-1,b+3,c+1,a+3,b+4,c+3,GREEN)


def Sol():
    for x in range(-50,50,5) :
        for z in range(-50,50,5):
            couleur = BLUE
            if (x+z)%10 == 0 : couleur = RED
            Face( couleur, (x, 0,z), (5,0,0) , (0,0,5)  )

def Foret():
    for P in Arbres:
        (x,z) = P
        TriangleIsocele( GREEN , (x, 1,z),  (1,0,0),(0,5,0) )
        TriangleIsocele( GREEN2, (x, 1 ,z), (0,0,1),(0,5,0) )
        Face( BROWN,  (x-0.5, 0, z), (1,0,0),(0,1,0) )
        Face( BROWN2, (x, 0, z-0.5), (0,0,1),(0,1,0) )


def Distance(x1,z1,pixEntre,Type):
    #sys.stdout.flush()
    for i in range( len(Room[now][Type]["Coord"]) ) :
        x2 = Room[now][Type]["Coord"][i][0]
        z2 = Room[now][Type]["Coord"][i][1]
        if( pixEntre**2 >= (x1-x2)**2+(z1-z2)**2):
            if Room[now][Type]["Type"] == "Porte" :
                if now == 9 :
                    if i == 0:
                        if list_player[PlayerID][1] < 68 :
                            return -1
                    list_player[PlayerID][1] = hauteur_joueur + Room[now]["Room"]["y"]
                return i
            return -1
    return -2


def DistanceRotate(x1,z1):
    x2 = Room[now]["Box1"]["x"]
    z2 = Room[now]["Box1"]["z"]

    min_dist = math.sqrt( ((x1-x2)**2+(z1-z2)**2) )
    min_index = 1
    for i in range(2,4) :
        x2 = Room[now]["Box"+str(i)]["x"]
        z2 = Room[now]["Box"+str(i)]["z"]
        dist_actuel = math.sqrt( ((x1-x2)**2+(z1-z2)**2) )
        if min_dist > dist_actuel :
            min_index = i
            min_dist = dist_actuel

    return (min_index,min_dist)


def Button(x,y,z,k) :
    glPushMatrix(); # cree un sous repère
    glColor3fv((255,255,255))

    glTranslatef(-x,y,-z)
    glRotatef(-90, 1, 0, 0)  # rotation autours de l'axe Y du repère parent

    if Room[now]["Bouton"]["Pressed"][k] == True :
        glTranslatef(0,0,-0.7)

    glCallList(objbutton1.gl_list)
    glPopMatrix();   # revient au repère parent et oublie le repère courant

def Key(x,y,z) :

    glPushMatrix();
    glColor3fv((255,255,255))

    glTranslatef(-x,y,-z)
    if(now == 6 or now == 10):
        glRotatef(-90, 0, 1, 0)
    glRotatef(-90, 0, 0, 1)

    if Room[now]["Key"]["Appear"] == True and Room[now]["Key"]["Taken"] == False:
        glCallList(objkey.gl_list)
    glPopMatrix();


def DistanceKey(x1,z1,pixEntre) :
    for objet in Room[now]:
        if objet == "Key" :
            x2 = Room[now][objet]["x"]
            z2 = Room[now][objet]["z"]
            if( (pixEntre**2 >= (x1-x2)**2+(z1-z2)**2) and (Room[now][objet]["Appear"] == True) and (Room[now][objet]["Taken"] == False)):
                Room[now][objet]["Taken"] = True
                return Room[now][objet]["Nb"]
    return -1



def DistanceButton(x1,z1,pixEntre):
    global presser
    for objet in Room[now]:
        if objet == "Bouton" :
            for i in range( len(Room[now][objet]["Coord"]) ) :
                x2 = Room[now][objet]["Coord"][i][0]
                z2 = Room[now][objet]["Coord"][i][2]
                if( (pixEntre**2 >= (x1-x2)**2+(z1-z2)**2) and list_player[PlayerID][1] < Room[now][objet]["Coord"][i][1]+hauteur_joueur+3.1 and list_player[PlayerID][1] > Room[now][objet]["Coord"][i][1]+hauteur_joueur-1):
                    if Room[now]["Bouton"]["Pressed"][i] == False :
                        Room[now]["Bouton"]["Pressed"][i] = True
                    presser=1
                    return i
                elif now != 6 :
                    Room[now]["Bouton"]["Pressed"][i] = False
                    
    return -1


def DistanceRotate(x1,z1,NumCube):
    x2 = Room[now]["Box"+str(NumCube)]["x"]
    z2 = Room[now]["Box"+str(NumCube)]["z"]

    min_dist = math.sqrt( ((x1-x2)**2+(z1-z2)**2) )

    return min_dist


def Chargement_du_jeu():
    #--------------INITIALISATION CONSTANTES, VARIABLES ET TABLEAUX ----------------------------
    global timerdebut,compte_a_rebours, hauteur_joueur,nbRoom,rotation_depl,rx,ry,ty,tx,zpos,rotate,move,montee_collision,descente_collision,player_y_previous,chute,saut,hauteur,ouverture_porte,rot_cube,play,list_player,player_play,ix,iy,iz,mix,miy,miz,now,dist_collision,bouge,roomlist,presser,finalporte,speed,speed_cam,timer,timer2,stop,skin_player_now,skin_joueur,effect1,effect2,effect3,effect4,effect5,effect6,cmpt,door0_bool,door12_bool,door34_bool,sound_buttons_room6,srf
    srf = pygame.display.set_mode((Screen_x,Screen_y), pygame.FULLSCREEN | OPENGL | DOUBLEBUF)
    nbRoom = 11
    timerdebut = pygame.time.get_ticks()
    compte_a_rebours = 1800 # en sec
    rotation_depl = [(0,0),(1,1),(2,0),(1,-1)]
    rx, ry = (0,0)
    tx, ty = (0,0)
    zpos = 5
    rotate = move = False
    #paramètres du saut
    montee_collision=False
    descente_collision=False
    hauteur = 10
    player_y_previous = 0
    saut = False
    chute = False
    hauteur_joueur = 4

    #paramètres des sons
    cmpt = 0
    door0_bool = False
    door12_bool = False
    door34_bool = False
    sound_buttons_room6 = 7*[False]

    rot_cube=[0,0,0]
    now = 0
    previous_room = 0
    dist_collision = 0
    bouge = 0
    finalporte = False
    speed = 0.6
    speed_cam = 0.15
    timer = 0
    timer2 = 0
    stop = False

    player1_z = -30
    player1_y = hauteur_joueur  #hauteur des yeux du joueur par rapport au sol 1.8m
    player1_x = 0
    rotdegres1 = 0
    rotdegres1_haut = 0

    player2_x = 0
    player2_y = hauteur_joueur
    player2_z= -35
    rotdegres2 = 0
    rotdegres2_haut = 0

    player3_x = 0
    player3_y = hauteur_joueur
    player3_z= -25
    rotdegres3 = 0
    rotdegres3_haut = 0

    player4_x = 0
    player4_y = hauteur_joueur
    player4_z= -20
    rotdegres4 = 0
    rotdegres4_haut = 0
    now1 = 0
    now2 = 0
    now3 = 0
    now4 = 0
    
    
    play = [0,0,0,0]
    list_player = [[player1_x, player1_y, player1_z ,rotdegres1,rotdegres1_haut,now1],[player2_x, player2_y, player2_z, rotdegres2,rotdegres2_haut,now2],[player3_x, player3_y, player3_z, rotdegres3, rotdegres3_haut,now3],[player4_x, player4_y, player4_z, rotdegres4, rotdegres4_haut,now4]]
    player_play = 1
    

    ix = (1,0,0)
    iy = (0,1,0)
    iz = (0,0,1)
    mix = (-1,0,0)
    miy = (0,-1,0)
    miz = (0,0,-1)

    background_sound = os.path.join(scriptDIR,"son.wav")
    pygame.mixer.music.load(background_sound)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    effect1_sound = os.path.join(scriptDIR,"son-block-side.wav")
    effect1 = pygame.mixer.Sound(effect1_sound)
    effect1.set_volume(1)

    effect2_sound = os.path.join(scriptDIR,"son-block-side-end.wav")
    effect2 = pygame.mixer.Sound(effect2_sound)
    effect2.set_volume(1)

    effect3_sound = os.path.join(scriptDIR,"door_lock.wav")
    effect3 = pygame.mixer.Sound(effect3_sound)
    effect3.set_volume(0.5)

    effect4_sound = os.path.join(scriptDIR,"applause.wav")
    effect4 = pygame.mixer.Sound(effect4_sound)
    effect4.set_volume(0.5)

    effect5_sound = os.path.join(scriptDIR,"electric_door_opening_1.wav")
    effect5 = pygame.mixer.Sound(effect5_sound)
    effect5.set_volume(0.7)

    effect6_sound = os.path.join(scriptDIR,"teleportation.wav")
    effect6 = pygame.mixer.Sound(effect6_sound)
    effect6.set_volume(0.5)



    #--------------FIN D'INITIALISATION CONSTANTES, VARIABLES ET TABLEAUX ----------------------------



    #--------------INITIALISATION DICTIONNAIRE DES OBJETS ET SALLES-------------------------
    global Room
    Room = {}
    for i in range(nbRoom):
        Room[i] = {}

    Room[0]["Room"] = {}
    Room[0]["Room"]["Type"] = "Room"
    Room[0]["Room"]["Size"] = 1
    Room[0]["Room"]["x"] = 0
    Room[0]["Room"]["y"] = 0
    Room[0]["Room"]["z"] = 0
    Room[0]["Room"]["function"] = RoomCreate

    Room[1]["Room"] = {}
    Room[1]["Room"]["Type"] = "Room"
    Room[1]["Room"]["Size"] = 1
    Room[1]["Room"]["x"] = 128
    Room[1]["Room"]["y"] = 0
    Room[1]["Room"]["z"] = 128
    Room[1]["Room"]["function"] = RoomCreate

    Room[2]["Room"] = {}
    Room[2]["Room"]["Type"] = "Room"
    Room[2]["Room"]["Size"] = 1
    Room[2]["Room"]["x"] = 0
    Room[2]["Room"]["y"] = 0
    Room[2]["Room"]["z"] = 128
    Room[2]["Room"]["function"] = RoomCreate

    Room[3]["Room"] = {}
    Room[3]["Room"]["Type"] = "Room"
    Room[3]["Room"]["Size"] = 1
    Room[3]["Room"]["x"] = 128
    Room[3]["Room"]["y"] = 0
    Room[3]["Room"]["z"] = 0
    Room[3]["Room"]["function"] = RoomCreate

    Room[4]["Room"] = {}
    Room[4]["Room"]["Type"] = "Room"
    Room[4]["Room"]["Size"] = 1
    Room[4]["Room"]["x"] = -128
    Room[4]["Room"]["y"] = 0
    Room[4]["Room"]["z"] = -128
    Room[4]["Room"]["function"] = RoomCreate

    Room[5]["Room"] = {}
    Room[5]["Room"]["Type"] = "Room"
    Room[5]["Room"]["Size"] = 1
    Room[5]["Room"]["x"] = 0
    Room[5]["Room"]["y"] = 0
    Room[5]["Room"]["z"] = -128
    Room[5]["Room"]["function"] = RoomCreate


    Room[6]["Room"] = {}
    Room[6]["Room"]["Type"] = "Room"
    Room[6]["Room"]["Size"] = 1
    Room[6]["Room"]["x"] = -128
    Room[6]["Room"]["y"] = 0
    Room[6]["Room"]["z"] = 0
    Room[6]["Room"]["function"] = RoomCreate

    Room[7]["Room"] = {}
    Room[7]["Room"]["Type"] = "Room"
    Room[7]["Room"]["Size"] = 1
    Room[7]["Room"]["x"] = 128
    Room[7]["Room"]["y"] = 0
    Room[7]["Room"]["z"] = -128
    Room[7]["Room"]["function"] = RoomCreate

    Room[8]["Room"] = {}
    Room[8]["Room"]["Type"] = "Room"
    Room[8]["Room"]["Size"] = 1
    Room[8]["Room"]["x"] = -128
    Room[8]["Room"]["y"] = 0
    Room[8]["Room"]["z"] = 128
    Room[8]["Room"]["function"] = RoomCreate

    Room[9]["Room"] = {}
    Room[9]["Room"]["Type"] = "Room"
    Room[9]["Room"]["Size"] = 1
    Room[9]["Room"]["x"] = 256
    Room[9]["Room"]["y"] = 0
    Room[9]["Room"]["z"] = 0
    Room[9]["Room"]["function"] = RoomCreate

    Room[10]["Room"] = {}
    Room[10]["Room"]["Type"] = "Room"
    Room[10]["Room"]["Size"] = 1
    Room[10]["Room"]["x"] = -256
    Room[10]["Room"]["y"] = 0
    Room[10]["Room"]["z"] = 0
    Room[10]["Room"]["function"] = RoomCreate

    Room[3]["BlackBox"] = {}
    Room[3]["BlackBox"]["Type"] = "Cube"
    Room[3]["BlackBox"]["Size"] = 1
    Room[3]["BlackBox"]["x"] = [Room[3]["Room"]["x"]+1,Room[3]["Room"]["x"]+27,Room[3]["Room"]["x"]]
    Room[3]["BlackBox"]["y"] = Room[3]["Room"]["y"]
    Room[3]["BlackBox"]["z"] = [Room[3]["Room"]["z"]-27,Room[3]["Room"]["z"],Room[3]["Room"]["z"]+27]
    Room[3]["BlackBox"]["function"] = Box

    Room[3]["Box1"] = {}
    Room[3]["Box1"]["Type"] = "MiniCube"
    Room[3]["Box1"]["Size"] = 1
    Room[3]["Box1"]["x"] = Room[3]["BlackBox"]["x"][0]#Room[1]["BlackBox"]["x"]-2
    Room[3]["Box1"]["y"] = Room[3]["BlackBox"]["y"]+4#Room[1]["BlackBox"]["y"]+4
    Room[3]["Box1"]["z"] = Room[3]["BlackBox"]["z"][0]+1#Room[1]["BlackBox"]["z"]+3
    Room[3]["Box1"]["function"] = Box
    Room[3]["Box1"]["Nb"] = 1
    Room[3]["Box1"]["Rotate"] = 0

    Room[3]["Box2"] = {}
    Room[3]["Box2"]["Type"] = "MiniCube"
    Room[3]["Box2"]["Size"] = 1
    Room[3]["Box2"]["x"] = Room[3]["BlackBox"]["x"][1]-1   #Room[1]["BlackBox"]["x"]
    Room[3]["Box2"]["y"] = Room[3]["BlackBox"]["y"]+4  #Room[1]["BlackBox"]["y"]+4
    Room[3]["Box2"]["z"] = Room[3]["BlackBox"]["z"][1]   #Room[1]["BlackBox"]["z"]+3
    Room[3]["Box2"]["function"] = Box
    Room[3]["Box2"]["Nb"] = 2
    Room[3]["Box2"]["Rotate"] = 0

    Room[3]["Box3"] = {}
    Room[3]["Box3"]["Type"] = "MiniCube"
    Room[3]["Box3"]["Size"] = 1
    Room[3]["Box3"]["x"] = Room[3]["BlackBox"]["x"][2]#Room[1]["BlackBox"]["x"]+2
    Room[3]["Box3"]["y"] = Room[3]["BlackBox"]["y"]+4#Room[1]["BlackBox"]["y"]+4
    Room[3]["Box3"]["z"] = Room[3]["BlackBox"]["z"][2]-1#Room[1]["BlackBox"]["z"]+3
    Room[3]["Box3"]["function"] = Box
    Room[3]["Box3"]["Nb"] = 3
    Room[3]["Box3"]["Rotate"] = 0

    Room[3]["Cell"] = {}
    Room[3]["Cell"]["Type"] = "Cell"
    Room[3]["Cell"]["Size"] = 1
    Room[3]["Cell"]["Rotate"] = [3,4,1,2]
    Room[3]["Cell"]["x"] = [Room[3]["Room"]["x"]-20,Room[3]["Room"]["x"]+20,Room[3]["Room"]["x"]+20,Room[3]["Room"]["x"]-20]
    Room[3]["Cell"]["y"] = 0
    Room[3]["Cell"]["z"] = [Room[3]["Room"]["z"]-20,Room[3]["Room"]["z"]-20,Room[3]["Room"]["z"]+20,Room[3]["Room"]["z"]+20]
    Room[3]["Cell"]["function"] = Prison

    Room[4]["Cell"] = {}
    Room[4]["Cell"]["Type"] = "Cell"
    Room[4]["Cell"]["Size"] = 1
    Room[4]["Cell"]["Rotate"] = [3,4,1,2]
    Room[4]["Cell"]["x"] = [Room[4]["Room"]["x"]-20,Room[4]["Room"]["x"]+20,Room[4]["Room"]["x"]+20,Room[4]["Room"]["x"]-20]
    Room[4]["Cell"]["y"] = 0
    Room[4]["Cell"]["z"] = [Room[4]["Room"]["z"]-20,Room[4]["Room"]["z"]-20,Room[4]["Room"]["z"]+20,Room[4]["Room"]["z"]+20]
    Room[4]["Cell"]["function"] = Prison

    Room[1]["Bibli"] = {}
    Room[1]["Bibli"]["Type"] = "Bibli"
    Room[1]["Bibli"]["Size"] = 1
    Room[1]["Bibli"]["Rotate"] = [True,False,False,True,True,True,True,False,False,False]
    Room[1]["Bibli"]["x"] = [Room[1]["Room"]["x"]+18.5,Room[1]["Room"]["x"]+19,Room[1]["Room"]["x"]-18.5,Room[1]["Room"]["x"]-19,
                             Room[1]["Room"]["x"]-23,Room[1]["Room"]["x"]-23,Room[1]["Room"]["x"],Room[1]["Room"]["x"],Room[1]["Room"]["x"]+23,Room[1]["Room"]["x"]+23]

    Room[1]["Bibli"]["y"] = [-0.8,-0.8,-0.8,-0.8,0,0,0,0,0,0]
    Room[1]["Bibli"]["z"] = [Room[1]["Room"]["z"]-20,Room[1]["Room"]["z"]+24,Room[1]["Room"]["z"]+24,Room[1]["Room"]["z"]-20,Room[1]["Room"]["z"]+8,
                            Room[1]["Room"]["z"]-8,Room[1]["Room"]["z"]-22,Room[1]["Room"]["z"]+22,Room[1]["Room"]["z"]-8,Room[1]["Room"]["z"]+8]

    Room[1]["Bibli"]["Nb"] = [1,1,1,1,3,4,5,5,3,4]
    Room[1]["Bibli"]["function"] = Furniture


    Room[1]["Table"] = {}
    Room[1]["Table"]["Type"] = "Table"
    Room[1]["Table"]["Size"] = 1
    Room[1]["Table"]["x"] = [Room[1]["Room"]["x"]]
    Room[1]["Table"]["y"] = 0
    Room[1]["Table"]["z"] = [Room[1]["Room"]["z"]]
    Room[1]["Table"]["function"] = Table

    Room[2]["Bibli"] = {}
    Room[2]["Bibli"]["Type"] = "Bibli"
    Room[2]["Bibli"]["Size"] = 1
    Room[2]["Bibli"]["Rotate"] = [True,False,False,True,True,True,True,False,False,False]
    Room[2]["Bibli"]["x"] = [Room[2]["Room"]["x"]+18.5,Room[2]["Room"]["x"]+19,Room[2]["Room"]["x"]-18.5,Room[2]["Room"]["x"]-19,
                             Room[2]["Room"]["x"]-23,Room[2]["Room"]["x"]-23,Room[2]["Room"]["x"],Room[2]["Room"]["x"],Room[2]["Room"]["x"]+23,Room[2]["Room"]["x"]+23]

    Room[2]["Bibli"]["y"] = [-0.8,-0.8,-0.8,-0.8,0,0,0,0,0,0]
    Room[2]["Bibli"]["z"] = [Room[2]["Room"]["z"]-20,Room[2]["Room"]["z"]+24,Room[2]["Room"]["z"]+24,Room[2]["Room"]["z"]-20,Room[2]["Room"]["z"]+8,
                            Room[2]["Room"]["z"]-8,Room[2]["Room"]["z"]-22,Room[2]["Room"]["z"]+22,Room[2]["Room"]["z"]-8,Room[2]["Room"]["z"]+8]

    Room[2]["Bibli"]["Nb"] = [1,1,1,1,3,4,5,5,3,4]
    Room[2]["Bibli"]["function"] = Furniture


    Room[2]["Table"] = {}
    Room[2]["Table"]["Type"] = "Table"
    Room[2]["Table"]["Size"] = 1
    Room[2]["Table"]["x"] = [Room[2]["Room"]["x"]]
    Room[2]["Table"]["y"] = 0
    Room[2]["Table"]["z"] = [Room[2]["Room"]["z"]]
    Room[2]["Table"]["function"] = Table

    Room[9]["Platforme"] = {}
    Room[9]["Platforme"]["Type"] = "Platforme" # différent de cube, psk ceux là peuvent être mis dans différent hauteur
    Room[9]["Platforme"]["Size"] = 1
    Room[9]["Platforme"]["x"] =[Room[9]["Room"]["x"]+90.05,Room[9]["Room"]["x"]-90.05,Room[9]["Room"]["x"]-80,Room[9]["Room"]["x"]-70,Room[9]["Room"]["x"]-90,
    Room[9]["Room"]["x"]-70,Room[9]["Room"]["x"]-32,Room[9]["Room"]["x"]-30,Room[9]["Room"]["x"]-50,Room[9]["Room"]["x"]-70,Room[9]["Room"]["x"]-50,Room[9]["Room"]["x"]-17,
    Room[9]["Room"]["x"],Room[9]["Room"]["x"]-10,Room[9]["Room"]["x"]+40,Room[9]["Room"]["x"]+15,Room[9]["Room"]["x"]+45,Room[9]["Room"]["x"]+75,Room[9]["Room"]["x"]+45,Room[9]["Room"]["x"]+20,Room[9]["Room"]["x"],
    Room[9]["Room"]["x"]+80,Room[9]["Room"]["x"]+70,Room[9]["Room"]["x"]+90,Room[9]["Room"]["x"]+70,Room[9]["Room"]["x"]+32,Room[9]["Room"]["x"]+30,
    Room[9]["Room"]["x"]+50,Room[9]["Room"]["x"]+70,Room[9]["Room"]["x"]+50,Room[9]["Room"]["x"]+17,Room[9]["Room"]["x"],Room[9]["Room"]["x"]+10,Room[9]["Room"]["x"]-40,
    Room[9]["Room"]["x"]-45,Room[9]["Room"]["x"]-75,Room[9]["Room"]["x"]-45,Room[9]["Room"]["x"]-20,Room[9]["Room"]["x"]-15]

    Room[9]["Platforme"]["y"] =[Room[9]["Room"]["y"]+4,Room[9]["Room"]["y"]+4,Room[9]["Room"]["y"]+2,Room[9]["Room"]["y"]+10,Room[9]["Room"]["y"]+10,Room[9]["Room"]["y"]+12,
    Room[9]["Room"]["y"]+14,Room[9]["Room"]["y"]+23,Room[9]["Room"]["y"]+32,Room[9]["Room"]["y"]+36,Room[9]["Room"]["y"]+45,Room[9]["Room"]["y"]+52,Room[9]["Room"]["y"]+60,
    Room[9]["Room"]["y"]+12,Room[9]["Room"]["y"]+18,Room[9]["Room"]["y"]+27,Room[9]["Room"]["y"]+36,Room[9]["Room"]["y"]+42,Room[9]["Room"]["y"]+50,Room[9]["Room"]["y"]+59,Room[9]["Room"]["y"]+67.95,
    Room[9]["Room"]["y"]+2,Room[9]["Room"]["y"]+10,Room[9]["Room"]["y"]+10,Room[9]["Room"]["y"]+12,
    Room[9]["Room"]["y"]+14,Room[9]["Room"]["y"]+23,Room[9]["Room"]["y"]+32,Room[9]["Room"]["y"]+36,Room[9]["Room"]["y"]+45,Room[9]["Room"]["y"]+52,Room[9]["Room"]["y"]+60,
    Room[9]["Room"]["y"]+12,Room[9]["Room"]["y"]+18,Room[9]["Room"]["y"]+36,Room[9]["Room"]["y"]+42,Room[9]["Room"]["y"]+50,Room[9]["Room"]["y"]+59,Room[9]["Room"]["y"]+27]

    Room[9]["Platforme"]["z"] =[Room[9]["Room"]["z"]-90.05,Room[9]["Room"]["z"]-90.05,Room[9]["Room"]["z"]-80,Room[9]["Room"]["z"]-90,Room[9]["Room"]["z"]-70,Room[9]["Room"]["z"]-32,
    Room[9]["Room"]["z"]-30,Room[9]["Room"]["z"]-10,Room[9]["Room"]["z"]-10,Room[9]["Room"]["z"]+25,Room[9]["Room"]["z"]+25,Room[9]["Room"]["z"]+20,Room[9]["Room"]["z"]+50,Room[9]["Room"]["z"]+55,
    Room[9]["Room"]["z"]+75,Room[9]["Room"]["z"]+85,Room[9]["Room"]["z"]+75,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+90,
    Room[9]["Room"]["z"]-80,Room[9]["Room"]["z"]-90,Room[9]["Room"]["z"]-70,Room[9]["Room"]["z"]-32,
    Room[9]["Room"]["z"]-30,Room[9]["Room"]["z"]-10,Room[9]["Room"]["z"]-10,Room[9]["Room"]["z"]+25,Room[9]["Room"]["z"]+25,Room[9]["Room"]["z"]+20,Room[9]["Room"]["z"]+50,Room[9]["Room"]["z"]+55,
    Room[9]["Room"]["z"]+75,Room[9]["Room"]["z"]+75,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+90,Room[9]["Room"]["z"]+85]
    Room[9]["Platforme"]["function"] = Platform

    Room[0]["Porte"] = {}
    Room[0]["Porte"]["Type"] = "Porte"
    Room[0]["Porte"]["Size"] = 1
    Room[0]["Porte"]["Range"] = 3
    Room[0]["Porte"]["Rotate"] = [2,1,1]
    Room[0]["Porte"]["Open"] = [3,0,0]
    Room[0]["Porte"]["x"] = [0,-48,48]
    Room[0]["Porte"]["y"] = [-0.4]*len(Room[0]["Porte"]["x"])
    Room[0]["Porte"]["z"] = [-48,0,0]                                           # back, right, left
    Room[0]["Porte"]["Coord"] = [(Room[0]["Room"]["x"],Room[0]["Room"]["z"]-47),(Room[0]["Room"]["x"]-47,Room[0]["Room"]["z"]),(Room[0]["Room"]["x"]+47,Room[0]["Room"]["z"])]
    Room[0]["Porte"]["TpCoord"] = [(Room[4]["Room"]["x"],Room[4]["Room"]["z"]+40,180,4),(Room[2]["Room"]["x"]-17,Room[2]["Room"]["z"], 270,2),(Room[1]["Room"]["x"]-17,Room[1]["Room"]["z"],270,1)] # x,z,rotadegres,RoomNb
    Room[0]["Porte"]["function"] = Door

    Room[1]["Porte"] = {}
    Room[1]["Porte"]["Type"] = "Porte"
    Room[1]["Porte"]["Size"] = 1
    Room[1]["Porte"]["Range"] = 3
    Room[1]["Porte"]["Rotate"] = [1,3]
    Room[1]["Porte"]["Open"] = [0,-1]
    Room[1]["Porte"]["x"] = [Room[1]["Room"]["x"]+24,Room[1]["Room"]["x"]-24]
    Room[1]["Porte"]["y"] = [-0.4]*len(Room[1]["Porte"]["x"])
    Room[1]["Porte"]["z"] = [Room[1]["Room"]["z"],Room[1]["Room"]["z"]] #placer le sprite du TP
    Room[1]["Porte"]["Coord"] = [(Room[1]["Room"]["x"]+22,Room[1]["Room"]["z"]),(Room[1]["Room"]["x"]-22,Room[1]["Room"]["z"])] #placer le TP's range
    Room[1]["Porte"]["TpCoord"] = [(Room[3]["Room"]["x"]-24,Room[3]["Room"]["z"],270,3),(Room[0]["Room"]["x"]+42,Room[0]["Room"]["z"],90,0)]
    Room[1]["Porte"]["function"] = Door

    Room[2]["Porte"] = {}
    Room[2]["Porte"]["Type"] = "Porte"
    Room[2]["Porte"]["Size"] = 1
    Room[2]["Porte"]["Range"] = 3
    Room[2]["Porte"]["Rotate"] = [1,1]
    Room[2]["Porte"]["Open"] = [0,-1]
    Room[2]["Porte"]["x"] = [Room[2]["Room"]["x"]+24,Room[2]["Room"]["x"]-24]
    Room[2]["Porte"]["y"] = [-0.4]*len(Room[2]["Porte"]["x"])
    Room[2]["Porte"]["z"] = [Room[2]["Room"]["z"],Room[2]["Room"]["z"]] #placer le sprite du TP
    Room[2]["Porte"]["Coord"] = [(Room[2]["Room"]["x"]+23,Room[2]["Room"]["z"]),(Room[2]["Room"]["x"]-22,Room[2]["Room"]["z"])] #placer le TP's range ##may bug
    Room[2]["Porte"]["TpCoord"] = [(Room[4]["Room"]["x"]+24,Room[4]["Room"]["z"],90,4),(Room[0]["Room"]["x"]-42,Room[0]["Room"]["z"],-90,0)]
    Room[2]["Porte"]["function"] = Door



    Room[3]["Porte"] = {}
    Room[3]["Porte"]["Type"] = "Porte"
    Room[3]["Porte"]["Size"] = 1
    Room[3]["Porte"]["Range"] = 5
    Room[3]["Porte"]["Rotate"] = [0,1]
    Room[3]["Porte"]["Open"] = [-3,-1] #-3 TP n'apparait pas, -2 TP apparait
    Room[3]["Porte"]["x"] = [Room[3]["Room"]["x"],Room[3]["Room"]["x"]-30]
    Room[3]["Porte"]["y"] = [-0.4]*len(Room[3]["Porte"]["x"])
    Room[3]["Porte"]["z"] = [Room[3]["Room"]["z"],Room[3]["Room"]["z"]]
    Room[3]["Porte"]["Coord"] = [(Room[3]["Room"]["x"],Room[3]["Room"]["z"]),(Room[3]["Room"]["x"]-29,Room[3]["Room"]["z"])]
    Room[3]["Porte"]["TpCoord"] = [(Room[5]["Room"]["x"],Room[5]["Room"]["z"]+40,180,5),(Room[1]["Room"]["x"]+18,Room[1]["Room"]["z"],90,1)] # x,z,rotadegres,RoomNb
    Room[3]["Porte"]["function"] = Door

    Room[4]["Porte"] = {}
    Room[4]["Porte"]["Type"] = "Porte"
    Room[4]["Porte"]["Size"] = 1
    Room[4]["Porte"]["Range"] = 4.5
    Room[4]["Porte"]["Rotate"] = [0,1]
    Room[4]["Porte"]["Open"] = [-3,-1] #-3 TP n'apparait pas, -2 TP apparait
    Room[4]["Porte"]["x"] = [Room[4]["Room"]["x"],Room[4]["Room"]["x"]+30]
    Room[4]["Porte"]["y"] = [-0.4]*len(Room[4]["Porte"]["x"])
    Room[4]["Porte"]["z"] = [Room[4]["Room"]["z"],Room[4]["Room"]["z"]]
    Room[4]["Porte"]["Coord"] = [(Room[4]["Room"]["x"],Room[4]["Room"]["z"]),(Room[4]["Room"]["x"]+29,Room[4]["Room"]["z"])]
    Room[4]["Porte"]["TpCoord"] = [(Room[6]["Room"]["x"],Room[6]["Room"]["z"]-40,0,6),(Room[2]["Room"]["x"]+18,Room[2]["Room"]["z"],90,2)] # x,z,rotadegres,RoomNb
    Room[4]["Porte"]["function"] = Door

    Room[5]["Porte"] = {}
    Room[5]["Porte"]["Type"] = "Porte"
    Room[5]["Porte"]["Size"] = 1
    Room[5]["Porte"]["Range"] = 3
    Room[5]["Porte"]["Rotate"] = [0,2]
    Room[5]["Porte"]["Open"] = [0,-1]
    Room[5]["Porte"]["x"] = [Room[5]["Room"]["x"],Room[5]["Room"]["x"]]
    Room[5]["Porte"]["y"] = [-0.4]*len(Room[5]["Porte"]["x"])
    Room[5]["Porte"]["z"] = [Room[5]["Room"]["z"]-48,Room[5]["Room"]["z"]+48] #placer le sprite du TP
    Room[5]["Porte"]["Coord"] = [(Room[5]["Room"]["x"],Room[5]["Room"]["z"]-47),(Room[5]["Room"]["x"],Room[5]["Room"]["z"]+47)] #placer le TP's range
    Room[5]["Porte"]["TpCoord"] = [(Room[7]["Room"]["x"]-25,Room[7]["Room"]["z"],270,7),(Room[3]["Room"]["x"]-10,Room[3]["Room"]["z"],90,3)]
    Room[5]["Porte"]["function"] = Door


    Room[6]["Porte"] = {}
    Room[6]["Porte"]["Type"] = "Porte"
    Room[6]["Porte"]["Size"] = 1
    Room[6]["Porte"]["Range"] = 3
    Room[6]["Porte"]["Rotate"] = [0,2]
    Room[6]["Porte"]["Open"] = [0,-1]
    Room[6]["Porte"]["x"] = [Room[6]["Room"]["x"],Room[6]["Room"]["x"]]
    Room[6]["Porte"]["y"] = [-0.4]*len(Room[6]["Porte"]["x"])
    Room[6]["Porte"]["z"] = [Room[6]["Room"]["z"]+48,Room[6]["Room"]["z"]-48] #placer le sprite du TP
    Room[6]["Porte"]["Coord"] = [(Room[6]["Room"]["x"],Room[6]["Room"]["z"]+47),(Room[6]["Room"]["x"],Room[6]["Room"]["z"]-47)] #placer le TP's range
    Room[6]["Porte"]["TpCoord"] = [(Room[8]["Room"]["x"]-24,Room[8]["Room"]["z"],270,8),(Room[4]["Room"]["x"]+12,Room[4]["Room"]["z"],270,4)]
    Room[6]["Porte"]["function"] = Door


    Room[7]["Porte"] = {}
    Room[7]["Porte"]["Type"] = "Porte"
    Room[7]["Porte"]["Size"] = 1
    Room[7]["Porte"]["Range"] = 3
    Room[7]["Porte"]["Rotate"] = [1,3]
    Room[7]["Porte"]["Open"] = [0,-1]
    Room[7]["Porte"]["x"] = [Room[7]["Room"]["x"]+30,Room[7]["Room"]["x"]-30]
    Room[7]["Porte"]["y"] = [-0.4]*len(Room[7]["Porte"]["x"])
    Room[7]["Porte"]["z"] = [Room[7]["Room"]["z"],Room[7]["Room"]["z"]] #placer le sprite du TP
    Room[7]["Porte"]["Coord"] = [(Room[7]["Room"]["x"]+29,Room[7]["Room"]["z"]),(Room[7]["Room"]["x"]-29,Room[7]["Room"]["z"])] #placer le TP's range
    Room[7]["Porte"]["TpCoord"] = [(Room[9]["Room"]["x"]-90,Room[9]["Room"]["z"]-94,0,9),(Room[5]["Room"]["x"],Room[5]["Room"]["z"]-43.5,0,5)]
    Room[7]["Porte"]["function"] = Door


    Room[8]["Porte"] = {}
    Room[8]["Porte"]["Type"] = "Porte"
    Room[8]["Porte"]["Size"] = 1
    Room[8]["Porte"]["Range"] = 3
    Room[8]["Porte"]["Rotate"] = [1,3]
    Room[8]["Porte"]["Open"] = [0,-1]
    Room[8]["Porte"]["x"] = [Room[8]["Room"]["x"]+30,Room[8]["Room"]["x"]-30]
    Room[8]["Porte"]["y"] = [-0.4]*len(Room[8]["Porte"]["x"])
    Room[8]["Porte"]["z"] = [Room[8]["Room"]["z"],Room[8]["Room"]["z"]] #placer le sprite du TP
    Room[8]["Porte"]["Coord"] = [(Room[8]["Room"]["x"]+29,Room[8]["Room"]["z"]),(Room[8]["Room"]["x"]-29,Room[8]["Room"]["z"])] #placer le TP's range
    Room[8]["Porte"]["TpCoord"] = [(Room[9]["Room"]["x"]+90,Room[9]["Room"]["z"]-94,0,9),(Room[6]["Room"]["x"],Room[6]["Room"]["z"]+42,180,6)]
    Room[8]["Porte"]["function"] = Door

    Room[9]["Porte"] = {}
    Room[9]["Porte"]["Type"] = "Porte"
    Room[9]["Porte"]["Size"] = 1
    Room[9]["Porte"]["Range"] = 3
    Room[9]["Porte"]["Rotate"] = [0,2,2]
    Room[9]["Porte"]["Open"] = [1,-1,-1]
    Room[9]["Porte"]["x"] = [Room[9]["Room"]["x"],Room[9]["Room"]["x"]-90,Room[9]["Room"]["x"]+90]
    Room[9]["Porte"]["y"] = [68.6,4.6,4.6]
    Room[9]["Porte"]["z"] = [Room[9]["Room"]["z"]+100,Room[9]["Room"]["z"]-100,Room[9]["Room"]["z"]-100] #placer le sprite du TP
    Room[9]["Porte"]["Coord"] = [(Room[9]["Room"]["x"],Room[9]["Room"]["z"]+99),(Room[9]["Room"]["x"]-90,Room[9]["Room"]["z"]-99),(Room[9]["Room"]["x"]+90,Room[9]["Room"]["z"]-99)]
    Room[9]["Porte"]["TpCoord"] = [(Room[10]["Room"]["x"],Room[10]["Room"]["z"]+50,180,10),(Room[7]["Room"]["x"]+24,Room[7]["Room"]["z"],90,7),(Room[8]["Room"]["x"]+24,Room[8]["Room"]["z"],90,8)]
    Room[9]["Porte"]["function"] = Door

    Room[10]["Porte"] = {}
    Room[10]["Porte"]["Type"] = "Porte"
    Room[10]["Porte"]["Size"] = 1
    Room[10]["Porte"]["Range"] = 3
    Room[10]["Porte"]["Rotate"] = [0]
    Room[10]["Porte"]["Open"] = [0]
    Room[10]["Porte"]["x"] = [Room[10]["Room"]["x"]]
    Room[10]["Porte"]["y"] = [-0.4]
    Room[10]["Porte"]["z"] = [Room[10]["Room"]["z"]+65] #placer le sprite du TP
    Room[10]["Porte"]["Coord"] = [(Room[10]["Room"]["x"],Room[10]["Room"]["z"]+64)]
    Room[10]["Porte"]["TpCoord"] = [(Room[0]["Room"]["x"],Room[0]["Room"]["z"]-30,180,0)]
    Room[10]["Porte"]["function"] = Door


    Room[0]["Bouton"] = {}
    Room[0]["Bouton"]["Type"] = "Cylindre"
    Room[0]["Bouton"]["Range"] = 3.5
    Room[0]["Bouton"]["Coord"] = [(Room[0]["Room"]["x"],-1.1,Room[0]["Room"]["z"]-20)]
    Room[0]["Bouton"]["Pressed"] = [False]
    Room[0]["Bouton"]["function"] = Button


    Room[1]["Bouton"] = {}
    Room[1]["Bouton"]["Type"] = "Cylindre"
    Room[1]["Bouton"]["Range"] = 3.5
    Room[1]["Bouton"]["Coord"] = [(Room[1]["Room"]["x"],2.1,Room[1]["Room"]["z"])]
    Room[1]["Bouton"]["Pressed"] = [False]
    Room[1]["Bouton"]["function"] = Button


    Room[2]["Bouton"] = {}
    Room[2]["Bouton"]["Type"] = "Cylindre"
    Room[2]["Bouton"]["Range"] = 3.5
    Room[2]["Bouton"]["Coord"] = [(Room[2]["Room"]["x"],2.1,Room[2]["Room"]["z"])]
    Room[2]["Bouton"]["Pressed"] = [False]
    Room[2]["Bouton"]["function"] = Button

    Room[6]["Bouton"] = {}
    Room[6]["Bouton"]["Type"] = "Cylindre"
    Room[6]["Bouton"]["Range"] = 3.5
    Room[6]["Bouton"]["Coord"] = [(Room[6]["Room"]["x"]+20,-1.1,Room[6]["Room"]["z"]),(Room[6]["Room"]["x"]+20,-1.1,Room[6]["Room"]["z"]-20),(Room[6]["Room"]["x"]-20,-1.1,Room[6]["Room"]["z"]+20),
    (Room[6]["Room"]["x"]-20,-1.1,Room[6]["Room"]["z"]-20),(Room[6]["Room"]["x"]+20,-1.1,Room[6]["Room"]["z"]+20), (Room[6]["Room"]["x"]-20,-1.1,Room[6]["Room"]["z"]), (Room[6]["Room"]["x"],-1.1,Room[6]["Room"]["z"]+10)]
    Room[6]["Bouton"]["Pressed"] = [False,False,False,False,False,False,False]
    Room[6]["Bouton"]["function"] = Button

    Room[0]["Pilier"] = {}
    Room[0]["Pilier"]["Type"] = "Cylindre"
    Room[0]["Pilier"]["Size"] = 4
    Room[0]["Pilier"]["Coord"] = [(0,0)]
    Room[0]["Pilier"]["function"] ="None"


    Room[5]["Pilier"] = {}
    Room[5]["Pilier"]["Type"] = "Cylindre"
    Room[5]["Pilier"]["Size"] = 3.5
    Room[5]["Pilier"]["Coord"] = [(Room[5]["Room"]["x"]+35,Room[5]["Room"]["z"]),(Room[5]["Room"]["x"]-35,Room[5]["Room"]["z"]),(Room[5]["Room"]["x"]+35,Room[5]["Room"]["z"]-31),
    (Room[5]["Room"]["x"]-35,Room[5]["Room"]["z"]-31),(Room[5]["Room"]["x"]+35,Room[5]["Room"]["z"]+31),(Room[5]["Room"]["x"]-35,Room[5]["Room"]["z"]+31),
    (Room[5]["Room"]["x"]+31,Room[5]["Room"]["z"]+35),(Room[5]["Room"]["x"]+31,Room[5]["Room"]["z"]-35),(Room[5]["Room"]["x"]-31,Room[5]["Room"]["z"]+35),(Room[5]["Room"]["x"]-31,Room[5]["Room"]["z"]-35)]
    Room[5]["Pilier"]["function"] ="None"


    Room[6]["Pilier"] = {}
    Room[6]["Pilier"]["Type"] = "Cylindre"
    Room[6]["Pilier"]["Size"] = 3.5
    Room[6]["Pilier"]["Coord"] = [(Room[6]["Room"]["x"]+35,Room[6]["Room"]["z"]),(Room[6]["Room"]["x"]-35,Room[6]["Room"]["z"]),(Room[6]["Room"]["x"]+35,Room[6]["Room"]["z"]-31),
    (Room[6]["Room"]["x"]-35,Room[6]["Room"]["z"]-31),(Room[6]["Room"]["x"]+35,Room[6]["Room"]["z"]+31),(Room[6]["Room"]["x"]-35,Room[6]["Room"]["z"]+31),
    (Room[6]["Room"]["x"]+31,Room[6]["Room"]["z"]+35),(Room[6]["Room"]["x"]+31,Room[6]["Room"]["z"]-35),(Room[6]["Room"]["x"]-31,Room[6]["Room"]["z"]+35),(Room[6]["Room"]["x"]-31,Room[6]["Room"]["z"]-35)]
    Room[6]["Pilier"]["function"] ="None"


    Room[10]["Pilier"] = {}
    Room[10]["Pilier"]["Type"] = "Cylindre"
    Room[10]["Pilier"]["Size"] = 3.5
    Room[10]["Pilier"]["Coord"] = [(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]+12),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]-12),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]+24),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]-24),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]+36),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]-36),(Room[10]["Room"]["x"]+12,Room[10]["Room"]["z"]+48),
                                   (Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]+12),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]-12),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]+24),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]-24),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]+36),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]-36),(Room[10]["Room"]["x"]-12,Room[10]["Room"]["z"]+48)]
    Room[10]["Pilier"]["function"] ="None"

    Room[10]["Bear"] = {}
    Room[10]["Bear"]["Type"] = "Cylindre"
    Room[10]["Bear"]["Size"] = 7
    Room[10]["Bear"]["Coord"] = [(Room[10]["Room"]["x"],Room[10]["Room"]["z"]-55)]
    Room[10]["Bear"]["function"] ="None"

    Room[7]["Signs"] = {}
    Room[7]["Signs"]["Type"] = "Signe"
    Room[7]["Signs"]["Size"] = 1
    Room[7]["Signs"]["x"] = [Room[7]["Room"]["x"]-8,Room[7]["Room"]["x"],Room[7]["Room"]["x"]+8,
                            Room[7]["Room"]["x"]-8,Room[7]["Room"]["x"],Room[7]["Room"]["x"]+8,
                            Room[7]["Room"]["x"]-8,Room[7]["Room"]["x"],Room[7]["Room"]["x"]+8]
    Room[7]["Signs"]["y"] = 0
    Room[7]["Signs"]["z"] = [Room[7]["Room"]["z"]-8,Room[7]["Room"]["z"]-8,Room[7]["Room"]["z"]-8,
                            Room[7]["Room"]["z"]-16,Room[7]["Room"]["z"]-16,Room[7]["Room"]["z"]-16,
                            Room[7]["Room"]["z"]-24,Room[7]["Room"]["z"]-24,Room[7]["Room"]["z"]-24]
    Room[7]["Signs"]["function"] = Sign
    Room[7]["Signs"]["Nb"] = [1,2,3,4,5,6,7,8,9]
    Room[7]["Signs"]["Rotate"] = [3,1,2,0,0,1,2,3,1]


    Room[7]["Stair"] = {}
    Room[7]["Stair"]["Type"] = "Escalier"
    Room[7]["Stair"]["Size"] = 1
    Room[7]["Stair"]["x"] = [Room[7]["Room"]["x"],Room[7]["Room"]["x"],Room[7]["Room"]["x"],Room[7]["Room"]["x"]]
    Room[7]["Stair"]["y"] = 0
    Room[7]["Stair"]["z"] = [Room[7]["Room"]["z"]+12,Room[7]["Room"]["z"]+12-3,Room[7]["Room"]["z"]+12-5,Room[7]["Room"]["z"]+12-7]
    Room[7]["Stair"]["function"] = Stair
    Room[7]["Stair"]["Nb"] = [1,2,3,4]

    Room[8]["Stair"] = {}
    Room[8]["Stair"]["Type"] = "Escalier"
    Room[8]["Stair"]["Size"] = 1
    Room[8]["Stair"]["x"] = [Room[8]["Room"]["x"],Room[8]["Room"]["x"],Room[8]["Room"]["x"],Room[8]["Room"]["x"]]
    Room[8]["Stair"]["y"] = 0
    Room[8]["Stair"]["z"] = [Room[8]["Room"]["z"]+12,Room[8]["Room"]["z"]+12-3,Room[8]["Room"]["z"]+12-5,Room[8]["Room"]["z"]+12-7]
    Room[8]["Stair"]["function"] = Stair
    Room[8]["Stair"]["Nb"] = [1,2,3,4]

    Room[10]["Stair"] = {}
    Room[10]["Stair"]["Type"] = "Escalier"
    Room[10]["Stair"]["Size"] = 1.1
    Room[10]["Stair"]["x"] = [Room[10]["Room"]["x"],Room[10]["Room"]["x"],Room[10]["Room"]["x"]]
    Room[10]["Stair"]["y"] = 0
    Room[10]["Stair"]["z"] = [Room[10]["Room"]["z"]-53,Room[10]["Room"]["z"]-54,Room[10]["Room"]["z"]-55]
    Room[10]["Stair"]["function"] = Stair
    Room[10]["Stair"]["Nb"] = [5,6,7]

    Room[3]["Key"] = {}
    Room[3]["Key"]["Type"] = "Clef"
    Room[3]["Key"]["Size"] = 1
    Room[3]["Key"]["Range"] = 7
    Room[3]["Key"]["x"] = Room[3]["Room"]["x"]
    Room[3]["Key"]["y"] = Room[3]["Room"]["y"]+2
    Room[3]["Key"]["z"] = Room[3]["Room"]["z"]
    Room[3]["Key"]["function"] = Key
    Room[3]["Key"]["Nb"] = 0
    Room[3]["Key"]["Appear"] = False
    Room[3]["Key"]["Taken"] = False

    Room[6]["Key"] = {}
    Room[6]["Key"]["Type"] = "Clef"
    Room[6]["Key"]["Size"] = 1
    Room[6]["Key"]["Range"] = 4
    Room[6]["Key"]["x"] = Room[6]["Room"]["x"]
    Room[6]["Key"]["y"] = Room[6]["Room"]["y"]+2
    Room[6]["Key"]["z"] = Room[6]["Room"]["z"] + 40
    Room[6]["Key"]["function"] = Key
    Room[6]["Key"]["Nb"] = 1
    Room[6]["Key"]["Appear"] = False
    Room[6]["Key"]["Taken"] = False

    Room[7]["Key"] = {}
    Room[7]["Key"]["Type"] = "Clef"
    Room[7]["Key"]["Size"] = 1
    Room[7]["Key"]["Range"] = 4
    Room[7]["Key"]["x"] = Room[7]["Room"]["x"]+20
    Room[7]["Key"]["y"] = Room[7]["Room"]["y"]+2
    Room[7]["Key"]["z"] = Room[7]["Room"]["z"]
    Room[7]["Key"]["function"] = Key
    Room[7]["Key"]["Nb"] = 2
    Room[7]["Key"]["Appear"] = False
    Room[7]["Key"]["Taken"] = False

    Room[10]["Key"] = {}
    Room[10]["Key"]["Type"] = "Clef"
    Room[10]["Key"]["Size"] = 1
    Room[10]["Key"]["Range"] = 4
    Room[10]["Key"]["x"] = Room[10]["Room"]["x"]
    Room[10]["Key"]["y"] = Room[10]["Room"]["y"] + 3
    Room[10]["Key"]["z"] = Room[10]["Room"]["z"] - 44
    Room[10]["Key"]["function"] = Key
    Room[10]["Key"]["Nb"] = 3
    Room[10]["Key"]["Appear"] = True
    Room[10]["Key"]["Taken"] = False
    #---------------- FIN D'INITIALISATION DU DICTIONNAIRE --------------------------------


    #---------------- CHARGEMENT DES .OBJ--------------------------------------------------
    global objroom1, objroom2, objroom3, objroom4, objroom5,objroom6,objroom7,objroom8,objroom9,objroom10, objdooropen, objdoorclose,objbackdoor,objfinaldoor, objplatforme, objbutton1, objarmoire1, objarmoire2, objarmoire3, objarmoire4, objarmoire5, objblackbox, objcube1, objcube2, objcube3,objcube,objcell,objtp,objsigne1,objsigne2,objsigne3,objsigne4,objsigne5,objsigne6,objsigne7,objsigne8,objsigne9,objtable, objhauteur1, objhauteur2, objhauteur3, objhauteur4, objhauteur5, objhauteur6, objhauteur7,skin1,skin2,skin3,skin4,skinlist,objbegindoor,objbeginopen,list_chiffre,chiffre_0,chiffre_1,chiffre_2,chiffre_3,chiffre_4,chiffre_5,chiffre_6,chiffre_7,chiffre_8,chiffre_9,chiffre_vide,chiffre_point,objkey,skin

    room1 = os.path.join(scriptDIR,"salle_1.obj")
    objroom1 = OBJ(room1,swapyz = True)
    room2 = os.path.join(scriptDIR,"salle2_1_2.obj")
    objroom2 = OBJ(room2,swapyz = True)
    room3 = os.path.join(scriptDIR,"salle3_1.obj")
    objroom3 = OBJ(room3,swapyz = True)
    room4 = os.path.join(scriptDIR,"salle3_2.obj")
    objroom4 = OBJ(room4,swapyz = True)
    room5 = os.path.join(scriptDIR,"salle4_1.obj")
    objroom5 = OBJ(room5,swapyz = True)
    room6 = os.path.join(scriptDIR,"salle4_2.obj")
    objroom6 = OBJ(room6,swapyz = True)
    room7 = os.path.join(scriptDIR,"salle5_1.obj")
    objroom7 = OBJ(room7,swapyz = True)
    room8 = os.path.join(scriptDIR,"salle5_2.obj")
    objroom8 = OBJ(room8,swapyz = True)
    room9 = os.path.join(scriptDIR,"salle6.obj")
    objroom9 = OBJ(room9,swapyz = True)
    room10 = os.path.join(scriptDIR,"salle7_moins_poly.obj")
    objroom10 = OBJ(room10,swapyz = True)

    begindoor = os.path.join(scriptDIR,"grande_porte_fermee.obj")
    objbegindoor = OBJ(begindoor, swapyz = True)
    beginopen = os.path.join(scriptDIR,"gande_porte_ouvert.obj")
    objbeginopen = OBJ(beginopen, swapyz = True)

    dooropen = os.path.join(scriptDIR,"porte_ouverte.obj")
    objdooropen = OBJ(dooropen,swapyz = True)
    doorclose = os.path.join(scriptDIR,"porte_fermée.obj")
    objdoorclose = OBJ(doorclose,swapyz = True)
    backdoor = os.path.join(scriptDIR,"porte_ouverte2.obj")
    objbackdoor = OBJ(backdoor,swapyz = True)
    finaldoor = os.path.join(scriptDIR,"porte_ouverte3.obj")
    objfinaldoor = OBJ(finaldoor,swapyz=True)
    tp = os.path.join(scriptDIR,"tp.obj")
    objtp = OBJ(tp,swapyz=True)

    button1 = os.path.join(scriptDIR,"bouton_sol.obj")
    objbutton1 = OBJ(button1,swapyz = True)

    armoire1 = os.path.join(scriptDIR,"armoire1.obj")
    objarmoire1 = OBJ(armoire1,swapyz = True)
    armoire2 = os.path.join(scriptDIR,"armoire2.obj")
    objarmoire2 = OBJ(armoire2,swapyz = True)
    armoire3 = os.path.join(scriptDIR,"armoire3.obj")
    objarmoire3 = OBJ(armoire3,swapyz = True)
    armoire5 = os.path.join(scriptDIR,"armoire5.obj")
    objarmoire5 = OBJ(armoire5,swapyz = True)
    armoire4 = os.path.join(scriptDIR,"armoire4.obj")
    objarmoire4 = OBJ(armoire4,swapyz = True)

    blackbox = os.path.join(scriptDIR,"selecteur_symbole.obj")
    objblackbox = OBJ(blackbox,swapyz = True)
    cube1 = os.path.join(scriptDIR,"cube1.obj")
    objcube1 = OBJ(cube1,swapyz = True)
    cube2 = os.path.join(scriptDIR,"cube2.obj")
    objcube2 = OBJ(cube2,swapyz = True)
    cube3 = os.path.join(scriptDIR,"cube3.obj")
    objcube3 = OBJ(cube3,swapyz = True)

    platforme = os.path.join(scriptDIR,"plateforme.obj")
    objplatforme = OBJ(platforme,swapyz = True)

    table = os.path.join(scriptDIR,"table.obj")
    objtable = OBJ(table,swapyz = True)

    hauteur1 = os.path.join(scriptDIR,"hauteur1.obj")
    objhauteur1 = OBJ(hauteur1,swapyz = True)
    hauteur2 = os.path.join(scriptDIR,"hauteur2.obj")
    objhauteur2 = OBJ(hauteur2,swapyz = True)
    hauteur3 = os.path.join(scriptDIR,"hauteur3.obj")
    objhauteur3 = OBJ(hauteur3,swapyz = True)
    hauteur4 = os.path.join(scriptDIR,"hauteur4.obj")
    objhauteur4 = OBJ(hauteur4,swapyz = True)
    hauteur5 = os.path.join(scriptDIR,"hauteur5.obj")
    objhauteur5 = OBJ(hauteur5,swapyz = True)
    hauteur6 = os.path.join(scriptDIR,"hauteur6.obj")
    objhauteur6 = OBJ(hauteur6,swapyz = True)
    hauteur7 = os.path.join(scriptDIR,"hauteur7.obj")
    objhauteur7 = OBJ(hauteur7,swapyz = True)

    cell = os.path.join(scriptDIR,"prison.obj")
    objcell = OBJ(cell,swapyz = True)

    cube = os.path.join(scriptDIR,"aa.obj")
    objcube = OBJ(cube,swapyz = True)

    key = os.path.join(scriptDIR,"clef.obj")
    objkey = OBJ(key,swapyz = True)

    signe1 = os.path.join(scriptDIR,"signe1.obj")
    objsigne1 = OBJ(signe1,swapyz = True)
    signe2 = os.path.join(scriptDIR,"signe2.obj")
    objsigne2 = OBJ(signe2,swapyz = True)
    signe3 = os.path.join(scriptDIR,"signe4.obj")
    objsigne3 = OBJ(signe3,swapyz = True)
    signe4 = os.path.join(scriptDIR,"signe6.obj")
    objsigne4 = OBJ(signe4,swapyz = True)
    signe5 = os.path.join(scriptDIR,"signe8.obj")
    objsigne5 = OBJ(signe5,swapyz = True)
    signe6 = os.path.join(scriptDIR,"signe10.obj")
    objsigne6 = OBJ(signe6,swapyz = True)
    signe7 = os.path.join(scriptDIR,"signe13.obj")
    objsigne7 = OBJ(signe7,swapyz = True)
    signe8 = os.path.join(scriptDIR,"signe14.obj")
    objsigne8 = OBJ(signe8,swapyz = True)
    signe9 = os.path.join(scriptDIR,"signe16.obj")
    objsigne9 = OBJ(signe9,swapyz = True)

    chiffre_1 = os.path.join(scriptDIR,"1.png")
    chiffre_2 = os.path.join(scriptDIR,"2.png")
    chiffre_3 = os.path.join(scriptDIR,"3.png")
    chiffre_4 = os.path.join(scriptDIR,"4.png")
    chiffre_5 = os.path.join(scriptDIR,"5.png")
    chiffre_6 = os.path.join(scriptDIR,"6.png")
    chiffre_7 = os.path.join(scriptDIR,"7.png")
    chiffre_8 = os.path.join(scriptDIR,"8.png")
    chiffre_9 = os.path.join(scriptDIR,"9.png")
    chiffre_0 = os.path.join(scriptDIR,"0.png")
    chiffre_point = os.path.join(scriptDIR,"point.png")
    chiffre_vide = os.path.join(scriptDIR,"vide.png")

    list_chiffre = [chiffre_0,chiffre_1,chiffre_2,chiffre_3,chiffre_4,chiffre_5,chiffre_6,chiffre_7,chiffre_8,chiffre_9,chiffre_vide]

    skin1 = os.path.join(scriptDIR,"perso1.obj")
    objskinJ1 = OBJ(skin1,swapyz = True)
    skin2 = os.path.join(scriptDIR,"perso2.obj")
    objskinJ2 = OBJ(skin2,swapyz = True)
    skin3 = os.path.join(scriptDIR,"perso3.obj")
    objskinJ3 = OBJ(skin3,swapyz = True)
    skin4 = os.path.join(scriptDIR,"perso4.obj")
    objskinJ4 = OBJ(skin4,swapyz = True)
    skin = [objskinJ1,objskinJ2,objskinJ3,objskinJ4]

    #------------ FIN DU CHARGEMENT DES OBJS---------------------------------------------



    #----------- REMPLISSAGE DU DICO GRACE AUX FICHIER .OBJ------------------------------

    roomlist = [objroom1,objroom2,objroom2,objroom3,objroom4,objroom5,objroom6,objroom7,objroom8,objroom9,objroom10]

    Room[0]["Room"]["filename"] = room1
    Room[1]["Room"]["filename"] = room2
    Room[2]["Room"]["filename"] = room2
    Room[3]["Room"]["filename"] = room3
    Room[4]["Room"]["filename"] = room4
    Room[5]["Room"]["filename"] = room5
    Room[6]["Room"]["filename"] = room6
    Room[7]["Room"]["filename"] = room7
    Room[8]["Room"]["filename"] = room8
    Room[9]["Room"]["filename"] = room9
    Room[10]["Room"]["filename"] = room10

    Room[1]["Bibli"]["filename"] = [armoire1,armoire1,armoire1,armoire1,armoire3,armoire4,armoire5,armoire5,armoire3,armoire4]
    Room[2]["Bibli"]["filename"] = [armoire1,armoire1,armoire1,armoire1,armoire3,armoire4,armoire5,armoire5,armoire3,armoire4]

    Room[1]["Table"]["filename"] = [table]
    Room[2]["Table"]["filename"] = [table]

    Room[3]["BlackBox"]["filename"] = [blackbox,blackbox,blackbox]

    Room[9]["Platforme"]["filename"] = len(Room[9]["Platforme"]["x"])*[platforme]

    Room[3]["Cell"]["filename"] = [cell,cell,cell,cell]
    Room[4]["Cell"]["filename"] = [cell,cell,cell,cell]

    Room[7]["Stair"]["filename"] = [hauteur1,hauteur2,hauteur3,hauteur4]
    Room[8]["Stair"]["filename"] = [hauteur1,hauteur2,hauteur3,hauteur4]
    Room[10]["Stair"]["filename"] = [hauteur5,hauteur6,hauteur7]


    for numRoom in range(nbRoom):
        for objet in Room[numRoom]:
            if Room[numRoom][objet]["Type"] == "Cube" or Room[numRoom][objet]["Type"]=="Bibli" or objet == "Cell" or objet == "Stair" or objet == "Platforme" or objet == "Table":

                dist_collision = 2
                Room[numRoom][objet]["max_xs"] = {}
                Room[numRoom][objet]["min_xs"] = {}
                Room[numRoom][objet]["max_ys"] = {}
                Room[numRoom][objet]["min_ys"] = {}
                Room[numRoom][objet]["max_zs"] = {}
                Room[numRoom][objet]["min_zs"] = {}
                Room[numRoom][objet]["max_x"] = {}
                Room[numRoom][objet]["max_y"] = {}
                Room[numRoom][objet]["max_z"] = {}
                Room[numRoom][objet]["min_x"] = {}
                Room[numRoom][objet]["min_y"] = {}
                Room[numRoom][objet]["min_z"] = {}
                for j in range(len(Room[numRoom][objet]["filename"])):
                    filename = Room[numRoom][objet]["filename"][j]
                    for line in open(filename, "r"):
                        if line.startswith('#'): continue
                        values = line.split()
                        if not values: continue
                        if values[0] == 'v':
                            v = list(map(float, values[1:4]))
                            if j not in Room[numRoom][objet]["max_x"].keys() :
                                Room[numRoom][objet]["max_x"][j] = v[0]
                                Room[numRoom][objet]["max_y"][j] = v[1]
                                Room[numRoom][objet]["max_z"][j] = v[2]
                                Room[numRoom][objet]["min_x"][j] = v[0]
                                Room[numRoom][objet]["min_y"][j] = v[1]
                                Room[numRoom][objet]["min_z"][j] = v[2]
                            else :
                                if Room[numRoom][objet]["max_x"][j] < v[0] :
                                    Room[numRoom][objet]["max_x"][j] = v[0]
                                if Room[numRoom][objet]["max_y"][j] < v[1] :
                                    Room[numRoom][objet]["max_y"][j] = v[1]
                                if Room[numRoom][objet]["max_z"][j] < v[2] :
                                    Room[numRoom][objet]["max_z"][j] = v[2]
                                if Room[numRoom][objet]["min_x"][j] > v[0] :
                                    Room[numRoom][objet]["min_x"][j] = v[0]
                                if Room[numRoom][objet]["min_y"][j] > v[1] :
                                    Room[numRoom][objet]["min_y"][j] = v[1]
                                if Room[numRoom][objet]["min_z"][j] > v[2] :
                                    Room[numRoom][objet]["min_z"][j] = v[2]
                    Room[numRoom][objet]["max_xs"][j] = Room[numRoom][objet]["max_x"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["x"][j] + dist_collision
                    Room[numRoom][objet]["min_xs"][j] = Room[numRoom][objet]["min_x"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["x"][j] - dist_collision
                    if objet != "Platforme"  and objet != "Bibli":
                        Room[numRoom][objet]["max_ys"][j] = Room[numRoom][objet]["max_y"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"]
                        Room[numRoom][objet]["min_ys"][j] = Room[numRoom][objet]["min_y"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"]
                    else :
                        Room[numRoom][objet]["max_ys"][j] = Room[numRoom][objet]["max_y"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"][j]
                        Room[numRoom][objet]["min_ys"][j] = Room[numRoom][objet]["min_y"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"][j]-dist_collision
                    Room[numRoom][objet]["max_zs"][j] = Room[numRoom][objet]["max_z"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["z"][j] + dist_collision
                    Room[numRoom][objet]["min_zs"][j] = Room[numRoom][objet]["min_z"][j]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["z"][j] - dist_collision

            elif  Room[numRoom][objet]["Type"] == "Room":
                filename = Room[numRoom][objet]["filename"]
                for line in open(filename, "r"):
                    if line.startswith('#'): continue
                    values = line.split()
                    if not values: continue
                    if values[0] == 'v':
                        v = list(map(float, values[1:4]))
                        if "max_x" not in Room[numRoom][objet].keys() :
                            Room[numRoom][objet]["max_x"] = v[0]
                            Room[numRoom][objet]["max_y"] = v[1]
                            Room[numRoom][objet]["max_z"] = v[2]
                            Room[numRoom][objet]["min_x"] = v[0]
                            Room[numRoom][objet]["min_y"] = v[1]
                            Room[numRoom][objet]["min_z"] = v[2]
                        else :
                            if Room[numRoom][objet]["max_x"] < v[0] :
                                Room[numRoom][objet]["max_x"] = v[0]
                            if Room[numRoom][objet]["max_y"] < v[1] :
                                Room[numRoom][objet]["max_y"] = v[1]
                            if Room[numRoom][objet]["max_z"] < v[2] :
                                Room[numRoom][objet]["max_z"] = v[2]
                            if Room[numRoom][objet]["min_x"] > v[0] :
                                Room[numRoom][objet]["min_x"] = v[0]
                            if Room[numRoom][objet]["min_y"] > v[1] :
                                Room[numRoom][objet]["min_y"] = v[1]
                            if Room[numRoom][objet]["min_z"] > v[2] :
                                Room[numRoom][objet]["min_z"] = v[2]
                dist_collision = -1.8
                Room[numRoom][objet]["max_x"] = Room[numRoom][objet]["max_x"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["x"] + dist_collision
                Room[numRoom][objet]["min_x"] = Room[numRoom][objet]["min_x"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["x"] - dist_collision
                Room[numRoom][objet]["max_y"] = Room[numRoom][objet]["max_y"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"]
                Room[numRoom][objet]["min_y"] = Room[numRoom][objet]["min_y"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["y"]
                Room[numRoom][objet]["max_z"] = Room[numRoom][objet]["max_z"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["z"] + dist_collision
                Room[numRoom][objet]["min_z"] = Room[numRoom][objet]["min_z"]*(Room[numRoom][objet]["Size"]) + Room[numRoom][objet]["z"] - dist_collision

                #print([Room[numRoom][objet]["max_x"],Room[numRoom][objet]["min_x"],Room[numRoom][objet]["max_z"],Room[numRoom][objet]["min_z"]])
                #sys.stdout.flush()

    #----------- FIN DU REMPLISSAGE DU DICO GRACE AUX FICHIER .OBJ------------------------------


    #---------- INITIALISATION LICHT ET PROJECTIONS OPENGL -------------------------------------

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    pygame.mouse.set_pos([Screen_x/2,Screen_y/2])
    pygame.mouse.set_visible(False)
    gluPerspective(90.0, Screen_x/float(Screen_y), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    #glEnable(GL_LIGHT2)
    #glEnable(GL_LIGHT3)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_POSITION,  (player1_y, player1_x, player1_z, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 2.0)
    glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION,0.5)
    glLightfv(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.2)
    glLightfv(GL_LIGHT1, GL_POSITION,  (player1_y, player1_x, -player1_z, 0.0))
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.5)
    glLightfv(GL_LIGHT1, GL_LINEAR_ATTENUATION,2.0)
    glLightfv(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.2)
    #glLightfv(GL_LIGHT2, GL_POSITION,  (0.0, 0.0, 0.0, 0.0))
    #glLightfv(GL_LIGHT2, GL_AMBIENT, (1.0, 0.0, 0.0, 1.0))
    #glLightfv(GL_LIGHT2, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    #glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 150.0)
    glLightfv(GL_LIGHT3, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT3, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT3, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT3, GL_POSITION, (0.0,0.0,0.0,1.0))
    glLightfv(GL_LIGHT3, GL_CONSTANT_ATTENUATION, 1.5)
    #glLightfv(GL_LIGHT3, GL_LINEAR_ATTENUATION,0.5)
    #glLightfv(GL_LIGHT3, GL_QUADRATIC_ATTENUATION, 0.2)
    #glLightfv(GL_LIGHT3, GL_SPOT_CUTOFF, 45.0)
    #glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION, (-1.0,-1.0,0.0))
    #glLightfv(GL_LIGHT3, GL_SPOT_EXPONENT, 2.0)
    glShadeModel(GL_SMOOTH)

    #----------- FIN D'INITIALISATION LIGHT ET PROJECTIONS OPENGL ------------------------------

    #----------- INITIALISATION RESEAUX --------------------------------------------------------


        #  ACTUALISATION SI DéCONNEXION
    global IPplayers,MyIP,PlayerID,MySocket,portIDstart,play2,skin_player_now
    skin_joueur = [-1,-1,-1,-1]
    skin_player_now = 0
    PlayerID = 2
    if reseau == True :
        global IPplayers,MyIP,MySocket,portIDstart
        IPplayers = [ ]
        MyIP = '192.168.1.60'
        
        
    
        MySocket = None
        portIDstart = 10010
        InitReseau()
        pygame.time.wait(1000)
        msg2=LitMessage()
        if len(msg2)>0:
            valeurs2 = msg2.split(' ')
            Room[3]["Box1"]["Rotate"] = int(valeurs2[8])
            Room[3]["Box2"]["Rotate"] = int(valeurs2[9])
            Room[3]["Box3"]["Rotate"] = int(valeurs2[10])
            Room[7]["Signs"]["Rotate"][0]= int(valeurs2[24])
            Room[7]["Signs"]["Rotate"][1]= int(valeurs2[25])
            Room[7]["Signs"]["Rotate"][2]= int(valeurs2[26])
            Room[7]["Signs"]["Rotate"][3]= int(valeurs2[27])
            Room[7]["Signs"]["Rotate"][4]= int(valeurs2[28])
            Room[7]["Signs"]["Rotate"][5]= int(valeurs2[29])
            Room[7]["Signs"]["Rotate"][6]= int(valeurs2[30])
            Room[7]["Signs"]["Rotate"][7]= int(valeurs2[31])
            Room[7]["Signs"]["Rotate"][8]= int(valeurs2[32])
            for i in range (7) :
                if (int(valeurs2[9+i]) == 1) :
                    Room[6]["Bouton"]["Pressed"][i] = True
            lastbouton = int(valeurs2[21])
            Room[0]["Porte"]["Open"][1] = int(valeurs2[34])
            Room[0]["Porte"]["Open"][2] = int(valeurs2[35])
            Room[1]["Porte"]["Open"][0] = int(valeurs2[36])
            Room[2]["Porte"]["Open"][0] = int(valeurs2[37])
            Room[3]["Porte"]["Open"][0] = int(valeurs2[38])
            Room[4]["Porte"]["Open"][0] = int(valeurs2[39])
            Room[5]["Porte"]["Open"][0] = int(valeurs2[40])
            Room[6]["Porte"]["Open"][0] = int(valeurs2[41])
            Room[7]["Porte"]["Open"][0] = int(valeurs2[42])
            Room[8]["Porte"]["Open"][0] = int(valeurs2[43])
            Room[9]["Porte"]["Open"][0] = int(valeurs2[44])
            Room[10]["Porte"]["Open"][0] = int(valeurs2[50])
            nbJoueur = int(valeurs2[51])
    #---------- FIN D'INITIALISATION RESEAUX --------------------------------------------------------

########################## FIN DE DEFINITION DE FONCTION







#----------- INITIALISATION CONSTANTES, VARIABLES ET TABLEAUX ------------------------------------------------------
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]
GREEN2= [100, 255, 100]
RED   = [255, 0, 0]
BLUE  = [0 , 0 , 255]
BROWN = [136, 66, 29]
BROWN2 = [136, 100, 60]
YELLOW= [255,255,0]
Screen_x = 1000
Screen_y = 600
done = False
chargement_effectue = False
chargement = False
menu = True
quitterpresser = False
optionpresser = False
aidepresser = False
optiongraphismes = False
dejafait = False
anim = 0
reseau = False
toucheclavier     = ['Effacer','Tab','Clear','Entrer','Pause','Echap','Espace','!','"','#','$','à',"ù",'(',')','*','+',';',')',':','!','à','&','é','"',"'",'(','-','è','_','ç','à','m','<','=','>'
                     ,'?','@','^','*','$','^','_','²','q','b','c','d','e','f','g','h','i','j','k','l',',','n','o','p','a','r','s','t','u','v','z','x','y','w','Suppr','Pad0','Pad1','Pad2'
                     ,'Pad3','Pad4','Pad5','Pad6','Pad7','Pad8','Pad9','Pad.','Pad/','Pad*','Pad-','Pad+','PadEntrer','Pad=','Haut','Bas','Droite','Gauche','Inser','Home','Fin','PageHaut','PageBas'
                     ,'F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12','F13','F14','F15','CtrlD','AltG','MetaD','MetaG','WinG','WinD'
                     ,'Mode','Help','Affichage','Sysrq','Break','Menu','Power','Euro','CtrlG']

codetoucheclavier = [pygame.K_BACKSPACE, pygame.K_TAB, pygame.K_CLEAR,pygame.K_RETURN,pygame.K_PAUSE,pygame.K_ESCAPE,pygame.K_SPACE,pygame.K_EXCLAIM
                        , pygame.K_QUOTEDBL,pygame.K_HASH, pygame.K_DOLLAR, pygame.K_AMPERSAND, pygame.K_QUOTE, pygame.K_LEFTPAREN, pygame.K_RIGHTPAREN
                        , pygame.K_ASTERISK, pygame.K_PLUS, pygame.K_COMMA, pygame.K_MINUS, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_0, pygame.K_1 
                        , pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_COLON, pygame.K_SEMICOLON  
                        , pygame.K_LESS, pygame.K_EQUALS, pygame.K_GREATER, pygame.K_QUESTION, pygame.K_AT, pygame.K_LEFTBRACKET, pygame.K_BACKSLASH   
                        , pygame.K_RIGHTBRACKET, pygame.K_CARET, pygame.K_UNDERSCORE, pygame.K_BACKQUOTE, pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d          
                        , pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o          
                        , pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z          
                        , pygame.K_DELETE, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7              
                        , pygame.K_KP8, pygame.K_KP9, pygame.K_KP_PERIOD, pygame.K_KP_DIVIDE, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, pygame.K_KP_PLUS, pygame.K_KP_ENTER    
                        , pygame.K_KP_EQUALS, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_INSERT, pygame.K_HOME, pygame.K_END          
                        , pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8                
                        , pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12, pygame.K_F13, pygame.K_F14, pygame.K_F15            
                        , pygame.K_RCTRL, pygame.K_LALT, pygame.K_RMETA, pygame.K_LMETA, pygame.K_LSUPER, pygame.K_RSUPER              
                        , pygame.K_MODE, pygame.K_HELP, pygame.K_PRINT ,pygame.K_SYSREQ, pygame.K_BREAK, pygame.K_MENU, pygame.K_POWER, pygame.K_EURO, pygame.K_LCTRL]
toutelescommandes=[66, 62, 47, 44, 88, 89, 90, 91, 60, 48, 6, 5, True, 59,126-13]
pause = False
compteur = 0
changementtouche = False
playerdecision = False
determinernbjoueur = True
skinjoueur = False
onetime = False      
nbjoueurdanspartie = 1
defilementdeskin = 0
onetime2 = False
attentejoueur = False
optionson = False
optionreseau = False
optionsensi = False
nbJoueur = 2
onetime1 = False
skin_player_now = 0
#----------- FIN D'INITIALISATION CONSTANTES, VARIABLES ET TABLEAUX ------------------------------------------------------




#----------- PREPARATION FENETRE DU JEU ------------------------------------------------------------

scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0)) # compatible interactive Python Shell
scriptDIR  = os.path.dirname(scriptPATH)
assets = os.path.join(scriptDIR,"") 

pygame.init()
pygame.font.init()

viewport = (Screen_x, Screen_y)
screen = pygame.display.set_mode((Screen_x,Screen_y) )
clock = pygame.time.Clock()
icon = os.path.join(scriptDIR,("icone.png"))
pygame.display.set_icon(pygame.image.load(icon))
pygame.display.set_caption("Enigma Room", "None")
hx = viewport[0]/2
hy = viewport[1]/2
clock = pygame.time.Clock()
imgmenu_play3 = pygame.image.load(os.path.join(assets, "menu_play3.png"))
imgmenu_play1 = pygame.image.load(os.path.join(assets, "menu_play1.png"))
imgmenu_play2 = pygame.image.load(os.path.join(assets, "menu_play2.png"))
imgmenu_play4 = pygame.image.load(os.path.join(assets, "menu_play4.png"))
imgmenu_option1 = pygame.image.load(os.path.join(assets, "option1.png"))
imgmenu_option2 = pygame.image.load(os.path.join(assets, "option2.png"))
imgmenu_option3 = pygame.image.load(os.path.join(assets, "option3.png"))
imgmenu_option4 = pygame.image.load(os.path.join(assets, "option4.png"))
imgmenu_option = pygame.image.load(os.path.join(assets, "option.png"))
imgmenu_quitter1 = pygame.image.load(os.path.join(assets, "quitter1.png"))
imgmenu_quitter2 = pygame.image.load(os.path.join(assets, "quitter2.png"))
imgmenu_quitter3 = pygame.image.load(os.path.join(assets, "quitter3.png"))
imgmenu_quitter4 = pygame.image.load(os.path.join(assets, "quitter4.png"))
imgmenu_quitter = pygame.image.load(os.path.join(assets, "quitter.png"))
imgmenu_aide1 = pygame.image.load(os.path.join(assets, "aide1.png"))
imgmenu_aide2 = pygame.image.load(os.path.join(assets, "aide2.png"))
imgmenu_aide3 = pygame.image.load(os.path.join(assets, "aide3.png"))
imgmenu_aide4 = pygame.image.load(os.path.join(assets, "aide4.png"))
imgmenu_aide = pygame.image.load(os.path.join(assets, "aide.png"))
imgquitter_ouinon = pygame.image.load(os.path.join(assets, "quitterouinon.png"))
imgquitter_oui = pygame.image.load(os.path.join(assets, "quitteroui.png"))
imgquitter_non = pygame.image.load(os.path.join(assets, "quitternon.png"))
imgmenuoption_controles0= pygame.image.load(os.path.join(assets, "menuoption_controles0.png"))
imgmenuoption_controles1= pygame.image.load(os.path.join(assets, "menuoption_controles1.png"))
imgmenuoption_controles2= pygame.image.load(os.path.join(assets, "menuoption_controles2.png"))
imgmenuretour1 = pygame.image.load(os.path.join(assets, "menuretour1.png"))
imgmenuretour2 = pygame.image.load(os.path.join(assets, "menuretour2.png"))
imgchargement = pygame.image.load(os.path.join(assets, "chargement.png"))
imgmenu_playnbjoueur = pygame.image.load(os.path.join(assets, "menu_playnbjoueur.png"))
imgflechegauche = pygame.image.load(os.path.join(assets, "flecheblanche.png"))
imgflechedroite = pygame.image.load(os.path.join(assets, "flecheblanche2.png"))
imgmenu_playsouris = pygame.image.load(os.path.join(assets, "menu_playsouris.png"))
img0 = pygame.image.load(os.path.join(assets, "0.png"))
img1 = pygame.image.load(os.path.join(assets, "1.png"))
img2 = pygame.image.load(os.path.join(assets, "2.png"))
img3 = pygame.image.load(os.path.join(assets, "3.png"))
img4 = pygame.image.load(os.path.join(assets, "4.png"))
img5 = pygame.image.load(os.path.join(assets, "5.png"))
img6 = pygame.image.load(os.path.join(assets, "6.png"))
img7 = pygame.image.load(os.path.join(assets, "7.png"))
img8 = pygame.image.load(os.path.join(assets, "8.png"))
img9 = pygame.image.load(os.path.join(assets, "9.png"))
imgmenusuivant1 = pygame.image.load(os.path.join(assets, "menusuivant1.png"))
imgmenusuivant2 = pygame.image.load(os.path.join(assets, "menusuivant2.png"))
imgmenuattente = pygame.image.load(os.path.join(assets, "menu_playattentedesjoueurs.png"))
imgskin = pygame.image.load(os.path.join(assets, "menu_playchoixskin.png"))
imgcadrecontroles = pygame.image.load(os.path.join(assets, "menuoption0.png"))
imgchiffre=[img0,img1,img2,img3,img4,img5,img6,img7,img8,img9]
fond = pygame.image.load(os.path.join(assets, "fond.png"))
#----------- FIN DE PREPARATION FENETRE DU JEU -----------------------------------------------------



codepressed = False
while not done:

    if chargement_effectue==False and chargement==True :
        Chargement_du_jeu()
        chargement_effectue=True
   
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            if chargement_effectue == True :
                player_play = 0
        elif event.type == KEYDOWN and event.key == K_F4 and bool(event.mod & KMOD_ALT):
            # elif e.key == K_F4 and bool(e.mod & KMOD_ALT):
            if chargement_effectue == True :
                player_play = 0
            sys.exit()

    KeysPressed = pygame.key.get_pressed()
    if pause == True and compteur < 5 :
        compteur+= 1
    elif pause == True :
        pause = False
        compteur = 0
        
    if menu == True : 
        if onetime1== False :
            screen = pygame.display.set_mode((Screen_x,Screen_y))
            onetime1 = True
        dessus = False
        dessus2 = False
        dessus3 = False
        dessus4 = False
            
        if anim < 20 :
            anim+=1
        else :
            anim = 0
            
            
        screen.blit(fond,(Screen_x-1050,Screen_y-630))
            
            
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-115 and pygame.mouse.get_pos()[0]<(Screen_x/2)+80 and pygame.mouse.get_pos()[1]>(Screen_y/2)+115 and pygame.mouse.get_pos()[1]<(Screen_y/2)+158) :
            dessus3 = True
                  
            
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-122 and pygame.mouse.get_pos()[0]<(Screen_x/2)+100 and pygame.mouse.get_pos()[1]>(Screen_y/2)+175 and pygame.mouse.get_pos()[1]<(Screen_y/2)+230) :
            dessus4 = True
        
        if anim <= 5 and dessus4 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_quitter1,((Screen_x/2)-122,(Screen_y/2)+165))
        elif anim > 5 and anim <= 10 and dessus4 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_quitter2,((Screen_x/2)-122,(Screen_y/2)+165))
        elif anim > 10 and anim <= 15 and dessus4 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_quitter3,((Screen_x/2)-122,(Screen_y/2)+165))
        elif anim > 15 and anim <= 20 and dessus4 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_quitter4,((Screen_x/2)-122,(Screen_y/2)+165))
        elif quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False  :
            screen.blit(imgmenu_quitter,((Screen_x/2)-122,(Screen_y/2)+165))
                
            
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-121.5 and pygame.mouse.get_pos()[0]<(Screen_x/2)+101.5 and pygame.mouse.get_pos()[1]>(Screen_y/2)+48 and pygame.mouse.get_pos()[1]<(Screen_y/2)+106) :
            dessus2 = True
        
        if anim <= 5 and dessus2 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_option1,((Screen_x/2)-121.5,(Screen_y/2)+40))
        elif anim > 5 and anim <= 10 and dessus2 == True and quitterpresser ==False and optionpresser ==False  and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_option2,((Screen_x/2)-121.5,(Screen_y/2)+40))
        elif anim > 10 and anim <= 15 and dessus2 == True and quitterpresser ==False and optionpresser ==False  and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_option3,((Screen_x/2)-121.5,(Screen_y/2)+40))
        elif anim > 15 and anim <= 20 and dessus2 == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False:
            screen.blit(imgmenu_option4,((Screen_x/2)-121.5,(Screen_y/2)+40))
        elif quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_option,((Screen_x/2)-121.5,(Screen_y/2)+40)) 
        
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-101.5 and pygame.mouse.get_pos()[0]<(Screen_x/2)+101.5 and pygame.mouse.get_pos()[1]>(Screen_y/2)-40 and pygame.mouse.get_pos()[1]<(Screen_y/2)+30) :
            dessus = True
            
        if anim <= 5 and dessus == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_play1,((Screen_x/2)-101.5,(Screen_y/2)-46))
        elif anim > 5 and anim <= 10 and dessus == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_play2,((Screen_x/2)-101.5,(Screen_y/2)-46))
        elif anim > 10 and anim <= 15 and dessus == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False  :
            screen.blit(imgmenu_play3,((Screen_x/2)-101.5,(Screen_y/2)-46))
        elif anim > 15 and anim <= 20 and dessus == True and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_play4,((Screen_x/2)-101.5,(Screen_y/2)-46))
        elif quitterpresser == False and optionpresser ==False and optiongraphismes ==  False and optionson == False and optionreseau== False and optionsensi== False :
            screen.blit(imgmenu_playsouris,((Screen_x/2)-101.5,(Screen_y/2)-46))
            
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-101.5 and quitterpresser == False and optionpresser ==False and optiongraphismes ==  False  and pygame.mouse.get_pos()[0]<(Screen_x/2)+101.5 and pygame.mouse.get_pos()[1]>(Screen_y/2)-40 and pygame.mouse.get_pos()[1]<(Screen_y/2)+30 and pygame.mouse.get_pressed()[0]==1) :
            menu = False
            screen.blit(imgchargement,(Screen_x-1000,Screen_y-600))
            chargement = True
            onetime1 = False

            
     
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-122 and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False  and pygame.mouse.get_pos()[0]<(Screen_x/2)+100 and pygame.mouse.get_pos()[1]>(Screen_y/2)+175 and pygame.mouse.get_pos()[1]<(Screen_y/2)+230 and pygame.mouse.get_pressed()[0]==1) :
            quitterpresser = True
        
        if (pygame.mouse.get_pos()[0]>(Screen_x/2)-121.5 and quitterpresser ==False and optionpresser ==False and optiongraphismes ==  False and pygame.mouse.get_pos()[0]<(Screen_x/2)+101.5 and pygame.mouse.get_pos()[1]>(Screen_y/2)+48 and pygame.mouse.get_pos()[1]<(Screen_y/2)+106 and pygame.mouse.get_pressed()[0]==1) :
            optionpresser = True
            pause = True
            
        if quitterpresser==True:
            screen.blit(imgquitter_ouinon,((Screen_x/2)-250,(Screen_y/2)-150))
            if (pygame.mouse.get_pos()[1]>(Screen_y/2) and pygame.mouse.get_pos()[1]<(Screen_y/2)+38 and pygame.mouse.get_pos()[0]>(Screen_x/2)-49 and pygame.mouse.get_pos()[0]<(Screen_x/2)+44 ) :
                screen.blit(imgquitter_oui,((Screen_x/2)-250,(Screen_y/2)-150))
                if (pygame.mouse.get_pressed()[0]==1) :
                    done = True
            if (pygame.mouse.get_pos()[1]>(Screen_y/2)+71 and pygame.mouse.get_pos()[1]<(Screen_y/2)+108 and pygame.mouse.get_pos()[0]>(Screen_x/2)-49 and pygame.mouse.get_pos()[0]<(Screen_x/2)+44 ) :
                screen.blit(imgquitter_non,((Screen_x/2)-250,(Screen_y/2)-150))
                if (pygame.mouse.get_pressed()[0]==1) :
                    quitterpresser = False
                    pygame.time.wait(250)
        
        if optionpresser == True and pause == False :
            if KeysPressed[codetoucheclavier[toutelescommandes[11]]] and pause == False and changementtouche == False :  
                optionpresser = False
                pause = True
                
            
            positionx=(Screen_x/2)-450
            positiony=(Screen_y/2)-250
            screen.blit(imgmenuoption_controles0,((Screen_x/2)-450,(Screen_y/2)-250))
            police = pygame.font.SysFont("arial", 15)
            zoneavancer = police.render(toucheclavier[toutelescommandes[0]] , True, WHITE) 
            zonereculer= police.render(toucheclavier[toutelescommandes[1]] , True, WHITE) 
            zonedroite = police.render(toucheclavier[toutelescommandes[2]] , True, WHITE) 
            zonegauche =police.render(toucheclavier[toutelescommandes[3]] , True, WHITE) 
            zonecamera_haut =police.render(toucheclavier[toutelescommandes[4]] , True, WHITE) 
            zonecamera_bas = police.render(toucheclavier[toutelescommandes[5]] , True, WHITE) 
            zonecamera_droite=police.render(toucheclavier[toutelescommandes[6]] , True, WHITE) 
            zonecamera_gauche=police.render(toucheclavier[toutelescommandes[7]] , True, WHITE) 
            zoneagir1 = police.render(toucheclavier[toutelescommandes[8]] , True, WHITE) 
            zoneagir2 = police.render(toucheclavier[toutelescommandes[9]] , True, WHITE) 
            zonesauttouche = police.render(toucheclavier[toutelescommandes[10]] , True, WHITE) 
            zonequittertouche = police.render(toucheclavier[toutelescommandes[11]] , True, WHITE) 
            if toutelescommandes[12] == True :
                zonecamera_souris =police.render("Activer" , True, WHITE) 
            else :
                zonecamera_souris =police.render("Désactiver" , True, WHITE) 
            zonepausetouche = police.render(toucheclavier[toutelescommandes[13]] , True, WHITE)
            zonecourir = police.render(toucheclavier[toutelescommandes[14]] , True, WHITE)
            zonenbjoueur = police.render(str(nbJoueur) , True, WHITE)
            zoneskin = police.render(str(skin_player_now) , True, WHITE)
            
            screen.blit(zoneavancer,(positionx+182,positiony+100))
            screen.blit(zonereculer,(positionx+182,positiony+149))
            screen.blit(zonedroite,(positionx+182,positiony+192))
            screen.blit(zonegauche,(positionx+182,positiony+241))
            screen.blit(zonecamera_haut,(positionx+357,positiony+287))
            screen.blit(zonecamera_bas,(positionx+352,positiony+336))
            screen.blit(zonecamera_droite,(positionx+371,positiony+380))
            screen.blit(zonecamera_gauche,(positionx+381,positiony+427))
            screen.blit(zoneagir1,(positionx+648,positiony+134))
            screen.blit(zoneagir2,(positionx+648,positiony+214))
            screen.blit(zonesauttouche,(positionx+740,positiony+275))
            screen.blit(zonequittertouche,(positionx+740,positiony+320))
            screen.blit(zonecamera_souris,(positionx+740,positiony+360))
            screen.blit(zonepausetouche,(positionx+740,positiony+402))
            screen.blit(imgmenuretour1,(positionx+600,positiony+440))
            screen.blit(zonenbjoueur,(positionx+310,positiony+44))
            screen.blit(zoneskin,(positionx+687,positiony+44))
            screen.blit(zonecourir,(positionx+510,positiony+214))
            
            
            
            if changementtouche == False :
                if pygame.mouse.get_pos()[0]>positionx+175 and pygame.mouse.get_pos()[0]<positionx+292 and pygame.mouse.get_pos()[1]>positiony+94 and pygame.mouse.get_pos()[1]<positiony+129 :
                    screen.blit(imgmenuoption_controles1,(positionx+174,positiony+93))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 0
                        changementtouche = True
                            
                if pygame.mouse.get_pos()[0]>positionx+600 and pygame.mouse.get_pos()[0]<positionx+740 and pygame.mouse.get_pos()[1]>positiony+440 and pygame.mouse.get_pos()[1]<positiony+480 :
                    screen.blit(imgmenuretour2,(positionx+600,positiony+440))
                    if pygame.mouse.get_pressed()[0]==1 :
                        optionpresser = False
                        
                if pygame.mouse.get_pos()[0]>positionx+176 and pygame.mouse.get_pos()[0]<positionx+292 and pygame.mouse.get_pos()[1]>positiony+144 and pygame.mouse.get_pos()[1]<positiony+177 :
                    screen.blit(imgmenuoption_controles1,(positionx+173,positiony+141))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 1
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+176 and pygame.mouse.get_pos()[0]<positionx+292 and pygame.mouse.get_pos()[1]>positiony+187 and pygame.mouse.get_pos()[1]<positiony+220 :
                    screen.blit(imgmenuoption_controles1,(positionx+173,positiony+184))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 2
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+174 and pygame.mouse.get_pos()[0]<positionx+292 and pygame.mouse.get_pos()[1]>positiony+232 and pygame.mouse.get_pos()[1]<positiony+267 :
                    screen.blit(imgmenuoption_controles1,(positionx+172,positiony+231))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 3
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+347 and pygame.mouse.get_pos()[0]<positionx+465 and pygame.mouse.get_pos()[1]>positiony+279 and pygame.mouse.get_pos()[1]<positiony+314 :
                    screen.blit(imgmenuoption_controles1,(positionx+347,positiony+278))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 4
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+341 and pygame.mouse.get_pos()[0]<positionx+459 and pygame.mouse.get_pos()[1]>positiony+327 and pygame.mouse.get_pos()[1]<positiony+363 :
                    screen.blit(imgmenuoption_controles1,(positionx+341,positiony+327))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 5
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+360 and pygame.mouse.get_pos()[0]<positionx+478 and pygame.mouse.get_pos()[1]>positiony+371 and pygame.mouse.get_pos()[1]<positiony+407 :
                    screen.blit(imgmenuoption_controles1,(positionx+360,positiony+371))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 6
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+372 and pygame.mouse.get_pos()[0]<positionx+490 and pygame.mouse.get_pos()[1]>positiony+418 and pygame.mouse.get_pos()[1]<positiony+454 :
                    screen.blit(imgmenuoption_controles1,(positionx+372,positiony+418))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 7
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+640 and pygame.mouse.get_pos()[0]<positionx+758 and pygame.mouse.get_pos()[1]>positiony+125 and pygame.mouse.get_pos()[1]<positiony+161 :
                    screen.blit(imgmenuoption_controles1,(positionx+640,positiony+125))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 8
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+641 and pygame.mouse.get_pos()[0]<positionx+759 and pygame.mouse.get_pos()[1]>positiony+206 and pygame.mouse.get_pos()[1]<positiony+242 :
                    screen.blit(imgmenuoption_controles1,(positionx+641,positiony+206))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 9
                        changementtouche = True
                if pygame.mouse.get_pos()[0]>positionx+731 and pygame.mouse.get_pos()[0]<positionx+849 and pygame.mouse.get_pos()[1]>positiony+267 and pygame.mouse.get_pos()[1]<positiony+303 :
                    screen.blit(imgmenuoption_controles1,(positionx+731,positiony+267))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 10
                        changementtouche = True
                        pause = True
                if pygame.mouse.get_pos()[0]>positionx+731 and pygame.mouse.get_pos()[0]<positionx+849 and pygame.mouse.get_pos()[1]>positiony+310 and pygame.mouse.get_pos()[1]<positiony+346 :
                    screen.blit(imgmenuoption_controles1,(positionx+731,positiony+310))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 11
                        changementtouche = True
                        pause = True
                if pygame.mouse.get_pos()[0]>positionx+732 and pygame.mouse.get_pos()[0]<positionx+850 and pygame.mouse.get_pos()[1]>positiony+351 and pygame.mouse.get_pos()[1]<positiony+387 :
                    screen.blit(imgmenuoption_controles1,(positionx+732,positiony+351))
                    if pygame.mouse.get_pressed()[0]==1 :
                        if toutelescommandes[12] == True:
                            toutelescommandes[12] = False
                        else :
                            toutelescommandes[12] = True
                        pygame.time.wait(250)
                        
                if pygame.mouse.get_pos()[0]>positionx+732 and pygame.mouse.get_pos()[0]<positionx+850 and pygame.mouse.get_pos()[1]>positiony+394 and pygame.mouse.get_pos()[1]<positiony+430 :
                    screen.blit(imgmenuoption_controles1,(positionx+732,positiony+394))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 13
                        changementtouche = True
                
                if pygame.mouse.get_pos()[0]>positionx+261 and pygame.mouse.get_pos()[0]<positionx+379 and pygame.mouse.get_pos()[1]>positiony+36 and pygame.mouse.get_pos()[1]<positiony+72 :
                    screen.blit(imgmenuoption_controles1,(positionx+261,positiony+36))
                    if pygame.mouse.get_pressed()[0]==1 :
                        nbJoueur += 1
                        pygame.time.wait(250)
                if nbJoueur >=5 :
                    nbJoueur = 2
                    
                if pygame.mouse.get_pos()[0]>positionx+501 and pygame.mouse.get_pos()[0]<positionx+619 and pygame.mouse.get_pos()[1]>positiony+206 and pygame.mouse.get_pos()[1]<positiony+242 :
                    screen.blit(imgmenuoption_controles1,(positionx+501,positiony+206))
                    if pygame.mouse.get_pressed()[0]==1 :
                        touchequichange = 14
                        changementtouche = True
                        
                if pygame.mouse.get_pos()[0]>positionx+640 and pygame.mouse.get_pos()[0]<positionx+758 and pygame.mouse.get_pos()[1]>positiony+36 and pygame.mouse.get_pos()[1]<positiony+72 :
                    screen.blit(imgmenuoption_controles1,(positionx+640,positiony+36))
                    if pygame.mouse.get_pressed()[0]==1 :
                        skin_player_now += 1
                        pygame.time.wait(250)
                if skin_player_now >=4 :
                    skin_player_now = 0
                
            
            if changementtouche == True and pause == False :
                screen.blit(imgmenuoption_controles2,((Screen_x/2)-350,(Screen_y/2)-100))
                screen.blit(imgmenuretour1,((Screen_x/2)-350+523,(Screen_y/2)-100+134))
                y=False
                j = testtouche()
                if j!=-5 :
                    for x in range (len(toutelescommandes)) :
                        if toutelescommandes[x] == j :
                            y=True
                    if y==False :    
                        changementtouche = False 
                        toutelescommandes[touchequichange] = j
                        if touchequichange==11 :
                            pause=True
                if pygame.mouse.get_pos()[0]>(Screen_x/2)-350+523 and pygame.mouse.get_pos()[0]<(Screen_x/2)-350+523+140 and pygame.mouse.get_pos()[1]>(Screen_y/2)-100+134 and pygame.mouse.get_pos()[1]<(Screen_y/2)-100+134+40 :
                    screen.blit(imgmenuretour2,((Screen_x/2)-350+523,(Screen_y/2)-100+134))
                    if pygame.mouse.get_pressed()[0]==1 :
                        changementtouche = False
                        pause = True
                        
            
            
            if KeysPressed[codetoucheclavier[toutelescommandes[11]]] and pause == False and quitterpresser==False and optionpresser == False and optiongraphismes==False  and optionson == False and optionreseau== False and optionsensi== False :  quitterpresser = True
                
              
                        
           
                                
                    
                
           
    if chargement_effectue == True :
    
        presser = 0
        bouge = 0
        rotsign = 0
    
        if( now == 0 or now == 1 or now == 2):
            DistanceButton(list_player[PlayerID][0],list_player[PlayerID][2],Room[now]["Bouton"]["Range"])
    
            
        if( now == 3 or now == 6 or now == 7 or now == 10):
            DistanceKey(list_player[PlayerID][0],list_player[PlayerID][2],Room[now]["Key"]["Range"])
        if Room[3]["Key"]["Taken"] == True and Room[6]["Key"]["Taken"] == True and Room[7]["Key"]["Taken"] == True and Room[10]["Key"]["Taken"] == True :
                Room[0]["Porte"]["Open"][0] = 4
    
    
        if now == 9 :
            if list_player[PlayerID][1] <= hauteur_joueur :
                if previous_room == 7 :
                    list_player[PlayerID][0] = Room[9]["Room"]["x"]-90
                else :
                    list_player[PlayerID][0] = Room[9]["Room"]["x"]+90
                list_player[PlayerID][1] = Room[9]["Room"]["y"]+7 + hauteur_joueur
                list_player[PlayerID][2] = Room[9]["Room"]["z"]-94
                list_player[PlayerID][3] = 0
    
        global lastbouton
    
        lastbouton = DistanceButton(list_player[PlayerID][0],list_player[PlayerID][2],Room[6]["Bouton"]["Range"])
    
        if now == 3 :
            rotationCube1 = DistanceRotate(list_player[PlayerID][0],list_player[PlayerID][2],1)
            rotationCube2 = DistanceRotate(list_player[PlayerID][0],list_player[PlayerID][2],2)
            rotationCube3 = DistanceRotate(list_player[PlayerID][0],list_player[PlayerID][2],3)
    
            NumCube = -1
            if( rotationCube1 < 6 and list_player[PlayerID][3] < 200 and list_player[PlayerID][3] > 160 ):
                NumCube = 1
    
            if( rotationCube2 < 6 and list_player[PlayerID][3] < 290 and list_player[PlayerID][3] > 250  ):
                NumCube = 2
    
            if( rotationCube3 < 6 and (list_player[PlayerID][3] < 60 or list_player[PlayerID][3] > 300) ):
                NumCube = 3
    
    
    
    
    
    
            if NumCube != -1 :
                if (pygame.mouse.get_pressed()[0] or KeysPressed[codetoucheclavier[toutelescommandes[8]]]) and timer == 0 :
                    Room[now]["Box"+str(NumCube)]["Rotate"] = (Room[now]["Box"+str(NumCube)]["Rotate"]+1)%4
                    effect4.play()
                    timer = 1
                    bouge = 1
    
                if (pygame.mouse.get_pressed()[2] or KeysPressed[codetoucheclavier[toutelescommandes[9]]]) and timer == 0 :
                    Room[now]["Box"+str(NumCube)]["Rotate"] = (Room[now]["Box"+str(NumCube)]["Rotate"]-1)%4
                    effect4.play()
                    timer = 1
                    bouge = 1
    
        if timer<15 and timer>0 :
            timer+=1
        if timer == 15 :
            timer = 0
    
    
    
        if reseau == True :
            msg=LitMessage()
            while len(msg)>0:
                #print(msg)
                DecodeMessage(msg)
                msg=LitMessage()
                
        if( Room[10]["Key"]["Taken"] == True ) :
            finalporte = True
    
        """
        if Room[1]["Bouton"]["Pressed"][0] == True and Room[2]["Bouton"]["Pressed"][0] == True :
            Room[1]["Porte"]["Open"][0] = 1
            Room[2]["Porte"]["Open"][0] = 1
        """
        if( now == 1 or now == 2):
            if Room[1]["Bouton"]["Pressed"][0] == True or Room[2]["Bouton"]["Pressed"][0] == True :
                Room[1]["Porte"]["Open"][0] = 1
                Room[2]["Porte"]["Open"][0] = 1
                if door12_bool == False:
                    effect3.play(0)
                    door12_bool = True
            elif Room[1]["Bouton"]["Pressed"][0] == True or Room[2]["Bouton"]["Pressed"][0] == True :
                cmpt +=1
                if cmpt == 1:
                        effect1.play(0)
            elif Room[1]["Bouton"]["Pressed"][0] == False or Room[2]["Bouton"]["Pressed"][0] == False:
                    if cmpt != 0:
                        effect2.play(0)
                        cmpt = 0
    
        """
        if Room[0]["Bouton"]["Pressed"][0] == True:
            Room[0]["Porte"]["Open"][1] = 1
            Room[0]["Porte"]["Open"][2] = 1
        """
    
        if now == 0 :
            if Room[0]["Bouton"]["Pressed"][0] == True:
                Room[0]["Porte"]["Open"][1] = 1
                Room[0]["Porte"]["Open"][2] = 1
                cmpt +=1
                if cmpt == 1:
                    effect1.play(0)
                elif door0_bool == False:
                    Room[0]["Porte"]["Open"][1] = 1
                    Room[0]["Porte"]["Open"][2] = 1
                    effect3.play(0)
                    door0_bool = True
            elif Room[0]["Bouton"]["Pressed"][0] == False:
                if cmpt != 0:
                    effect2.play(0)
                    cmpt = 0
     
    
        if nbJoueur >= 3 :
            nbJoueurMax = 2
        else :
            nbJoueurMax = 1
        
        if nbTeam()[0] == nbJoueurMax :
            Room[0]["Porte"]["Open"][2] = 0
            
        if nbTeam()[1] == nbJoueurMax :
            Room[0]["Porte"]["Open"][1] = 0
        
        
     
        
    
        if finalporte == True :
            Room[10]["Porte"]["Open"][0] = 2
    
        """ #Le cas est traité avec les sons lors des tests sur lastbouton
        if Room[6]["Bouton"]["Pressed"] == [True,True,True,True,True,True,True] :
            Room[6]["Porte"]["Open"][0] = 1
        """
    
        if Room[7]["Signs"]["Rotate"] == [2,3,3,0,2,1,2,2,0] :
            Room[7]["Porte"]["Open"][0] = 1
            Room[8]["Porte"]["Open"][0] = 1
            Room[7]["Key"]["Appear"] = True
    
        if( Room[3]["Box1"]["Rotate"] == 2 and Room[3]["Box2"]["Rotate"] == 3 and Room[3]["Box3"]["Rotate"] == 2):
            if door34_bool == False :
                effect5.play()
                door34_bool = True
            Room[3]["Porte"]["Open"][0] = -2
            Room[4]["Porte"]["Open"][0] = -2
            Room[3]["Key"]["Appear"] = True
    
        else :
            Room[3]["Porte"]["Open"][0] = -3
            Room[4]["Porte"]["Open"][0] = -3
            Room[3]["Key"]["Appear"] = False
            door34_bool = False
    
    
        if Room[6]["Bouton"]["Pressed"] == [True,True,True,True,True,True,True] :
            Room[6]["Porte"]["Open"][0] = 1
            Room[5]["Porte"]["Open"][0] = 1
    
        rotrad = math.radians(list_player[PlayerID][3])
        dir_cam_x = math.sin(rotrad)
        dir_cam_z = -math.cos(rotrad)
    
        PossibleMove = [True,True,True,True] #down up left right
        deplacement = [(dir_cam_x * speed,dir_cam_z * speed),(-dir_cam_x * speed,-dir_cam_z * speed),(+math.sin(rotrad + math.pi/2)*speed,-math.cos(rotrad + math.pi/2) * speed), (- math.sin(rotrad + math.pi/2)*speed,+ math.cos(rotrad + math.pi/2) * speed)]
    
        for objet in Room[now]:
    
            if objet == "Pilier" or objet == "Bear":
                for j in range(4):
                    if(Distance(list_player[PlayerID][0]+deplacement[j][0],list_player[PlayerID][2]+deplacement[j][1],Room[now][objet]["Size"],objet)==-1):
                        PossibleMove[j] = False
    
            if Room[now][objet]["Type"] == "Bibli" or Room[now][objet]["Type"] == "Cube" or  Room[now][objet]["Type"] == "Cell" or  objet == "Stair" or objet == "Platforme" or objet == "Table":
                for i in range(4):
                    for j in range(len(Room[now][objet]["x"]) ) :
                        if(  list_player[PlayerID][0] + deplacement[i][0]<Room[now][objet]["max_xs"][j] and list_player[PlayerID][0] + deplacement[i][0]>Room[now][objet]["min_xs"][j] and ( (list_player[PlayerID][1]-hauteur_joueur<=Room[now][objet]["max_ys"][j] and list_player[PlayerID][1]-hauteur_joueur >=Room[now][objet]["min_ys"][j])
                            or (list_player[PlayerID][1]<=Room[now][objet]["max_ys"][j] and list_player[PlayerID][1]>=Room[now][objet]["min_ys"][j]) or (list_player[PlayerID][1]-hauteur_joueur<=Room[now][objet]["max_ys"][j] and list_player[PlayerID][1]-hauteur_joueur>=Room[now][objet]["min_ys"][j]) )
                            and list_player[PlayerID][2]+deplacement[i][1]<Room[now][objet]["max_zs"][j] and list_player[PlayerID][2]+deplacement[i][1]> Room[now][objet]["min_zs"][j]):
                            PossibleMove[i] = False
    
    
            if Room[now][objet]["Type"]=="Room":
                for i in range(4):
                    if(  list_player[PlayerID][0] + deplacement[i][0]>Room[now][objet]["max_x"] or list_player[PlayerID][0] + deplacement[i][0]<Room[now][objet]["min_x"] or ( (list_player[PlayerID][1]-hauteur_joueur>Room[now][objet]["max_y"] or list_player[PlayerID][1]-hauteur_joueur <Room[now][objet]["min_y"])
                        or (list_player[PlayerID][1]>Room[now][objet]["max_y"] or list_player[PlayerID][1]<Room[now][objet]["min_y"]) or (list_player[PlayerID][1]-hauteur_joueur>Room[now][objet]["max_y"] or list_player[PlayerID][1]-hauteur_joueur<Room[now][objet]["min_y"]) )
                        or list_player[PlayerID][2]+deplacement[i][1]>Room[now][objet]["max_z"] or list_player[PlayerID][2]+deplacement[i][1]<Room[now][objet]["min_z"]):
                        PossibleMove[i] = False
        #if(list_player[PlayerID][0])
    
        palissade = [(10,-11),(10,10),(-11,10),(-11,-11)]
        paliwidth = 2
        if now == 0 :
            for i in range(4):
                for j in range(-1,3):
                    if(  list_player[PlayerID][0] + deplacement[i][0]<max(palissade[j][0],palissade[j+1][0])+paliwidth and list_player[PlayerID][0] + deplacement[i][0]>min(palissade[j][0],palissade[j+1][0])-paliwidth and ( (list_player[PlayerID][1]-hauteur_joueur>0 and list_player[PlayerID][1]-hauteur_joueur <5)
                        or (list_player[PlayerID][1]>0 and list_player[PlayerID][1]<5) or (list_player[PlayerID][1]-hauteur_joueur>0 and list_player[PlayerID][1]-hauteur_joueur<5) )
                        and list_player[PlayerID][2]+deplacement[i][1]<max(palissade[j][1],palissade[j+1][1])+paliwidth and list_player[PlayerID][2]+deplacement[i][1]> min(palissade[j][1],palissade[j+1][1])-paliwidth):
                        PossibleMove[i] = False
    
    
        if now == 5 :
            obelisk = [Room[5]["Room"]["x"]-7,Room[5]["Room"]["x"]+7,Room[5]["Room"]["z"]-26,Room[5]["Room"]["z"]-11.5]#the tormentor !!
            for i in range(4):
                if(  list_player[PlayerID][0] + deplacement[i][0]<obelisk[1] and list_player[PlayerID][0] + deplacement[i][0]>obelisk[0] and
                    list_player[PlayerID][2]+deplacement[i][1]<obelisk[3] and list_player[PlayerID][2]+deplacement[i][1]> obelisk[2]):
                    PossibleMove[i] = False
    
            
    
        if ((KeysPressed[codetoucheclavier[toutelescommandes[1]]] or KeysPressed[codetoucheclavier[toutelescommandes[0]]] or KeysPressed[codetoucheclavier[toutelescommandes[3]]] or KeysPressed[codetoucheclavier[toutelescommandes[2]]]) and KeysPressed[codetoucheclavier[toutelescommandes[14]]] ) :
            speed = 1.1#1
        else :
            speed = 0.7#0.6
    
    
    
        if(PossibleMove[0]==True ):#and stop == False):
            if KeysPressed[codetoucheclavier[toutelescommandes[1]]]:
               list_player[PlayerID][0]   += dir_cam_x * speed
               list_player[PlayerID][2]   += dir_cam_z * speed
    
        if(PossibleMove[1]==True ):#and stop == False):
            if KeysPressed[codetoucheclavier[toutelescommandes[0]]]:
               list_player[PlayerID][0]   -= dir_cam_x * speed
               list_player[PlayerID][2]   -= dir_cam_z * speed
    
        if(PossibleMove[2]==True ):#and stop == False):
            if KeysPressed[codetoucheclavier[toutelescommandes[3]]]:
                list_player[PlayerID][0] += math.sin(rotrad + math.pi/2) * speed
                list_player[PlayerID][2] += -math.cos(rotrad + math.pi/2) *speed
    
        if(PossibleMove[3]==True ):#and stop == False):
            if KeysPressed[codetoucheclavier[toutelescommandes[2]]]:
                list_player[PlayerID][0] -= math.sin(rotrad + math.pi/2) * speed
                list_player[PlayerID][2] -= -math.cos(rotrad + math.pi/2) *speed
    
        if ( toutelescommandes[12]== False and stop == False):
            pygame.mouse.set_visible(True)
        else :
            pygame.mouse.set_visible(False)
    
    
        if (toutelescommandes[12]== True and stop == False) :
            list_player[PlayerID][3] = list_player[PlayerID][3]+(pygame.mouse.get_pos()[0]-Screen_x/2)*speed_cam
            if (list_player[PlayerID][4]+(pygame.mouse.get_pos()[1]-Screen_y/2)*speed_cam<=40 and list_player[PlayerID][4]+(pygame.mouse.get_pos()[1]-Screen_y/2)*speed_cam>=-80):
                list_player[PlayerID][4] = list_player[PlayerID][4]+(pygame.mouse.get_pos()[1]-Screen_y/2)*speed_cam
            pygame.mouse.set_pos([Screen_x/2,Screen_y/2])
    
        if KeysPressed[codetoucheclavier[toutelescommandes[5]]]:
            if list_player[PlayerID][4] <=50 :
                list_player[PlayerID][4] += 10
    
        if KeysPressed[codetoucheclavier[toutelescommandes[4]]]:
            if list_player[PlayerID][4] >=-80 :
                list_player[PlayerID][4] -= 10
    
        if KeysPressed[codetoucheclavier[toutelescommandes[7]]]:    list_player[PlayerID][3] -= 10
    
        if KeysPressed[codetoucheclavier[toutelescommandes[6]]]:   list_player[PlayerID][3] += 10
    
        if KeysPressed[codetoucheclavier[toutelescommandes[11]]]:
            menu = True
            chargement_effectue = False
            chargement = False
            quitterpresser = True
            player_play = 0
            stop = True
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
        
        if (KeysPressed[codetoucheclavier[toutelescommandes[13]]] ) :
            stop = True
            menu = True
            chargement_effectue = False
            chargement = False
            pygame.mixer.music.stop()
            pygame.mouse.set_visible(True)
            
    
        list_player[PlayerID][3] = list_player[PlayerID][3]%360
    
    
        if (KeysPressed[codetoucheclavier[toutelescommandes[10]]] and saut == False and chute==False):
            cte = int(pygame.time.get_ticks()/10)
            saut=True
            hauteur_actuelle = list_player[PlayerID][1]
            descente_collision = False
        #    saut_test = True
        #    test_list_player[PlayerID][1] = 1.8 + hauteur * math.sin((math.pi/10)*( (int(pygame.time.get_ticks()/10)-cte)))
    
    
        if saut==True :
            #saut en sinus
            if(list_player[PlayerID][1] >= hauteur_actuelle):
                list_player[PlayerID][1] = hauteur_actuelle  + hauteur * math.sin(1.3*(math.pi/100)*( (int(pygame.time.get_ticks()/10)-cte)))
                for objet in Room[now] :
                    if objet == "Blackbox" or Room[now][objet]["Type"] == "Bibli" or Room[now][objet]["Type"] == "Cube" or Room[now][objet]["Type"] == "Escalier" or objet == "Platforme" or objet == "Table":
                        for k in range(len(Room[now][objet]["min_xs"])) :
                            #collision cube dessus
                            if( (Room[now][objet]["min_xs"][k]<list_player[PlayerID][0])  and (list_player[PlayerID][0]<Room[now][objet]["max_xs"][k]) ):
                                if( (Room[now][objet]["min_zs"][k]<list_player[PlayerID][2])  and (list_player[PlayerID][2]<Room[now][objet]["max_zs"][k]) ):
                                    if( (list_player[PlayerID][1]>=Room[now][objet]["min_ys"][k]-2) and (list_player[PlayerID][1]<Room[now][objet]["max_ys"][k]) and (list_player[PlayerID][1]-player_y_previous>0)):
    
                                        list_player[PlayerID][1]=Room[now][objet]["min_ys"][k]-2
                                        montee_collision = True
    
                            #collision cube dessous
                            if( (Room[now][objet]["min_xs"][k]<list_player[PlayerID][0])  and (list_player[PlayerID][0]<Room[now][objet]["max_xs"][k]) ):
                                if( (Room[now][objet]["min_zs"][k]<list_player[PlayerID][2])  and (list_player[PlayerID][2]<Room[now][objet]["max_zs"][k]) ):
                                    if( (list_player[PlayerID][1]>=Room[now][objet]["min_ys"][k]) and (list_player[PlayerID][1]<Room[now][objet]["max_ys"][k]+4) and list_player[PlayerID][1]-player_y_previous<0):
    
                                        list_player[PlayerID][1] = hauteur_joueur + Room[now][objet]["max_ys"][k]+1
                                        descente_collision = True
                                        saut = False
    
                                        cube_collision = Room[now][objet]
                                        indice = k
    
    
                if(montee_collision == True):
                    chute = True
                    saut = False
                    a = int(pygame.time.get_ticks()/10)
    
            elif(list_player[PlayerID][1] < hauteur_actuelle) :
                booleen = True
                if (list_player[PlayerID][1]-difference>=hauteur_joueur) :
                    list_player[PlayerID][1] -= difference
                    booleen = False
    
                    for objet in Room[now] :
                        if objet == "Blackbox" or Room[now][objet]["Type"] == "Bibli" or Room[now][objet]["Type"] == "Cube" or Room[now][objet]["Type"] == "Escalier" or objet == "Platforme" or objet == "Table":
                            for k in range(len(Room[now][objet]["min_xs"])) :
    
                                #collision cube dessous
                                if( (Room[now][objet]["min_xs"][k]<list_player[PlayerID][0])  and (list_player[PlayerID][0]<Room[now][objet]["max_xs"][k]) ):
                                    if( (Room[now][objet]["min_zs"][k]<list_player[PlayerID][2])  and (list_player[PlayerID][2]<Room[now][objet]["max_zs"][k]) ):
                                        if( (list_player[PlayerID][1]>=Room[now][objet]["min_ys"][k]) and (list_player[PlayerID][1]<Room[now][objet]["max_ys"][k]+4) and list_player[PlayerID][1]-player_y_previous<0):
    
                                            list_player[PlayerID][1] = hauteur_joueur + Room[now][objet]["max_ys"][k]+1
                                            descente_collision = True
                                            saut = False
    
                                            cube_collision = Room[now][objet]
                                            indice = k
                elif (booleen == True):
                    list_player[PlayerID][1] = hauteur_joueur + Room[now]["Room"]["y"]
                    saut = False
    
                    #Rotation des signes
                    if ( min(Room[7]["Signs"]["x"])-4<=list_player[PlayerID][0] and list_player[PlayerID][0]<=max(Room[7]["Signs"]["x"])+4
                    and min(Room[7]["Signs"]["z"])-4<=list_player[PlayerID][2] and list_player[PlayerID][2]<=max(Room[7]["Signs"]["z"])+4 ):
    
                        for k in range(len(Room[7]["Signs"]["Nb"])):
                            if ( Room[7]["Signs"]["x"][k]-4 <= list_player[PlayerID][0] and list_player[PlayerID][0] <= Room[7]["Signs"]["x"][k]+4 and
                             Room[7]["Signs"]["z"][k]-4 <= list_player[PlayerID][2] and list_player[PlayerID][2] <= Room[7]["Signs"]["z"][k]+4 ):
                                effect1.play(0)
                                Room[7]["Signs"]["Rotate"][k] = (Room[7]["Signs"]["Rotate"][k]+1)%4
                                rotsign = 1
    
    
            difference = player_y_previous-list_player[PlayerID][1]+0.2 #on incrémente de 0.2 la différence pour que la vitesse de retomber à la fin du sinus croisse
            player_y_previous = list_player[PlayerID][1]
    
    
        #Si le player est sur un cube (s'il a eu une collision lors de sa descente)
        if (descente_collision == True and chute == False):
            #chute
            if ( (cube_collision["min_xs"][indice]>list_player[PlayerID][0]) or (list_player[PlayerID][0]>cube_collision["max_xs"][indice]) or (cube_collision["min_zs"][indice]>list_player[PlayerID][2])  or (list_player[PlayerID][2]>cube_collision["max_zs"][indice])):
                a = int(pygame.time.get_ticks()/10)
                chute = True
            hauteur_actuelle = list_player[PlayerID][1]
    
    
        if (chute == True):
            bool = True
    
            if ( ( (math.pi/100)*((int(pygame.time.get_ticks()/10)-a)) < math.pi/2 ) and (hauteur_actuelle * math.cos(0.7*(math.pi/100)*( (int(pygame.time.get_ticks()/10)-a)))>hauteur_joueur) ): #chute en cosinus
                list_player[PlayerID][1] = hauteur_actuelle * math.cos(0.7*(math.pi/100)*( (int(pygame.time.get_ticks()/10)-a)))
                bool = False
    
            if( (math.pi/100)*( (int(pygame.time.get_ticks()/10)-a)) >= math.pi/2 and list_player[PlayerID][1]-difference>=hauteur_joueur ):
                list_player[PlayerID][1] -= difference
                bool = False
    
            elif (bool == True) :
                list_player[PlayerID][1] = hauteur_joueur + Room[now]["Room"]["y"]
                descente_collision = False
                montee_collision = False
                chute = False
                saut = False
    
            for objet in Room[now] :
                if objet == "Blackbox" or Room[now][objet]["Type"] == "Bibli" or Room[now][objet]["Type"] == "Cube" or Room[now][objet]["Type"] == "Escalier" or objet == "Platforme" or objet == "Table":
                    for k in range(len(Room[now][objet]["min_xs"])) :
    
                        #collision cube dessous
                        if( (Room[now][objet]["min_xs"][k]<list_player[PlayerID][0])  and (list_player[PlayerID][0]<Room[now][objet]["max_xs"][k]) ):
                            if( (Room[now][objet]["min_zs"][k]<list_player[PlayerID][2])  and (list_player[PlayerID][2]<Room[now][objet]["max_zs"][k]) ):
                                if( (list_player[PlayerID][1]>=Room[now][objet]["min_ys"][k]) and (list_player[PlayerID][1]<Room[now][objet]["max_ys"][k]+4) and list_player[PlayerID][1]-player_y_previous<0):
    
                                    list_player[PlayerID][1] = hauteur_joueur + Room[now][objet]["max_ys"][k]+1
                                    descente_collision = True
                                    montee_collision = False
                                    saut = False
    
                                    cube_collision = Room[now][objet]
                                    indice = k
                                    chute = False
            difference = player_y_previous-list_player[PlayerID][1]+0.2 #on incrémente de 0.2 la différence pour que la vitesse de retomber à la fin du sinus croisse
            player_y_previous = list_player[PlayerID][1]
    
    
        OpenGLRepereCamera();
    
    
        if "Porte" in Room[now].keys() :
            Tp = Distance(list_player[PlayerID][0],list_player[PlayerID][2],Room[now]["Porte"]["Range"],"Porte")
            if( (Tp!=-2 and Tp!=-1 ) and Room[now]["Porte"]["Open"][Tp] != 0 and Room[now]["Porte"]["Open"][Tp] != -3 and Room[now]["Porte"]["Open"][Tp] != 3): #-3 = Teleporteur qui n'apparait pas !
                effect6.play()
                if Room[0]["Porte"]["Open"][0]==4 :
                    menu = True
                    chargement_effectue = False
                    chargement = False
                    player_play = 0
                    stop = True
                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.stop()
                list_player[PlayerID][0] = Room[now]["Porte"]["TpCoord"][Tp][0]
                list_player[PlayerID][2] = Room[now]["Porte"]["TpCoord"][Tp][1]
                list_player[PlayerID][3] = Room[now]["Porte"]["TpCoord"][Tp][2]
                previous_room = now
                
                now = Room[now]["Porte"]["TpCoord"][Tp][3]
                list_player[PlayerID][5]= now
                if(now == 9) :
                    list_player[PlayerID][1] = 7+hauteur_joueur
    
    
    
        boutonR0 = 0
        boutonR1 = 0
        boutonR2 = 0
        boutonR41 = 0
        boutonR42 = 0
        boutonR43 = 0
        boutonR44 = 0
        boutonR45 = 0
        boutonR46 = 0
        boutonR47 = 0
        key1=0
        key2=0
        key3=0
        key4=0
        
        if Room[0]["Bouton"]["Pressed"][0] == True :
            boutonR0 = 1
        if Room[1]["Bouton"]["Pressed"][0] == True :
            boutonR1 = 1
        if Room[2]["Bouton"]["Pressed"][0] == True :
            boutonR2 = 1
        if Room[6]["Bouton"]["Pressed"][0] == True :
            boutonR41 = 1
        if Room[6]["Bouton"]["Pressed"][1] == True :
            boutonR42 = 1
        if Room[6]["Bouton"]["Pressed"][2] == True :
            boutonR43= 1
        if Room[6]["Bouton"]["Pressed"][3] == True :
            boutonR44 = 1
        if Room[6]["Bouton"]["Pressed"][4] == True :
            boutonR45 = 1
        if Room[6]["Bouton"]["Pressed"][5] == True :
            boutonR46 = 1
        if Room[6]["Bouton"]["Pressed"][6] == True :
            boutonR47 = 1
        if Room[3]["Key"]["Taken"] == True :
            key1 = 1
        if Room[6]["Key"]["Taken"] == True :
            key2 = 1
        if Room[7]["Key"]["Taken"] == True :
            key3 = 1
        if Room[10]["Key"]["Taken"] == True:
            key4 = 1
    
        
    
        if reseau == True :
            EnvoiMessage((PlayerID,int(list_player[PlayerID][0]*10**5),int(list_player[PlayerID][1]*10**5),int(list_player[PlayerID][2]*10**5),int(list_player[PlayerID][3]*10**5),int(list_player[PlayerID][4]*10**5),boutonR0,boutonR1,boutonR2,boutonR41,boutonR42,boutonR43,boutonR44,boutonR45,boutonR46,boutonR47,Room[3]["Box1"]["Rotate"],Room[3]["Box2"]["Rotate"],Room[3]["Box3"]["Rotate"],bouge,presser,lastbouton,player_play,skin_player_now,Room[7]["Signs"]["Rotate"][0],Room[7]["Signs"]["Rotate"][1],Room[7]["Signs"]["Rotate"][2],Room[7]["Signs"]["Rotate"][3],Room[7]["Signs"]["Rotate"][4],Room[7]["Signs"]["Rotate"][5],Room[7]["Signs"]["Rotate"][6],Room[7]["Signs"]["Rotate"][7],Room[7]["Signs"]["Rotate"][8],rotsign,Room[0]["Porte"]["Open"][1],Room[0]["Porte"]["Open"][2],Room[1]["Porte"]["Open"][0],Room[2]["Porte"]["Open"][0],Room[3]["Porte"]["Open"][0],Room[4]["Porte"]["Open"][0],Room[5]["Porte"]["Open"][0],Room[6]["Porte"]["Open"][0],Room[7]["Porte"]["Open"][0],Room[8]["Porte"]["Open"][0],Room[9]["Porte"]["Open"][0],key1,key2,key3,key4,now,Room[10]["Porte"]["Open"][0],nbJoueur))
    
        """
        if lastbouton != -1 :
            if( lastbouton != 0 and Room[6]["Bouton"]["Pressed"][lastbouton-1]!=True  ):
                    Room[6]["Bouton"]["Pressed"] = [False,False,False,False,False,False,False]
        """
    
        if lastbouton != -1 :
            if( lastbouton != 0 and Room[6]["Bouton"]["Pressed"][lastbouton-1]!=True  ):
                cmpt += 1
                if cmpt == 1 and sound_buttons_room6 != 7*[False]:
                    effect2.play()
                Room[6]["Bouton"]["Pressed"] = [False,False,False,False,False,False,False]
                sound_buttons_room6 = 7*[False]
            else :
                if sound_buttons_room6[lastbouton] == False and now == 6:
                    if lastbouton == 0 : #si bouton 0 appuyé
                        cmpt += 1
                        if cmpt == 1:
                            effect1.play()
                    elif lastbouton == len(Room[6]["Bouton"]["Pressed"])-1 and sound_buttons_room6[lastbouton] == False: #si derier bouton appuyé
                        effect1.play()
                        effect3.play(0)
                        Room[5]["Porte"]["Open"][0] = 1
                        Room[6]["Porte"]["Open"][0] = 1
                        Room[6]["Key"]["Appear"] = True
                    else : #si bouton intermédiaire appuyé
                        if  Room[6]["Bouton"]["Pressed"][lastbouton]==True and  Room[6]["Bouton"]["Pressed"][lastbouton-1]==True :
                            cmpt += 1
                            if cmpt == 1:
                                effect1.play()
                    sound_buttons_room6[lastbouton] = True
        else: #si pas de bouton appuyé
            cmpt = 0
    
    
    
    
        if reseau == True :
            drawPlayers()
    
        for j in Room[now].keys() :
            if(Room[now][j]["function"] != "None"):
                if(Room[now][j]["Type"]=="Bibli"):
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Nb"],Room[now][j]["Rotate"])
    
                if(Room[now][j]["Type"]=="Platforme" or Room[now][j]["Type"]=="Table"):
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"])
    
                if j == "Cell" :
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Rotate"])
    
                if Room[now][j]["Type"]=="Cube":
                    for k in range(len(Room[now][j]["x"])):
                        Room[now][j]["function"](Room[now][j]["x"][k],Room[now][j]["y"],Room[now][j]["z"][k],k+1,True)
    
                if  Room[now][j]["Type"]=="MiniCube":
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Nb"],False)
    
                if  Room[now][j]["Type"]=="Escalier":
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Nb"])
    
                if Room[now][j]["Type"]=="Signe":
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Nb"],Room[now][j]["Rotate"])
    
                if(Room[now][j]["Type"]=="Porte"):
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],Room[now][j]["Rotate"],Room[now][j]["Open"])
    
                if(Room[now][j]["Type"]=="Clef"):
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"])
    
                if(Room[now][j]["Type"]=="Room"):
                    Room[now][j]["function"](Room[now][j]["x"],Room[now][j]["y"],Room[now][j]["z"],now)
                if j == "Bouton" :
                    for k in range(len(Room[now][j]["Pressed"])):
                        Room[now][j]["function"](Room[now][j]["Coord"][k][0],Room[now][j]["Coord"][k][1],Room[now][j]["Coord"][k][2],k)
    
    
        # DESSIN
    
        #print(list_player[PlayerID][3],dir_cam_x,dir_cam_z)
        # commande affichage
    
    
    
    
        glPopMatrix();
    
    
    
        #Begin 2D
    
        glMatrixMode (GL_PROJECTION)
        glPushMatrix ()
        glLoadIdentity ()
        glOrtho (0, Screen_x, 0, Screen_y, float(-1.0), float(1.0))
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()
        glDisable(GL_DEPTH_TEST)
    
        #Draw
    
        Aim()
        """
        timernow = pygame.time.get_ticks()
        time_left = compte_a_rebours - int(((timernow - timerdebut)/1000)) #en seconde
        seconde = time_left % 60
        minute = time_left // 60
    
        seconde_dix = seconde // 10
        minute_dix = minute//10
        seconde_unit = seconde % 10
        minute_unit = minute % 10
    
        if minute_dix != 0 :
            affichageimage(list_chiffre[minute_dix],50+85,100-5,80,80)
        else :
            affichageimage(chiffre_vide,50+85,100-5,80,80)
        affichageimage(list_chiffre[minute_unit],50+165,100-5,80,80)
        affichageimage(chiffre_point,50+245,100-5,80,80)
        affichageimage(list_chiffre[seconde_dix],50+325,100-5,80,80)
        affichageimage(list_chiffre[seconde_unit],50+405,100-5,80,80)
        """
    
        glMatrixMode (GL_PROJECTION)
        glPopMatrix ()
        glMatrixMode (GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

    pygame.display.flip()
    pygame.time.wait(25)
# Close everything down
pygame.quit()


#Fullscreen ~done, clef/grandeporte,palissade, torch, chrono , , , , , , , mamifère gris de moins 8cm3
