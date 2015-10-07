# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:08:02 2015

@author: Oliver
"""

import pygame

class Defensa(pygame.sprite.Sprite):
    """Clase para controlar las bases que el jugador tiene que defender de los enemigos"""
    
    """
    Constructor de la clase
    """
    def __init__(self,posx,posy,identificador):
        pygame.sprite.Sprite.__init__(self)
        
        self.identificador = identificador
        self.imageDefensa = pygame.image.load('Imagenes/defender.png')
        self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionDefensa.png'),0)
        self.rect = self.imageDefensa.get_rect()#obtener el rectangulo de la imagen
        
        self.resistencia = 100 #resistencia de la defensa a disparos
        self.vida = self.resistencia
        self.rect.top = posy #posicion donde aparece zona a defender
        self.rect.left = posx
        
        self.refrescosExplosion = 10 #numero de veces que se refrescara la explosion del vehiculo cuando este sea tocado con un proyectil
        
        try:
            self.sonidoExplosion = pygame.mixer.Sound("Sonidos/explosionDefensa.wav")
        except:
            print "No se ha cargado el sonido"
        
    
    """
    Metodo que dibuja el muro
    """
    def dibujar(self,superficie):
        superficie.blit(self.imageDefensa, self.rect)
        
    """
    Metodo para la explosion cuando el enemigo ha sido tocado por el jugador
    """
    def dibujarExplosion(self,superficie):
        if self.refrescosExplosion == 10:
            self.sonidoExplosion.play()
        superficie.blit(self.ImagenExplosion,self.rect)
        self.refrescosExplosion -= 1
    
    def dibujarVida(self,superficie):
        if self.vida < self.resistencia:
            pygame.draw.rect(superficie,(0,0,0), (self.rect.centerx-2,self.rect.centery-2,self.resistencia+4,9))#rectangulo negro
            pygame.draw.rect(superficie,(255,0,0), (self.rect.centerx,self.rect.centery,self.resistencia,5))#rectangulo rojo
            pygame.draw.rect(superficie,(0,255,0), (self.rect.centerx,self.rect.centery,self.vida,5))#rectangulo verde
    
    def restarVida(self):
        self.vida -= 5 
        if self.vida > 0:
            return True
        else:
            return False
        
        