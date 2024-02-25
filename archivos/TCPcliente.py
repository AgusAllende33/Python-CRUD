import socket
import tkinter as tk
from tkinter import filedialog
import os
import time

HOST = "127.0.0.1"
PORT = 51624

if __name__ == "__main__":
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo de texto", filetypes=[("Archivos de texto", "*.txt")]
    )

    if file_path:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            timestamp = os.path.getmtime(file_path)
            print("Se seleccionó el archivo:", file_path)
            with open(file_path, "r") as log1:
                print("Enviando log:")
                log3 = log1.read()
                client_socket.sendall(log3.encode())

            while True:
                current_timestamp = os.path.getmtime(file_path)
                if current_timestamp != timestamp:
                    timestamp = current_timestamp
                    with open(file_path, "r") as file:
                        content = file.read()
                        client_socket.sendall(content.encode())
                        print("El log ha sido enviado.")
                    time.sleep(1)
                else:
                    pass

    else:
        print("La selección de archivo fue cancelada por el usuario.")

    root = tk.Tk()
    root.withdraw()
