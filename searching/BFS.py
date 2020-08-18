
class BFS:
    '''
        Clase para aplicar una busqueda Breath First Search
    '''
    def __init__(self, initial_state):
        # Se define la Cola donde almacenar los estados a visitar
        self.stack = list()
        if initial_state.is_final_state():
            print('El estado ingresado ya es solucion')
            sys.exit(0)
        else:
            print('Inicializando BFS')
            print('Estado Inicial :')
            print(initial_state)
            # Se inserta el primer elemento en la Pila
            self.stack.append(initial_state)
    
    def solve(self, notify = 100):
        # Se define un contador para calcular la cantidad de iteraciones
        iter_cont = 0
        while(len(self.stack) > 0):
            iter_cont +=1
            # Se obtiene el elemento del comienzo de la cola
            state = self.stack.pop(0)
            # Si el estado es un estado final valido entonces se finaliza
            if state.is_final_state():
                print('Se han necesitado {} iteraciones para encontrar una solucion'.format(iter_cont))
                return state
            # Se obtienen todas las acciones posibles para el estado
            actions = state.get_actions()
            # Se itera para cada accion de la lista de acciones
            for action in actions:
                # Se aplica la transicion obteniendo un nuevo estado
                state_s = state.transition(action)
                # Si el estado no ha sido visitado
                self.stack.append(state_s)
            if iter_cont % notify == 0:
                print('Iteracion {}'.format(iter_cont))
                print(state)
        return None
