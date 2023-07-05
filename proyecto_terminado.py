import tkinter as tk
import psycopg2
from tkinter import messagebox
from tkinter import ttk
from customtkinter  import CTk, CTkFrame, CTkEntry, CTkLabel,CTkButton,CTkCheckBox
from tkinter import PhotoImage

# Conectar a la base de datos
conn = psycopg2.connect(database="db_colegio", user="postgres", password="80434894")

#Clase para el Login
class Login():
    def __init__(self):
        self.username_entry = None
        self.password_entry = None
        self.usuario_actual = None

    def login(self):
        self.root = CTk() 
        self.root.geometry("500x600+350+20")
        self.root.minsize(480,500)
        self.root.config(bg ='#010101')
        self.root.title("Iniciar Sesion")
        #En lo que respecta de estas lineas es la alineacion de la ventana y como se va a centrar.
        ancho_ventana = self.root.winfo_width()
        alto_ventana = self.root.winfo_height()
        posicion_x = self.root.winfo_screenwidth() // 2 - ancho_ventana // 2
        posicion_y = self.root.winfo_screenheight() // 2 - alto_ventana // 1
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

        #Se establece el fondo
        frame = CTkFrame(self.root, fg_color='#010101')
        frame.grid(column=0, row = 0, sticky='nsew')
        #Se establecen que cuando se cambie la dimension este se vaya adaptando
        frame.columnconfigure([0,1], weight=1)
        frame.rowconfigure([0,1,2,3,5,6], weight=1)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        #Opcional en el caso que se desee implementar una imagen
        #logo = PhotoImage(file='imagenes/logo.png') 
        #CTkLabel(frame, image = logo).grid(columnspan=2, row=0)

        aviso_label = tk.Label(frame, text="LOGIN", font=("Poppins Medium", 40), bg='#010101', fg='#2cb67d')
        aviso_label.grid(columnspan=2)
        
        correo = CTkEntry(frame, placeholder_text='Usuario', border_color='#2cb67d', fg_color='#FFFFFF', width=220, height=40,justify="center")
        correo.configure(font=('Poppins light', 12))
        correo.grid(columnspan=2)
        #Se almacena el correo para su verificacion
        self.correo_entry = correo
                
        contra = CTkEntry(frame, placeholder_text='Contraseña',show="*", border_color='#2cb67d', fg_color='#FFFFFF', width=220, height=40,justify="center")
        contra.configure(font=('poppins light', 12))
        contra.grid(columnspan=2)
        #Se almacena la contraseña para su verificacion
        self.contra_entry = contra
        
        #En el caso que se desee implementar un check
        '''checkbox = CTkCheckBox(frame, text="Recordarme",hover_color='#7f5af0', 
            border_color='#2cb67d', fg_color='#2cb67d')
        checkbox.grid(columnspan=2, row=3,padx=4, pady =4)
                                                            '''
        #Boton para el inicio de sesion
        bt_iniciar = CTkButton(frame, border_color='#2cb67d', fg_color='#010101', hover_color='#2cb67d', corner_radius=12, border_width=2, text='INICIAR SESIÓN', command=self.verificacion)
        bt_iniciar.configure(font=('poppins light', 12))
        bt_iniciar.grid(columnspan=2)
        # Vincular el evento <Return> al botón de iniciar sesión
        contra.bind("<Return>", lambda event: bt_iniciar.invoke())
        bt_salir = CTkButton(frame, border_color='#2cb67d', fg_color='#010101', hover_color='#2cb67d', corner_radius=12, border_width=2, text='Cerrar', command=self.cerrar)
        bt_salir.configure(font=('poppins light', 12))
        bt_salir.grid(columnspan=2)

        # Establecer el enfoque en el botón "Cerrar"
        bt_salir.focus_set()

        # Vincular el evento <Escape> a la ventana principal
        self.root.bind("<Escape>", lambda event: self.cerrar())

        #Donde se realiza la llamada para la carga del logo
        #self.root.call('wm', 'iconphoto', self.root._w, logo)
        self.root.mainloop()

    def cerrar(self):
        self.root.destroy()

    def verificacion(self):
        username = self.correo_entry.get()
        password = self.contra_entry.get()

        # Verificar si el usuario existe en la base de datos
        cur = conn.cursor()
        cur.execute("SELECT id,tipo_usuario FROM usuario WHERE nombre = %s AND password = %s", (username, password))
        result = cur.fetchone()
        print(result) # Imprimir el resultado de la consulta

        if result is not None:
            tipo_usuario = result[1]
            self.usuario_actual = result[0] # Asignar el valor del ID del usuario actual

            # Cerrar la ventana de inicio de sesión
            self.root.destroy()

            # Abrir la ventana correspondiente según el tipo de usuario
            if tipo_usuario == 2:
                user_window = tk.Tk()
                labeluser = User(user_window, result[0])
                labeluser.pack()
                user_window.mainloop()                
            elif tipo_usuario == 1:
                profe = tk.Tk()
                labeladmin = Profe(profe)
                profe.mainloop()
            elif tipo_usuario == 3:
                admin = tk.Tk()
                labeladmin = Admi(admin)
                admin.mainloop()    
            else:
                # Si las credenciales son incorrectas, mostrar un mensaje de error
                error = tk.Tk()
                error_label = tk.Label(error, text="Error, verificar tipo de usuario en la base de datos")
                error_label.pack()
                error.mainloop()
        else:
            self.usuario_actual = None

    def show(self):
        self.login()
        
