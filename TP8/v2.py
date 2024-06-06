import pygame
import random
import locale
import numpy as np

locale.setlocale(locale.LC_ALL, '')

# Pygame config
pygame.init()
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Simulación de Sistema de Atención al Público')
CLOCK = pygame.time.Clock()

# setup colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# parametros predefinidos
NUM_BOXES = random.randint(1, 10)
BOX_COST = 1000
CUSTOMER_LOSS_COST = 10000
OPEN_HOURS = 4
SECONDS_PER_HOUR = 3600
TOTAL_SECONDS = OPEN_HOURS * SECONDS_PER_HOUR
SERVICE_TIME_MEAN = 10 * 60
SERVICE_TIME_STD_DEV = 5 * 60

# Distribución de llegada de clientes
ARRIVAL_MEAN_HOUR = 10
ARRIVAL_STD_DEV_HOUR = 2
ARRIVAL_START_HOUR = 8
ARRIVAL_END_HOUR = 12
TOTAL_CUSTOMERS_EXPECTED = 100

# variables
customers = []
boxes = [None] * NUM_BOXES
waiting_queue = []
served_customers = 0
unserved_customers = 0
total_customers = 0
current_time = 0
service_times = []
waiting_times = []

def generate_service_time():
    """Genera un tiempo de servicio basado en una distribución normal."""
    return max(1, int(random.gauss(SERVICE_TIME_MEAN, SERVICE_TIME_STD_DEV)))

class Customer:
    """Clase que representa a un cliente."""
    def __init__(self, arrival_time):
        self.arrival_time = arrival_time
        self.service_start_time = None
        self.service_end_time = None

    def start_service(self, start_time):
        """Inicia el servicio para el cliente."""
        self.service_start_time = start_time
        self.service_end_time = start_time + generate_service_time()
        service_times.append(self.service_end_time - self.service_start_time)

    def is_being_served(self, current_time):
        """Verifica si el cliente está siendo atendido."""
        return self.service_start_time is not None and self.service_start_time <= current_time < self.service_end_time

    def is_served(self, current_time):
        """Verifica si el cliente ya fue atendido."""
        return self.service_end_time is not None and current_time >= self.service_end_time

def draw_simulation(screen, boxes, waiting_queue):
    """Dibuja el estado actual de la simulación en la pantalla."""
    screen.fill(BLACK)
    for i in range(NUM_BOXES):
        color = GREEN if boxes[i] is None else RED
        pygame.draw.rect(screen, color, (50 + i * 70, 50, 60, 60))
    for i, customer in enumerate(waiting_queue):
        pygame.draw.circle(screen, WHITE, (100, 150 + i * 30), 10)
    pygame.display.flip()

def generate_arrival_times(mean_hour, std_dev_hour, total_customers, start_hour, end_hour):
    """Genera tiempos de llegada para los clientes según una distribución normal truncada."""
    arrival_times = []
    while len(arrival_times) < total_customers:
        arrival_time = random.gauss(mean_hour, std_dev_hour) * SECONDS_PER_HOUR
        if start_hour * SECONDS_PER_HOUR <= arrival_time <= end_hour * SECONDS_PER_HOUR:
            arrival_times.append(int(arrival_time) - start_hour * SECONDS_PER_HOUR)
    arrival_times.sort()
    return arrival_times

def main():
    global current_time, served_customers, unserved_customers, total_customers

    arrival_times = generate_arrival_times(ARRIVAL_MEAN_HOUR, ARRIVAL_STD_DEV_HOUR, TOTAL_CUSTOMERS_EXPECTED, ARRIVAL_START_HOUR, ARRIVAL_END_HOUR)
    print(f"Tiempos de llegada generados: {arrival_times}")
    running = True
    while running and current_time <= TOTAL_SECONDS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Añadir clientes basados en los tiempos de llegada generados
        if arrival_times and current_time >= arrival_times[0]:
            customers.append(Customer(current_time))
            total_customers += 1
            arrival_times.pop(0)

        for i in range(NUM_BOXES):
            if boxes[i] is None and waiting_queue:
                customer = waiting_queue.pop(0)
                customer.start_service(current_time)
                boxes[i] = customer
                waiting_times.append(current_time - customer.arrival_time)

        for i in range(NUM_BOXES):
            if boxes[i] is not None and boxes[i].is_served(current_time):
                boxes[i] = None
                served_customers += 1

        for customer in customers[:]:
            if not customer.is_being_served(current_time):
                if current_time - customer.arrival_time >= 30 * 60:
                    unserved_customers += 1
                    customers.remove(customer)
                elif customer not in waiting_queue and customer.service_start_time is None:
                    waiting_queue.append(customer)

        draw_simulation(SCREEN, boxes, waiting_queue)
        CLOCK.tick(60)
        current_time += 1

    pygame.quit()
    calculate_statistics()

def calculate_statistics():
    """Calcula y muestra las estadísticas de la simulación."""
    if service_times:
        min_service_time = min(service_times)
        max_service_time = max(service_times)
    else:
        min_service_time = max_service_time = 0

    if waiting_times:
        min_waiting_time = min(waiting_times)
        max_waiting_time = max(waiting_times)
    else:
        min_waiting_time = max_waiting_time = 0

    total_cost = NUM_BOXES * BOX_COST + unserved_customers * CUSTOMER_LOSS_COST

    print(f'Total de clientes: {total_customers}')
    print(f'Clientes atendidos: {served_customers}')
    print(f'Clientes no atendidos: {unserved_customers}')
    print(f'Tiempo mínimo de atención en box: {min_service_time / 60:.2f} minutos')
    print(f'Tiempo máximo de atención en box: {max_service_time / 60:.2f} minutos')
    print(f'Tiempo mínimo de espera en salón: {min_waiting_time / 60:.2f} minutos')
    print(f'Tiempo máximo de espera en salón: {max_waiting_time / 60:.2f} minutos')
    print(f"Costo total de operación: {locale.currency(total_cost, grouping=True)}")

if __name__ == '__main__':
    main()
