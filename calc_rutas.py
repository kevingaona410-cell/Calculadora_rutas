import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# ==================== Ventana principal ====================
root = tk.Tk()
root.title("Calculadora de Rutas")
root.geometry("500x500")
root.configure(bg="#DBDBDB")

# ==================== Constantes de terreno ====================
CAMINO = 0
EDIFICIO = 1
AGUA = 2
BLOQUEADO = 3

posibles_terrenos = [CAMINO, EDIFICIO, AGUA, BLOQUEADO]

COLORES = {
    CAMINO: "#FFFFFF",
    EDIFICIO: "#424242",
    AGUA: "#2196f3",
    BLOQUEADO: "#b71c1c"
}

# ==================== Estilos ====================
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))

# ==================== Variables ====================
filas_var = tk.IntVar()
columnas_var = tk.IntVar()
terreno = []

# ==================== CONTENEDOR SUPERIOR ====================
frame_controles = tk.Frame(
    root,
    bg="#B0B0B0",
    padx=10,
    pady=10
)
frame_controles.pack(fill="x", padx=10, pady=10)

tk.Label(
    frame_controles,
    text="Filas:",
    bg="#DBDBDB",
    fg="black"
).grid(row=0, column=0, padx=5)

ttk.Entry(
    frame_controles,
    textvariable=filas_var,
    width=5,
    justify="center"
).grid(row=0, column=1, padx=5)

tk.Label(
    frame_controles,
    text="Columnas:",
    bg="#DBDBDB",
    fg="black"
).grid(row=0, column=2, padx=5)

ttk.Entry(
    frame_controles,
    textvariable=columnas_var,
    width=5,
    justify="center"
).grid(row=0, column=3, padx=5)

# ==================== CONTENEDOR DEL MAPA ====================
frame_mapa = tk.Frame(
    root,
    bg="#EDEDED",
    padx=10,
    pady=10
)
frame_mapa.pack(padx=10, pady=10)

# ==================== Funciones ====================
def generar_mundo():
    global terreno

    filas = filas_var.get()
    columnas = columnas_var.get()

    if filas <= 0 or columnas <= 0:
        messagebox.showerror(
            "Error",
            "Filas y columnas deben ser mayores que 0"
        )
        return

    terreno = [
        [random.choice(posibles_terrenos) for _ in range(columnas)]
        for _ in range(filas)
    ]

    dibujar_mundo()

def dibujar_mundo():
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    for i, fila in enumerate(terreno):
        for j, valor in enumerate(fila):
            lbl = tk.Label(
                frame_mapa,
                bg=COLORES.get(valor, "#000000"),
                width=4,
                height=2,
                relief="ridge",
                borderwidth=1
            )
            lbl.grid(row=i, column=j, padx=2, pady=2)

# ==================== Botón ====================
ttk.Button(
    frame_controles,
    text="Generar Mundo",
    command=generar_mundo
).grid(row=0, column=4, padx=10)

# ==================== Main loop ====================
root.mainloop()
