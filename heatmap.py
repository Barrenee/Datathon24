import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
from config.literals import LANGUAGES
from utils.matchesCompulsory import find_obligatory_compatibles, init_tables, get_compatible_groups
from utils.abstraction import abstract_objective, abstract_expertise, abstract_tryhard, abstract_general, init_participant
from utils.matchesBasic import  roles_match, interests_match, programming_skills_match
from Group import Group
from participant import Participant, load_participants
from ParticipantAbstract import ParticipantAbstract
import json
from utils.k_best_tests import maikelfunction



data = json.load(open("data/datathon_participants.json", "r"))


all_groups = []
for person in data[0:6]:
    all_groups.append(init_participant(ParticipantAbstract(Participant(**person))))

tuplas, _, _, _, matrix = maikelfunction(all_groups, 2, matrix_bool=True)
print(matrix, tuplas)

matrix[matrix == -np.inf] = 0

size = len(matrix)

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
create_heatmap_animation(matrix, group_labels, tuplas)


