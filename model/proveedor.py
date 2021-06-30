class Proveedor:
    def __init__(self, id, n, f):
       self.idproveedor = id
       self.nombre = n
       self.fono = f
    def getResumen(self):
        return f"{self.idproveedor} - {self.nombre} - {self.fono} "