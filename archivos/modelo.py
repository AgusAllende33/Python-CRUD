from peewee import SqliteDatabase, CharField, Model, IntegrityError
from tkinter.messagebox import showinfo, showerror
import re
from tkinter.colorchooser import askcolor
import os
import datetime
import tkinter as tk
from observador import Sujeto

db = SqliteDatabase("mi_base.db")


class BaseModel(Model):
    class Meta:
        database = db


class Usuarios(BaseModel):
    usuario = CharField(unique=True)
    cargo = CharField()


db.connect()
db.create_tables([Usuarios])


class RegistroLogError(Exception):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(BASE_DIR, "log.txt")

    def __init__(self, error, archivo, fecha):
        self.error = error
        self.archivo = archivo
        self.fecha = fecha

    def registrar_error(self):
        p = "---" * 50
        with open(self.ruta, "a") as log:
            log.write(
                f"\nSe ha dado un error: {self.error}  |  Archivo: {self.archivo}  |  Fecha y hora: {self.fecha}\n{p}"
            )


def registro_de_errores(func):
    def env(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            reg_log = RegistroLogError(str(e), "modelo.py", datetime.datetime.now())
            reg_log.registrar_error()
            raise

    return env


class Crud(Sujeto):
    def __init__(
        self,
    ):
        pass

    @registro_de_errores
    def insert(self, usuario, cargo, mitreeview):
        er = re.compile(r"\w+(\s|\w+)\w+")
        data_usuario = usuario.get()
        data_cargo = cargo.get()
        if not re.fullmatch(er, data_usuario) or not re.fullmatch(er, data_cargo):
            showerror(
                "Error",
                "No validado, por favor inserte caracteres alfanuméricos e/o inserte tanto usuario como cargo",
            )
            usuario.set("")
            cargo.set("")
            raise re.error(
                "No validado, por favor inserte caracteres alfanuméricos e/o inserte tanto usuario como cargo"
            )

        else:
            Usuarios.create(usuario=data_usuario, cargo=data_cargo)
            self.act_tree(mitreeview)
            showinfo("Aviso", "Usuario registrado correctamente")
            self.notificar(usuario.get(), cargo.get())
            usuario.set("")
            cargo.set("")

    @registro_de_errores
    def delete(self, mitreeview):
        item_sel = mitreeview.focus()
        try:
            valor_id = mitreeview.item(item_sel)
            borrar = Usuarios.get(Usuarios.id == valor_id["text"])
            borrar.delete_instance()
            self.act_tree(mitreeview)
            showinfo("Aviso", "Usuario eliminado correctamente")
        except:
            showinfo("Aviso", "Seleccione un usuario a eliminar")

    @registro_de_errores
    def mod(self, mitreeview, boton_m, usuario, cargo, boton_a, boton_e, boton_c):
        m = mitreeview.selection()
        if m:
            boton_a.config(state=tk.DISABLED)
            boton_e.config(state=tk.DISABLED)
            boton_c.config(state=tk.DISABLED)

            boton_m.config(
                text="Terminar modificacion",
                command=lambda: self.mod2(
                    usuario, cargo, mitreeview, boton_m, boton_a, boton_e, boton_c
                ),
            )
            showinfo("Aviso", "Introduzca los datos modificados en los campos")
        else:
            showinfo("Aviso", "No se ha seleccionado ningun elemento")

    @registro_de_errores
    def mod2(self, usuario, cargo, mitreeview, boton_m, boton_a, boton_e, boton_c):
        er = re.compile(r"\w+(\s|\w+)\w+")
        data_usuario = usuario.get()
        data_cargo = cargo.get()
        try:
            if not re.fullmatch(er, data_usuario) or not re.fullmatch(er, data_cargo):
                showerror(
                    "No validado, por favor inserte caracteres alfanuméricos e/o inserte tanto usuario como cargo"
                )
                raise re.error(
                    "No validado, por favor inserte caracteres alfanuméricos e/o inserte tanto usuario como cargo"
                )

            else:
                item_sel = mitreeview.focus()
                valor_id = mitreeview.item(item_sel)
                Usuarios.update(usuario=data_usuario, cargo=data_cargo).where(
                    Usuarios.id == valor_id["text"]
                ).execute()
                boton_a.config(state=tk.NORMAL)
                boton_e.config(state=tk.NORMAL)
                boton_c.config(state=tk.NORMAL)
                boton_m.config(
                    text="Modificar",
                    font=("Verdana", 12),
                    command=lambda: self.mod(
                        mitreeview, boton_m, usuario, cargo, boton_a, boton_c, boton_e
                    ),
                )
                self.act_tree(mitreeview)
                showinfo("Aviso", "Usuario registrado correctamente")
        except IntegrityError as e:
            showerror("Error", "El usuario ya esta registrado")
            raise re.error(
                "No validado, por favor inserte caracteres alfanuméricos e/o inserte tanto usuario como cargo"
            )

        finally:
            usuario.set("")
            cargo.set("")

    @registro_de_errores
    def consulta(self, usuario):
        for usuario in Usuarios.select():
            usu_sel = usuario.select()
        trad = len(usu_sel)
        if trad > 1:
            cont = str(trad), "usuarios", "registrados"
            showinfo("Consulta", cont[0:])
        else:
            cont = str(trad), "usuario", "registrado"
            showinfo("Consulta", cont[0:])

    @registro_de_errores
    def change1(self, v2, v4, frame):
        color = askcolor(color="#00ff00", title="Seleccion de color de fondo")
        if color[1]:
            v2.config(fg="#000")
            v4.config(fg="#000")
            frame.config(bg=color[1])
            v2.config(bg=color[1])
            v4.config(bg=color[1])
        if color[1] == "#000000":
            v2.config(fg="#fff")
            v4.config(fg="#fff")

    @registro_de_errores
    def act_tree(self, mitreeview):
        try:
            mitreeview.delete(*mitreeview.get_children())
            for fila in Usuarios.select():
                mitreeview.insert(
                    "", 0, text=fila.id, values=(fila.usuario, fila.cargo)
                )
        except Exception as e:
            raise (f"Error en act_tree: {e}")
