
class Calentador:
    def __init__(self, material, forma, capacidad, proposito, fluido, tiempo_deseado, tension, resistencia, temp_inicial, temp_ambiente):
        self.material = material
        self.forma = forma
        self.capacidad = capacidad
        self.proposito = proposito
        self.fluido = fluido
        self.tiempo_deseado = tiempo_deseado
        self.tension = tension
        self.resistencia = resistencia
        self.temp_inicial = temp_inicial
        self.temp_ambiente = temp_ambiente
        self.cp = self.get_specific_heat_capacity(fluido)  # Calor específico del fluido en J/(kg·K)

    def get_specific_heat_capacity(self, fluido):
        # Calor específico en J/(kg·K)
        capacidades = {
            'agua': 4181,
            'aceite': 1970,
            'miel': 1420,
            'alcohol': 2440
        }
        return capacidades.get(fluido.lower(), 4181)  # Valor por defecto: agua

    def potencia(self):
        # Potencia eléctrica P = V^2 / R
        return (self.tension ** 2) / self.resistencia

    def calor_generado(self, tiempo):
        # Calor Q = P * t
        return self.potencia() * tiempo

    def aumento_temperatura(self, tiempo):
        # Aumento de temperatura ΔT = Q / (m * cp)
        masa = self.capacidad / 1000  # Convertir capacidad de cc a kg (suponiendo densidad de agua = 1 g/cc)
        Q = self.calor_generado(tiempo)
        return Q / (masa * self.cp)

# Ejemplo de uso
calentador = Calentador(
    material='espuma de poliestireno',
    forma='cilíndrica',
    capacidad=1000,  # en cc
    proposito='agua para el té',
    fluido='agua',
    tiempo_deseado=300,  # en segundos
    tension=220,  # en volts
    resistencia=50,  # en ohms
    temp_inicial=25,  # en grados Celsius
    temp_ambiente=20  # en grados Celsius
)

# Aumento de temperatura del fluido luego de 1 segundo
# aumento_temp_1s = calentador.aumento_temperatura(1)
# print(f'Aumento de temperatura del fluido luego de 1 segundo: {aumento_temp_1s:.2f} °C')
for seconds in range(1, 31):
    aumento_temp = calentador.aumento_temperatura(seconds)
    print(f'Aumento de temperatura del fluido luego de {seconds} segundos: {aumento_temp:.2f} °C')
