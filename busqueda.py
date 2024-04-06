from nodos import *
from heurísticas import *

from abc import abstractmethod
from abc import ABCMeta



#Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass



### BÚSQUEDAS NO INFORMADAS
class BusquedaAnchura(Busqueda): #Implementa la búsqueda en anchura
    
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



class BusquedaProfundidad(Busqueda): # Implementa la búsqueda en profundidad
    
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



class BusquedaProfundidadIterativa(Busqueda): # Implementa la búsqueda en profundidad con cota iterativa

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
        


### BÚSQUEDAS INFORMADAS
class BusquedaVoraz_manhattan(Busqueda): # Implementa la búsqueda voraz usando la heurística de Manhattan
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
            abiertos.sort(key=lambda x: heuristica_manhattan(x.estado.cubo))
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



class BusquedaVoraz_comprueba_cara(Busqueda): # Implementa la búsqueda voraz usando la heurística del nº de caras en la casilla correcta
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
            abiertos.sort(key=lambda x: heuristica_comprueba_cara(x.estado.cubo))
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


class BusquedaAEstrella_manhattan(Busqueda): # Implementa la búsqueda A* usando la heurística de Manhattan
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAEstrella(inicial, None, None, 0, heuristica_manhattan(inicial.cubo)))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            # Ordenar la lista de abiertos según la heurística
            abiertos.sort(key=lambda x: x.coste_f)
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        sucesor_g = nodoActual.coste_g + 1
                        sucesor_f = sucesor_g + heuristica_manhattan(hijo.cubo)

                        nuevoNodoSucesor = NodoAEstrella(hijo, nodoActual, operador, sucesor_g, sucesor_f)
                        
                        abiertos.append(nuevoNodoSucesor)
                        cerrados[hijo.cubo.visualizar()] = hijo

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        


class BusquedaAEstrella_comprueba_cara(Busqueda): # Implementa la búsqueda A* usando la heurística del nº de caras en la casilla correcta
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAEstrella(inicial, None, None, 0, heuristica_comprueba_cara(inicial.cubo)))
        cerrados[inicial.cubo.visualizar()] = inicial

        while not solucion and len(abiertos) > 0:
            # Ordenar la lista de abiertos según la heurística
            abiertos.sort(key=lambda x: x.coste_f)
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado

            if actual.esFinal():
                solucion = True
            
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        sucesor_g = nodoActual.coste_g + 1
                        sucesor_f = sucesor_g + heuristica_comprueba_cara(hijo.cubo)

                        nuevoNodoSucesor = NodoAEstrella(hijo, nodoActual, operador, sucesor_g, sucesor_f)
                        
                        abiertos.append(nuevoNodoSucesor)
                        cerrados[hijo.cubo.visualizar()] = hijo

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        

class BusquedaIDA_manhattan(Busqueda): # Implementa la búsqueda IDA* usando la heurística de Manhattan
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        nueva_cota = heuristica_manhattan(inicial.cubo)

        while not solucion:
            cota = nueva_cota
            nueva_cota = float('inf')
            abiertos = []
            abiertos.append(NodoAEstrella(inicial, None, None, 0, heuristica_manhattan(inicial.cubo)))

            while not solucion and len(abiertos) > 0:
                abiertos.sort(key=lambda x: x.coste_f)
                nodoActual = abiertos.pop(0)
                actual = nodoActual.estado

                if actual.esFinal():
                    solucion = True
                else:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        sucesor_g = nodoActual.coste_g + 1
                        sucesor_f = sucesor_g + heuristica_manhattan(hijo.cubo)
                        
                        if sucesor_f <= cota:
                            nuevoNodoSucesor = NodoAEstrella(hijo, nodoActual, operador, sucesor_g, sucesor_f)
                            abiertos.append(nuevoNodoSucesor)
                        else:
                            nueva_cota = min(nueva_cota, sucesor_f)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None
        


class BusquedaIDA_comprueba_cara(Busqueda): # Implementa la búsqueda IDA* usando la heurística del nº de caras en la casilla correcta
    
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        nueva_cota = heuristica_comprueba_cara(inicial.cubo)

        while not solucion:
            cota = nueva_cota
            nueva_cota = float('inf')
            abiertos = []
            abiertos.append(NodoAEstrella(inicial, None, None, 0, heuristica_comprueba_cara(inicial.cubo)))

            while not solucion and len(abiertos) > 0:
                abiertos.sort(key=lambda x: x.coste_f)
                nodoActual = abiertos.pop(0)
                actual = nodoActual.estado

                if actual.esFinal():
                    solucion = True
                else:
                    for operador in actual.operadoresAplicables():
                        hijo = actual.aplicarOperador(operador)
                        sucesor_g = nodoActual.coste_g + 1
                        sucesor_f = sucesor_g + heuristica_comprueba_cara(hijo.cubo)
                        
                        if sucesor_f <= cota:
                            nuevoNodoSucesor = NodoAEstrella(hijo, nodoActual, operador, sucesor_g, sucesor_f)
                            abiertos.append(nuevoNodoSucesor)
                        else:
                            nueva_cota = min(nueva_cota, sucesor_f)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None