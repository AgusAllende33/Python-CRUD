from modelo import Crud
from tkinter import Frame
from tkinter import StringVar
from tkinter import ttk
from tkinter import Label
from tkinter import Entry
from tkinter import Button


class Ventanita:
    def __init__(self, window):
        self.root = window
        r_i = "img\icono.ico"
        self.root.iconbitmap(r_i)
        self.root.title("CRUD de usuarios")
        self.frame = Frame(self.root, width=613, height=681)
        self.frame.pack()
        self.objeto_base = Crud()
        self.usu = StringVar()
        self.car = StringVar()

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("col2", "col3")
        self.tree.heading("#0", text="Id")
        self.tree.heading("col2", text="Usuario")
        self.tree.heading("col3", text="Cargo")
        self.tree.column("#0", width=50, minwidth=50)
        self.tree.column("col2", width=200, minwidth=200)
        self.tree.column("col3", width=200, minwidth=200)
        self.tree.place(x=1, y=230, width=611, height=450)
        self.style = ttk.Style()
        self.style.configure("Treeview", background="#777")
        self.style.configure("Treeview.Heading", font=("Verdana Negrita", 14, "bold"))

        self.v1 = Label(
            self.root,
            text="Ingrese sus datos",
            bg="black",
            foreground="#fff",
            font=("Verdana Negrita", 22),
        )
        self.v2 = Label(self.root, text="Usuario:", font=("Verdana Negrita", 15))
        self.v3 = Entry(self.root, textvariable=self.usu)
        self.v4 = Label(self.root, text="Cargo:", font=("Verdana Negrita", 15))
        self.v5 = Entry(self.root, textvariable=self.car)
        self.boton_a = Button(
            text="Alta", font=("Verdana", 12), command=lambda: self.insert()
        )
        self.boton_cc = Button(
            text="Cambiar color de fondo",
            font=("Verdana", 12),
            command=lambda: self.change1(),
        )
        self.boton_c = Button(
            text="Usuarios registrados",
            font=("Verdana", 12),
            command=lambda: self.consulta(),
        )
        self.boton_e = Button(
            text="Eliminar", font=("Verdana", 12), command=lambda: self.delete()
        )
        self.boton_m = Button(
            text="Modificar", font=("Verdana", 12), command=lambda: self.mod()
        )

        self.v1.place(x=1, y=1, width=611)
        self.v2.place(x=10, y=55)
        self.v3.place(x=150, y=62, width=200, height=23)
        self.v4.place(x=10, y=82)
        self.v5.place(x=150, y=89, width=200, height=23)
        self.boton_a.place(x=362, y=55, width=250)
        self.boton_m.place(x=362, y=89, width=250)
        self.boton_cc.place(x=362, y=123, width=250)
        self.boton_c.place(x=362, y=157, width=250)
        self.boton_e.place(x=362, y=191, width=250)

    def change1(
        self,
    ):
        self.objeto_base.change1(self.v2, self.v4, self.frame)

    def insert(
        self,
    ):
        self.objeto_base.insert(self.usu, self.car, self.tree)

    def delete(
        self,
    ):
        self.objeto_base.delete(self.tree)

    def mod(
        self,
    ):
        self.objeto_base.mod(
            self.tree,
            self.boton_m,
            self.usu,
            self.car,
            self.boton_a,
            self.boton_e,
            self.boton_c,
        )

    def mod2(
        self,
    ):
        self.objeto_base.mod2(
            self.usu,
            self.car,
            self.tree,
            self.boton_m,
            self.boton_a,
            self.boton_e,
            self.boton_c,
        )

    def consulta(
        self,
    ):
        self.objeto_base.consulta(self.tree)

    def act_tree(
        self,
    ):
        self.objeto_base.act_tree(self.tree)