#Clase para el tipo Profesor
class Profe():
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x600")
        self.master.title("Panel de administrador")

        # Configurar estilo para los widgets
        bg_color = "#010101"  # Color de fondo
        fg_color = "#ffffff"  # Color de texto
        font_style = "Poppins 14 bold"  # Estilo de fuente

        # Crear frame principal con color de fondo
        main_frame = tk.Frame(self.master, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Agregar etiqueta de aviso en el frame principal
        aviso_label = tk.Label(main_frame, text="OPCIONES DE ADMINISTRADOR", font=("Poppins Medium", 20), bg=bg_color, fg=fg_color)
        aviso_label.pack(pady=10)

        # Crear y agregar botones en el frame principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }

        #Se crea el boton que llama a la funcion para agregar las materias a los Alumnos
        add_subject_button = tk.Button(main_frame, text="Agregar materias a Alumnos", command=self.agregar_materias, **button_style)
        add_subject_button.pack(pady=7)
        add_subject_button.bind("<Enter>", lambda event: add_subject_button.configure(bg='#2cb67d', fg='#010101'))
        add_subject_button.bind("<Leave>", lambda event: add_subject_button.configure(bg='#010101', fg='#2cb67d'))

        #Se crea el boton que llama a la funcion para visualizar a los Alumnos
        listauser_button = tk.Button(main_frame, text="Ver Alumnos", command=lambda: self.ver(2), **button_style)
        listauser_button.pack(pady=7)
        listauser_button.bind("<Enter>", lambda event: listauser_button.configure(bg='#2cb67d', fg='#010101'))
        listauser_button.bind("<Leave>", lambda event: listauser_button.configure(bg='#010101', fg='#2cb67d'))

        #Se crea el boton para salir/volver al login.
        salir_button = tk.Button(main_frame, text="Salir", command=self.mostrar_login, **button_style)
        salir_button.pack(pady=7)
        salir_button.bind("<Enter>", lambda event: salir_button.configure(bg='#2cb67d', fg='#010101'))
        salir_button.bind("<Leave>", lambda event: salir_button.configure(bg='#010101', fg='#2cb67d'))

    def mostrar_login(self):
        self.master.destroy()  # Cerrar la ventana actual de administrador
        login = Login()
        login.show()
 
    def agregar_materias(self):
        # Crear ventana para agregar materias a usuarios
        add_subject_window = tk.Toplevel(self.master)
        add_subject_window.geometry("500x500")
        add_subject_window.title("Agregar materias a Alumnos")
        add_subject_window.config(bg='#010101')

        aviso_label = tk.Label(add_subject_window, text="Proceda a la Carga", font=('Poppins 20 bold'), bg='#010101', fg='#2cb67d')
        aviso_label.pack()

        # Agregar widgets para la entrada del ID del usuario y la materia a agregar
        id_label = tk.Label(add_subject_window, text="ID del usuario:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        id_label.pack()
        id_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        id_entry.pack()

        # Agregar widgets para la entrada de la materia
        materia_label = tk.Label(add_subject_window, text="Materia:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        materia_label.pack()
        materia_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        materia_entry.pack()

        # Agregar widgets para la entrada de la nota
        nota_label = tk.Label(add_subject_window, text="Nota:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        nota_label.pack()
        nota_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        nota_entry.pack()

        # Crear y agregar botones en el update_window principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }
        # Agregar botón para agregar la materia al usuario
        add_button = tk.Button(add_subject_window, text="Agregar",command=lambda: self.agregar_materia_a_usuario(id_entry.get(),materia_entry.get(),nota_entry.get(), add_subject_window), **button_style)
        add_button.pack(pady=5)
        # Configurar el estilo del botón cuando el mouse está sobre él
        add_button.bind("<Enter>", lambda event: add_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        add_button.bind("<Leave>", lambda event: add_button.configure(bg='#010101', fg='#2cb67d'))

    def agregar_materia_a_usuario(self, id_usuario,notas, materia,add_subject_window):

        # Verificar si el tipo de usuario es válido para la carga de notas
        cur = conn.cursor()
        cur.execute("SELECT tipo_usuario FROM usuario WHERE id = %s", (id_usuario,))
        result = cur.fetchone()

        if result is not None:
            tipo_usuario = result[0]
            if tipo_usuario == 2:
                # Agregar la materia al usuario en la base de datos
                cur.execute("INSERT INTO notas (id_usuario, notas, materia) VALUES (%s, %s, %s)", (id_usuario, materia, notas))
                conn.commit()
                messagebox.showinfo(title="Nota Cargada", message="El usuario con ID {} ha optenido su calificación exitosamente.".format(id_usuario))
            else:
                messagebox.showerror(title="Tipo de usuario no válido", message="El tipo de usuario no es válido para la carga de notas.")
        else:
            messagebox.showerror(title="Usuario no encontrado", message="El usuario con ID {} no ha podido ser localizado.".format(id_usuario))

        # Cerrar la ventana de carga de notas del usuario
        add_subject_window.destroy()

    def ver(self, tipo_usuario):
        # Crear la ventana de notas
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, tipo_usuario, password, curso FROM usuario WHERE tipo_usuario = %s ORDER BY id", (tipo_usuario,))
        results = cur.fetchall()
        ver_window = tk.Toplevel(self.master)
        ver_window.geometry("650x300")
        ver_window.title("USUARIOS")
        # Agregar una tabla de notas
        ver_table = ttk.Treeview(ver_window)
        ver_table['columns'] = ('ID', 'Nombre','Tipo Usuario','Password', 'Curso')
        ver_table.column('#0', width=0, stretch=tk.NO)
        ver_table.column('ID', anchor=tk.CENTER, width=100)
        ver_table.column('Nombre', anchor=tk.CENTER, width=100)
        ver_table.column('Tipo Usuario', anchor=tk.CENTER, width=100)
        ver_table.column('Password', anchor=tk.CENTER, width=100)
        ver_table.column('Curso', anchor=tk.CENTER, width=100)

        ver_table.heading('#0', text='')
        ver_table.heading('ID', text='ID', anchor=tk.CENTER)
        ver_table.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        ver_table.heading('Tipo Usuario', text='Tipo Usuario', anchor=tk.CENTER)
        ver_table.heading('Password', text='Password', anchor=tk.CENTER)
        ver_table.heading('Curso', text='Curso', anchor=tk.CENTER)
        

        for user in results:
            ver_table.insert('', 'end', text='', values=user)

        ver_table.pack(padx=5, pady=5, fill='both', expand=True)

#Clase para el tipo Administrador
class Admi():
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x600")
        self.master.title("Panel de administrador")

        # Configurar estilo para los widgets
        bg_color = "#010101"  # Color de fondo
        fg_color = "#ffffff"  # Color de texto
        font_style = "Poppins 14 bold"  # Estilo de fuente

        # Crear frame principal con color de fondo
        main_frame = tk.Frame(self.master, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Agregar etiqueta de aviso en el frame principal
        aviso_label = tk.Label(main_frame, text="OPCIONES DE ADMINISTRADOR", font=("Poppins Medium", 20), bg=bg_color, fg=fg_color)
        aviso_label.pack(pady=10)

        # Crear y agregar botones en el frame principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }


        new_user_button = tk.Button(main_frame, text="Crear nuevo usuario", command=self.crear_usuario, **button_style)
        new_user_button.pack(pady=7)
        # Configurar el estilo del botón cuando el mouse está sobre él
        new_user_button.bind("<Enter>", lambda event: new_user_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        new_user_button.bind("<Leave>", lambda event: new_user_button.configure(bg='#010101', fg='#2cb67d'))

        update_user_button = tk.Button(main_frame, text="Actualizar usuario", command=self.actualizar_usuario, **button_style)
        update_user_button.pack(pady=7)
        update_user_button.bind("<Enter>", lambda event: update_user_button.configure(bg='#2cb67d', fg='#010101'))
        update_user_button.bind("<Leave>", lambda event: update_user_button.configure(bg='#010101', fg='#2cb67d'))

        delete_user_button = tk.Button(main_frame, text="Eliminar usuario", command=self.eliminar_usuario, **button_style)
        delete_user_button.pack(pady=7)
        delete_user_button.bind("<Enter>", lambda event: delete_user_button.configure(bg='#2cb67d', fg='#010101'))
        delete_user_button.bind("<Leave>", lambda event: delete_user_button.configure(bg='#010101', fg='#2cb67d'))

        add_subject_button = tk.Button(main_frame, text="Agregar materias a usuarios", command=self.agregar_materias, **button_style)
        add_subject_button.pack(pady=7)
        add_subject_button.bind("<Enter>", lambda event: add_subject_button.configure(bg='#2cb67d', fg='#010101'))
        add_subject_button.bind("<Leave>", lambda event: add_subject_button.configure(bg='#010101', fg='#2cb67d'))

        listadmi_button = tk.Button(main_frame, text="Ver Administradores", command=lambda: self.ver(1), **button_style)
        listadmi_button.pack(pady=7)
        listadmi_button.bind("<Enter>", lambda event: listadmi_button.configure(bg='#2cb67d', fg='#010101'))
        listadmi_button.bind("<Leave>", lambda event: listadmi_button.configure(bg='#010101', fg='#2cb67d'))

        listauser_button = tk.Button(main_frame, text="Ver Usuarios", command=lambda: self.ver(2), **button_style)
        listauser_button.pack(pady=7)
        listauser_button.bind("<Enter>", lambda event: listauser_button.configure(bg='#2cb67d', fg='#010101'))
        listauser_button.bind("<Leave>", lambda event: listauser_button.configure(bg='#010101', fg='#2cb67d'))


        salir_button = tk.Button(main_frame, text="Salir", command=self.mostrar_login, **button_style)
        salir_button.pack(pady=7)
        salir_button.bind("<Enter>", lambda event: salir_button.configure(bg='#2cb67d', fg='#010101'))
        salir_button.bind("<Leave>", lambda event: salir_button.configure(bg='#010101', fg='#2cb67d'))

    def mostrar_login(self):
        self.master.destroy()  # Cerrar la ventana actual de administrador
        login = Login()
        login.show()
 
    def crear_usuario(self):
        # Crear la ventana de creación de usuario
        new_user_window = tk.Toplevel(self.master)
        new_user_window.geometry("500x500")
        new_user_window.title("Crear nuevo usuario")
        new_user_window.config(bg='#010101')

        aviso_label = tk.Label(new_user_window, text="Carga de Usuarios", font=('Poppins 20 bold'), bg='#010101', fg='#2cb67d')
        aviso_label.pack()

        # Agregar widgets para la entrada de datos del nuevo usuario
        username_label = tk.Label(new_user_window, text="Nombre de usuario:", font=('Poppins 14'), bg='#010101', fg='#ffffff')
        username_label.pack()
        username_entry = tk.Entry(new_user_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        username_entry.pack()

        password_label = tk.Label(new_user_window, text="Contraseña:", font=('Poppins 14'), bg='#010101', fg='#ffffff')
        password_label.pack()
        password_entry = tk.Entry(new_user_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        password_entry.pack()

        aviso_label = tk.Label(new_user_window, text="Seleccione el tipo", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        aviso_label.pack()

        type_var = tk.StringVar(value="0")

        def toggle_create_button():
            if type_var.get() == "1":
                aviso_label1.pack_forget()  # Ocultar el label si se selecciona "1"     
                create_button.pack()
                curso_menu.pack_forget()
                create_button.pack()
            elif type_var.get() == "2":
                aviso_label1.pack()  # Mostrar el label si se selecciona "2"
                curso_var.set("1")
                create_button.pack_forget()
                curso_menu.pack()
                create_button.pack()

        aviso_label1 = tk.Label(new_user_window, text="Seleccione el Curso", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        curso_var = tk.StringVar(new_user_window)
        curso_options = ["1", "2", "3", "4", "5"]
        curso_menu = tk.OptionMenu(new_user_window, curso_var, *curso_options)

        # Configurar valor inicial
        curso_var.set("99")

        # Ocultar el menú desplegable al inicio
        curso_menu.pack_forget()

        type_admin_rb = tk.Radiobutton(new_user_window, text="Profesor", variable=type_var, value="1", command=toggle_create_button, bg='#010101', fg='#ffffff')
        type_admin_rb.pack()

        type_user_rb = tk.Radiobutton(new_user_window, text="Alumno", variable=type_var, value="2", command=toggle_create_button, bg='#010101', fg='#ffffff')
        type_user_rb.pack()

        # Crear y agregar botones en el frame principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }
        # Botón de creación
        create_button = tk.Button(new_user_window, text="Crear usuario", command=lambda: self.guardar_usuario(username_entry.get(), password_entry.get(), type_var.get(), new_user_window), **button_style)

    # Campos para usuarios de tipo "Usuario"
        curso_label = tk.Label(new_user_window, text="Curso:", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        curso_entry = tk.Entry(new_user_window)
        create_button = tk.Button(new_user_window, text="Crear usuario", command=lambda: self.guardar_usuario1(username_entry.get(), password_entry.get(), type_var.get(),curso_var.get(), new_user_window), **button_style)

    # Mostrar el botón apropiado al iniciar
        toggle_create_button()
  
        # Configurar el estilo del botón cuando el mouse está sobre él
        create_button.bind("<Enter>", lambda event: create_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        create_button.bind("<Leave>", lambda event: create_button.configure(bg='#010101', fg='#2cb67d'))

    def guardar_usuario(self, username, password, tipo, new_user_window):
        # Guardar el nuevo usuario en la base de datos
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (nombre, password, tipo_usuario) VALUES (%s, %s, %s, %s)", (username, password, tipo))
        conn.commit()
        # Cerrar la ventana de creación de usuario
        new_user_window.destroy()
        self.master.deiconify()
        messagebox.showinfo(title="Nuevo usuario creado", message="El usuario {} ha sido creado exitosamente.".format(username))

    def guardar_usuario1(self, username, password, tipo, curso,new_user_window):
        # Guardar el nuevo usuario en la base de datos
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (nombre, password, tipo_usuario,curso) VALUES (%s, %s, %s,%s)", ( username, password, tipo, curso))
        conn.commit()

        # Cerrar la ventana de creación de usuario
        new_user_window.destroy()
        self.master.deiconify()
        messagebox.showinfo(title="Nuevo usuario creado", message="El usuario {} ha sido creado exitosamente.".format(username))

    def actualizar_usuario(self):
        # Crear la ventana de actualización de usuario
        update_window = tk.Toplevel(self.master)
        update_window.geometry("600x400")
        update_window.title("Actualizar usuario")
        update_window.config(bg='#010101')

        aviso_label = tk.Label(update_window, text="Complete el Formulario para Actualizar", font=('Poppins 20 bold'), bg='#010101', fg='#2cb67d')
        aviso_label.pack()

        # Agregar widgets para la entrada de credenciales
        id_label = tk.Label(update_window, text="ID de usuario:", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        id_label.pack()
        id_entry = tk.Entry(update_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        id_entry.pack()

        username_label = tk.Label(update_window, text="Nombre de usuario:", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        username_label.pack()
        username_entry = tk.Entry(update_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        username_entry.pack()

        password_label = tk.Label(update_window, text="Contraseña:", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        password_label.pack()
        password_entry = tk.Entry(update_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        password_entry.pack()

        type_var = tk.StringVar(value="0")

        def toggle_create_button():
            if type_var.get() == "1":
                aviso_label1.pack_forget()  # Ocultar el label si se selecciona "1"     
                update_button.pack()
                curso_menu.pack_forget()
                update_button.pack()
            elif type_var.get() == "2":
                aviso_label1.pack()  # Mostrar el label si se selecciona "2"
                curso_var.set("1")
                update_button.pack_forget()
                curso_menu.pack()
                update_button.pack()

        aviso_label1 = tk.Label(update_window, text="Seleccione el Curso", font=('Poppins 12'), bg='#010101', fg='#ffffff')
        curso_var = tk.StringVar(update_window)
        curso_options = ["1", "2", "3", "4", "5"]
        curso_menu = tk.OptionMenu(update_window, curso_var, *curso_options)

        type_admin_rb = tk.Radiobutton(update_window, text="Profesor", variable=type_var, value="1", command=toggle_create_button,font=('Poppins 12'), bg='#010101', fg='#ffffff')
        type_admin_rb.pack()

        type_user_rb = tk.Radiobutton(update_window, text="Alumno", variable=type_var, value="2", command=toggle_create_button,font=('Poppins 12'), bg='#010101', fg='#ffffff')
        type_user_rb.pack()

        # Crear y agregar botones en el update_window principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }

        # Agregar botón para actualizar usuario
        update_button = tk.Button(update_window, text="Actualizar", command=lambda: self.update_user_db(username_entry.get(),password_entry.get(),type_var.get(),  id_entry.get(), update_window), **button_style)
        update_button.pack(pady=10)

        update_button = tk.Button(update_window, text="Actualizar", command=lambda: self.update_user_db2(username_entry.get(),password_entry.get(),curso_var.get(),type_var.get(), id_entry.get(), update_window), **button_style)
        update_button.pack(pady=10)
        # Configurar el estilo del botón cuando el mouse está sobre él
        update_button.bind("<Enter>", lambda event: update_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        update_button.bind("<Leave>", lambda event: update_button.configure(bg='#010101', fg='#2cb67d'))

        update_window.mainloop()

    def update_user_db(self, username, password, tipo, id, update_window):
        # Actualizar los datos del usuario en la base de datos
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET nombre=%s,  tipo_usuario=%s, password=%s WHERE id = %s", (username, tipo, password, id))
        conn.commit()
        cur.close()

        # Cerrar la ventana de actualización
        update_window.destroy()
        self.master.deiconify()
        messagebox.showinfo(title="Usuario Modificado!", message="El usuario {} ha sido modificado exitosamente.".format(username))

    def update_user_db2(self, username, password, tipo, curso, id,update_window):
        # Actualizar los datos del usuario en la base de datos
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET nombre=%s,  tipo_usuario=%s, password=%s, curso=%s WHERE id = %s", (username, tipo, password, curso,id))
        conn.commit()
        cur.close()

        # Cerrar la ventana de actualización
        update_window.destroy()
        self.master.deiconify()
        messagebox.showinfo(title="Usuario Modificado!", message="El usuario {} ha sido modificado exitosamente.".format(username))

    def eliminar_usuario(self):
        # Crear la ventana de eliminación de usuario
        delete_window = tk.Toplevel(self.master)
        delete_window.geometry("800x300")
        delete_window.title("Eliminar Usuario")
        delete_window.config(bg='#010101')

        aviso_label = tk.Label(delete_window, text="Introduzca el ID o el Nombre para su eliminacion", font=('Poppins 20 bold'), bg='#010101', fg='#2cb67d')
        aviso_label.pack()


        # Agregar widgets para la entrada de ID del usuario a eliminar
        id_label = tk.Label(delete_window, text="ID del usuario:", font=('Poppins 14'), bg='#010101', fg='#ffffff')
        id_label.pack()
        id_entry = tk.Entry(delete_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        id_entry.pack()

        #Captura el nombre para que pueda borrar indistintamente
        nombre_label = tk.Label(delete_window, text="Nombre del usuario:", font=('Poppins 14'), bg='#010101', fg='#ffffff')
        nombre_label.pack()
        nombre_entry = tk.Entry(delete_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        nombre_entry.pack()

        # Crear y agregar botones en el update_window principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }
        # Agregar botón para eliminar el usuario
        delete_button = tk.Button(delete_window, text="Eliminar", command=lambda: self.borrar_usuario(id_entry.get(),nombre_entry.get(),delete_window), **button_style)
        delete_button.pack(pady=5)
        # Configurar el estilo del botón cuando el mouse está sobre él
        delete_button.bind("<Enter>", lambda event: delete_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        delete_button.bind("<Leave>", lambda event: delete_button.configure(bg='#010101', fg='#2cb67d'))

    def borrar_usuario(self, id_usuario, nombre,delete_window):
        #Si el Usuario ingresa por ID se borra
        if id_usuario:
            cur = conn.cursor()
            cur.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))
            conn.commit()
            messagebox.showinfo(title="Usuario eliminado", message="El usuario con ID {} ha sido eliminado exitosamente.".format(id_usuario))
        #Si opta por borrar por nombre se borra.
        elif nombre:
            cur = conn.cursor()
            cur.execute("DELETE FROM usuario WHERE nombre = %s", (nombre,))
            conn.commit()
            messagebox.showinfo(title="Usuario eliminado", message="El usuario con nombre {} ha sido eliminado exitosamente.".format(nombre))

        # Cerrar la ventana de eliminación de usuario
        delete_window.destroy()

    def agregar_materias(self):
        # Crear ventana para agregar materias a usuarios
        add_subject_window = tk.Toplevel(self.master)
        add_subject_window.geometry("500x500")
        add_subject_window.title("Agregar materias a usuarios")
        add_subject_window.config(bg='#010101')

        aviso_label = tk.Label(add_subject_window, text="Proceda a la Carga", font=('Poppins 20 bold'), bg='#010101', fg='#2cb67d')
        aviso_label.pack()

        # Agregar widgets para la entrada del ID del usuario y la materia a agregar
        id_label = tk.Label(add_subject_window, text="ID del usuario:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        id_label.pack()
        id_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        id_entry.pack()

        # Agregar widgets para la entrada de la materia
        materia_label = tk.Label(add_subject_window, text="Materia:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        materia_label.pack()
        materia_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        materia_entry.pack()

        # Agregar widgets para la entrada de la nota
        nota_label = tk.Label(add_subject_window, text="Nota:", font=('Poppins 14 bold'), bg='#010101', fg='#ffffff')
        nota_label.pack()
        nota_entry = tk.Entry(add_subject_window, font=('Poppins 12'), bg='#010101', fg='#ffffff',justify="center")
        nota_entry.pack()

        # Crear y agregar botones en el update_window principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }
        # Agregar botón para agregar la materia al usuario
        add_button = tk.Button(add_subject_window, text="Agregar",command=lambda: self.agregar_materia_a_usuario(id_entry.get(),materia_entry.get(),nota_entry.get(), add_subject_window), **button_style)
        add_button.pack(pady=5)
        # Configurar el estilo del botón cuando el mouse está sobre él
        add_button.bind("<Enter>", lambda event: add_button.configure(bg='#2cb67d', fg='#010101'))
        # Restaurar el estilo del botón cuando el mouse deja de estar sobre él
        add_button.bind("<Leave>", lambda event: add_button.configure(bg='#010101', fg='#2cb67d'))

    def agregar_materia_a_usuario(self, id_usuario,notas, materia,add_subject_window):

        # Verificar si el tipo de usuario es válido para la carga de notas
        cur = conn.cursor()
        cur.execute("SELECT tipo_usuario FROM usuario WHERE id = %s", (id_usuario,))
        result = cur.fetchone()

        if result is not None:
            tipo_usuario = result[0]
            if tipo_usuario == 2:
                # Agregar la materia al usuario en la base de datos
                cur.execute("INSERT INTO notas (id_usuario, notas, materia) VALUES (%s, %s, %s)", (id_usuario, materia, notas))
                conn.commit()
                messagebox.showinfo(title="Nota Cargada", message="El usuario con ID {} ha optenido su calificación exitosamente.".format(id_usuario))
            else:
                messagebox.showerror(title="Tipo de usuario no válido", message="El tipo de usuario no es válido para la carga de notas.")
        else:
            messagebox.showerror(title="Usuario no encontrado", message="El usuario con ID {} no ha podido ser localizado.".format(id_usuario))

        # Cerrar la ventana de carga de notas del usuario
        add_subject_window.destroy()

    def ver(self, tipo_usuario):
        # Crear la ventana de notas
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, tipo_usuario, password, curso FROM usuario WHERE tipo_usuario = %s ORDER BY id", (tipo_usuario,))
        results = cur.fetchall()
        ver_window = tk.Toplevel(self.master)
        ver_window.geometry("650x300")
        ver_window.title("USUARIOS")
        if tipo_usuario == 1:
            # Agregar una tabla de notas
            ver_table = ttk.Treeview(ver_window)
            ver_table['columns'] = ('ID', 'Nombre','Tipo Usuario','Password', 'Curso')
            ver_table.column('#0', width=0, stretch=tk.NO)
            ver_table.column('ID', anchor=tk.CENTER, width=100)
            ver_table.column('Nombre', anchor=tk.CENTER, width=100)
            ver_table.column('Tipo Usuario', anchor=tk.CENTER, width=100)
            ver_table.column('Password', anchor=tk.CENTER, width=100)
            ver_table.column('Curso', anchor=tk.CENTER, width=100)

            ver_table.heading('#0', text='')
            ver_table.heading('ID', text='ID', anchor=tk.CENTER)
            ver_table.heading('Nombre', text='Nombre', anchor=tk.CENTER)
            ver_table.heading('Tipo Usuario', text='Tipo Usuario', anchor=tk.CENTER)
            ver_table.heading('Password', text='Password', anchor=tk.CENTER)
            ver_table.heading('Curso', text='Curso', anchor=tk.CENTER)
            

            for user in results:
                ver_table.insert('', 'end', text='', values=user)

            ver_table.pack(padx=5, pady=5, fill='both', expand=True)
        elif tipo_usuario == 2: 
            # Agregar una tabla de notas
            ver_table = ttk.Treeview(ver_window)
            ver_table['columns'] = ('ID', 'Nombre','Tipo Usuario','Password', 'Curso')
            ver_table.column('#0', width=0, stretch=tk.NO)
            ver_table.column('ID', anchor=tk.CENTER, width=100)
            ver_table.column('Nombre', anchor=tk.CENTER, width=100)
            ver_table.column('Tipo Usuario', anchor=tk.CENTER, width=100)
            ver_table.column('Password', anchor=tk.CENTER, width=100)
            ver_table.column('Curso', anchor=tk.CENTER, width=100)

            ver_table.heading('#0', text='')
            ver_table.heading('ID', text='ID', anchor=tk.CENTER)
            ver_table.heading('Nombre', text='Nombre', anchor=tk.CENTER)
            ver_table.heading('Tipo Usuario', text='Tipo Usuario', anchor=tk.CENTER)
            ver_table.heading('Password', text='Password', anchor=tk.CENTER)
            ver_table.heading('Curso', text='Curso', anchor=tk.CENTER)
            

            for user in results:
                ver_table.insert('', 'end', text='', values=user)

            ver_table.pack(padx=5, pady=5, fill='both', expand=True)

#Clase para el tipo Usuario
class User():
    def __init__(self, master, usuario_actual):
        self.master = master
        self.usuario_actual = usuario_actual
        self.master.geometry("500x300")
        self.master.title("Panel de Usuario")
       
        # Obtener las dimensiones de la pantalla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Obtener las dimensiones de la ventana
        window_width = 500
        window_height = 300

        # Calcular la posición x e y para centrar la ventana
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        # Establecer la posición de la ventana
        self.master.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
         # Configurar estilo para los widgets
        bg_color = "#010101"  # Color de fondo
        fg_color = "#ffffff"  # Color de texto
        font_style = "Poppins 14 bold"  # Estilo de fuente

        # Crear frame principal con color de fondo
        main_frame = tk.Frame(self.master, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)

        aviso_label = tk.Label(main_frame, text="BIENVENIDO!", font=("Poppins Medium", 20), bg=bg_color, fg=fg_color)
        aviso_label.pack(pady=10)

         # Crear y agregar botones en el frame principal
        button_style = {
            "bg": "#010101",  # Color de fondo del botón
            "fg": "#2cb67d",  # Color de texto del botón
            "font": "Poppins 12 bold",  # Estilo de fuente del botón
            "relief": tk.RAISED,  # Tipo de relieve del botón
            "bd": 4,  # Tamaño del borde del botón
            "highlightbackground": "#2cb67d"  # Color del borde del botón
            #"corner_radius": 0  # Radio de las esquinas del botón (en píxeles)
        }

        # Agregar botones para generar nuevos usuarios, actualizar, cargar notas y eliminar
        notas_button = tk.Button(main_frame, text="Ver Notas", command=lambda: self.ver_notas(), **button_style)
        notas_button.pack(pady=7)
        notas_button.bind("<Enter>", lambda event: notas_button.configure(bg='#2cb67d', fg='#010101'))
        notas_button.bind("<Leave>", lambda event: notas_button.configure(bg='#010101', fg='#2cb67d'))

        #El siguiente boton retorna al login
        salir_button = tk.Button(main_frame, text="Salir", command=lambda: self.mostrar_login(), **button_style)
        salir_button.pack(pady=7)
        salir_button.bind("<Enter>", lambda event: salir_button.configure(bg='#2cb67d', fg='#010101'))
        salir_button.bind("<Leave>", lambda event: salir_button.configure(bg='#010101', fg='#2cb67d'))

    def mostrar_login(self):
        self.master.destroy()  # Cerrar la ventana actual de administrador
        login = Login()
        login.show()

    def ver_notas(self):
       # Verificar que el ID del usuario actual existe en la base de datos
        if self.usuario_actual is not None:
            cur = conn.cursor()
            cur.execute("SELECT nombre FROM usuario WHERE id = %s", (self.usuario_actual,))
            result = cur.fetchone()
            if result:
                # Obtener las notas del usuario actual
                cur.execute("SELECT materia, notas FROM notas WHERE id_usuario = %s", (self.usuario_actual,))
                notas = cur.fetchall()

                # Crear la ventana de notas
                notas_window = tk.Toplevel(self.master)
                notas_window.title("Notas de {}".format(result[0]))
                notas_window.geometry("600x300")
                
                # Establecer el estilo del fondo y color de texto
                bg_color = "#010101"
                fg_color = "#2cb67d"

                # Establecer el estilo de fuente
                font_style = "Poppins 12 bold"

                # Agregar una tabla de notas
                notas_table = ttk.Treeview(notas_window, style="Custom.Treeview")
                notas_table['columns'] = ('Materia', 'Nota')
                notas_table.column('#0', width=0, stretch=tk.NO)
                notas_table.column('Materia', anchor=tk.CENTER, width=100)
                notas_table.column('Nota', anchor=tk.CENTER, width=100)

                notas_table.heading('#0', text='')
                notas_table.heading('Materia', text='Materia', anchor=tk.CENTER)
                notas_table.heading('Nota', text='Nota', anchor=tk.CENTER)

                for nota in notas:
                    notas_table.insert('', 'end', text='', values=nota)

                notas_table.pack(padx=5, pady=5, fill='both', expand=True)

                # Establecer el estilo de la tabla
                notas_table_style = ttk.Style()
                notas_table_style.configure("Custom.Treeview",
                                            background=bg_color,
                                            foreground=fg_color,
                                            font=font_style)

                notas_window.mainloop()
            else:
                messagebox.showerror(title="Error de usuario", message="El usuario actual no existe en la base de datos.")
        else:
            messagebox.showerror(title="Error de usuario", message="No se ha iniciado sesión o las credenciales son incorrectas.")
            

#PARA LA FINAL AGREGAR Y LIMITAR LOS ACCESOS A ADMINISTRADOR, CREAR PERFILES DE PROFESORES EN DONDE
#LOS PROFESORES PUEDEN AGREGAR MATERIAS, MODIFICAR MATERIAS Y VER ALUMNOS. 

if __name__ == '__main__':
    login = Login()
    login.show()
