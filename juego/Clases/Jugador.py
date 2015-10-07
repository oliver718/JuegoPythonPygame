"""
@author: oliver
"""
import pygame
import Proyectil
import Muro

class Jugador(pygame.sprite.Sprite):
    """Clase controlar el vehiculo del jugador y sus acciones"""
    
    """
    Constructor de la clase
    """
    def __init__(self, ancho, alto,iniXjugador,iniYjugador):
        pygame.sprite.Sprite.__init__(self)
        
        self.resistencia = 3
        self.ImagenVehiculo = self.__cargarVehiculo(0)  #cargar imagen del vehiculo
        self.ImagenExplosion = pygame.transform.rotate(pygame.image.load('Imagenes/explosionTank.png'),0)
        self.orientacion = 'N'
        self.rect = self.ImagenVehiculo.get_rect() #obtener un rectangulo del tamanio de la imagen
        self.rect.top = iniYjugador #indicar la posicion inicial en x donde aparecera
        self.rect.left = iniXjugador #indicar la posicion inicial en y donde aparecera
        self.listaDisparo = [] #almacenara los proyectiles lanzados (para poder ser destruidos y controlar las colisicones)
        self.vida = True #para controlar si el jugador a perdido o no
        self.velocidad = 3 #velocidad de movimiento del vehiculo del jugador
        self.anchoVentana = ancho
        self.altoVentana = alto
        self.refrescosExplosion = 15 #numero de veces que se refrescara la explosion del vehiculo cuando este sea tocado con un proyectil
        try:
            self.sonidoDisparo = pygame.mixer.Sound("Sonidos/disparoJugador.wav")
            self.sonidoExplosion = pygame.mixer.Sound("Sonidos/explosionTank.wav")
        except:
            print "No se ha cargado el sonido"
    
    
    """
    Metodo que devuelve la imagen del vehiculo cargada con unos grados de rotacion
    """
    def __cargarVehiculo(self,grados):
        
        self.gradosMov = grados #guardar la orientacion del vehiculo en cada momento
        if self.resistencia == 3:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankNegro.png'),grados)
        elif self.resistencia == 2:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankNegroGolpe1.png'),grados)  #cargar imagen del vehiculo
        else:
            return pygame.transform.rotate(pygame.image.load('Imagenes/tankNegroGolpe2.png'),grados)    
    
    
    def muerto(self):
        return self.resistencia <= 0
    
    def restarVida(self):
        self.resistencia -= 1 
        if self.resistencia > 0:
            self.ImagenVehiculo = self.__cargarVehiculo(self.gradosMov)
            return True
        else:
            return False

    """
    Metodo que ejecutara el disparo del jugador
    """  
    def disparar(self,x,y):
        if len(self.listaDisparo) < 2: #solo puede haber 2 proyectiles activos por cada vehiculo
            self.sonidoDisparo.play()
            miProyectil = Proyectil.Proyectil(x,y,self.orientacion)
            self.listaDisparo.append(miProyectil)
    
    """
    Metodo para dibujar el vehiculo del jugador
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

    """
    Metodo que realiza el movimento del vehiculo hacia la derecha
    orientando (hacia el este) el vehiculo
    """
    def movimientoDerecha(self,listaObstaculos):
        if self.orientacion != 'E':
            self.ImagenVehiculo = self.__cargarVehiculo(270)          
            self.orientacion = 'E'
        self.rect.right += self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if self.rect.colliderect(muro.rect):
                if self.rect.right > muro.rect.left:
                    self.rect.right = muro.rect.left
    
    """
    Metodo que realiza el movimento del vehiculo hacia la izquierda
    orientando (hacia el oeste) el vehiculo 
    """
    def movimientoIzquierda(self,listaObstaculos):
        if self.orientacion != 'O':
    		self.ImagenVehiculo = self.__cargarVehiculo(90)
        	self.orientacion = 'O'
        self.rect.left -= self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if self.rect.colliderect(muro.rect):
                if self.rect.left < muro.rect.right:
                    self.rect.left = muro.rect.right
        
    """
    Metodo que realiza el movimento del vehiculo hacia arriba
    orientando (hacia el norte) el vehiculo 
    """  
    def movimientoArriba(self,listaObstaculos):
        if self.orientacion != 'N':
    		self.ImagenVehiculo = self.__cargarVehiculo(0)
        	self.orientacion = 'N'
        self.rect.top -= self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if self.rect.colliderect(muro.rect):
                if self.rect.top < muro.rect.bottom:
                    self.rect.top = muro.rect.bottom
        
    """
    Metodo que realiza el movimento del vehiculo hacia abajo
    orientando (hacia el sur) el vehiculo 
    """  
    def movimientoAbajo(self,listaObstaculos):
        if self.orientacion != 'S':
    		self.ImagenVehiculo = self.__cargarVehiculo(180)
        	self.orientacion = 'S'
        self.rect.bottom += self.velocidad
        self.__movimiento()
        for muro in listaObstaculos:
            if self.rect.colliderect(muro.rect):
                if self.rect.bottom > muro.rect.top:
                    self.rect.bottom = muro.rect.top
    
    
    """
    Metodo privado que limita el movimiento del vehiculo para que 
    no se salga de la pantalla
    """
    def __movimiento(self):
        if self.vida == True:
            if self.rect.left < 0:
                self.rect.left = 0
            elif self.rect.right > self.anchoVentana:
                self.rect.right = self.anchoVentana
            elif self.rect.top < 0:
                self.rect.top = 0
            elif self.rect.bottom > self.altoVentana:
                self.rect.bottom = self.altoVentana
                        
                
