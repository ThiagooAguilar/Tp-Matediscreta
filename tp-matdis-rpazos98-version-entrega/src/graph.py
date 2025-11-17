from abc import ABC, abstractmethod
##matriz de adyacencia
class Graph(ABC):
    # para la implementacion vamos a usar una lista de lista siendo la matriz
    # y una lista con todos los vertices y en que indice estan en mi lista de lista

    @abstractmethod
    def add_vertex(self, v):
        # me añada un nodo
        # genero una lista de lista
        pass

    def add_edge(self, u, v):
        # me agrega un arista donde u y v son los nodos a conectar
        # asigno a los valores de la lista con lista en 1 cuando existe la conexión
        pass

    def delete_vertex(self, v):
        pass

    def delete_edge(self, u, v):
        # busco si existe la conexion
            #--> no existe tiro excepcion
            #--> reemplazo por cero en la matriz
        pass

    def exist_vertex(self, v):
        pass

    def exist_edge(self, u, v):
        pass

    def order(self):
        pass

    def edge_count(self):
        # voy hasta la diagonal y cuento ya que se que la matriz tiene propiedad
        # que es simetrica, para lograr eficiencia
        # o agarrar un count y en el add_edge
        pass

    def get_vertex(self, v):
        # me devuelve el indice
        # si el vertice guarda un dato deberia devolver un objeto vertice
        pass

    def get_adjacency_vertex(self, v):
        # me devuelve una lista con los nodos que puedo recorrer con v
        pass

