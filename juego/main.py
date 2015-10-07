"""
@author: oliver
"""

import pygame,sys
from pygame.locals import *
from random import randint
import os.path
import time
import pygame._view

from Clases import Jugador
from Clases import Enemigo
from Clases import Muro
from Clases import Defensa
from Clases import EntradaEnemigo
from Clases import Estadisticas

#variables globales
ancho = 0
alto = 0
listaEnemigos = []
listaEntradasEnemigos = []
listaMuros = []
listaDefensas = []
listaExplosiones = []
mapaInterno = []
mapaEnemigo = []
iniXjugador = -1
iniYjugador = -1
numTanquesRojos = -1
numTanquesVerdes = -1
numExploradores = -1
maxEnemigosJuntos = -1
tiempo = 0



def checkfile(archivo):

    if os.path.exists(archivo):
        print "El fichero existe"
    else:
        print "El fichero no existe"

#Funcion para cargar el mapa de la pantalla       
def cargarMapa(mapa):
    global ancho
    global alto
    global mapaInterno
    global mapaEnemigo
    global iniXjugador
    global iniYjugador
    global numTanquesRojos
    global numTanquesVerdes
    global numExploradores
    global maxEnemigosJuntos
    global tiempo
    asignarTam = False
    asignarEnemigos = True
    

    f = open(mapa, mode = 'r') #abrir el fichero en modo lectura
    y = 0
    for linea in f: #recorrer todas las lineas del fichero
        temp = linea.split() #cargar una lista con la siguiente linea del fichero
        if not asignarEnemigos:
            if not asignarTam:       
                x = 0
                for elem in temp:
                    if mapaInterno[y][x] == 0:
                        if elem == '1':
                            listaMuros.append(Muro(x*30,y*30,True))
                            mapaInterno[y][x] = 1
                        elif elem == '2':
                            listaMuros.append(Muro(x*30,y*30,False))
                            mapaInterno[y][x] = 2
                        elif elem == 'e':
                            listaEntradasEnemigos.append(EntradaEnemigo(x*30,y*30,60))
                            mapaInterno[y][x] = mapaInterno[y][x+1] = mapaInterno[y+1][x] = mapaInterno[y+1][x+1] = 'e'
                            mapaEnemigo[y][x][0] = mapaEnemigo[y][x+1][0] = mapaEnemigo[y+1][x][0] = mapaEnemigo[y+1][x+1][0] = 'e' #inicialmente el mapa enemigo solo tendra la entrada de enemigo
                        elif elem == 'd':
                            listaDefensas.append(Defensa(x*30,y*30,len(listaDefensas)+1))
                            mapaInterno[y][x] = mapaInterno[y][x+1] = mapaInterno[y][x+2] = mapaInterno[y+1][x] = 'd'
                            mapaInterno[y+2][x] = mapaInterno[y+1][x+1] = mapaInterno[y+2][x+2] = mapaInterno[y+2][x+1] = mapaInterno[y+1][x+2] = 'd'
                        elif elem == 'j' and iniXjugador == -1:
                            iniXjugador = x*30
                            iniYjugador = y*30
                    x += 1
                y += 1
            else: #conseguir el tamanio del mapa
                ancho = int(temp[0]) * 30
                alto = int(temp[1]) * 30
                mapaInterno = [[0 for col in range(int(temp[0]))] for row in range(int(temp[1]))]
                mapaEnemigo = [[[-1,0] for col in range(int(temp[0]))] for row in range(int(temp[1]))]#cada posicion del mapa enemigo tiene [identificador de que hay, numero de veces visitada]
                asignarTam = False
        else:
            numTanquesRojos = int(temp[0])
            numTanquesVerdes = int(temp[1])
            numExploradores = int(temp[2])
            maxEnemigosJuntos = int(temp[3])
            asignarTam = True
            asignarEnemigos = False
    
    f.close()
    


