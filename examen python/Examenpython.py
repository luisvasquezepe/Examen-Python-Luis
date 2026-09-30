import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def conectar_bd():
    conexion = sqlite3.connect("estudiantes_registro.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            edad INTEGER NOT NULL,
            curso TEXT NOT NULL,
            nota REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

conectar_bd()

PALETA = {
    "bg_principal": "#F3F4F6",      
    "header_bg": "#2E1065",        
    "header_fg": "#FFFFFF",      
    "card_bg": "#FFFFFF",          
    "resumen_bg": "#F3E8FF",    
    "texto_principal": "#1F2937",  
    "texto_secundario": "#4B5563", 
    
    "btn_guardar": "#0D9488",    
    "btn_mostrar": "#6366F1",   
    "btn_buscar": "#8B5CF6",   
    "btn_eliminar": "#E11D48", 
    "btn_limpiar": "#6B7280"  
}

def obtener_datos_formulario() -> dict:
    """Extrae datos de los campos de entrada y los devuelve en un diccionario."""
    return {
        "nombre": entry_nombre.get().strip(),
        "apellido": entry_apellido.get().strip(),
        "edad": entry_edad.get().strip(),
        "curso": combo_curso.get().strip(),
        "nota": entry_nota.get().strip()
    }

def guardar_estudiante():
    """Valida los campos e inserta un nuevo estudiante en la BD."""
    datos = obtener_datos_formulario()
    
    # Validaciones
    if not (datos["nombre"] and datos["apellido"] and datos["edad"] and datos["curso"] and datos["nota"]):
        messagebox.showwarning("Advertencia", "Por favor complete todos los campos del formulario.")
        return

    try:
        edad = int(datos["edad"])
        nota = float(datos["nota"])
    except ValueError:
        messagebox.showerror("Error de entrada", "La edad debe ser un número entero y la nota un número válido.")
        return

    conexion = sqlite3.connect("estudiantes_registro.db")
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO estudiantes (nombre, apellido, edad, curso, nota) VALUES (?, ?, ?, ?, ?)",
        (datos["nombre"], datos["apellido"], edad, datos["curso"], nota)
    )
    conexion.commit()
    conexion.close()

    messagebox.showinfo("Éxito", f"Estudiante '{datos['nombre']} {datos['apellido']}' guardado correctamente.")
    limpiar_formulario()
    mostrar_estudiantes()

def mostrar_estudiantes():
    """Función para el botón MOSTRAR: Carga y muestra todos los registros de la BD en la tabla y calcula el resumen."""
    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = sqlite3.connect("estudiantes_registro.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes")
    registros = cursor.fetchall()
    conexion.close()

    total_estudiantes = len(registros)
    suma_notas = 0.0

    for reg in registros:
        tabla.insert("", tk.END, values=reg)
        suma_notas += float(reg[5])

    promedio = (suma_notas / total_estudiantes) if total_estudiantes > 0 else 0.0
    lbl_total_val.config(text=str(total_estudiantes))
    lbl_prom_val.config(text=f"{promedio:.1f}")

def buscar_estudiante(event=None):
    """Función para el cuadro y botón BUSCAR: Filtra los datos por nombre o apellido ingresado."""
    criterio = entry_buscar.get().strip()
    
    if not criterio:
        mostrar_estudiantes()
        return

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = sqlite3.connect("estudiantes_registro.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ? OR apellido LIKE ?", (f"%{criterio}%", f"%{criterio}%"))
    registros = cursor.fetchall()
    conexion.close()

    for reg in registros:
        tabla.insert("", tk.END, values=reg)

    if len(registros) == 0:
        messagebox.showinfo("Búsqueda", f"No se encontraron estudiantes que coincidan con '{criterio}'.")

def eliminar_estudiante():
    """Elimina el registro seleccionado de la lista/tabla."""
    seleccionado = tabla.selection()
    
    if not seleccionado:
        messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante de la lista para eliminar.")
        return

    item = tabla.item(seleccionado)
    estudiante_id = item["values"][0]
    estudiante_nombre = f"{item['values'][1]} {item['values'][2]}"

    confirmar = messagebox.askyesno("Confirmar", f"¿Desea eliminar a '{estudiante_nombre}'?")
    if confirmar:
        conexion = sqlite3.connect("estudiantes_registro.db")
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))
        conexion.commit()
        conexion.close()

        messagebox.showinfo("Información", "Estudiante eliminado correctamente.")
        limpiar_formulario()
        mostrar_estudiantes()

