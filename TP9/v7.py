import pygame
import random
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de parámetros
WIDTH, HEIGHT = 750, 750
PARTICLE_SIZE = 5
CENTER = WIDTH // 2, HEIGHT // 2

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
        if len(particles) < 700:  # Limitar el número de partículas activas para evitar sobrecarga
            new_particle = Particle(CENTER[0], CENTER[1])
            particles.append(new_particle)

        # Mover y chequear adherencia de cada partícula
        for particle in particles[:]:
            particle.move()

            adhered, collided_particle = particle.check_adherence(adhered_particles)
            if adhered:
                if collided_particle:
                    # Encontrar una posición válida adyacente a la partícula colisionada
                    for dx, dy in [(PARTICLE_SIZE, 0), (-PARTICLE_SIZE, 0), (0, PARTICLE_SIZE), (0, -PARTICLE_SIZE)]:
                        new_rect = particle.rect.move(dx, dy)
                        if not any(new_rect.colliderect(p.rect) for p in adhered_particles) and \
                           0 <= new_rect.x < WIDTH and 0 <= new_rect.y < HEIGHT:
                            particle.rect = new_rect
                            particle.x, particle.y = particle.rect.topleft
                            break
                else:
                    # Asegurar que la partícula se quede dentro de los límites
                    if particle.x < 0:
                        particle.x = 0
                    elif particle.x > WIDTH - PARTICLE_SIZE:
                        particle.x = WIDTH - PARTICLE_SIZE
                    if particle.y < 0:
                        particle.y = 0
                    elif particle.y > HEIGHT - PARTICLE_SIZE:
                        particle.y = HEIGHT - PARTICLE_SIZE

                    particle.rect.topleft = (particle.x, particle.y)

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
