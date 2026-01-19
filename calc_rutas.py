
# IMPORTACIONES - Librerías necesarias para la aplicación
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import heapq  # Para el algoritmo de búsqueda A*
import random  # Para generar terrenos aleatorios

# CONFIGURACIÓN DE VENTANA PRINCIPAL
# Crea la ventana principal de la aplicación
root = tk.Tk()
root.title("Calculadora de Rutas")
root.geometry("500x500")
root.configure(bg="#DBDBDB")

# CONSTANTES DE TERRENO
# Define los tipos de terreno que pueden existir en el mapa
CAMINO = 0      
EDIFICIO = 1    
AGUA = 2        
BLOQUEADO = 3   

# Variables para almacenar inicio y fin de ruta
INICIO = None
FIN = None

posibles_terrenos = [CAMINO, EDIFICIO, AGUA, BLOQUEADO]

# COLORES de terreno
COLORES = {
    CAMINO: "#FFFFFF",      # Blanco
    EDIFICIO: "#424242",    # Gris oscuro
    AGUA: "#2196f3",        # Azul
    BLOQUEADO: "#FF0000"    # Rojo
}

# el costo de movimiento por tipo de terreno
COSTOS = { 
    CAMINO: 1,              # Costo bajo, fácil de transitar
    AGUA: 4,                # Costo alto, difícil de transitar
    BLOQUEADO: float("inf"),   # Imposible de transitar
    EDIFICIO: float("inf")     # Imposible de transitar
}

# símbolo visual para cada terreno
SIMBOLOS = {
    CAMINO: ".",        # Punto para camino libre
    EDIFICIO: "X",      # X para edificio
    AGUA: "~",          # Tilde para agua
    BLOQUEADO: "#"      # Numeral para bloqueado
}

# CONFIGURACIÓN DE ESTILOS 
style = ttk.Style()
style.theme_use("clam")  
style.configure("TButton", font=("Segoe UI", 10), padding=6)
style.configure("TLabel", font=("Segoe UI", 10))

# Variable para almacenar el número de filas y columnas del mapa
filas_var = tk.IntVar()
columnas_var = tk.IntVar()

# Matriz que representa el terreno/mapa de la aplicación
terreno = []

# CONTENEDOR SUPERIOR - Contiene los campos de entrada y botones
# Crea un frame para organizar los controles de entrada
frame_controles = tk.Frame(
    root,
    bg="#B0B0B0",
    padx=10,
    pady=10
)
frame_controles.pack(fill="x", padx=10, pady=10)

# Etiqueta para el campo de filas y columnas
tk.Label(
    frame_controles,
    text="Filas:",
    bg="#DBDBDB",
    fg="black"
).grid(row=0, column=0, padx=5)

tk.Label(
    frame_controles,
    text="Columnas:",
    bg="#DBDBDB",
    fg="black"
).grid(row=0, column=2, padx=5)

# Campo de entrada para el número de filas y columnas
ttk.Entry(
    frame_controles,
    textvariable=filas_var,
    width=5,
    justify="center"
).grid(row=0, column=1, padx=5)

ttk.Entry(
    frame_controles,
    textvariable=columnas_var,
    width=5,
    justify="center"
).grid(row=0, column=3, padx=5)

# Contenedor donde se dibuja la cuadrícula
# Crea un frame que contendrá la visualización del mapa
frame_mapa = tk.Frame(
    root,
    bg="#EDEDED",
    padx=10,
    pady=10
)
frame_mapa.pack(padx=10, pady=10)

# Función para generar un mapa aleatorio 
def generar_mundo():
    global terreno

    # Obtiene las dimensiones del mapa desde los campos de entrada
    filas = filas_var.get()
    columnas = columnas_var.get()

    # Valida las dimensiones 
    if filas <= 0 or columnas <= 0:
        messagebox.showerror(
            "Error",
            "Filas y columnas deben ser mayores que 0"
        )
        return

    # Genera una matriz con terrenos aleatorios
    terreno = [
        [random.choice(posibles_terrenos) for _ in range(columnas)]
        for _ in range(filas)
    ]
    dibujar_mundo()

