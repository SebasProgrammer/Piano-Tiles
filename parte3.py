import tkinter as tk
from tkinter import ttk
import random
import json
import os
import tkinter.font as tkfont

tamano = 4
movimientos_maximos = 6
filas_visibles = 6
tamano_poblacion = 10
tasa_mutacion = 0.20
retardo = 200
archivo = "progreso_guardado.json"

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

def guardar_progreso(casillas, poblacion, generacion):
    poblacion.sort(key=lambda ind: aptitud(ind, casillas), reverse=True)
    with open(archivo, "w") as f:
        json.dump({
            "casillas": casillas,
            "poblacion": poblacion,
            "generacion": generacion
        }, f)

def cargar_progreso():
    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            datos = json.load(f)
            return datos["casillas"], datos["poblacion"], datos["generacion"]
    return None

class juego_piano_tiles:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("piano tiles - algoritmos genéticos")
        self.inicializar_juego()

    def inicializar_juego(self):
        progreso = cargar_progreso()
        if progreso:
            self.casillas, self.poblacion, self.generacion = progreso
        else:
            self.casillas = [random.randint(0, tamano - 1) for _ in range(movimientos_maximos)]
            self.poblacion = [generar_individuo() for _ in range(tamano_poblacion)]
            self.generacion = 1
        self.individuo_actual = None
        self.movimiento_actual = 0
        self.puntuacion = 0
        self.indice_error = None
        self.en_ejecucion = True
        self.crear_interfaz()

    def crear_interfaz(self):
        for widget in self.raiz.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.raiz, width=tamano * 100, height=filas_visibles * 160, bg="#0d0d0d", highlightthickness=0)
        self.canvas.pack()

        self.etiqueta_info = tk.Label(
            self.raiz,
            text=f"gen: {self.generacion} | puntos: {self.puntuacion}",
            font=("helvetica", 16),
            fg="cyan",
            bg="#0d0d0d"
        )
        self.etiqueta_info.pack()

        self.boton_jugar = tk.Button(
            self.raiz,
            text="Jugar",
            command=self.iniciar_juego,
            font=("helvetica", 14),
            bg="cyan",
            fg="black"
        )
        self.boton_jugar.pack()

        self.actualizar_canvas()

    def iniciar_juego(self):
        self.boton_jugar.config(state=tk.DISABLED)
        self.individuo_actual = self.poblacion[0]
        self.movimiento_actual = 0
        self.puntuacion = 0
        self.indice_error = None
        self.en_ejecucion = True
        self.etiqueta_info.config(text=f"gen: {self.generacion} | puntos: {self.puntuacion}")
        self.canvas.yview_moveto(0)
        self.actualizar_canvas()
        self.raiz.after(retardo, self.jugar_movimiento)

    def jugar_movimiento(self):
        if not self.en_ejecucion or self.movimiento_actual >= movimientos_maximos:
            return

        movimiento = self.individuo_actual[self.movimiento_actual]
        correcto = self.casillas[self.movimiento_actual]

        if movimiento != correcto:
            self.indice_error = self.movimiento_actual
            self.en_ejecucion = False
            guardar_progreso(self.casillas, self.poblacion, self.generacion)
            self.actualizar_canvas()
            self.raiz.after(1500, self.reiniciar_generacion)
            return

        self.puntuacion += 1
        self.movimiento_actual += 1
        self.etiqueta_info.config(text=f"gen: {self.generacion} | puntos: {self.puntuacion}")
        self.actualizar_canvas()

        if self.movimiento_actual < movimientos_maximos:
            self.raiz.after(retardo, self.jugar_movimiento)
        else:
            self.poblacion = evolucionar_poblacion(self.poblacion, self.casillas)
            self.generacion += 1
            guardar_progreso(self.casillas, self.poblacion, self.generacion)
            self.raiz.after(1000, self.iniciar_juego)

    def actualizar_canvas(self):
        self.canvas.delete("all")
        ancho = 100
        alto = 160
        for i in range(movimientos_maximos):
            fila_invertida = movimientos_maximos - 1 - i
            for j in range(tamano):
                x0 = j * ancho
                y0 = fila_invertida * alto
                x1 = x0 + ancho
                y1 = y0 + alto
                correcto = self.casillas[i]
                color = "#000000" if j == correcto else "#64b3ef"
                if self.indice_error == i and self.individuo_actual[i] == j:
                    color = "red"
                elif self.movimiento_actual > 0 and i == self.movimiento_actual - 1 and self.individuo_actual[i] == j:
                    color = "green" if self.individuo_actual[i] == correcto else "blue"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)

    def reiniciar_generacion(self):
        self.poblacion = evolucionar_poblacion(self.poblacion, self.casillas)
        self.generacion += 1
        guardar_progreso(self.casillas, self.poblacion, self.generacion)
        self.iniciar_juego()

if __name__ == "__main__":
    raiz = tk.Tk()
    raiz.attributes('-fullscreen', True)
    raiz.configure(bg="#0d0d0d")
    juego = juego_piano_tiles(raiz)
    raiz.mainloop()
