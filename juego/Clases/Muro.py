# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 19:06:19 2015

@author: Oliver
"""

import pygame

class Muro(pygame.sprite.Sprite):
    """Clase para controlar los muros que hay distribuidos por el mapa"""
    
    """
    Constructor de la clase
    """
    def __init__(self,posx,posy,tipoLadrillo):
        pygame.sprite.Sprite.__init__(self)
        
        self.tipoLadrillo = tipoLadrillo
        if tipoLadrillo:#cargar el tipo de muro indicado
            self.imageMuro = pygame.image.load('Imagenes/ladrillosPeque.png')
            self.imageMuroGolpe1 = pygame.image.load('Imagenes/ladrillosPequeGolpe1.png')
        else:
            self.imageMuro = pygame.image.load('Imagenes/piedraPeque.png')
            self.imageMuroGolpe1 = pygame.image.load('Imagenes/piedraPequeGolpe1.png')
            self.imageMuroGolpe2 = pygame.image.load('Imagenes/piedraPequeGolpe2.png')
            
        self.rect = self.imageMuro.get_rect()#obtener el rectangulo de la imagen
        
        if tipoLadrillo:
            self.resistencia = 2 #resistencia del muro a disparos
        else:
            self.resistencia = 3
        
        self.rect.top = posy #posicion donde aparecera el muro
        self.rect.left = posx
        
    
    """
    Metodo que dibuja el muro
    """
    def dibujar(self,superficie):
        if self.tipoLadrillo:
            if self.resistencia == 2:
                superficie.blit(self.imageMuro, self.rect)
            else:
                superficie.blit(self.imageMuroGolpe1, self.rect)
        else:
            if self.resistencia == 3:
                superficie.blit(self.imageMuro, self.rect)
            elif self.resistencia == 2:
                superficie.blit(self.imageMuroGolpe1, self.rect)
            else:
                superficie.blit(self.imageMuroGolpe2, self.rect)
                
                
            
            
    def restarVida(self):
        self.resistencia -= 1
        if self.resistencia > 0:
            return True
        else:
            return False