# Función para visualizar el mapa en la interfaz gráfica
def dibujar_mundo():
    # Elimina todos los widgets previos del frame del mapa
    for widget in frame_mapa.winfo_children():
        widget.destroy()

    
    for i, fila in enumerate(terreno):
        for j, valor in enumerate(fila):
            # Determina el color y símbolo según si es inicio, fin u otro terreno
            if INICIO == (i,j):
                color = "#4cad50"  # Verde para inicio
                texto = "S"
            elif FIN == (i,j):
                color = "#FFA6A6"  # Rojo para fin
                texto = "E"
            else:
                color = COLORES.get( valor, "#000000")
                texto = SIMBOLOS.get( valor, "#000000")

            # Crea un label (celda) para representar el terreno
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
            # Vincula clic izquierdo para seleccionar inicio/fin
            lbl.bind("<Button-1>", lambda e, x=i, y=j: seleccionar_celda(e, x, y))
            # Vincula clic derecho para bloquear/desbloquear celdas
            lbl.bind("<Button-3>", lambda e, x=i, y=j: bloquear_celda(x, y))

# Función para validar si existe una ruta entre inicio y fin
def ruta_existe():
    # Verifica que se haya generado un mapa
    if not terreno:
        messagebox.showwarning("Error", "Primero genera el mundo")
        return
        # Verifica que se hayan seleccionado puntos de inicio y fin
    if INICIO is None or FIN is None:
        messagebox.showwarning("Advertencia", "Selecciona inicio y fin primero")
        return
    
    # Calcula el camino más corto usando el algoritmo A*
    camino = camino_corto(terreno, INICIO, FIN)
    mostrar_camino(camino)

# Función para visualizar el camino encontrado sobre el mapa
def mostrar_camino(camino):
    dibujar_mundo()  # Redibuja el mapa
    # Verifica si se encontró un camino válido
    if camino is None: 
        messagebox.showwarning("Error", "No se encontro un camino 🥲")
        return

    # Marca cada celda del camino (excepto inicio y fin) con un asterisco
    for i, j in camino [1:-1]:
        lbl = tk.Label(
                frame_mapa,
                text= "*",
                fg= "black",
                font=("Consolas", 12, "bold"),
                bg="#ffeb3b",  # Amarillo para resaltar el camino
                width=4,
                height=2,
                relief="ridge",
                borderwidth=1
            )
        lbl.grid(row=i, column=j)
        # Permite hacer clic en las celdas del camino
        lbl.bind("<Button-1>", lambda e, x=i, y=j: seleccionar_celda(e, x, y))

# Función para seleccionar/deseleccionar puntos de inicio y fin
def seleccionar_celda(e,i,j):
    global INICIO, FIN


    if INICIO == None:      # Si no hay inicio marcado, la celda actual será el inicio
        INICIO = (i, j)
    elif FIN == None:       # Si hay inicio pero no fin, la celda actual será el fin
        FIN = (i, j)
    elif INICIO == (i, j):  # Si ya hay inicio y se hace clic en él, lo deselecciona
        INICIO = None
    elif FIN == (i, j):     # Si ya hay fin y se hace clic en él, lo deselecciona
        FIN = None
    elif terreno[i][j] != CAMINO: # Si la celda no es transitable, muestra error
        messagebox.showwarning("Invalid", "Solo puedes seleccionar caminos libres")
        return
    else:                   # Si ambos están marcados, reemplaza el fin
        FIN = (i, j)
    dibujar_mundo()

# Función para alternar entre bloqueado y desbloqueado con clic derecho
def bloquear_celda(x, y):
    global terreno

    # Si es camino o agua, lo convierte a edificio 
    if terreno[x][y] in (CAMINO, AGUA):
        terreno[x][y] = EDIFICIO
    # Si es bloqueado o edificio, lo convierte a camino
    elif terreno[x][y] in (BLOQUEADO, EDIFICIO):
        terreno[x][y] = CAMINO
    dibujar_mundo()

# ALGORITMO DE BÚSQUEDA A* 
direcciones = [ # Define los movimientos posibles
    (-1, 0),    # Arriba
    (1, 0),     # Abajo
    (0, -1),    # Izquierda
    (0, 1),     # Derecha
]

# Heuristica de Manhattan - Estima la distancia entre dos puntos
def manhattan(a,b):
    h = abs(a[0]-b[0]) + abs(a[1]-b[1])
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

