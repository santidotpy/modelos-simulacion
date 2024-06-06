import pygame
import random
import math

# Configuración inicial
pygame.init()

# Función para obtener los parámetros del conducto y las partículas
def obtener_parametros():
    forma = input("Ingrese la forma del conducto (circular/cuadrado/rectangular): ").strip().lower()
    while forma not in ["circular", "cuadrado", "rectangular"]:
        forma = input("Forma no válida. Ingrese circular, cuadrado o rectangular: ").strip().lower()
    
    if forma == "circular":
        diametro = int(input("Ingrese el diámetro del conducto (1-1000 mm): "))
        ancho, alto = diametro, diametro
    else:
        ancho = int(input("Ingrese el ancho del conducto (1-1000 mm): "))
        alto = int(input("Ingrese el alto del conducto (1-1000 mm): "))

    lado_particula = int(input("Ingrese el tamaño de las partículas (1-10 mm): "))

    limite_distancia = int(input("Ingrese la distancia máxima de crecimiento desde el centro (mm): "))

    return forma, ancho, alto, lado_particula, limite_distancia

# Parámetros del conducto y partículas
forma_conducto, ancho_conducto, alto_conducto, lado_particula, limite_distancia = obtener_parametros()

# Configuración de la ventana
ventana = pygame.display.set_mode((ancho_conducto, alto_conducto))
pygame.display.set_caption("Simulación de Depósito de Partículas")

# Clase para las partículas
class Particula:
    def __init__(self, x, y, lado):
        self.rect = pygame.Rect(x, y, lado, lado)
        self.lado = lado

    def mover(self):
        direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if direccion == 'arriba':
            self.rect.y -= self.lado
        elif direccion == 'abajo':
            self.rect.y += self.lado
        elif direccion == 'izquierda':
            self.rect.x -= self.lado
        elif direccion == 'derecha':
            self.rect.x += self.lado

    def colisiona_con(self, otro):
        return self.rect.colliderect(otro.rect)

    def colisiona_con_pared(self, ancho, alto):
        if forma_conducto == 'circular':
            cx, cy = ancho // 2, alto // 2
            radio = ancho // 2
            dist = math.sqrt((self.rect.centerx - cx) ** 2 + (self.rect.centery - cy) ** 2)
            return dist + self.lado // 2 >= radio
        else:
            return (self.rect.left <= 0 or self.rect.right >= ancho or
                    self.rect.top <= 0 or self.rect.bottom >= alto)

# Inicializar la primera partícula en el centro del conducto
centro_x, centro_y = ancho_conducto // 2, alto_conducto // 2
particulas = [Particula(centro_x, centro_y, lado_particula)]
crecimiento_alcanzado = False

# Bucle principal de la simulación
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    if not crecimiento_alcanzado:
        nueva_particula = Particula(centro_x, centro_y, lado_particula)
        while True:
            nueva_particula.mover()
            colision = False
            for p in particulas:
                if nueva_particula.colisiona_con(p) or nueva_particula.colisiona_con_pared(ancho_conducto, alto_conducto):
                    colision = True
                    break
            if colision:
                particulas.append(nueva_particula)
                break

        distancia_desde_centro = math.sqrt((nueva_particula.rect.centerx - centro_x) ** 2 + (nueva_particula.rect.centery - centro_y) ** 2)
        if distancia_desde_centro >= limite_distancia:
            crecimiento_alcanzado = True

    # Mover las partículas existentes
    for particula in particulas:
        particula.mover()
        if particula.colisiona_con_pared(ancho_conducto, alto_conducto):
            particula.mover()  # Mover en dirección contraria si colisiona con la pared

    ventana.fill((255, 255, 255))
    for p in particulas:
        pygame.draw.rect(ventana, (0, 0, 0), p.rect)
    
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
