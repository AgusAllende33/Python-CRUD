import vista
from tkinter import Tk
import observador
import socket
import os


class Controller:
    def __init__(self, root):
        self.root_controler = root
        self.objeto_view = vista.Ventanita(self.root_controler)
        self.el_observador = observador.ConcreteObserverA(self.objeto_view.objeto_base)
        self.HOST = "192.168.0.11"  # Dirección IP del servidor
        self.PORT = 139  # Puerto del servidor

    def enviar_log_servidor(self, log):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((self.HOST, self.PORT))  # Conectar al servidor
                client_socket.sendall(log.encode())  # Enviar log al servidor
            except Exception as e:
                print(f"Error al enviar log al servidor: {e}")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    log = os.path.join(BASE_DIR, "log.txt")
    root_tk = Tk()
    application = Controller(root_tk)
    application.objeto_view.act_tree()
    application.enviar_log_servidor(log)

    root_tk.mainloop()
