import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import heapq 
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

INICIO = None
FIN = None

posibles_terrenos = [CAMINO, EDIFICIO, AGUA, BLOQUEADO]

COLORES = {
    CAMINO: "#FFFFFF",
    EDIFICIO: "#424242",
    AGUA: "#2196f3",
    BLOQUEADO: "#FF0000"
}

COSTOS = { 
    CAMINO: 1,
    AGUA: 4,
    BLOQUEADO:  float("inf"),
    EDIFICIO: float("inf")
}

SIMBOLOS = {
    CAMINO: ".",
    EDIFICIO: "X",
    AGUA: "~",
    BLOQUEADO: "#"
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
            if INICIO == (i,j):
                color = "#4cad50"  # verde
                texto = "S"
            elif FIN == (i,j):
                color = "#FFA6A6"  # rojo
                texto = "E"
            else:
                color = COLORES.get( valor, "#000000")
                texto = SIMBOLOS.get( valor, "#000000")


            lbl = tk.Label(
                frame_mapa,
                text= texto,
                bg=color,
                fg= "black",
                font=("Consolas", 12, "bold"),
                width=4,
                height=2,
                relief="ridge",
                borderwidth=1
            )
            lbl.grid(row=i, column=j)
            lbl.bind("<Button-1>", lambda e, x=i, y=j: seleccionar_celda(e, x, y))
            lbl.bind("<Button-3>", lambda e, x=i, y=j: bloquear_celda(x, y))


def ruta_existe():

    if not terreno:
        messagebox.showwarning("Error", "Primero genera el mundo")
        return
    
    if INICIO is None or FIN is None:
        messagebox.showwarning("Advertencia", "Selecciona inicio y fin primero")
        return
    
    camino = camino_corto(terreno, INICIO, FIN)
    mostrar_camino(camino)

def mostrar_camino(camino):
    dibujar_mundo()

    if camino is None: 
        messagebox.showwarning("Error", "No se encontro un camino 🥲")


    for i, j in camino [1:-1]:
        lbl = tk.Label(
                frame_mapa,
                text= "*",
                fg= "black",
                font=("Consolas", 12, "bold"),
                bg="#ffeb3b",
                width=4,
                height=2,
                relief="ridge",
                borderwidth=1
            )
        lbl.grid(row=i, column=j)
        lbl.bind("<Button-1>", lambda e, x=i, y=j: seleccionar_celda(e, x, y))

def seleccionar_celda(e,i,j):
    global INICIO, FIN

    # Si haces clic en una celda sin marcar
    if INICIO == None:  # Marcar como inicio
        INICIO = (i, j)
    elif FIN == None:  # Marcar como fin
        FIN = (i, j)
    # Si haces clic en una celda marcada, la deselecciona
    elif INICIO == (i, j):
        INICIO = None
    elif FIN == (i, j):
        FIN = None
    # Si ambas están marcadas, reemplaza el fin
    elif terreno[i][j] != CAMINO:
        messagebox.showwarning("Invalid", "Solo puedes seleccionar caminos libres")
        return
    else:
        FIN = (i, j)
    

    dibujar_mundo()

def bloquear_celda(x, y):
    global terreno

    if terreno[x][y] in (CAMINO, AGUA):
        terreno[x][y] = EDIFICIO
    elif terreno[x][y] in (BLOQUEADO, EDIFICIO):
        terreno[x][y] = CAMINO

    dibujar_mundo()



# =================== Calcular rutas =================== 
direcciones = [
    (-1, 0),    # arriba
    (1, 0),     # abajo
    (0, -1),    # izquierda
    (0, 1),     # derecha
    
]  
def manhattan(a,b):
    h = abs(a[0]-b[0]) + abs(a[1]-b[1])
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def movimiento_valido( x, y, filas, columnas):
    if x < 0 or x >= filas:
        return False
    if y < 0 or y >= columnas: 
        return False 
    else:
        return True

# con A*    
def camino_corto(terreno, INICIO, FIN):
    if INICIO is None or FIN is None:
        messagebox.showwarning(
            "Advertencia",
            "Debe seleccionar un punto de inicio y fin"
        )
        return None

    filas = len(terreno)
    columnas = len(terreno[0]) if terreno else 0 

    visitados = [[False] * columnas for _ in range(filas)]
    padre = [[None] * columnas for _ in range(filas)]
    g_cost = [[float('inf')] * columnas for _ in range(filas)]
    h_cost = [[0] * columnas for _ in range(filas)]
    
    abiertos = []
    g_cost[INICIO[0]][INICIO[1]] = 0
    f_inicio = manhattan(INICIO, FIN)
    heapq.heappush(abiertos, (f_inicio, INICIO))

    while abiertos: 
        f_actual, (x, y) = heapq.heappop(abiertos)

        if visitados[x][y]:
            continue
        
        visitados[x][y] = True

        if (x, y) == FIN:
            return reconstruir_camino(padre, INICIO, FIN)

        for dx, dy in direcciones:
            nuevo_x = x + dx
            nuevo_y = y + dy

            if movimiento_valido(nuevo_x, nuevo_y, filas, columnas) and not visitados[nuevo_x][nuevo_y]:
                costo = COSTOS[terreno[nuevo_x][nuevo_y]]
                if costo == float("inf"):
                    continue

                nuevo_g = g_cost[x][y] + costo

                if nuevo_g < g_cost[nuevo_x][nuevo_y]:
                    padre[nuevo_x][nuevo_y] = (x, y)
                    h = manhattan((nuevo_x, nuevo_y), FIN)
                    f = nuevo_g + h
                    g_cost[nuevo_x][nuevo_y] = nuevo_g
                    heapq.heappush(abiertos, (f, (nuevo_x, nuevo_y)))
    return None  # No se encontró camino


def reconstruir_camino(padre, INICIO, FIN):
    camino = []
    actual = FIN

    while actual is not None:
        camino.append(actual)
        if actual == INICIO:
            camino.reverse()
            return camino
        actual = padre[actual[0]][actual[1]]

    return None   # ← protección: no se llegó al inicio





# ==================== Botón ====================
ttk.Button(
    frame_controles,
    text="Generar Mundo",
    command=generar_mundo
).grid(row=0, column=4, padx=10)
ttk.Button(
    frame_controles, 
    text="Buscar Ruta",
    command=ruta_existe
).grid(row=0, column=5, padx=10)
ttk.Button(
    frame_controles, 
    text="Limpiar Camino", 
    command=dibujar_mundo
    ).grid(row=1, column=5, padx=10)

# ==================== Main loop ====================
root.mainloop()