# Función para validar si una posición está dentro de los límites del mapa
def movimiento_valido( x, y, filas, columnas):
    if x < 0 or x >= filas:     # Verifica si está fuera de límites en el eje X
        return False
    if y < 0 or y >= columnas:  # Verifica si está fuera de límites en el eje Y 
        return False 
    else:
        return True

# Función principal del algoritmo A* para encontrar el camino más corto
def camino_corto(terreno, INICIO, FIN):
    # Valida que los puntos de inicio y fin estén definidos
    if INICIO is None or FIN is None:
        messagebox.showwarning(
            "Advertencia",
            "Debe seleccionar un punto de inicio y fin"
        )
        return None

    # Obtiene las dimensiones del mapa
    filas = len(terreno)
    columnas = len(terreno[0]) if terreno else 0 

    # Inicializa matrices de control para el algoritmo A*
    visitados = [[False] * columnas for _ in range(filas)]          # Matriz para marcar celdas visitadas
    padre = [[None] * columnas for _ in range(filas)]               # Matriz para para reconstruir el camino
    g_cost = [[float('inf')] * columnas for _ in range(filas)]      # Matriz para el costo acumulado desde el inicio (g_cost)
    h_cost = [[0] * columnas for _ in range(filas)]                 # Matriz para el costo heurístico al fin 
    
    abiertos = []       # Cola de prioridad 
    g_cost[INICIO[0]][INICIO[1]] = 0    # El costo inicial en el inicio es 0
    f_inicio = manhattan(INICIO, FIN)   # Calcula el costo f 
    heapq.heappush(abiertos, (f_inicio, INICIO))    # Añade el nodo inicial a la cola de prioridad

    # Bucle principal del algoritmo 
    while abiertos: 
        f_actual, (x, y) = heapq.heappop(abiertos)
        # Si ya fue visitado, salta al siguiente
        if visitados[x][y]:
            continue
        # Marca el nodo actual como visitado
        visitados[x][y] = True

        if (x, y) == FIN:
            return reconstruir_camino(padre, INICIO, FIN)

        # Explora los vecinos del nodo actual
        for dx, dy in direcciones:
            nuevo_x = x + dx
            nuevo_y = y + dy

            # Verifica si el movimiento es válido y no ha sido visitado
            if movimiento_valido(nuevo_x, nuevo_y, filas, columnas) and not visitados[nuevo_x][nuevo_y]:
                costo = COSTOS[terreno[nuevo_x][nuevo_y]]
                if costo == float("inf"):
                    continue

                # Calcula el nuevo costo g
                nuevo_g = g_cost[x][y] + costo

                # Si encontró un camino más corto, actualiza
                if nuevo_g < g_cost[nuevo_x][nuevo_y]:
                    padre[nuevo_x][nuevo_y] = (x, y)
                    h = manhattan((nuevo_x, nuevo_y), FIN)
                    f = nuevo_g + h
                    g_cost[nuevo_x][nuevo_y] = nuevo_g
                    heapq.heappush(abiertos, (f, (nuevo_x, nuevo_y)))
    
    # Si la cola se vacía sin encontrar el fin, no hay camino
    return None  # No se encontró camino

# Función para reconstruir el camino desde el fin hasta el inicio usando la matriz de padres
def reconstruir_camino(padre, INICIO, FIN):
    # Lista para almacenar el camino reconstruido
    camino = []
    actual = FIN

    # Sigue los padres hasta llegar al inicio
    while actual is not None:
        camino.append(actual)
        # Si llegó al inicio, invierte el camino y lo retorna
        if actual == INICIO:
            camino.reverse()
            return camino
        actual = padre[actual[0]][actual[1]]

    # si no se llegó al inicio, retorna None
    return None

# BOTONES DE CONTROL - Interfaz para ejecutar las funciones principales
# Botón para generar un mundo aleatorio
ttk.Button(
    frame_controles,
    text="Generar Mundo",
    command=generar_mundo
).grid(row=0, column=4, padx=10)

# Botón para buscar la ruta más corta entre inicio y fin
ttk.Button(
    frame_controles, 
    text="Buscar Ruta",
    command=ruta_existe
).grid(row=0, column=5, padx=10)

# Botón para limpiar el camino y volver a mostrar solo el mapa
ttk.Button(
    frame_controles, 
    text="Limpiar Camino", 
    command=dibujar_mundo
).grid(row=1, column=5, padx=10)

# BUCLE PRINCIPAL - Inicia la aplicación
root.mainloop()
