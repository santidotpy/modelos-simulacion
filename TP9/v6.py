import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de parámetros
WIDTH, HEIGHT = 750, 750
PARTICLE_SIZE = 5
CENTER = WIDTH // 2, HEIGHT // 2
TOLERANCE = 5

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
                return True, particle
        if (self.x <= 0 or self.x >= WIDTH - PARTICLE_SIZE or
            self.y <= 0 or self.y >= HEIGHT - PARTICLE_SIZE):
            return True, None
        return False, None

# Lista para las partículas adheridas
adhered_particles = []

# Función principal
def main():
    running = True
    clock = pygame.time.Clock()
    particles = []

    while running:
        screen.fill(BLACK)

        # Generar nuevas partículas en el centro a intervalos regulares
        if len(particles) < 500:  # Limitar el número de partículas activas para evitar sobrecarga
            new_particle = Particle(CENTER[0], CENTER[1])
            particles.append(new_particle)

        # Mover y chequear adherencia de cada partícula
        for particle in particles[:]:
            particle.move()

            adhered, collided_particle = particle.check_adherence(adhered_particles)
            if adhered:
                if collided_particle:
                    # Mover la partícula para que se adhiera al lado de la partícula colisionada
                    if particle.rect.x < collided_particle.rect.x:
                        particle.rect.x = collided_particle.rect.x - PARTICLE_SIZE
                    elif particle.rect.x > collided_particle.rect.x:
                        particle.rect.x = collided_particle.rect.x + PARTICLE_SIZE
                    elif particle.rect.y < collided_particle.rect.y:
                        particle.rect.y = collided_particle.rect.y - PARTICLE_SIZE
                    elif particle.rect.y > collided_particle.rect.y:
                        particle.rect.y = collided_particle.rect.y + PARTICLE_SIZE

                    particle.x, particle.y = particle.rect.topleft

                adhered_particles.append(particle)
                particles.remove(particle)

            # Dibujar la partícula en movimiento
            pygame.draw.rect(screen, WHITE, particle.rect)

        # Dibujar todas las partículas adheridas
        for particle in adhered_particles:
            pygame.draw.rect(screen, WHITE, particle.rect)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(30)

        # Chequear si el ducto está completamente lleno
        if len(adhered_particles) >= (WIDTH // PARTICLE_SIZE) * (HEIGHT // PARTICLE_SIZE):
            running = False

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

    pygame.quit()

if __name__ == "__main__":
    main()
