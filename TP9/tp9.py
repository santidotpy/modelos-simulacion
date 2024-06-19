import pygame
import sys
import numpy as np
import random
from typing import Dict, List

# Initialize Pygame
pygame.init()

TUBE_FORM = ["rectangular", "circular", "squared"]
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 0, 0)  # Black
PARTICLE_COLOR = (255, 255, 255)  # White
TUBE_COLOR = (255, 121, 0)  # Orange
TUBE_TYPE = random.choice(TUBE_FORM)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particles in Tube")

# Define fonts
font = pygame.font.Font(None, 36)

# FPS (Frames Per Second) settings
FPS = 60
clock = pygame.time.Clock()

# in pixels
tube_diameter = 400
particle_size = 10
max_particles = 700  # Max number of particles to generate

# particles start at the center of the tube)
tube_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# store particle positions
particles: List[Dict[str, float]] = []

# Probability function for adherence based on distance
def probability_of_adherence(distance: float) -> float:
    return min(1.0, 1 / (1 + np.exp(distance)))

def particle_generation() -> Dict[str, float]:
    return {"x": tube_center[0], "y": tube_center[1], "moving": True}

def is_within_bounds(particle: Dict[str, float]) -> bool:
    if TUBE_TYPE == "rectangular":
        return (
            SCREEN_WIDTH // 2 - tube_diameter * 1.5 // 2 < particle["x"] - particle_size // 2 < SCREEN_WIDTH // 2 + tube_diameter * 1.5 // 2 and
            SCREEN_HEIGHT // 2 - tube_diameter // 2 < particle["y"] - particle_size // 2 < SCREEN_HEIGHT // 2 + tube_diameter // 2
        )
    elif TUBE_TYPE == "circular":
        distance_from_center = np.sqrt((particle["x"] - tube_center[0]) ** 2 + (particle["y"] - tube_center[1]) ** 2)
        return distance_from_center < (tube_diameter // 2 - particle_size // 2)
    elif TUBE_TYPE == "squared":
        return (
            SCREEN_WIDTH // 2 - tube_diameter // 2 < particle["x"] - particle_size // 2 < SCREEN_WIDTH // 2 + tube_diameter // 2 and
            SCREEN_HEIGHT // 2 - tube_diameter // 2 < particle["y"] - particle_size // 2 < SCREEN_HEIGHT // 2 + tube_diameter // 2
        )
    return False

def move_particles():
    for particle in particles:
        if particle["moving"]:
            direction = random.choice(["up", "down", "left", "right"])
            original_x, original_y = particle["x"], particle["y"]
            
            if direction == "up":
                particle["y"] -= 2
            elif direction == "down":
                particle["y"] += 2
            elif direction == "left":
                particle["x"] -= 2
            elif direction == "right":
                particle["x"] += 2

            if not is_within_bounds(particle):
                particle["x"], particle["y"] = original_x, original_y

            # Check if particle is close to the wall
            distance_to_wall = calculate_distance_to_wall(particle)

            if random.random() < probability_of_adherence(distance_to_wall):
                particle["moving"] = False

            # Check if particle is close to other particles that are adhered to the wall
            for other_particle in particles:
                if not other_particle["moving"]:
                    distance_to_other = np.sqrt(
                        (particle["x"] - other_particle["x"]) ** 2 +
                        (particle["y"] - other_particle["y"]) ** 2
                    ) - particle_size
                    if distance_to_other <= 0 and random.random() < probability_of_adherence(distance_to_other):
                        particle["moving"] = False
                        break

def calculate_distance_to_wall(particle: Dict[str, float]) -> float:
    if TUBE_TYPE == "rectangular":
        return min(
            abs(particle["x"] - particle_size // 2 - (SCREEN_WIDTH // 2 - tube_diameter * 1.5 // 2)),
            abs(particle["x"] + particle_size // 2 - (SCREEN_WIDTH // 2 + tube_diameter * 1.5 // 2)),
            abs(particle["y"] - particle_size // 2 - (SCREEN_HEIGHT // 2 - tube_diameter // 2)),
            abs(particle["y"] + particle_size // 2 - (SCREEN_HEIGHT // 2 + tube_diameter // 2))
        )
    elif TUBE_TYPE == "squared":
        return min(
            abs(particle["x"] - particle_size // 2 - (SCREEN_WIDTH // 2 - tube_diameter // 2)),
            abs(particle["x"] + particle_size // 2 - (SCREEN_WIDTH // 2 + tube_diameter // 2)),
            abs(particle["y"] - particle_size // 2 - (SCREEN_HEIGHT // 2 - tube_diameter // 2)),
            abs(particle["y"] + particle_size // 2 - (SCREEN_HEIGHT // 2 + tube_diameter // 2))
        )
    elif TUBE_TYPE == "circular":
        return tube_diameter // 2 - particle_size // 2 - np.sqrt(
            (particle["x"] - tube_center[0]) ** 2 +
            (particle["y"] - tube_center[1]) ** 2
        )
    return 0

def draw_simulation(elapsed_time: float):
    screen.fill(BACKGROUND_COLOR)
    
    # tube
    if TUBE_TYPE == "rectangular":
        pygame.draw.rect(screen, TUBE_COLOR, [
            SCREEN_WIDTH // 2 - tube_diameter * 1.5 // 2,
            SCREEN_HEIGHT // 2 - tube_diameter // 2,
            tube_diameter * 1.5,
            tube_diameter
        ], 2)
    elif TUBE_TYPE == "circular":
        pygame.draw.circle(screen, TUBE_COLOR, tube_center, tube_diameter // 2, 2)
    elif TUBE_TYPE == "squared":
        pygame.draw.rect(screen, TUBE_COLOR, [
            SCREEN_WIDTH // 2 - tube_diameter // 2,
            SCREEN_HEIGHT // 2 - tube_diameter // 2,
            tube_diameter,
            tube_diameter
        ], 2)
    
    # particles
    for particle in particles:
        pygame.draw.rect(screen, PARTICLE_COLOR, [
            particle["x"] - particle_size // 2,
            particle["y"] - particle_size // 2,
            particle_size,
            particle_size
        ])
    
    # display statistics
    moving_particles = len([particle for particle in particles if particle["moving"]])
    adhered_particles = len([particle for particle in particles if not particle["moving"]])
    text = font.render(
        f"Particulas en Movimiento: {moving_particles}, Adheridas: {adhered_particles}, Tiempo: {elapsed_time:.2f}s",
        True,
        PARTICLE_COLOR
    )
    
    # Text position
    text_rect = text.get_rect()
    text_rect.topleft = (10, SCREEN_HEIGHT - text_rect.height - 10)
    screen.blit(text, text_rect)
    
    pygame.display.flip()


def main():
    global particles
    running = True
    frame_count = 0
    
    while running:       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if len(particles) < max_particles:
            particles.append(particle_generation())
        
        move_particles()
        elapsed_time = frame_count / FPS
        draw_simulation(elapsed_time)
        
        frame_count += 1

        clock.tick(FPS)

        if all(not particle["moving"] for particle in particles):
            running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
