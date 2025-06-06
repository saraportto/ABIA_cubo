
#Nodos a almacenar como parte de los algoritmos de búsqueda

class Nodo:
    def __init__(self, estado, padre):
        self.estado = estado
        self.padre = padre



#Nodos usados por la BusquedaAnchura. 
#Añade el Operador usado para generar el estado almacenado en este Nodo. 
#Usado para simplificar la reconstrucción del camino solución.

class NodoAnchura(Nodo):
    def __init__(self, estado, padre, operador):
        super().__init__(estado, padre)
        self.operador = operador


class NodoProfundidad(Nodo):
    def __init__(self, estado, padre, operador, profundidad):
        super().__init__(estado, padre)
        self.operador = operador
        self.profundidad = profundidad


class NodoAEstrella(Nodo):
    def __init__(self, estado, padre, operador, coste_g, coste_f):
        super().__init__(estado, padre)
        self.operador = operador
        self.coste_g = coste_g
        self.coste_f = coste_f
