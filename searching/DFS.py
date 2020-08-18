import sys
import time
class DFS:
    '''
        Clase para aplicar una busqueda Depth Fist Search 
    '''
    def __init__(self, 
                initial_state,
                notify_progress = True,
                notify_iterations = 10000,
                show_solution = False,
                show_execution_time = False,
                show_iterations = False,
                show_initial_state = False,
                show_initial_instance_name = True):
        # Se define la Pila donde almacenar los estados a visitar
        self.stack = list()
        if initial_state.is_final_state():
            print('El estado ingresado ya es solucion')
            sys.exit(0)
        else:
            if show_initial_instance_name:
                print('Inicializando DFS para resolver : {}'.format(initial_state.file_name))
            if show_initial_state:
                print('Estado Inicial :')
                print(initial_state)
            # Se inserta el primer elemento en la Pila
            self.stack.append(initial_state)
            # Configuracion para encontrar solucion final
            self.show_solution = show_solution
            # Configuracion para mostrar tiempo tomado
            self.show_execution_time = show_execution_time
            # Configuracion para mostrar notificaciones de progreso
            self.notify_progress = notify_progress
            # Configuracion para cada cuantas iteraciones mostrar progreso
            self.notify_iterations = notify_iterations
            # Configuracion para mostrar cantidad de iteraciones para llegar a solucion
            self.show_iterations = show_iterations
    
    def solve(self):
        # Se define un contador para calcular la cantidad de iteraciones
        iter_cont = 0
        # Se toma el tiempo de inicio del programa
        start_time = time.time()
        while(len(self.stack) > 0):
            iter_cont +=1
            # Se obtiene el elemento del comienzo de la pila
            state = self.stack.pop()
            # Si el estado es un estado final valido entonces se finaliza
            if state.is_final_state():
                if self.show_iterations:
                    print('Se han necesitado {} iteraciones para encontrar una solucion'.format(iter_cont))
                if self.show_solution:
                    print(state)
                if self.show_execution_time:
                    print('Se ha necesitado {} segundos para encontrar una solucion'.format(time.time() - start_time))
                return state
            # Se obtienen todas las acciones posibles para el estado
            actions = state.get_actions()
            # Se itera para cada accion de la lista de acciones
            for action in actions:
                # Se aplica la transicion obteniendo un nuevo estado
                state_s = state.transition(action)
                # Si el estado no ha sido visitado
                self.stack.append(state_s)
            if iter_cont % self.notify_iterations == 0 and self.notify_progress:
                print('Iteracion {}'.format(iter_cont))
                print(state)
        return None
