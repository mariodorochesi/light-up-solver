import numpy as np
import copy
from .Casilla import Casilla
from .Action import Action


class State:
    '''
        Clase que define la representacion de un estado
        cualquiera para el juego Light-Up
    '''

    def __init__(self, tablero):
        '''
            Funcion que inicializa el tablero. 
            Para ello recibe por parametro la ruta a un archivo
            lo lee y carga los datos en una matriz llamada tablero.
        '''
        self.tamano = None
        self.file_name = tablero
        if tablero is not None:
            fila = 1
            # Se abre el archivo en modo lectura
            archivo = open(tablero, 'r')
            linea = archivo.readline()
            # Se verifica que el tamano no haya sido inferido aun del archivo
            if self.tamano is None:
                # Se obtiene el tamano de las instancias
                self.tamano = int(linea.strip().split(',')[0]) + 2
                # Se vectoriza la clase Casilla
                vCasilla = np.vectorize(Casilla)
                # Se crea una matriz inicial de Tamano X Tamano
                init_arr = np.arange(self.tamano*self.tamano).reshape((self.tamano,self.tamano))
                lattice = np.empty((self.tamano,self.tamano), dtype=object)
                # Se rellena la matriz con los objetos vectorizados
                lattice[:,:] = vCasilla(init_arr)
                self.tablero = lattice
                # En este proceso de inicializa el tablero con Casillas
                # de valor 0
                for i in range(self.tamano):
                    for j in range(self.tamano):
                        self.tablero[i][j] = Casilla('X')
                for i in range(1,self.tamano-1):
                    for j in range(1,self.tamano-1):
                        self.tablero[i][j] = Casilla('B')
            for linea in archivo:
                linea = linea.strip().split(',')
                if int(linea[0]) == 9:
                    self.tablero[int(linea[1])+1][int(linea[2])+1] = Casilla('N')
                else:
                    self.tablero[int(linea[1])+1][int(linea[2])+1] = Casilla(int(linea[0]))
            self.lista_acciones = list()
        else:
            raise Exception('No se ha pasado por parametro la ruta del archivo que contiene el tablero a resolver.')
    
    def __str__(self):
        '''
            Se sobrescribe el metodo __str__ para definir
            como se debe comportar el objeto cuando es llamado
            por la funcion print.
        '''
        nombre = ''
        for i in range(1,self.tamano-1):
            for j in range(1,self.tamano-1):
                if self.tablero[i][j].isLit and self.tablero[i][j].value == 'B':
                    nombre = nombre +  ' ' + 'I'
                else:
                    nombre = nombre +  ' ' + str(self.tablero[i][j].value)
            nombre = nombre + '\n'
        return nombre

    def copy(self):
        '''
            Retorna una copia de si mismo
        '''
        return copy.deepcopy(self)

    def get_actions(self):
        '''
            Se genera las lista de acciones posibles
            para la casilla mas prometedora.
        '''
        actions = list()

        
        for i in range(1, self.tamano-1):
            for j in range(1, self.tamano-1):
                if self.tablero[i][j].is_numeric_block():
                    if self.tablero[i-1][j].allows_bulb():
                        action = Action(i-1,j,'A')
                        if self.copy().transition(action).is_valid_state():
                            actions.append(action)
                    if self.tablero[i+1][j].allows_bulb():
                        action = Action(i+1,j,'A')
                        if self.copy().transition(action).is_valid_state():
                            actions.append(action)
                    if self.tablero[i][j-1].allows_bulb():
                        action = Action(i,j-1,'A')
                        if self.copy().transition(action).is_valid_state():
                            actions.append(action)
                    if self.tablero[i][j+1].allows_bulb():
                        action = Action(i,j+1,'A')
                        if self.copy().transition(action).is_valid_state():
                            actions.append(action)
                if (len(actions) > 0) : return actions

        for i in range(1, self.tamano-1):
            for j in range(1, self.tamano-1):
                if self.tablero[i][j].isLit == False and self.tablero[i][j].value == 'B':
                    action = Action(i,j,'A')
                    estado = self.copy().transition(action)
                    if estado.is_valid_state():
                        actions.append(action)
                        #return actions
        return actions

    def transition(self, action):
        '''
            Se aplica una transicion al estado
        '''
        # Se copia el estado
        estado_nuevo = self.copy()
        # Se inserta la ampolleta en la posicion indicada por la accion
        estado_nuevo.tablero[action.pos_x][action.pos_y].value = action.value
        # Se ilumina a la izquierda de la ampolleta
        if action.value == 'A':
            for i in range(action.pos_y-1, 0, -1):
                if(not estado_nuevo.tablero[action.pos_x][i].is_block()):
                    estado_nuevo.tablero[action.pos_x][i].isLit = True
                else:
                    break
            # Se ilumina a la derecha de la ampolleta
            for i in range(action.pos_y+1, self.tamano-1):
                if(not estado_nuevo.tablero[action.pos_x][i].is_block()):
                    estado_nuevo.tablero[action.pos_x][i].isLit = True
                else:
                    break
            # Se ilumina hacia abajo de la ampolleta
            for i in range(action.pos_x+1, self.tamano-1):
                if(not estado_nuevo.tablero[i][action.pos_y].is_block()):
                    estado_nuevo.tablero[i][action.pos_y].isLit = True
                else:
                    break
            # Se ilumina hacia arriba de la ampolleta
            for i in range(action.pos_x-1, 0, -1):
                if(not estado_nuevo.tablero[i][action.pos_y].is_block()):
                    estado_nuevo.tablero[i][action.pos_y].isLit = True
                else:
                    break
        estado_nuevo.lista_acciones.append(action)
        return estado_nuevo

    def is_valid_state(self):
        '''
            Define si un estado es valido o no.

            Para ello verifica que todo bloque numerico contenga
            a su alrededor a lo mas la misma cantidad de ampolletas
            que su bloque indica. En caso contrario se descarta el estado.

            Ademas de lo anteior, si es que una ampolleta esta siendo iluminada
            por otra ampolleta tambien se descarta el estado.
        '''
        for i in range(1, self.tamano-1):
            for j in range(1, self.tamano-1):
                # Si el estado es un bloque numerico
                if self.tablero[i][j].is_numeric_block():
                    cont = 0
                    # Se comprueba si tiene una ampolleta a la izquierda
                    if self.tablero[i][j-1].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta a la derecha
                    if self.tablero[i][j+1].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta arriba
                    if self.tablero[i-1][j].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta abajo
                    if self.tablero[i+1][j].is_bulb():
                        cont += 1
                    # Si tiene mas ampolletas de las que su numero indica se descarta
                    if cont > self.tablero[i][j].value:
                        return False
                elif self.tablero[i][j].is_bulb():
                    # Si la ampolleta esta siendo iluminada se descarta
                    if self.tablero[i][j].isLit:
                        return False
        return True

    def is_final_state(self):
        '''
            Define si el estado es un estado final del problema o no.

            Para ello se considera que todo espacio blanco del tablero debe
            encontrarse iluminado, y ademas debe ser un estado valido, siguiendo
            la logica del metodo anterior
        '''
        for i in range(1, self.tamano-1):
            for j in range(1, self.tamano-1):
                if self.tablero[i][j].value == 'B' and self.tablero[i][j].isLit == False:
                    return False
                # Si el estado es un bloque numerico
                if self.tablero[i][j].is_numeric_block():
                    cont = 0
                    # Se comprueba si tiene una ampolleta a la izquierda
                    if self.tablero[i][j-1].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta a la derecha
                    if self.tablero[i][j+1].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta arriba
                    if self.tablero[i-1][j].is_bulb():
                        cont += 1
                    # Se comprueba si tiene una ampolleta abajo
                    if self.tablero[i+1][j].is_bulb():
                        cont += 1
                    # Si tiene mas ampolletas de las que su numero indica se descarta
                    if cont != self.tablero[i][j].value:
                        return False
                elif self.tablero[i][j].is_bulb():
                    # Si la ampolleta esta siendo iluminada se descarta
                    if self.tablero[i][j].isLit:
                        return False
        return True


