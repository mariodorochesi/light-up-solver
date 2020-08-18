
class Action:
    '''
        Define una accion a aplicar sobre un tablero
        de Light-Up
    '''

    def __init__(self, pos_x, pos_y, value):
        '''
            Se inicializa una accion recibiendo por parametro
            la posicion en x e y donde se coloca la ampolleta.
        '''
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.value = value

    def __str__(self):
        '''
            Se sobrescribe la funcion a llamar cuando se intente
            imprimir el objeto Action.
        '''
        return 'Insertar {} en coordenadas {},{}'.format(self.value, self.pos_x, self.pos_y)
