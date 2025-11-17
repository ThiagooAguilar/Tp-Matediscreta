"""
Graph analysis module for Buenos Aires city networks.
Students must implement all functions marked with TODO.
"""

from src.output import (
    format_componentes_conexos,
    format_orden_fallos,
    format_camino_minimo,
    format_simulacion_corte,
    format_ruta_recoleccion,
    format_plantas_asignadas,
    format_puentes_y_articulaciones,
)

# -----------------------------
# Graph loading
# -----------------------------

def load_graph(path):
    """
    Load a simple graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [neighbors]}
    """
    # TODO: Implement
    graph = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                # Quitamos espacios extra y dividimos la línea
                parts = line.strip().split()

                if not parts:
                    continue

                u = parts[0]
                v = parts[1]


                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []

                if v not in graph[u]:
                    graph[u].append(v)
                if u not in graph[v]:
                    graph[v].append(u)

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta {path}")
        return {}

    return graph


def load_weighted_graph(path):
    """
    Load a weighted graph from a file.

    Args:
        path: File path

    Returns:
        Adjacency dictionary {node: [(neighbor, weight), ...]}
    """
    # TODO: Implement
    graph = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                # Quitamos espacios extra y dividimos la línea
                parts = line.strip().split()

                if not parts or len(parts) < 3:
                    continue

                u = parts[0]
                v = parts[1]

                try:
                    weight = int(parts[2])  # Convertir el peso a entero
                except ValueError:
                    print(f"Advertencia: Peso inválido '{parts[2]}' en la línea: {line.strip()}")
                    continue

                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []


                if (v, weight) not in graph[u]:
                    graph[u].append((v, weight))
                if (u, weight) not in graph[v]:
                    graph[v].append((u, weight))

    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en la ruta {path}")
        return {}

    return graph


def process_queries(queries_file, output_file, electric_graph, road_graph, water_graph):
    """
    Process queries from file and generate output.

    Args:
        queries_file: Path to queries file
        output_file: Path to output file
        electric_graph: Electric network graph
        road_graph: Road network graph
        water_graph: Water network graph
    """
    # TODO: Implement
    pass
