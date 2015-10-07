import pygame

class EntradaEnemigo(pygame.sprite.Sprite):
    """Clase para controlar los muros que hay distribuidos por el mapa"""
    
    """
    Constructor de la clase
    """
    def __init__(self,posx,posy,tam):
        pygame.sprite.Sprite.__init__(self)
            
        self.rect = pygame.Rect(posx,posy,tam,tam)