def totalProtection(puntuacion,mapa):
    global alto
    global ancho
    global mapaInterno
    global mapaEnemigo
    global iniXjugador
    global iniYjugador
    global numTanquesRojos
    global numTanquesVerdes
    global numExploradores
    global maxEnemigosJuntos
    
    
    pygame.init() #inicializar pygame
    cargarMapa(mapa)
    
    anchoEstadisticas = 200    
    
    ventana = pygame.display.set_mode((ancho+anchoEstadisticas, alto)) #crear una ventana de un tamanio
    colorFondo = pygame.Color(194,176,120)
    ventana.fill(colorFondo)
    pygame.display.set_caption("Total Protection") #nombre que aparecera en la ventana
    
    jugador = Jugador(ancho, alto,iniXjugador,iniYjugador)  #creacion de el objeto jugador  
    
    reloj = pygame.time.Clock()
    enJuego = True
    victoria = False
    tiempoFin = -1
    pulsadoArriba = pulsadoAbajo = pulsadoDerecha = pulsadoIzquierda = False
    aux = 0
    cuadroEstadisticas = Estadisticas(ancho, alto, anchoEstadisticas) 
    
    cuadroFinJuego = pygame.Rect((ancho//2)-75,(alto//2)-25,150,50)
    cuadroVictoria = pygame.Rect((ancho//2)-100,(alto//2)-50,200,75)
    
    miFuente = pygame.font.Font(None,30)
    while True:
        reloj.tick(60) #controlar la velocidad del juego
        ventana.fill(colorFondo) #pintar el color de fondo
        cuadroEstadisticas.dibujarCuadro(ventana)
        
        
        if enJuego:
            tiempo = pygame.time.get_ticks()/1000 
        
        cuadroEstadisticas.setDatos(tiempo, numTanquesRojos,numTanquesVerdes,numExploradores, puntuacion)
        
        #pongo aux <= tiempo porque si se mueve la pantalla el tiempo continua contando pero el programa se queda bloqueado y no vuelve a entra al if cuando continua la ejecucion
        if aux <= tiempo: #entrara cada segundo
            aux += 1
            if numTanquesRojos != 0 or numTanquesVerdes != 0 or numExploradores != 0:
                if aux % 2 == 0 and len(listaEnemigos) < maxEnemigosJuntos: #crea cada dos segundos un enemigo (no puede haber mas de maxEnemigosJuntos enemigos)
                    entradaAleat = randint(0,len(listaEntradasEnemigos)-1)
                    posx, posy = listaEntradasEnemigos[entradaAleat].rect.x, listaEntradasEnemigos[entradaAleat].rect.y
                    eneAleat = [] 
                    
                    if numTanquesRojos > 0:
                        eneAleat.append(0)
                    if numTanquesVerdes > 0:
                        eneAleat.append(1)
                    if numExploradores > 0:
                        eneAleat.append(2)
                       
                    eneSacado = eneAleat[randint(0,len(eneAleat)-1)]
                    
                    if eneSacado == 0:
                        enem = Enemigo(ancho,alto,posx,posy,True,True)#crear un vehiculo tipo tanque rojo
                    elif eneSacado == 1:
                        enem = Enemigo(ancho,alto,posx,posy,True,False)#crear un vehiculo tipo tanque verde
                    else:
                        enem = Enemigo(ancho,alto,posx,posy,False,False)#crear un vehiculo tipo coche explorador
                    
                    ocupado = False
                    for e in listaEnemigos:
                        if enem.rect.colliderect(e.rect):
                            ocupado = True
                    if not ocupado:
                        listaEnemigos.append(enem)
                        if eneSacado == 0:
                            numTanquesRojos -= 1
                        elif eneSacado == 1:
                            numTanquesVerdes -= 1
                        else:
                            numExploradores -= 1
                
                


        #para que el vehiculo del jugador se mueva dejando pulsada la tecla de direccion
        if enJuego and pulsadoIzquierda:
            jugador.movimientoIzquierda(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
        elif enJuego and pulsadoDerecha:
            jugador.movimientoDerecha(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
        elif enJuego and pulsadoArriba:
            jugador.movimientoArriba(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
        elif enJuego and pulsadoAbajo:
            jugador.movimientoAbajo(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)

        #Recorrer lista de eventos
        for event in pygame.event.get():#extraer lista de eventos predeterminados
                if event.type == QUIT: #cuando el usuario pulsa en la cruz para cerrar la ventana
                    pygame.quit() #detener modulos de pygame iniciados         
                    sys.exit() #cerrar la ventana
                if enJuego and not victoria:
                    
                    #si se ha pulsado alguna tecla... hacer una determinada accion        
                    if event.type == pygame.KEYDOWN:
                        if event.key == K_LEFT:
                            pulsadoIzquierda = True
                            jugador.movimientoIzquierda(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
                        elif event.key == K_RIGHT:
                            pulsadoDerecha = True                        
                            jugador.movimientoDerecha(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
                        if event.key == K_UP:
                            pulsadoArriba = True
                            jugador.movimientoArriba(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
                        elif event.key == K_DOWN:
                            pulsadoAbajo = True                        
                            jugador.movimientoAbajo(listaMuros+listaEnemigos+listaDefensas+listaEntradasEnemigos)
                        elif event.key == K_d:
                            x,y = jugador.rect.center
                            jugador.disparar(x,y)
                    
                    #cuando se deje de pulsar alguna tecla, si es alguna tecla de direccion se marcara como no pulsada
                    elif event.type == pygame.KEYUP:
                        if pygame.key.name(event.key) == 'left':
                            pulsadoIzquierda = False
                        elif pygame.key.name(event.key) == 'right':
                            pulsadoDerecha = False
                        if pygame.key.name(event.key) == 'up':
                            pulsadoArriba = False
                        elif pygame.key.name(event.key) == 'down':
                            pulsadoAbajo = False            
        
        #dibujar los disparos del jugador
        if len(jugador.listaDisparo) > 0:
            for x in jugador.listaDisparo:
                eliminado = False
                x.dibujar(ventana)
                x.trayectoria()
                
                #eliminar el disparo si se sale de la pantalla
                if x.rect.top < 1 or x.rect.bottom > alto-1 or x.rect.left < 1 or x.rect.right > ancho-1:
                    jugador.listaDisparo.remove(x)
                    eliminado = True
                else:
                    for enemigo in listaEnemigos:#si el disparo colisiona con algun enemigo eliminar el enemigo y el disparo
                        if x.rect.colliderect(enemigo.rect):
                            if not enemigo.restarVida():
                                listaExplosiones.append(enemigo)
                                listaEnemigos.remove(enemigo)
                                puntuacion += 200
                            jugador.listaDisparo.remove(x)
                            eliminado = True
                            
                            break
                            
                    if not eliminado: #si el disparo colisiona con un muro
                        for muro in listaMuros:
                            if x.rect.colliderect(muro.rect):
                                if not muro.restarVida(): 
                                    mapaInterno[muro.rect.centery//30][muro.rect.centerx//30] = 0
                                    listaMuros.remove(muro)
                                jugador.listaDisparo.remove(x)
                                eliminado = True
                                break
                            
                    if not eliminado: #si el disparo colisiona con una defensa
                        for defensa in listaDefensas:
                            if x.rect.colliderect(defensa.rect):
                                if not defensa.restarVida(): #sera true cuando la defensa no tenga vida
                                    listaExplosiones.append(defensa)
                                    listaDefensas.remove(defensa)
                                    if len(listaDefensas) == 0:
                                            enJuego = False
                                            tiempoFin = tiempo
                                    puntuacion -= 600
                                jugador.listaDisparo.remove(x)
                                eliminado = True
                                puntuacion -= 50
                                break
                                    
        
        #dibujar los muros del mapa
        for muro in listaMuros:
            muro.dibujar(ventana)
        
        #dibujar las bases de defensa
        for defensa in listaDefensas:
            defensa.dibujar(ventana)
            defensa.dibujarVida(ventana)
                
        #dibujar enemigo, llamar a su comportamiento y dibujar disparos
        for enemigo in listaEnemigos:
            if enJuego:
                enemigo.comportamiento(tiempo, listaMuros+listaEnemigos+listaDefensas+[jugador],mapaEnemigo, mapaInterno,jugador.rect.center)
            else:
                enemigo.comportamiento(tiempo, listaMuros+listaEnemigos+listaDefensas+[jugador],mapaEnemigo, mapaInterno,[5000,5000])
            if len(enemigo.listaDisparo) > 0:
                for x in enemigo.listaDisparo:
                    eliminado = False
                    x.dibujar(ventana)
                    x.trayectoria()
                    
                    #eliminar el disparo si se sale de la pantalla
                    if x.rect.top < 1 or x.rect.bottom > alto-1 or x.rect.left < 1 or x.rect.right > ancho-1:
                        enemigo.listaDisparo.remove(x)
                    
                    else:
                        for ene in listaEnemigos:#si el disparo colisiona con algun enemigo por el momento solo se elimina el disparo
                            if ene != enemigo and x.rect.colliderect(ene.rect):
                                #listaEnemigos.remove(enemigo)
                                enemigo.listaDisparo.remove(x)
                                eliminado = True
                                break
                                
                        if not eliminado:
                            for muro in listaMuros:
                                if x.rect.colliderect(muro.rect):
                                    if not muro.restarVida():
                                        mapaInterno[muro.rect.centery//30][muro.rect.centerx//30] = 0
                                        mapaEnemigo[muro.rect.centery//30][muro.rect.centerx//30][0] = 0
                                        listaMuros.remove(muro)
                                    enemigo.listaDisparo.remove(x)
                                    eliminado = True
                                    break
                        
                        if not eliminado: #si el disparo colisiona con una defensa
                            for defensa in listaDefensas:
                                if x.rect.colliderect(defensa.rect):
                                    if not defensa.restarVida(): #sera true cuando la defensa no tenga vida
                                        listaExplosiones.append(defensa)
                                        listaDefensas.remove(defensa)
                                        if len(listaDefensas) == 0:
                                            enJuego = False
                                            tiempoFin = tiempo
                                        if enJuego:
                                            puntuacion -= 300
                                    enemigo.listaDisparo.remove(x)
                                    eliminado = True
                                    if enJuego:
                                        puntuacion -= 30
                                    break
                                
                        if not eliminado and (not jugador.muerto()):
                            if x.rect.colliderect(jugador.rect):
                                if not jugador.restarVida():
                                    listaExplosiones.append(jugador)
                                    enJuego = False
                                    tiempoFin = tiempo
                                    puntuacion -= 1000
                                enemigo.listaDisparo.remove(x)
                                eliminado = True
                                puntuacion -= 30
                        
            enemigo.dibujar(ventana)
                
        
        if not jugador.muerto():
            jugador.dibujar(ventana)#dibujar el vehiculo del jugador
        
        
        for exp in listaExplosiones:#dibujar las explosiones de los vehiculos eliminados
            exp.dibujarExplosion(ventana)
            if exp.refrescosExplosion <= 0:
                listaExplosiones.remove(exp)
                
                
        cuadroEstadisticas.dibujarDatos(ventana)
        
        if not victoria:
            if len(listaEnemigos) == 0 and numTanquesRojos == 0 and numTanquesVerdes == 0 and numExploradores == 0:
                victoria = True
                tiempoFin = tiempo
                
                
        if victoria:
            if tiempo - tiempoFin == 10: # 10 segundos de descanso entre mapa y mapa
                tiempoFin = -1
                return puntuacion
            else:
                pygame.draw.rect(ventana,pygame.Color(0,0,0),cuadroVictoria)
                textoVictoria = miFuente.render("Victoria!",0,pygame.Color(230,230,230))
                textoCargando = miFuente.render("Cargando mapa...",0,pygame.Color(230,230,230))
                ventana.blit(textoVictoria,((ancho//2)-45,(alto//2)-30))
                ventana.blit(textoCargando,((ancho//2)-85,(alto//2)))
                
        
        if not enJuego:
            pygame.draw.rect(ventana,pygame.Color(220,0,0),cuadroFinJuego)
            textoFin = miFuente.render("Fin del juego!",0,pygame.Color(230,230,230))
            ventana.blit(textoFin,((ancho//2)-65,(alto//2)-10))
            
        
            
            
            
            
        pygame.display.update() #actualizar la ventana (refresco)
        
        
            

puntuacion = 0
i = 1
mapa = "Mapas/mapa"+str(i)+".mp"
while os.path.exists(mapa):
    puntuacion = totalProtection(puntuacion, mapa)
    i += 1
    mapa = "Mapas/mapa"+str(i)+".mp"
    ancho = 0
    alto = 0
    listaEnemigos = []
    listaEntradasEnemigos = []
    listaMuros = []
    listaDefensas = []
    listaExplosiones = []
    mapaInterno = []
    mapaEnemigo = []
    iniXjugador = -1
    iniYjugador = -1
    numTanquesRojos = -1
    numTanquesVerdes = -1
    numExploradores = -1
    maxEnemigosJuntos = -1

pygame.display.quit()
pygame.quit()

minutos = tiempo // 60
segundos = tiempo % 60

if minutos < 10:
    minutStr = "0"+str(minutos)
else:
    minutStr = str(minutos)
if segundos < 10:
    segunStr = "0"+str(segundos)
else:
    segunStr = str(segundos)
    
f = open ("puntuaciones.txt", "a")
f.write("\n"+time.strftime("%d/%m/%y") + " " + time.strftime("%H:%M:%S") + "  -->  " + "puntuacion: " + str(puntuacion))
f.close()

sys.exit()