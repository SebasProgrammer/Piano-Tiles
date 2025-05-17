import tkinter as tk
import random
tamanio = 4
movimientos = 6
fichas = [random.randint(0, tamanio - 1) for _ in range(movimientos)]

def empezar_juego():
    print('iniciando')

def hacer_canvas(canvas, fichas):
    ancho_celda = 100
    alto_celda = 150
    filas_visibles = 6

    for i in range(filas_visibles):
        for j in range(tamanio):
            x1 = j * ancho_celda
            y1 = i * alto_celda
            x2 = x1 + ancho_celda
            y2 = y1 + alto_celda
            if j == fichas[i]:
                color = 'black'
            else:
                color = 'white'
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')
def main():
    ventana = tk.Tk()
    ventana.title('piano tiles')

    canvas = tk.Canvas(ventana, width=tamanio * 100, height=6 * 150, bg='white')
    canvas.pack()

    hacer_canvas(canvas, fichas)

    boton_inicio = tk.Button(ventana, text='empezar', command=empezar_juego)
    boton_inicio.pack(pady=10)

    etiqueta_info = tk.Label(ventana, text='puntuacion: 0')
    etiqueta_info.pack()

    ventana.mainloop()

if __name__ == '__main__':
    main()
