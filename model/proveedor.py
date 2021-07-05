class Proveedor:
    def __init__(self, id, n, f):
       self.idproveedor = id
       self.nombre = n
       self.fono = f
    def getResumen(self):
        return f"Id: {self.idproveedor} - {self.nombre} - Telefono: {self.fono} "
    def getId(self):
        return self.idproveedor