import heapq

#1 - CAMINO MÍNIMO ENTRE DOS BARRIOS

def camino_minimo(graph, origen, destino):
    """
    Calculo el camino mínimo entre dos barrios (Dijkstra)

    Devuelve:
        (distancia_total, [nodos_del_camino])
        o en cambio (None, []) si no existe el camino
    """
    if origen not in graph or destino not in graph:
        return float('inf'), []

    dist = {n: float("inf") for n in graph}
    dist[origen] = 0
    padree = {n: None for n in graph}

    pq = [(0, origen)]

    while pq:
        d, u = heapq.heappop(pq)

        if u == destino:
            break

        if d > dist[u]:
            continue

        for v, w in graph[u]:
            nuevo = d + w
            if nuevo < dist[v]:
                dist[v] = nuevo
                padree[v] = u
                heapq.heappush(pq, (nuevo, v))

    if dist[destino] == float("inf"):
        return float('inf'), []

    # reconstruir camino
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padree[actual]
    camino.reverse()

    return dist[destino], camino


#2 - SIMULACIÓN DE CORTE

def simulacion_corte(graph, nodos_cortados, origen, destino):
    """
    Camino mínimo entre origen y destino luego de cortar nodos.
    """
    nodos_cortados = set(nodos_cortados)

    # Construir grafo reducido
    reducido = {}
    for u in graph:
        if u in nodos_cortados:
            continue
        reducido[u] = []
        for v, w in graph[u]:
            if v not in nodos_cortados:
                reducido[u].append((v, w))

    return camino_minimo(reducido, origen, destino)


#3 - RUTA DE RECOLECCIÓN (Usando Aproximación por MST)

def _obtener_mst_prim(graph, todos_los_nodos):
    """
    Calcula el Árbol de Tendido Mínimo (MST) para todas
    las componentes del grafo (un "bosque").
    """
    mst = {nodo: [] for nodo in graph}
    visitados = set()
    pq = [] # Fila de prioridad

    # Iteramos sobre todos los nodos para encontrar componentes disconexas
    for nodo_inicio_componente in todos_los_nodos:
        if nodo_inicio_componente not in visitados:
            # Empezamos Prim para una nueva componente
            heapq.heappush(pq, (0, nodo_inicio_componente, nodo_inicio_componente))

            while pq:
                peso, u, v = heapq.heappop(pq)
                
                if v in visitados:
                    continue
                visitados.add(v)
                
                if u != v:
                    mst[u].append((v, peso))
                    mst[v].append((u, peso))
                
                for vecino, peso_arista in graph.get(v, []):
                    if vecino not in visitados:
                        heapq.heappush(pq, (peso_arista, v, vecino))
    return mst

def _dfs_preorden_ruta(mst, todos_los_nodos_ordenados):
    """
    Realiza un recorrido DFS (pre-orden) sobre el bosque MST
    para generar una ruta, respetando el orden de inicio.
    """
    ruta = []
    visitados = set()
    
    # Iteramos sobre la lista ordenada de barrios (de main.py)
    for inicio_componente in todos_los_nodos_ordenados:
        if inicio_componente not in visitados:
            # Si no visitamos este nodo (y su componente),
            # empezamos un nuevo DFS
            stack = [inicio_componente]
            
            while stack:
                u = stack.pop()
                if u not in visitados:
                    visitados.add(u)
                    ruta.append(u)
                    
                    # Añadir vecinos al stack en orden alfabético reverso
                    # para que el DFS los visite en orden alfabético
                    vecinos_ordenados = sorted([v for v, w in mst[u]], reverse=True)
                    for v in vecinos_ordenados:
                        if v not in visitados:
                            stack.append(v)
    return ruta


def ruta_recoleccion(graph, barrios):
    """
    Aproxima la ruta de recolección (TSP) usando el Árbol de Tendido Mínimo (MST).
    La ruta se obtiene de un recorrido pre-orden del MST.
    
    Args:
        graph: El grafo vial.
        barrios: Lista ORDENADA de todos los barrios (de main.py).
    """
    if not barrios:
        return 0.0, []

    # 1. Construir el Bosque de Tendido Mínimo (MST)
    #    Le pasamos la lista 'barrios' (que ya está ordenada)
    #    para que itere sobre todos
    mst = _obtener_mst_prim(graph, barrios)

    # 2. Obtener la ruta haciendo un recorrido en pre-orden (DFS) sobre el MST
    #    Le pasamos la lista 'barrios' (ordenada)
    #    para asegurar el orden de inicio de componentes ("Almagro" primero)
    ruta = _dfs_preorden_ruta(mst, barrios)

    return 0.0, ruta # Devolvemos 0.0 como distancia, no se usa