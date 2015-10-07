# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 21:25:51 2015

@author: Oliver
"""

import pygame

class Estadisticas(pygame.sprite.Sprite):
    """Clase para controlar los muros que hay distribuidos por el mapa"""
    
    """
    Constructor de la clase
    """
    def __init__(self,ancho,alto,anchoEstadisticas):
        pygame.sprite.Sprite.__init__(self)
        
        self.cuadro = pygame.Rect(ancho,0,anchoEstadisticas,alto)
        self.ancho = ancho
        self.alto = alto
        self.anchoEstadisticas = anchoEstadisticas
        self.numRojos = 0
        self.numVerdes = 0
        self.numExplo = 0
        self.minutos = 0
        self.segundos = 0
        self.imRojo = pygame.image.load('Imagenes/tankRojo.png')
        self.imVerde = pygame.image.load('Imagenes/tankVerde.png')
        self.imExplo = pygame.image.load('Imagenes/car.png')
        self.rectRojo = self.imRojo.get_rect()
        self.rectRojo.top = (self.alto//2)-100
        self.rectRojo.left = self.ancho+20
        self.rectVerde = self.imVerde.get_rect()
        self.rectVerde.top = (self.alto//2)-20
        self.rectVerde.left = self.ancho+20
        self.rectExplo = self.imVerde.get_rect()
        self.rectExplo.top = (self.alto//2)+60
        self.rectExplo.left = self.ancho+30
        self.puntuacion = 0
        self.miFuente = pygame.font.Font(None,30)
        
        
    
    """
    Metodo que dibuja el cuadro donde apareceran las estadisticas
    """
    def dibujarCuadro(self,superficie):
        pygame.draw.rect(superficie,pygame.Color(100,100,100),self.cuadro) #pintar cuadro de estadisticas
        
    
    def dibujarDatos(self,superficie):         
        if self.minutos < 10:
            minut = "0"+str(self.minutos)
        else:
            minut = str(self.minutos)
        if self.segundos < 10:
            segun = "0"+str(self.segundos)
        else:
            segun = str(self.segundos)
        
        
        textoTiempo = self.miFuente.render("Tiempo:",0,(220,220,220))
        textoMinSeg = self.miFuente.render(minut+" : "+segun,0,(220,220,220)) 
        numRojos = self.miFuente.render("X "+str(self.numRojos),0,(220,220,220))
        numVerdes = self.miFuente.render("X "+str(self.numVerdes),0,(220,220,220))
        numExplo = self.miFuente.render("X "+str(self.numExplo),0,(220,220,220))
        textoPuntuacion = self.miFuente.render("Puntuacion:",0,(220,220,220))
        textoNumPuntuacion = self.miFuente.render(str(self.puntuacion),0,(220,220,220))
        superficie.blit(numRojos,(self.ancho+90,(self.alto//2)-70))
        superficie.blit(numVerdes,(self.ancho+90,(self.alto//2)+10))
        superficie.blit(numExplo,(self.ancho+90,(self.alto//2)+65))
        superficie.blit(textoTiempo,(self.ancho+20,25))
        superficie.blit(textoMinSeg,(self.ancho+20,50))
        superficie.blit(self.imRojo,self.rectRojo)
        superficie.blit(self.imVerde,self.rectVerde)
        superficie.blit(self.imExplo,self.rectExplo)
        superficie.blit(textoPuntuacion,(self.ancho+20,self.alto-75))
        superficie.blit(textoNumPuntuacion,(self.ancho+20,self.alto-50))
        
        #superficie.blit(miTexto,(10,50))
        
    def setDatos(self,tiempo, numTanquesRojos,numTanquesVerdes,numExploradores, puntuacion):
        self.numRojos = numTanquesRojos
        self.numVerdes = numTanquesVerdes
        self.numExplo = numExploradores
        self.minutos = tiempo // 60
        self.segundos = tiempo % 60
        self.puntuacion = puntuacion
                