import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# Crear una matriz de calor simétrica de ejemplo (por ejemplo, una matriz 10x10 de valores aleatorios)
size = 10  # Tamaño de la matriz
heatmap_data = np.random.rand(size, size)

# Hacer la matriz simétrica (es decir, matriz[i,j] = matriz[j,i])
heatmap_data = (heatmap_data + heatmap_data.T) / 2  # Hacerla simétrica tomando la media

# Lista de tuplas con nombres de grupos válidos, sin "Group0"
tuplas = [
    ("Group2", "Group3"),         # Tupla de 2 elementos
    ("Group6", "Group7", "Group5"),  # Tupla de 3 elementos
    ("Group1", "Group9"),         # Tupla de 2 elementos
    ("Group1", "Group2", "Group3"),  # Tupla de 3 elementos
    ("Group6", "Group4"),         # Tupla de 2 elementos
    ("Group8", "Group9"),         # Tupla de 2 elementos
    ("Group3", "Group4"),         # Tupla de 2 elementos
    ("Group9", "Group10"),         # Tupla de 2 elementos
    ("Group7", "Group5", "Group8"),  # Tupla de 3 elementos
    ("Group2", "Group3", "Group4", "Group5")  # Tupla de 4 elementos
]

# Crear etiquetas personalizadas para los grupos
group_labels = [f"Group{i+1}" for i in range(size)]  # Nombres de grupos como Group1, Group2, ...

def create_heatmap_animation(heatmap_data: np.ndarray, group_labels: list, tuplas: list):
    # Función para actualizar el heatmap en cada frame
    def update(frame):
        ax.clear()  # Limpiar el eje para cada nuevo frame
        
        # Dibujar la matriz sin resaltar ninguna fila/columna al principio
        sns.heatmap(heatmap_data, ax=ax, cmap="Blues", cbar=False, annot=False, linewidths=0.5, xticklabels=group_labels, yticklabels=group_labels)
        
        # Extraer la tupla para este frame y el color para el resaltado
        tupla = tuplas[frame]
        color = 'red'  # Color fijo (rojo)
        alpha = 0.6  # Translucidez de las celdas de intersección
        
        # Mapeo de nombres de grupos a índices
        indices = {group_labels[i]: i for i in range(size)}
        
        # Pintar las celdas correspondientes a las intersecciones de la tupla
        for i in range(len(tupla)):
            for j in range(i, len(tupla)):  # Para evitar resaltar dos veces la misma intersección
                row = indices[tupla[i]]  # Obtener el índice del grupo en la fila
                col = indices[tupla[j]]  # Obtener el índice del grupo en la columna
                
                # Pintar la intersección (row, col) y (col, row) si son distintos
                ax.add_patch(patches.Rectangle((col, row), 1, 1, linewidth=0, edgecolor='none', facecolor=color, alpha=alpha, zorder=10))
                if row != col:  # Si es una celda diferente, pintamos la intersección simétrica
                    ax.add_patch(patches.Rectangle((row, col), 1, 1, linewidth=0, edgecolor='none', facecolor=color, alpha=alpha, zorder=10))

        # Actualizar el título con los valores de la tupla
        ax.set_title(f"{' + '.join(tupla)}")

    # Crear la figura y los ejes para el heatmap
    fig, ax = plt.subplots(figsize=(8, 6))

    # Crear la animación
    anim = FuncAnimation(fig, update, frames=len(tuplas), interval=3000, repeat=False)

    # Guardar la animación como un GIF
    anim.save("heatmap_animation_groups_varying_tuples_group_names_corrected.gif", writer="pillow", fps=1/3)

    # Mostrar la animación
    plt.show()

# Crear la animación del heatmap con las tuplas y nombres de grupos dados
create_heatmap_animation(heatmap_data, group_labels, tuplas)