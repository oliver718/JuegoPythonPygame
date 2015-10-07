"""
@author: oliver
"""
import pygame

class Proyectil(pygame.sprite.Sprite):
    """Clase para controlar los disparos de los vehiculos"""
    
    """
    Constructor de la clase
    """
    def __init__(self,posx,posy, orientacion):
        pygame.sprite.Sprite.__init__(self)
        
        #Segun para donde este dirigido el tanque, el proyetil se orientara hacia un lado u otro
        if orientacion == 'S':
            self.imageProyectil = pygame.transform.rotate(pygame.image.load('Imagenes/disparo.png'),180)
        elif orientacion == 'N':
            self.imageProyectil = pygame.image.load('Imagenes/disparo.png')
        if orientacion == 'E':
            self.imageProyectil = pygame.transform.rotate(pygame.image.load('Imagenes/disparo.png'),270)
        if orientacion == 'O':
            self.imageProyectil = pygame.transform.rotate(pygame.image.load('Imagenes/disparo.png'),90)
        
        self.rect = self.imageProyectil.get_rect()#obtener el rectangulo de la imagen
        self.velocidadDisparo = 10
        
        self.rect.centery = posy #la posx y posy obtenidas sera el centro de la imagen donde aparecera inicialmente
        self.rect.centerx = posx
        
        self.orientacion = orientacion #orientacion hacia donde ira el proyectil
        
    """
    Metodo que define la trayectoria del proyectil
    """    
    def trayectoria(self):
        if self.orientacion == 'N':
            self.rect.top = self.rect.top - self.velocidadDisparo
        elif self.orientacion == 'S':
            self.rect.bottom = self.rect.bottom + self.velocidadDisparo
        elif self.orientacion == 'E':
            self.rect.left = self.rect.left + self.velocidadDisparo
        elif self.orientacion == 'O':
            self.rect.right = self.rect.right - self.velocidadDisparo
        
    
    """
    Metodo que dibuja el proyectil
    """
    def dibujar(self,superficie):
        superficie.blit(self.imageProyectil, self.rect)