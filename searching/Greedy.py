import time
import random
from datetime import datetime
import sys

class Greedy:

    def __init__(self,
                initial_state,
                notify_progress = True,
                notify_iterations = 10000,
                show_solution = False,
                show_execution_time = False,
                show_iterations = False,
                show_initial_state = False,
                show_initial_instance_name = True,
                time_limit = 120):
        # Se define la Cola donde almacenar los estados a visitar
        self.stack = list()
        self.actual = initial_state
        self.initial_time = time.time()
        self.time_limit = time_limit
        if initial_state.is_final_state():
            print('El estado ingresado ya es solucion')
            #sys.exit(0)
        else:
            print('Inicializando GREEDY')
            print('Estado Inicial :')
            print(initial_state)

    def solve(self):
        '''
            Metodo resolutivo mediante Greedy
        '''
        #Contador de iteraciones del solver
        iter = 0
        #Se obtienen las primeras acciones para el estado inicial
        self.stack = self.actual.get_actions()
        
        #Se inicia greedy
        while(len(self.stack) > 0):
            if time.time() - self.initial_time > self.time_limit:
                print('Se ha abortado la solucion por tiempo limite alcanzado.')
                return None
            if(self.actual.is_final_state() ):
                print("Solucion Encontrada") 
                break
            #Guarda el valor del estado mas prometedor
            val_max = 0
            change = False
            #Busqueda del proximo estado mas prometedor bajo nuestra heuristica
            for x in self.stack:
                #Se realiza una copia del estado actual aplicandole la transicion x
                piv_state = (self.actual.copy()).transition(x)
                #Verifica el valor de la ponderacion de piv_state, si es mayor que el valor del actual estado prometedor se elige piv_state
                if( val_max < self.ponderateAction(piv_state) ):
                    #Se le da prioridad a que tenga mas estados o que sea un estado final
                    if(len(piv_state.get_actions()) > 0 or piv_state.is_final_state()):
                        val_max = self.ponderateAction(piv_state)
                        self.actual = piv_state.copy()
                        change = True
                        if(piv_state.is_final_state()):
                            break
                    
            if(change):
                self.stack = self.actual.get_actions()
            else:
                #El estado actual no es capaz de realizar mas transiciones
                print("SALIO PORQUE LLEGA A UN ESTADO SIN ACCIONES")
                break
            #nueva iteracion del solver
            iter +=1 

        print('Solucion Greedy')
        print('Iter: ' + str(iter) + " - Time: {} ".format(time.time() -self.initial_time))
        print(self.actual)
        if(self.actual.is_final_state()): 
            self.actual.taken_time = time.time() -self.initial_time
            return self.actual
        else: 
            return None
    
    def ponderateAction(self,state):
        '''
            Pondera la cantidad de casilla que se iluminan en el estado propuesto
            si el estado no es valido, se pasa un 0
        '''
        if(not(state.is_valid_state())):
            return 0
        else: 
            #x = state.valorated_space()
            return state.eval()



class Grasp:
    
    def __init__(self, 
                initial_state,
                notify_progress = True,
                notify_iterations = 10000,
                show_solution = False,
                show_execution_time = False,
                show_iterations = False,
                show_initial_state = False,
                show_initial_instance_name = True,
                time_limit = 120):
        # Se define la Cola donde almacenar los estados a visitar
        self.stack = list()
        self.actual = initial_state
        self.initial_time = time.time()
        random.seed(datetime.now())
        self.time_limit = time_limit
        
        if initial_state.is_final_state():
            print('El estado ingresado ya es solucion')
        else:
            print('Inicializando GRASP')
            print('Estado Inicial :')
            print(initial_state)
        
    def solve(self):
        '''
            Metodo resolutivo mediante GRASP
        '''
        #Contador de iteraciones del solver
        iter = 0
        #Se obtienen las primeras acciones para el estado inicial
        self.stack = self.actual.get_actions()
        
        #Se inicia Grasp
        while(len(self.stack) > 0):
            if time.time() - self.initial_time > self.time_limit:
                print('Se ha abortado la solucion por tiempo limite alcanzado.')
                return None
            change = False
            val_max = 0
            if(self.actual.is_final_state()):
                print("Hay solucion ")
                break
            
            for x in self.stack:
                #Se realiza una copia del estado actual aplicandole la transicion x
                piv_state = (self.actual.copy()).transition(x)
                #Verifica el valor de la ponderacion de piv_state, si es mayor que el valor del actual estado prometedor se elige piv_state
                if( val_max <= self.ponderateAction(piv_state) ):
                    #Se le da prioridad a que tenga mas estados o que sea un estado final
                    if(len(piv_state.get_actions()) > 0 or piv_state.is_final_state()):
                        val_max = self.ponderateAction(piv_state)
                        self.actual = piv_state.copy()
                        change = True
                        if(piv_state.is_final_state()):
                            break
                    
            if(change):
                self.stack = self.actual.get_actions()
            else:
                #El estado actual no es capaz de realizar mas transiciones
                #print("SALIO PORQUE LLEGA A UN ESTADO SIN VALOR")
                break
            iter +=1

        print('Solucion Grasp')
        print('Iter: ' + str(iter) + " - Time: {} ".format(time.time() -self.initial_time))
        print(self.actual)

        if(self.actual.is_final_state()): 
            self.actual.taken_time = time.time() -self.initial_time
            return self.actual
        return None
          

    def ponderateAction(self,state):
        '''
            Pondera la cantidad de casilla que se iluminan en el estado propuesto
            si el estado no es valido, se pasa un 0
        '''
        if(not(state.is_valid_state())):
            return 0
        else: 
            x = state.valorated_space()
            alpha = random.random()
            return alpha*x[0] + (1-alpha)*x[1]