def limpiar_formulario():
    """Limpia los campos del formulario y el cuadro de búsqueda."""
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_edad.delete(0, tk.END)
    combo_curso.set("")
    entry_nota.delete(0, tk.END)
    entry_buscar.delete(0, tk.END)

def seleccionar_registro(event):
    """Carga los datos de la fila seleccionada de la tabla al formulario."""
    seleccionado = tabla.selection()
    if seleccionado:
        item = tabla.item(seleccionado)
        valores = item["values"]
        
        limpiar_formulario()
        entry_nombre.insert(0, valores[1])
        entry_apellido.insert(0, valores[2])
        entry_edad.insert(0, valores[3])
        combo_curso.set(valores[4])
        entry_nota.insert(0, valores[5])

ventana = tk.Tk()
ventana.title("Sistema de Registro de Estudiantes")
ventana.geometry("950x670")
ventana.configure(bg=PALETA["bg_principal"])
ventana.resizable(False, False)

frame_header = tk.Frame(ventana, bg=PALETA["header_bg"], height=70)
frame_header.pack(fill="x")

lbl_titulo = tk.Label(
    frame_header, 
    text="Sistema de Registro de Estudiantes", 
    font=("Segoe UI", 18, "bold"), 
    bg=PALETA["header_bg"], 
    fg=PALETA["header_fg"]
)
lbl_titulo.pack(pady=(10, 0))

lbl_subtitulo = tk.Label(
    frame_header, 
    text="Designed by Luis Vásquez", 
    font=("Segoe UI", 10, "italic"), 
    bg=PALETA["header_bg"], 
    fg="#C084FC"
)
lbl_subtitulo.pack(pady=(0, 10))

container = tk.Frame(ventana, bg=PALETA["bg_principal"], padx=15, pady=15)
container.pack(fill="both", expand=True)

col_izquierda = tk.Frame(container, bg=PALETA["bg_principal"], width=320)
col_izquierda.pack(side="left", fill="y", padx=(0, 15))

col_derecha = tk.Frame(container, bg=PALETA["bg_principal"])
col_derecha.pack(side="right", fill="both", expand=True)

frame_form = tk.LabelFrame(
    col_izquierda, 
    text=" 👤 Datos del estudiante ", 
    font=("Segoe UI", 11, "bold"), 
    bg=PALETA["card_bg"], 
    fg=PALETA["texto_principal"],
    padx=12, pady=10
)
frame_form.pack(fill="x", pady=(0, 10))

tk.Label(frame_form, text="Nombre:", bg=PALETA["card_bg"], font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=4)
entry_nombre = tk.Entry(frame_form, font=("Segoe UI", 10), width=20)
entry_nombre.grid(row=0, column=1, pady=4)

tk.Label(frame_form, text="Apellido:", bg=PALETA["card_bg"], font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=4)
entry_apellido = tk.Entry(frame_form, font=("Segoe UI", 10), width=20)
entry_apellido.grid(row=1, column=1, pady=4)

tk.Label(frame_form, text="Edad:", bg=PALETA["card_bg"], font=("Segoe UI", 10)).grid(row=2, column=0, sticky="w", pady=4)
entry_edad = tk.Entry(frame_form, font=("Segoe UI", 10), width=20)
entry_edad.grid(row=2, column=1, pady=4)

tk.Label(frame_form, text="Curso:", bg=PALETA["card_bg"], font=("Segoe UI", 10)).grid(row=3, column=0, sticky="w", pady=4)
combo_curso = ttk.Combobox(
    frame_form, 
    font=("Segoe UI", 10), 
    width=18, 
    values=["Matemáticas", "Lenguaje", "Ciencias", "Inglés", "Historia", "Computación"],
    state="readonly"
)
combo_curso.grid(row=3, column=1, pady=4)

tk.Label(frame_form, text="Nota:", bg=PALETA["card_bg"], font=("Segoe UI", 10)).grid(row=4, column=0, sticky="w", pady=4)
entry_nota = tk.Entry(frame_form, font=("Segoe UI", 10), width=20)
entry_nota.grid(row=4, column=1, pady=4)

frame_btns = tk.Frame(col_izquierda, bg=PALETA["bg_principal"])
frame_btns.pack(fill="x", pady=(0, 10))