class StatePreProcessor:

    def __init__(self, state : State):
        self.state = state

    def process_state(self):
        print('Preprocesando : ')
        empty = self.state.tamano * self.state.tamano
        while(self.get_empty() < empty):
            self.verificar_completitud()
            self.verificar_completitud_anulada()
            empty = self.get_empty()
        return self.state

    def get_empty(self):
        cont = 0
        for i in range(1, self.state.tamano-1):
            for j in range(1, self.state.tamano-1):
                if self.state.tablero[i][j].empty_not_lit():
                    cont = cont + 1
        return cont

    def verificar_completitud(self):
        '''
            Si el número en un cuadrado negro es igual a la cantidad de espacios 
            blancos disponibles + ampolletas adyacentes a este , entonces se inserta 
            una ampolleta en cada uno de los espacios blancos adyacentes
        '''
        for i in range(1, self.state.tamano-1):
            for j in range(1, self.state.tamano-1):
                if self.state.tablero[i][j].is_numeric_block():
                    cont = 0
                    cont_b = 0
                    if self.state.tablero[i-1][j].empty_not_lit():
                        cont += 1
                    if self.state.tablero[i+1][j].empty_not_lit():
                        cont += 1
                    if self.state.tablero[i][j-1].empty_not_lit():
                        cont += 1
                    if self.state.tablero[i][j+1].empty_not_lit():
                        cont += 1
                    if self.state.tablero[i-1][j].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i+1][j].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i][j-1].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i][j+1].is_bulb():
                        cont_b += 1
                    if cont + cont_b == self.state.tablero[i][j].value:
                        if self.state.tablero[i-1][j].allows_bulb():
                            self.state = self.state.transition(Action(i-1,j,'A'))
                        if self.state.tablero[i+1][j].allows_bulb():
                            self.state = self.state.transition(Action(i+1,j,'A'))
                        if self.state.tablero[i][j-1].allows_bulb():
                            self.state = self.state.transition(Action(i,j-1,'A'))
                        if self.state.tablero[i][j+1].allows_bulb():
                            self.state = self.state.transition(Action(i,j+1,'A'))

    def verificar_completitud_anulada(self):
        for i in range(1, self.state.tamano-1):
            for j in range(1, self.state.tamano-1):
                if self.state.tablero[i][j].is_numeric_block():
                    cont_b = 0
                    if self.state.tablero[i-1][j].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i+1][j].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i][j-1].is_bulb():
                        cont_b += 1
                    if self.state.tablero[i][j+1].is_bulb():
                        cont_b += 1
                    if cont_b == self.state.tablero[i][j].value:
                        if self.state.tablero[i-1][j].empty_not_lit():
                            self.state = self.state.transition(Action(i-1,j,'X'))
                        if self.state.tablero[i+1][j].empty_not_lit():
                            self.state = self.state.transition(Action(i+1,j,'X'))
                        if self.state.tablero[i][j-1].empty_not_lit():
                            self.state = self.state.transition(Action(i,j-1,'X'))
                        if self.state.tablero[i][j+1].empty_not_lit():
                            self.state = self.state.transition(Action(i,j+1,'X'))
