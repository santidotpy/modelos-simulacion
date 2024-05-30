import math


cct = 0.032  # Coeficiente de Conductividad Térmica en W/mK
espesor = 0.001  # Espesor en metros (1 mm)
diametro = 0.1 # en metros
altura = 0.15 # en metros

def get_superficie_total():
    # superficie total en m²
    return 2 * math.pi * (diametro / 2) * (altura + diametro / 2)
    
def perdida():
    perdida=cct*get_superficie_total()/espesor
    return perdida

if __name__ == "__main__":
    print(f'Perdida de calor: {perdida()} W/°K')