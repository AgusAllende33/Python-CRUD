import os


class Sujeto:

    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, arg1, arg2):
        for observador in self.observadores:
            observador.update(arg1, arg2)


class Observador:
    def update(self):
        raise NotImplementedError("Delegación de registro")


class ConcreteObserverA(Observador):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(BASE_DIR, "Notificaciones.txt")

    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, arg1, arg2):
        p = "---" * 50
        with open(self.ruta, "a") as log:
            log.write("Notificacion de CRUD, Se ha hecho un nuevo registro: ")
            log.write("\n")
            log.write(str(arg1))
            log.write(", ")
            log.write(str(arg2))
            log.write("\n")
            log.write(p)
            log.write("\n")
