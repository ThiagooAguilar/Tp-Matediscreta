from src.graph import  Graph
class AdjMatrix(Graph):
    def __init__(self):
        self.nodes = []
        self.matrix = []
    def add_vertex(self, v):
        # me añada un nodo
        if v not in self.nodes:
            self.nodes.append(v)
            for u in self.matrix:
                u.append(False)
            self.matrix.append([False] * len(self.nodes))



    def add_edge(self, u, v):
        if v  in self.nodes or u  in self.nodes:
            indexu = self.nodes.index(u)
            indexv = self.nodes.index(v)
            return self.matrix[indexu][indexv] == True and self.matrix[indexv][indexu] == True

        # me agrega un arista donde u y v son los nodos a conectar
        # asigno a los valores de la lista con lista en 1 cuando existe la conexión


    def delete_vertex(self, v):

        if v not in self.nodes:
            return None

        index = self.nodes.index(v)
        self.matrix.pop(index)

        for row in self.matrix:
            row.pop(index)


        self.nodes.pop(index)

    def delete_edge(self, u, v):
        indexu = self.nodes.index(u)
        indexv = self.nodes.index(v)
        if self.matrix[indexu][indexv] == False:
            return None
        else:
            self.matrix[indexv][indexu] = False
            self.matrix[indexu][indexv] = False



    def exist_vertex(self, v):
        return v in self.nodes

    def exist_edge(self, u, v):
        indexu = self.nodes.index(u)
        indexv = self.nodes.index(v)
        return self.matrix[indexu][indexv]

    def order(self):
        return len(self.nodes)

    def edge_count(self):
        count=0
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.matrix[i][j]:
                    count += 1
        return count


    def get_lassos(self):
        result=0
        for v in range(len(self.nodes)):
            if self.matrix[v][v]:
                result+=1
        return result

    def array_with_lassos(self):
        array=[]
        for i in  range ( len ( self.nodes)):
            if self.matrix[i][i]:
                array.append(self.nodes[i])

        return array


    def is_isolated(self, v):
        if v not in self.nodes:
            return None
        return not any(self.matrix[self.nodes.index(v)])

    def arrar_with_isolated(self):
        array=[]
        for i in range ( len ( self.nodes)):
            if  not any(self.matrix[self.nodes.index(i)]):
                array.append(self.nodes[i])
        return array

    def remove_lassos_and_isolated(self):
        new_graph = AdjMatrix()

        valid_nodes = [
            self.nodes[i] for i in range(len(self.nodes))
            if not self.matrix[i][i] and any(self.matrix[i])
        ]


        for v in valid_nodes:
            new_graph.add_vertex(v)

        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if self.matrix[i][j]:
                    u, v = self.nodes[i], self.nodes[j]
                    if u in valid_nodes and v in valid_nodes:
                        new_graph.add_edge(u, v)

        return new_graph

    def matrix_adyacence(self):
        return self.matrix

    def get_incidence_matrix(self):
        edges = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):  # solo mitad superior
                if self.matrix[i][j]:
                    edges.append((self.nodes[i], self.nodes[j]))

        n = len(self.nodes)
        m = len(edges)
        incidence = [[0] * m for _ in range(n)]

        # Lleno la matriz de incidencia
        for col, (u, v) in enumerate(edges):
            iu = self.nodes.index(u)
            iv = self.nodes.index(v)
            incidence[iu][col] = 1
            incidence[iv][col] = 1


        return incidence


    def __str__(self):
        edges=[]
        for i,row in enumerate(self.matrix):
            for j in range(i,len(row)):
                if self.matrix[i][j]:
                    edges.append((self.nodes[j],self.nodes[i]))

        return f"Nodes:{self.nodes} Edges: {edges}"
