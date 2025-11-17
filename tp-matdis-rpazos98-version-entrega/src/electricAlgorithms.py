## Redes conexas
## grado de cada nodo


def encontrar_componentes_conexos(graph):
    """
     Encuentra todos los componentes conexos de un grafo 
     
     Args: toma como argumento un diccionario de  clave nodo valor lista de adyacencia
     Lista de listas donde cada lista son los nodos conexos
     
     """

    visitados = set()
    componentes = []

    for nodo in graph:
        if nodo not in visitados:
            componente_actual = []
            pila = [nodo]
            visitados.add(nodo)

            while pila:
                u = pila.pop()
                componente_actual.append(u)

                # Recorrer vecinos
                for v in graph.get(u, []):
                    if v not in visitados:
                        visitados.add(v)
                        pila.append(v)

            componente_actual.sort()
            componentes.append(componente_actual)

    return componentes



def criticidad_de_componentes(graph):

    """
    Me devuelve el numero de conexiones que tiene cada nodo
    Args:  Toma como argumento un diccionario de clave nodo valor lista de adyacencia
    retorna el numero de conexiones que tiene cada nodo
    """
    criticidad = {}
    ## me creo un un mapa que contendra el grado y todos los nodos que contengan ese valor
    for nodo, vecinos in graph.items():
        grado = len(vecinos)

        if grado not in criticidad:
            criticidad[grado] = [nodo]
        else:
            criticidad[grado].append(nodo)

    for grado in criticidad:
        criticidad[grado].sort()

    return criticidad