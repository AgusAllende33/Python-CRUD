import tkinter as tk
import socket
import threading


class ServidorTCP:
    def __init__(self, window):
        self.root = window
        self.root.title("Servidor TCP")
        self.root.geometry("1200x1200")
        r_i = "img\icono2.ico"
        self.root.iconbitmap(r_i)
        self.textarea = tk.Text(self.root, bg="white")
        self.textarea.pack(fill=tk.BOTH, expand=True)
        self.server_socket = None
        self.ejecutando = False
        self.btn_iniciar = tk.Button(
            self.root, text="Iniciar servidor", command=self.iniciar_servidor
        )
        self.btn_iniciar.pack(pady=10)

        self.btn_detener = tk.Button(
            self.root,
            text="Detener servidor",
            command=self.detener_servidor,
            state=tk.DISABLED,
        )
        self.btn_detener.pack(pady=5)

        self.servidor = None

    def iniciar_servidor(self):
        if not self.ejecutando:
            self.ejecutando = True

            self.btn_iniciar.config(state=tk.DISABLED)
            self.btn_detener.config(state=tk.NORMAL)

            self.servidor = threading.Thread(target=self.iniciar_conexion)
            self.servidor.daemon = True
            self.servidor.start()

            self.log("Servidor iniciado.")

    def detener_servidor(self):
        if self.ejecutando:
            self.ejecutando = False
            if self.servidor:
                try:
                    self.servidor.join()
                except Exception as e:
                    print(f"Error al detener el servidor: {e}")

    def iniciar_conexion(self):
        HOST = "127.0.0.1"
        PORT = 51624
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen()

        self.log(f"Servidor escuchando en {HOST}:{PORT}")

        while self.ejecutando:
            try:
                conn, addr = self.server_socket.accept()
                with conn:
                    self.log(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
                    while self.ejecutando:
                        data = conn.recv(7024)
                        contenido = data.decode()
                        if not data:
                            break
                        self.log(contenido)
            except:
                if self.ejecutando:
                    self.log(f"Error durante la aceptación de conexiones: {e}")

        if self.server_socket:
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
                self.server_socket.close()
            except Exception as e:
                self.log(f"Error al cerrar el socket del servidor: {e}")

    def log(self, message):
        self.textarea.insert(tk.END, f"{message}\n")
        self.textarea.see(tk.END)