btn_guardar = tk.Button(frame_btns, text="💾  Guardar", bg=PALETA["btn_guardar"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=guardar_estudiante)
btn_guardar.pack(fill="x", pady=2)

btn_mostrar = tk.Button(frame_btns, text="📋  Mostrar", bg=PALETA["btn_mostrar"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=mostrar_estudiantes)
btn_mostrar.pack(fill="x", pady=2)

btn_buscar = tk.Button(frame_btns, text="🔍  Buscar", bg=PALETA["btn_buscar"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=buscar_estudiante)
btn_buscar.pack(fill="x", pady=2)

btn_eliminar = tk.Button(frame_btns, text="🗑️  Eliminar", bg=PALETA["btn_eliminar"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=eliminar_estudiante)
btn_eliminar.pack(fill="x", pady=2)

btn_limpiar = tk.Button(frame_btns, text="🔄  Limpiar", bg=PALETA["btn_limpiar"], fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=limpiar_formulario)
btn_limpiar.pack(fill="x", pady=2)

frame_resumen = tk.LabelFrame(
    col_izquierda, 
    text=" 💡 Resumen ", 
    font=("Segoe UI", 11, "bold"), 
    bg=PALETA["resumen_bg"], 
    fg=PALETA["texto_principal"],
    padx=10, pady=10
)
frame_resumen.pack(fill="x")

tk.Label(frame_resumen, text="Total de estudiantes:", bg=PALETA["resumen_bg"], font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w")
lbl_total_val = tk.Label(frame_resumen, text="0", bg=PALETA["resumen_bg"], font=("Segoe UI", 10, "bold"))
lbl_total_val.grid(row=0, column=1, sticky="e", padx=(20, 0))

tk.Label(frame_resumen, text="Promedio general:", bg=PALETA["resumen_bg"], font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")
lbl_prom_val = tk.Label(frame_resumen, text="0.0", bg=PALETA["resumen_bg"], font=("Segoe UI", 10, "bold"), fg=PALETA["btn_mostrar"])
lbl_prom_val.grid(row=1, column=1, sticky="e", padx=(20, 0))

frame_tabla = tk.LabelFrame(
    col_derecha, 
    text=" 👨‍🎓 Lista de estudiantes ", 
    font=("Segoe UI", 11, "bold"), 
    bg=PALETA["card_bg"], 
    fg=PALETA["texto_principal"],
    padx=10, pady=10
)
frame_tabla.pack(fill="both", expand=True, pady=(0, 10))

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", font=("Segoe UI", 9), rowheight=25, background="#FFFFFF", fieldbackground="#FFFFFF")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#E5E7EB", foreground="#1F2937")
style.map("Treeview", background=[("selected", PALETA["btn_mostrar"])], foreground=[("selected", "#FFFFFF")])

cols = ("ID", "Nombre", "Apellido", "Edad", "Curso", "Nota")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=12)

tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Apellido", text="Apellido")
tabla.heading("Edad", text="Edad")
tabla.heading("Curso", text="Curso")
tabla.heading("Nota", text="Nota")

tabla.column("ID", width=35, anchor="center")
tabla.column("Nombre", width=110)
tabla.column("Apellido", width=110)
tabla.column("Edad", width=45, anchor="center")
tabla.column("Curso", width=100)
tabla.column("Nota", width=55, anchor="center")

scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tabla.bind("<<TreeviewSelect>>", seleccionar_registro)

frame_buscar = tk.LabelFrame(
    col_derecha, 
    text=" 🔍 Buscar estudiante ", 
    font=("Segoe UI", 10, "bold"), 
    bg=PALETA["card_bg"], 
    fg=PALETA["texto_principal"],
    padx=10, pady=10
)
frame_buscar.pack(fill="x")

entry_buscar = tk.Entry(frame_buscar, font=("Segoe UI", 10))
entry_buscar.pack(side="left", fill="x", expand=True, padx=(0, 10))
entry_buscar.bind("<Return>", buscar_estudiante)

btn_buscar_bottom = tk.Button(
    frame_buscar, 
    text="🔍  Buscar", 
    bg=PALETA["btn_mostrar"], 
    fg="white", 
    font=("Segoe UI", 9, "bold"), 
    relief="flat", 
    command=buscar_estudiante
)
btn_buscar_bottom.pack(side="right", ipadx=10)

mostrar_estudiantes()

ventana.mainloop()