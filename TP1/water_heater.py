import math

# Función para calcular la resistencia eléctrica
def calcular_resistencia(tension, potencia):
    return (tension ** 2) / potencia

# Función para calcular el aumento de temperatura del fluido después de 1 segundo
def aumento_temperatura(fluido, potencia, resistencia, tiempo):
    # Constante específica del fluido (agua: 4.18 J/g°C)
    constante_especifica = 4.18
    
    # Masa del fluido en gramos (considerando 1 mL = 1 g)
    masa = volumen * densidades[fluido]
    
    # Calor generado en 1 segundo (Q = V^2 / R * t)
    calor_generado = (potencia ** 2) / resistencia * tiempo
    
    # Aumento de temperatura (ΔT = Q / (m * c))
    aumento_temp = calor_generado / (masa * constante_especifica)
    
    return aumento_temp

# Parámetros del calentador
material_aislante = "fibra de vidrio"
forma_recipiente = "cúbica"
volumen = 1000 # en cc
proposito = "calentar"
fluido = "agua"
tiempo = 100 # en segundos
tension_alimentacion = 220 # en Volts
potencia = 1000 # en Watts
temperatura_inicial_fluido = 20 # en °C
temperatura_ambiente = 25 # en °C

# Densidades de algunos fluidos en g/mL
densidades = {"agua": 1, "aceite": 0.92, "miel": 1.42, "alcohol": 0.79}

# Calcular resistencia eléctrica
resistencia = calcular_resistencia(tension_alimentacion, potencia)

# Calcular aumento de temperatura después de 1 segundo
aumento_temp_1s = aumento_temperatura(fluido, potencia, resistencia, 1)

# Resultados
print("Material aislante:", material_aislante)
print("Forma del recipiente:", forma_recipiente)
print("Volumen del recipiente:", volumen, "cc")
print("Propósito del calentador:", proposito)
print("Fluido a calentar:", fluido)
print("Tiempo deseado para alcanzar la temperatura:", tiempo, "segundos")
print("Tensión de alimentación:", tension_alimentacion, "Volts")
print("Valor de Resistencia Eléctrica empleado:", resistencia, "Ohms")
print("Temperatura inicial del fluido:", temperatura_inicial_fluido, "°C")
print("Temperatura ambiente al iniciar el proceso:", temperatura_ambiente, "°C")
print("Aumento de temperatura del fluido después de 1 segundo:", aumento_temp_1s, "°C")
