
class Casilla:
    
    '''
        Clase que define cada una de las casillas del tablero
    '''

    def __init__(self, value):
        self.isLit = False
        self.value = value

    def __str__(self):
        return "Test" 

    def is_block(self):
        '''
            Retorna True si es que la casilla contiene un 
            bloque que sea 0, 1, 2, 3, 4 o una casilla Negra.
        '''
        return self.value in [0,1,2,3,4,'N']

    def is_numeric_block(self):
        return self.value in [0,1,2,3,4]

    def is_bulb(self):
        return self.value == 'A'

    def allows_bulb(self):
        return not self.is_block() and not self.is_bulb() and self.value != 'X' and not self.isLit

    def empty_not_lit(self):
        return self.value == 'B' and not self.isLit

    def is_empty(self):
        return self.value == 'B'