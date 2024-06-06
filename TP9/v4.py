import pygame
import random
import sys
import math

# Inicialización de Pygame
pygame.init()

# Configuración de parámetros
WIDTH, HEIGHT = 750, 750
PARTICLE_SIZE = 5
CENTER = WIDTH // 2, HEIGHT // 2
TOLERANCE = 5
STOP_RADIUS = 350  # Distancia desde el centro en la que se detendrá la simulación

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modelos Estocásticos de Crecimiento por Agregación en Confinamiento")

# Clase para las partículas
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, PARTICLE_SIZE, PARTICLE_SIZE)

    def move(self):
        directions = [(PARTICLE_SIZE, 0), (-PARTICLE_SIZE, 0), (0, PARTICLE_SIZE), (0, -PARTICLE_SIZE)]
        dx, dy = random.choice(directions)
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

    def check_adherence(self, particles):
        for particle in particles:
            if self.rect.colliderect(particle.rect):
                return True
        if (self.x <= 0 or self.x >= WIDTH - PARTICLE_SIZE or
            self.y <= 0 or self.y >= HEIGHT - PARTICLE_SIZE):
            return True
        return False

# Lista para las partículas adheridas
adhered_particles = []

# Función principal
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)

        # Generar una nueva partícula en el centro
        new_particle = Particle(CENTER[0], CENTER[1])

        while True:
            new_particle.move()

            # Dibujar la partícula en movimiento
            pygame.draw.rect(screen, WHITE, new_particle.rect)

            # Chequear adherencia
            if new_particle.check_adherence(adhered_particles):
                adhered_particles.append(new_particle)
                break

            # Actualizar la pantalla
            pygame.display.flip()
            clock.tick(30)

            # Chequear si se ha alcanzado el radio de detención
            distance_from_center = math.sqrt((new_particle.x - CENTER[0]) ** 2 + (new_particle.y - CENTER[1]) ** 2)
            if distance_from_center >= STOP_RADIUS:
                running = False
                break

        # Dibujar todas las partículas adheridas
        for particle in adhered_particles:
            pygame.draw.rect(screen, WHITE, particle.rect)

        # Actualizar la pantalla
        pygame.display.flip()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

    pygame.quit()

if __name__ == "__main__":
    main()
