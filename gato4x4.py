import matplotlib.pyplot as plt
import random

# Crear un tablero 4x4 vacío
tablero = [['' for _ in range(4)] for _ in range(4)]
turno_j = True  # Para saber si es turno del jugador
simbolo_U = ''  # Símbolo del jugador
simbolo_IA = ''  # Símbolo de la IA
fig, ax = None, None  # Para usar en funciones

def dibujar_tablero():
    global fig, ax
    # Crear la figura y los ejes
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title('Juego de Gato')
    # Dibujar las líneas del tablero 4x4
    for i in range(1, 4):
        ax.plot([i, i], [0, 4], color='black')  # Líneas verticales
    for i in range(1, 4):
        ax.plot([0, 4], [i, i], color='black')  # Líneas horizontales

    # Ajustar los límites y aspecto de la gráfica
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')

    # Eliminar los ejes
    ax.axis('off')

    return fig, ax

def ganador(simbolo):
    # Verificar filas y columnas
    for i in range(4):
        if all(tablero[i][j] == simbolo for j in range(4)) or all(tablero[j][i] == simbolo for j in range(4)):
            return True
    # Verificar diagonales
    if all(tablero[i][i] == simbolo for i in range(4)) or all(tablero[i][3 - i] == simbolo for i in range(4)):
        return True
    return False

def turno_IA(simbolo_IA):
    # Elegir una casilla aleatoria
    cvacia = [(i, j) for i in range(4) for j in range(4) if tablero[i][j] == '']
    if cvacia:
        i, j = random.choice(cvacia)
        tablero[i][j] = simbolo_IA
        ax.text(j + 0.5, i + 0.5, simbolo_IA, fontsize=30, ha='center', va='center', color='red')
        plt.draw()

        # Verificar si la IA ganó
        if ganador(simbolo_IA):
            plt.title("¡Haz perdido!")
            plt.show()
            return True
    return False

def lleno():
    # Verificar si las casillas están llenas
    return all(tablero[i][j] != '' for i in range(4) for j in range(4))

def click_event(event):
    global turno_j, simbolo_U, simbolo_IA

    if simbolo_U == '':
        simbolo_U = random.choice(['X', 'O'])
        simbolo_IA = 'O' if simbolo_U == 'X' else 'X'

    # Si no es turno del jugador, no hacer nada
    if not turno_j:
        return  

    # Verificar si las coordenadas del clic del ratón están dentro del área del tablero.
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        # Verificar que el clic esté dentro del tablero y la casilla esté vacía
        if x >= 0 and x < 4 and y >= 0 and y < 4 and tablero[y][x] == '':
            # Colocar el símbolo en la casilla seleccionada por el usuario
            tablero[y][x] = simbolo_U
            ax.text(x + 0.5, y + 0.5, simbolo_U, fontsize=30, ha='center', va='center', color='blue')
            plt.draw()

            if ganador(simbolo_U):
                plt.title("¡El jugador ha ganado!")
                plt.show()
                return
            # Turno de la IA
            turno_j = False

            if not lleno():
                if turno_IA(simbolo_IA):
                    return

            # Turno del Jugador
            turno_j = True

            # Verificar si el tablero está lleno
            if lleno():
                plt.title("¡Es un empate!")
                plt.show()

# Dibujar el tablero
fig, ax = dibujar_tablero()
# Conectar el evento de clic
fig.canvas.mpl_connect('button_press_event', click_event)
# Mostrar el tablero
plt.show()
