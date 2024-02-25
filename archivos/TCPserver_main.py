from tkinter import Tk
import TCPserver_MV


class Controller:
    def __init__(self, root):
        self.root_controler = root
        self.objeto_view = TCPserver_MV.ServidorTCP(self.root_controler)


if __name__ == "__main__":
    root_tk = Tk()
    app = Controller(root_tk)
    root_tk.mainloop()
