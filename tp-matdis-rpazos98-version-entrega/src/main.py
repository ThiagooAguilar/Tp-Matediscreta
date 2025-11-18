"""
Graph analysis module for Buenos Aires city networks.
Students must implement all functions marked with TODO.
"""
from src.electricAlgorithms import encontrar_componentes_conexos, criticidad_de_componentes
from src.vialAlgorithms import camino_minimo, simulacion_corte, ruta_recoleccion
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
    graph = {}
    try:
        with open(path, 'r') as f:
            for line in f:
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
    graph = {}
    try:
        with open(path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts or len(parts) < 3:
                    continue

                u = parts[0]
                v = parts[1]

                try:
                    weight = int(parts[2])
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

    try:
        with open(output_file, 'w') as f_out:
            with open(queries_file, 'r') as f_in:

                for line in f_in:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    parts = line.split()
                    comando = parts[0]

                    # -----------------------------
                    # Parsing flexible
                    # -----------------------------
                    if comando in ["CAMINO_MINIMO", "CAMINO_MINIMO_SIMULAR_CORTE"]:
                        red = "VIAL"
                        args = parts[1:]

                    elif comando in ["COMPONENTES_CONEXOS", "ORDEN_FALLOS"]:
                        red = "ELECTRICA"
                        args = parts[1:]

                    else:
                        if len(parts) < 2:
                            print(f"Advertencia: Consulta incompleta: {line}")
                            continue
                        red = parts[1]
                        args = parts[2:]

                    # -----------------------------
                    # Select graph
                    # -----------------------------
                    if red == "ELECTRICA":
                        graph = electric_graph
                    elif red == "VIAL":
                        graph = road_graph
                    elif red == "HIDRICA":
                        graph = water_graph
                    else:
                        print(f"Advertencia: Red no reconocida para el comando {comando}: {red}")
                        continue

                    # -----------------------------
                    # Commands
                    # -----------------------------

                    # --- Electric network ---
                    if comando == "COMPONENTES_CONEXOS":
                        componentes = encontrar_componentes_conexos(graph)
                        output_str = format_componentes_conexos(componentes)
                        f_out.write(output_str)

                    elif comando == "ORDEN_FALLOS":
                        criticos_agrupados = criticidad_de_componentes(graph)

                        criticos_para_formatter = []
                        for grado, nodos in criticos_agrupados.items():
                            for nodo in nodos:
                                criticos_para_formatter.append((nodo, grado))

                        output_str = format_orden_fallos(criticos_para_formatter)
                        f_out.write(output_str)

                    # --- Road network ---
                    elif comando == "CAMINO_MINIMO":
                        origen = args[0]
                        destino = args[1]

                        distancia, camino = camino_minimo(graph, origen, destino)

                        # *** FIX CORRECTO ***
                        output_str = format_camino_minimo(distancia, camino, origen, destino)

                        f_out.write(output_str)

                    elif comando == "CAMINO_MINIMO_SIMULAR_CORTE":
                        cortes_str = args[0].strip('{}')
                        cortes = {c.strip() for c in cortes_str.split(',')}
                        origen = args[1]
                        destino = args[2]

                        camino = simulacion_corte(graph, origen, destino, cortes)
                        output_str = format_simulacion_corte(camino, origen, destino, cortes)
                        f_out.write(output_str)

                    elif comando == "CAMINO_RECOLECCION_BASURA":
                        ruta = ruta_recoleccion(graph)
                        output_str = format_ruta_recoleccion(ruta)
                        f_out.write(output_str)

                    # --- Water network (disabled) ---
                    """
                    elif comando == "PLANTAS_ASIGNADAS":
                        planta1 = args[0]
                        planta2 = args[1]
                        asignaciones = plantas_asignadas(graph, planta1, planta2)
                        output_str = format_plantas_asignadas(asignaciones)
                        f_out.write(output_str)

                    elif comando == "PUENTES_Y_ARTICULACIONES":
                        puentes, articulaciones = puentes_y_articulaciones(graph)
                        output_str = format_puentes_y_articulaciones(puentes, articulaciones)
                        f_out.write(output_str)
                    """

    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {e}")
    except Exception as e:
        print(f"Ocurrió un error al procesar las consultas: {e}")
