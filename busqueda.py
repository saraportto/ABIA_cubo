from nodos import *


from abc import abstractmethod
from abc import ABCMeta


#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass



#Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
#Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None



class BusquedaProfundidad(Busqueda):
    
    #Implementa la búsqueda en anchura. Si encuentra solución recupera la lista de Operadores empleados almacenada en los atributos de los objetos NodoAnchura
    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()]=inicial
        while not solucion and len(abiertos)>0:
            nodoActual = abiertos.pop(-1)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                #cerrados[actual.cubo.visualizar()] = actual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None



class BusquedaProfundidadIterativa(Busqueda):

    def buscarSolucion(self,inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        profundidad_maxima = 1 
        abiertos.append(NodoProfundidad(inicial, None, None,0))
        cerrados[inicial.cubo.visualizar()]=inicial

        while not solucion:
            while not solucion and len(abiertos) > 0:
                nodoActual = abiertos.pop(-1)
                actual = nodoActual.estado
                if actual.esFinal():
                    solucion = True

                elif nodoActual.profundidad < profundidad_maxima: 
                    #cerrados[actual.cubo.visualizar()] = actual
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        if hijo.cubo.visualizar() not in cerrados.keys() and hijo.cubo.visualizar() not in abiertos:
                            abiertos.insert(0, NodoProfundidad(hijo, nodoActual, operador, nodoActual.profundidad + 1))
                            cerrados[hijo.cubo.visualizar()] = hijo #utilizamos CERRADOS para mantener también traza de los nodos añadidos a ABIERTOS 
                            print(profundidad_maxima)
                            profundidad_maxima +=1
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre != None: #Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        

class BusquedaVoraz(Busqueda):
    cara_opuesta = {
        0: 5,
        1: 3,
        2: 4,
        3: 1,
        4: 2,
        5: 0
    }


    @staticmethod
    def heuristica(cubo) -> int:
        distancia = 0

        for num_cara, cara in enumerate(cubo.caras):
            for num_casilla, casilla in enumerate(cara.casillas):
                distancia += BusquedaVoraz.distancia(casilla, (num_cara, num_casilla))
    
        return distancia  # Devuelve la distancia total calculada
    
    @staticmethod
    def distancia(casilla, pos_actual) -> int:
        if pos_actual[1] != casilla.posicionCorrecta and pos_actual[1] != 8:
            dist_cara = 2  # Si la posición actual no es la correcta
        else:
            dist_cara = 0  # Si la posición actual es la correcta o el centro

        if pos_actual[0] != casilla.color:
            if pos_actual[0] == BusquedaVoraz.cara_opuesta[casilla.color]:
                dist_color = 6  # Si el color actual es el opuesto
            else:
                dist_color = 3  # Si el color actual no es el correcto ni el opuesto
        else:
            dist_color = 0

        return dist_cara + dist_color  # Devuelve la distancia calculada

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial
        
        while not solucion and len(abiertos) > 0:
            # Ordenar la lista de abiertos según la heurística
            abiertos.sort(key=lambda x: self.heuristica(x.estado.cubo))
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None: # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
