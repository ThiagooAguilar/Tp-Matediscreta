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
        return None, []

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
        return None, []

    # reconstruir camino
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padree[actual]
    camino.reverse()

    return dist[destino], camino


#2 - SIMULACIÓN DE CORTE

def simulacion_corte(graph, nodos_cortados):
    """
    Devuelvo los componentes conexos del grafo vial
    habiendo eliminado los grafos cortados
    """
    nodos_cortados = set(nodos_cortados)

    # construir grafo reducido
    reducido = {}
    for u in graph:
        if u in nodos_cortados:
            continue
        reducido[u] = []
        for v, w in graph[u]:
            if v not in nodos_cortados:
                reducido[u].append((v, w))

    # BFS /// DFS
    visitado = set()
    comps = []

    for nodo in reducido:
        if nodo not in visitado:
            stack = [nodo]
            comp = []
            visitado.add(nodo)

            while stack:
                x = stack.pop()
                comp.append(x)
                for y, _ in reducido[x]:
                    if y not in visitado:
                        visitado.add(y)
                        stack.append(y)

            comps.append(sorted(comp))

    return comps

#3 - RUTA DE RECOLECCIÓN

def ruta_recoleccion(graph, barrios):
    """
    Aproximo con TSP usando el vecino mas cercano posible.

    Devuelve:
        (dist_total, [ruta_en_orden])
        o en cambio (None, []) si algún barrio no lo peudo alcanzar.
    """
    if not barrios:
        return 0, []

    inicio = barrios[0]
    restantes = set(barrios)
    restantes.remove(inicio)

    ruta = [inicio]
    total = 0
    actual = inicio

    while restantes:
        mejor = None
        mejor_d = float("inf")
        mejor_camino = []

        for b in restantes:
            d, cam = camino_minimo(graph, actual, b)
            if d is not None and d < mejor_d:
                mejor = b
                mejor_d = d
                mejor_camino = cam

        if mejor is None:
            return None, []

        # Agregar solo los nuevos nodos al camino final
        ruta.extend(mejor_camino[1:])
        total += mejor_d
        actual = mejor
        restantes.remove(mejor)

    return total, ruta
