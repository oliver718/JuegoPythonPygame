# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 10:15:34 2015

@author: Oliver
"""

import pygame
import Proyectil
from random import randint

class Enemigo(pygame.sprite.Sprite):
    """Clase controlar el vehiculo del enemigo y sus acciones"""
    
    """
    Constructor de la clase
    """
    def __init__(self, ancho,alto,posx,posy,esTanque,tankFuerte):
        pygame.sprite.Sprite.__init__(self)
        
        self.esTanque = esTanque #por parametros se indica si el vehiculo enemigo sera un tanque
        self.tankFuerte = tankFuerte
        
        if esTanque and tankFuerte:#con un 30 porciento de probabilidad el tanque sera un tanque fuerte (mas resistente a proyectiles)
            self.resistencia = 2
        else:
            self.resistencia = 1
        
        self.gradosMov = 0#para saber en cada momento la orientacion en grados del vehiculo
        
        self.ImagenVehiculo = self.__cargarVehiculo(180)
        
        if self.esTanque:
            self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionTank.png'),0)
        else:
            self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionCar.png'),0)
        self.orientacion = 'S'
        self.rect = self.ImagenVehiculo.get_rect() #obtener un rectangulo del tamanio de la imagen
        self.listaDisparo = [] #almacenara los proyectiles lanzados (para poder ser destruidos y controlar las colisicones)
        if esTanque:
            self.velocidad = 3 #velocidad de movimiento de los tanques
        else:
            self.velocidad = 7 #velocidad de movimiento de los vehiculos exploradores
        self.anchoVentana = ancho
        self.altoVentana = alto
        self.refrescosExplosion = 15 #numero de veces que se refrescara la explosion del vehiculo cuando este sea tocado con un proyectil
        self.rect.top = posy #posicion inicial del vehiculo
        self.rect.left = posx
        
        self.rangoDisparo = 10
        self.rangoCambioMov = 10
        self.tocaPared = False
        
        self.posMapaX = self.rect.centerx//30
        self.posMapaY = self.rect.centery//30
        
        self.centerxAnt = self.rect.centerx
        self.centeryAnt = self.rect.centery
        
        
        try:
            #self.sonidoDisparo = pygame.mixer.Sound("Sonidos/disparoEnemigo.wav")
            if self.esTanque:
                self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionTank.png'),0)
                self.sonidoExplosion = pygame.mixer.Sound("Sonidos/explosionTank.wav")
            else:
                self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionCar.png'),0)
                self.sonidoExplosion = pygame.mixer.Sound("Sonidos/explosionCar.wav")
            
        except:
            print "No se ha cargado el sonido"
    
    """
    Metodo que devuelve la imagen del vehiculo cargada con unos grados de rotacion
    """
    def __cargarVehiculo(self,grados):
        
        self.gradosMov = grados #guardar la orientacion del vehiculo en cada momento
        if self.esTanque and self.tankFuerte and self.resistencia == 1:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankRojoGolpe1.png'),grados)
        elif self.esTanque and self.tankFuerte:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankRojo.png'),grados)  #cargar imagen del vehiculo
        elif self.esTanque:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankVerde.png'),grados)
        else:
            return pygame.transform.rotate(pygame.image.load('Imagenes/car.png'),grados)
        
    
    """
    Metodo para dibujar el vehiculo del enemigo
    """
    def dibujar(self,superficie):
        superficie.blit(self.ImagenVehiculo,self.rect)
        
    """
    Metodo para la explosion cuando el enemigo ha sido tocado por el jugador
    """
    def dibujarExplosion(self,superficie):
        if self.refrescosExplosion == 10:
            self.sonidoExplosion.play()
        superficie.blit(self.ImagenExplosion,self.rect)
        self.refrescosExplosion -= 1
        
    def comportamiento(self,tiempo, listaObstaculos, mapaEnemigo, mapaInterno, posJugador):
        
        if self.esTanque:
            if randint(0,100) < 50:
                if posJugador[0] + 20 > self.rect.x  and  posJugador[0] - 20 < self.rect.x and abs(posJugador[1]-self.rect.y) <= 100:#atacar si tiene al jugador cerca por arriba o por abajo
                    if posJugador[1] > self.rect.y:
                        self.movimientoAbajo(listaObstaculos)
                    else:
                        self.movimientoArriba(listaObstaculos)
                    self.__ataque(True)
                    
                elif posJugador[1] + 20 > self.rect.y  and  posJugador[1] - 20 < self.rect.y and abs(posJugador[0]-self.rect.x) <= 100: #atacar si tiene al jugador cerca por la derecha o por la izquierda
                    if posJugador[0] > self.rect.x:
                        self.movimientoDerecha(listaObstaculos)
                    else:
                        self.movimientoIzquierda(listaObstaculos)
                    self.__ataque(True)
            
            elif randint(0,100) < self.rangoCambioMov or self.tocaPared: #cambiar la orientacion del vehiculo 
                ori = randint(1,4)
                if ori == 1:
                    self.movimientoArriba(listaObstaculos)
                elif ori == 2:
                    self.movimientoAbajo(listaObstaculos)
                elif ori == 3:
                    self.movimientoDerecha(listaObstaculos)
                else:
                    self.movimientoIzquierda(listaObstaculos)
                self.__ataque(False)
            elif randint(0,100) < 80: #avanzar en la direccion que esta el vehiculo
                if self.orientacion == 'N':
                    self.movimientoArriba(listaObstaculos)
                elif self.orientacion == 'S':
                    self.movimientoAbajo(listaObstaculos)
                elif self.orientacion == 'E':
                    self.movimientoDerecha(listaObstaculos)
                else:
                    self.movimientoIzquierda(listaObstaculos)
                self.__ataque(False)
        
        else: #si es un vehiculo explorador
            if randint(0,100) < 50:
                mapaEnemigo[self.posMapaY][self.posMapaX][1] += 1
                self.__explorar(mapaEnemigo, mapaInterno)
                
                #if mapaEnemigo[self.posMapaY][self.posMapaX][0] != 'e':
                self.__movimientoExploracion(listaObstaculos, mapaEnemigo)
                #else:
                    #self.__salirZonaSalida(listaObstaculos, mapaEnemigo)
                    
                if self.centerxAnt == self.rect.centerx and self.centeryAnt == self.rect.centery:
                    self.__solucionarColision(listaObstaculos, mapaEnemigo)
                    
                
        self.posMapaX = self.rect.centerx//30
        self.posMapaY = self.rect.centery//30
        
        
            
        self.centerxAnt = self.rect.centerx
        self.centeryAnt = self.rect.centery
            
        
        
    
    
    """
    Funcion para solucionar un atasco del vehiculo
    """
    def __solucionarColision(self, listaObstaculos, mapaEnemigo):
        posibleMov = []
        if self.orientacion == 'N':
            posibleMov = ['S','E','O']
        elif self.orientacion == 'S':
            posibleMov = ['N','E','O']
        elif self.orientacion == 'E':
            posibleMov = ['N','S','O']
        elif self.orientacion == 'O':
            posibleMov = ['N','E','S']
            
        mov = posibleMov[randint(0,len(posibleMov)-1)]
            
        if mov == 'E':
            self.movimientoDerecha(listaObstaculos)
        elif mov == 'S':
            self.movimientoAbajo(listaObstaculos)
        elif mov == 'O':
            self.movimientoIzquierda(listaObstaculos)
        elif mov == 'N':
            self.movimientoArriba(listaObstaculos)
            
    """
    Funcion que realiza el movimiento del vehiculo explorador
    """
    def __movimientoExploracion(self, listaObstaculos, mapaEnemigo):
        minExplo = None
        if self.orientacion == 'N' and self.posMapaY-1 >= 0: #sacar inicialmente la orientacion a la que esta el vehiculo, para que en el caso de igualdad avanzar
            if mapaEnemigo[self.posMapaY-1][self.posMapaX][0] == 0 or mapaEnemigo[self.posMapaY-1][self.posMapaX][0] == 'e':
                minExplo = mapaEnemigo[self.posMapaY-1][self.posMapaX][1]
        elif self.orientacion == 'S' and self.posMapaY+1 < len(mapaEnemigo):
            if mapaEnemigo[self.posMapaY+1][self.posMapaX][0] == 0 or mapaEnemigo[self.posMapaY+1][self.posMapaX][0] == 'e':
                minExplo = mapaEnemigo[self.posMapaY+1][self.posMapaX][1]
        elif self.orientacion == 'E' and self.posMapaX+1 < len(mapaEnemigo[0]):
            if mapaEnemigo[self.posMapaY][self.posMapaX+1][0] == 0 or mapaEnemigo[self.posMapaY][self.posMapaX+1][0] == 'e':
                minExplo = mapaEnemigo[self.posMapaY][self.posMapaX+1][1]
        elif self.orientacion == 'O' and self.posMapaX-1 >= 0:
            if mapaEnemigo[self.posMapaY][self.posMapaX-1][0] == 0 or mapaEnemigo[self.posMapaY][self.posMapaX-1][0] == 'e':
                minExplo = mapaEnemigo[self.posMapaY][self.posMapaX-1][1]
        oriMinExplo = self.orientacion
        
        
        if self.posMapaX+1 < len(mapaEnemigo[0]): #buscar la orientacion menos explorada
            if (minExplo > mapaEnemigo[self.posMapaY][self.posMapaX+1][1] or minExplo == None) and (mapaEnemigo[self.posMapaY][self.posMapaX+1][0] == 0 or mapaEnemigo[self.posMapaY][self.posMapaX+1][0] == 'e'):
                minExplo = mapaEnemigo[self.posMapaY][self.posMapaX+1][1]
                oriMinExplo = 'E'
        if self.posMapaY+1 < len(mapaEnemigo):
            if (minExplo > mapaEnemigo[self.posMapaY+1][self.posMapaX][1] or minExplo == None) and (mapaEnemigo[self.posMapaY+1][self.posMapaX][0] == 0 or mapaEnemigo[self.posMapaY+1][self.posMapaX][0] == 'e'):
                minExplo = mapaEnemigo[self.posMapaY+1][self.posMapaX][1]
                oriMinExplo = 'S'
        if self.posMapaX-1 >= 0:
            if (minExplo > mapaEnemigo[self.posMapaY][self.posMapaX-1][1] or minExplo == None) and (mapaEnemigo[self.posMapaY][self.posMapaX-1][0] == 0 or mapaEnemigo[self.posMapaY][self.posMapaX-1][0] == 'e'):
                minExplo = mapaEnemigo[self.posMapaY][self.posMapaX-1][1]
                oriMinExplo = 'O'
        
        if self.posMapaY-1 >= 0:
            if (minExplo > mapaEnemigo[self.posMapaY-1][self.posMapaX][1] or minExplo == None) and (mapaEnemigo[self.posMapaY-1][self.posMapaX][0] == 0 or mapaEnemigo[self.posMapaY-1][self.posMapaX][0] == 'e'):
                minExplo = mapaEnemigo[self.posMapaY-1][self.posMapaX][1]
                oriMinExplo = 'N'
            
        if oriMinExplo == 'E':#realizar el movimiento
            self.movimientoDerecha(listaObstaculos)
        elif oriMinExplo == 'S':
            self.movimientoAbajo(listaObstaculos)
        elif oriMinExplo == 'O':
            self.movimientoIzquierda(listaObstaculos)
        elif oriMinExplo == 'N':
            self.movimientoArriba(listaObstaculos)
            
    
    """
    Funcion para reconocer el alrededor del vehiculo explorador
    """
    def __explorar(self, mapaEnemigo, mapaInterno):
        if self.posMapaX+1 < len(mapaEnemigo[0]):
            mapaEnemigo[self.posMapaY][self.posMapaX+1][0] = mapaInterno[self.posMapaY][self.posMapaX+1]
        if self.posMapaY+1 < len(mapaEnemigo):
            mapaEnemigo[self.posMapaY+1][self.posMapaX][0] = mapaInterno[self.posMapaY+1][self.posMapaX]
        if self.posMapaX-1 >= 0:
            mapaEnemigo[self.posMapaY][self.posMapaX-1][0] = mapaInterno[self.posMapaY][self.posMapaX-1]                
        if self.posMapaY-1 >= 0:
            mapaEnemigo[self.posMapaY-1][self.posMapaX][0] = mapaInterno[self.posMapaY-1][self.posMapaX]                   

            
    def __ataque(self,disparar):
        if disparar:
            if randint(0,100) < 40:
                self.__disparar()
        elif randint(0,100) < self.rangoDisparo:
            self.__disparar()
    
    def __disparar(self):
        if len(self.listaDisparo) < 2: #solo puede haber 2 proyectiles lanzados activos por cada vehiculo
            #self.sonidoDisparo.play()
            x,y = self.rect.center
            miProyectil = Proyectil.Proyectil(x,y,self.orientacion)
            self.listaDisparo.append(miProyectil)
            
    def restarVida(self):
        self.resistencia -= 1 
        if self.resistencia > 0:
            self.ImagenVehiculo = self.__cargarVehiculo(self.gradosMov)
            return True
        else:
            return False

    """
    Metodo que realiza el movimento del vehiculo hacia la derecha
    orientando (hacia el este) el vehiculo
    """
    def movimientoDerecha(self, listaObstaculos):
        if self.orientacion != 'E':
            self.ImagenVehiculo = self.__cargarVehiculo(270)          
            self.orientacion = 'E'
        self.rect.right += self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if muro != self and self.rect.colliderect(muro.rect):
                if self.rect.right > muro.rect.left:
                    self.rect.right = muro.rect.left
    
    """
    Metodo que realiza el movimento del vehiculo hacia la izquierda
    orientando (hacia el oeste) el vehiculo 
    """
    def movimientoIzquierda(self, listaObstaculos):
        if self.orientacion != 'O':
    		self.ImagenVehiculo = self.__cargarVehiculo(90) 
        	self.orientacion = 'O'
        self.rect.left -= self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if muro != self and self.rect.colliderect(muro.rect):
                if self.rect.left < muro.rect.right:
                    self.rect.left = muro.rect.right
        
    """
    Metodo que realiza el movimento del vehiculo hacia arriba
    orientando (hacia el norte) el vehiculo 
    """  
    def movimientoArriba(self, listaObstaculos):
        if self.orientacion != 'N':
    		self.ImagenVehiculo = self.__cargarVehiculo(0) 
        	self.orientacion = 'N'
        self.rect.top -= self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if muro != self and self.rect.colliderect(muro.rect):
                if self.rect.top < muro.rect.bottom:
                    self.rect.top = muro.rect.bottom
        
    """
    Metodo que realiza el movimento del vehiculo hacia abajo
    orientando (hacia el sur) el vehiculo 
    """  
    def movimientoAbajo(self, listaObstaculos):
        if self.orientacion != 'S':
    		self.ImagenVehiculo = self.__cargarVehiculo(180) 
        	self.orientacion = 'S'
        self.rect.bottom += self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if muro != self and self.rect.colliderect(muro.rect):
                if self.rect.bottom > muro.rect.top:
                    self.rect.bottom = muro.rect.top
        
    
    
    """
    Metodo privado que limita el movimiento del vehiculo para que 
    no se salga de la pantalla
    """
    def __movimiento(self):
        self.tocaPared = True
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.anchoVentana:
            self.rect.right = self.anchoVentana
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.altoVentana:
            self.rect.bottom = self.altoVentana
        else:
            self.tocaPared = False
                
