class Movimiento:
    def __init__(self, nombre, tipo, poder):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder


class Pokemon:
    def __init__(self, nombre, tipo, ps, movimientos):
        self.nombre = nombre
        self.tipo = tipo
        self.ps = ps
        self.movimientos = movimientos

    def esta_vivo(self):
        return self.ps > 0
    
    