import random
tamano = 4
movimientos_maximos = 6
filas_visibles = 6
tamano_poblacion = 10
tasa_mutacion = 0.20
retardo = 200

def generar_individuo():
    return [random.randint(0, tamano - 1) for _ in range(movimientos_maximos)]

def aptitud(individuo, casillas):
    puntuacion = 0
    for movimiento, casilla in zip(individuo, casillas):
        if movimiento == casilla:
            puntuacion += 1
        else:
            break
    return puntuacion

def seleccion_torneo(poblacion, casillas, k=3):
    seleccionados = random.sample(poblacion, k)
    seleccionados.sort(key=lambda ind: aptitud(ind, casillas), reverse=True)
    return seleccionados[0]

def cruce(padre1, padre2):
    punto = random.randint(1, len(padre1) - 1)
    return padre1[:punto] + padre2[punto:]

def mutar(individuo):
    return [
        movimiento if random.random() > tasa_mutacion else random.randint(0, tamano - 1)
        for movimiento in individuo
    ]
def evolucionar_poblacion(poblacion, casillas):
    poblacion.sort(key=lambda ind: aptitud(ind, casillas), reverse=True)
    elites = poblacion[:2]
    nueva_poblacion = elites.copy()

    while len(nueva_poblacion) < tamano_poblacion:
        padre1 = seleccion_torneo(poblacion, casillas)
        padre2 = seleccion_torneo(poblacion, casillas)
        hijo = mutar(cruce(padre1, padre2))
        nueva_poblacion.append(hijo)
        return nueva_poblacion
    
    