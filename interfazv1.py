from tkinter import *
import tkinter as tk
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

device = 'COM5'
mySerial = serial.Serial(device, 9600)

temperaturas = []
eje_x = []
i = 0
parar = True  # Empieza parado
threadRecepcion = None

# Configurar la figura y el eje para la gráfica
fig, ax = plt.subplots(figsize=(6,4), dpi=100)
ax.set_xlim(0, 100)
ax.set_ylim(20, 40)
ax.set_title('Grafica dinamica Temperatura[ºC] - temps[s]:')

def recepcion():
    global i, parar, temperaturas, eje_x, mySerial
    i = 0
    while not parar:
        if mySerial.in_waiting > 0:
            line = mySerial.readline().decode('utf-8').rstrip()
            trozos = line.split(':')
            if len(trozos) > 1:
                temperatura = float(trozos[1])
                eje_x.append(i)
                temperaturas.append(temperatura)
                ax.cla()
                ax.plot(eje_x, temperaturas)
                ax.set_xlim(max(0, i-15), i+5)
                ax.set_ylim(20, 40)
                ax.set_title('Grafica dinamica Temperatura[ºC] - temps[s]:')
                canvas.draw()
                i = i+3

def InicioClick():
    global parar, threadRecepcion
    parar = False
    threadRecepcion = threading.Thread(target=recepcion)
    threadRecepcion.daemon = True
    threadRecepcion.start()

def PararClick():
    global parar
    parar = True
    mensaje = "Parar\n"
    print(mensaje)
    mySerial.write(mensaje.encode('utf-8'))

def ReanudarClick():
    global parar, threadRecepcion
    if threadRecepcion is None or not threadRecepcion.is_alive():
        parar = False
        threadRecepcion = threading.Thread(target=recepcion)
        threadRecepcion.daemon = True
        threadRecepcion.start()
    else:
        parar = False
    mensaje = "Reanudar\n"
    print(mensaje)
    mySerial.write(mensaje.encode('utf-8'))


window = Tk()
window.geometry("800x400")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=2)

tituloLabel = Label(window, text="Versión 1", font=("Courier", 20, "italic"))
tituloLabel.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky=N + S + E + W)

InicioButton = Button(window, text="Inicio", bg='green', fg="white", command=InicioClick)
InicioButton.grid(row=1, column=0, padx=1, pady=1, sticky=N + S + E + W)

PararButton = Button(window, text="Parar", bg='red', fg="white", command=PararClick)
PararButton.grid(row=1, column=1, padx=1, pady=1, sticky=N + S + E + W)

ReanudarButton = Button(window, text="Reanudar", bg='orange', fg="white", command=ReanudarClick)
ReanudarButton.grid(row=1, column=2, padx=1, pady=1, sticky=N + S + E + W)

graph_frame = tk.LabelFrame(window, text="Grafica temperatura en viu")
graph_frame.grid(row=0, column=3, rowspan=2, padx=1, pady=1, sticky=N+S+E+W)

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

window.mainloop()
