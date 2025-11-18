from collections import deque

# --- Función Auxiliar para BFS (Usada por plantas_asignadas) ---

def _bfs_distancias(graph, inicio):
    """
    Calcula las distancias desde un nodo de inicio a todos los demás en un grafo no ponderado.
    """
    distancias = {nodo: float('inf') for nodo in graph}
    if inicio not in graph:
        return distancias
        
    distancias[inicio] = 0
    cola = deque([inicio])
    visitados = {inicio}

    while cola:
        u = cola.popleft()
        for v in graph.get(u, []):
            if v not in visitados:
                visitados.add(v)
                distancias[v] = distancias[u] + 1
                cola.append(v)
                
    return distancias

# --- 1. PLANTAS ASIGNADAS ---

def plantas_asignadas(graph, planta1, planta2):
    """
    Asigna cada barrio a la planta de agua más cercana (planta1 o planta2).
    Utiliza BFS para calcular las distancias en el grafo no ponderado.

    Args:
        graph (dict): Grafo no ponderado (lista de adyacencia).
        planta1 (str): Nombre del nodo de la primera planta.
        planta2 (str): Nombre del nodo de la segunda planta.

    Returns:
        dict: Un diccionario {barrio: planta_asignada}
    """
    
    # Calcular distancias desde cada planta a todos los nodos
    dist_planta1 = _bfs_distancias(graph, planta1)
    dist_planta2 = _bfs_distancias(graph, planta2)
    
    asignaciones = {}
    
    # Asegurar que las plantas se asignen a sí mismas
    if planta1 in graph:
        asignaciones[planta1] = planta1
    if planta2 in graph:
        asignaciones[planta2] = planta2

    # Asignar cada barrio a la planta más cercana
    for barrio in graph:
        if barrio == planta1 or barrio == planta2:
            continue
            
        dist1 = dist_planta1.get(barrio, float('inf'))
        dist2 = dist_planta2.get(barrio, float('inf'))
        
        if dist1 < dist2:
            asignaciones[barrio] = planta1
        elif dist2 < dist1:
            asignaciones[barrio] = planta2
        elif dist1 != float('inf'):
            # Caso de empate: asignar alfabéticamente
            asignaciones[barrio] = min(planta1, planta2)
        else:
            # Nodo inalcanzable (no debería pasar si el grafo es conexo)
            pass 
            
    return asignaciones

# --- 2. PUENTES Y PUNTOS DE ARTICULACIÓN ---

def puentes_y_articulaciones(graph):
    """
    Encuentra todos los puentes y puntos de articulación en un grafo no dirigido.
    Usa un algoritmo basado en DFS (similar a Tarjan).

    Args:
        graph (dict): Grafo no ponderado (lista de adyacencia).

    Returns:
        tuple: (list_articulaciones, list_puentes)
               - list_articulaciones: Lista de nodos que son puntos de articulación.
               - list_puentes: Lista de tuplas (u, v) que son puentes.
    """
    visitados = set()
    descubierto = {}  # Tiempo de descubrimiento
    low_link = {}     # El 'low-link' (tiempo de descubrimiento más bajo alcanzable)
    parent = {}
    tiempo = 0
    
    articulaciones = set()
    puentes = []

    def _dfs_criticos(u):
        nonlocal tiempo
        visitados.add(u)
        descubierto[u] = low_link[u] = tiempo
        tiempo += 1
        hijos_dfs = 0 # Contador de hijos en el árbol DFS

        for v in graph.get(u, []):
            if v not in visitados:
                hijos_dfs += 1
                parent[v] = u
                _dfs_criticos(v)

                # Actualizar low-link del padre
                low_link[u] = min(low_link[u], low_link[v])

                # (1) Condición de Punto de Articulación (para nodos no-raíz)
                if parent.get(u) is not None and low_link[v] >= descubierto[u]:
                    articulaciones.add(u)
                
                # (2) Condición de Puente
                if low_link[v] > descubierto[u]:
                    # Ordenar la tupla para consistencia
                    puentes.append(tuple(sorted((u, v))))

            elif v != parent.get(u):
                # Es un 'back-edge' (arista de retroceso), actualizamos low-link
                low_link[u] = min(low_link[u], descubierto[v])
        
        # (3) Condición de Punto de Articulación (para el nodo raíz del árbol DFS)
        if parent.get(u) is None and hijos_dfs > 1:
            articulaciones.add(u)

    # Iterar por todos los nodos para manejar grafos disconexos
    for nodo in graph:
        if nodo not in visitados:
            _dfs_criticos(nodo)
            
    return sorted(list(articulaciones)), sorted(list(puentes))