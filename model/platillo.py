class Platillo:

    def __init__(self, id, d, n, p):
        self.idplatillo = id
        self.disponibilidad = d
        self.nombrep = n
        self.precio = p

    def getResumen(self):
        return f"{self.idplatillo} - {self.nombrep} - {self.precio} Bs"
