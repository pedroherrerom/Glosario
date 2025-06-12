import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

# ------------------------
# FUNCIONES GLOBALES
# ------------------------

def listar_glosarios():
    """Lista todos los archivos .db en el directorio actual"""
    return [f for f in os.listdir() if f.endswith('.db')]

# ------------------------
# VENTANA DE SELECCIÓN DE GLOSARIO
# ------------------------

def seleccionar_glosario():
    def crear_nuevo():
        nombre = entrada_nombre.get()
        if not nombre:
            messagebox.showwarning("Error", "Debes ingresar un nombre para el glosario")
            return
        
        nombre_db = f"{nombre}.db" if not nombre.endswith('.db') else nombre
        conn = sqlite3.connect(nombre_db)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS glosario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            palabra_ingles TEXT NOT NULL,
            traduccion_espanol TEXT NOT NULL,
            categoria TEXT,
            ejemplo TEXT,
            notas TEXT
        )
        ''')
        conn.commit()
        conn.close()
        
        ventana_seleccion.destroy()
        iniciar_aplicacion(nombre_db)
    
    def seleccionar_existente():
        seleccion = combo_glosarios.get()
        if not seleccion:
            messagebox.showwarning("Error", "Debes seleccionar un glosario")
            return
        
        ventana_seleccion.destroy()
        iniciar_aplicacion(seleccion)
    
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Seleccionar Glosario")
    ventana_seleccion.geometry("500x300")
    
    tk.Label(ventana_seleccion, text="Gestión de Glosarios", font=('Arial', 14)).pack(pady=10)
    
    # Frame para nuevo glosario
    frame_nuevo = tk.LabelFrame(ventana_seleccion, text="Crear nuevo glosario", padx=10, pady=10)
    frame_nuevo.pack(pady=5, padx=10, fill="x")
    
    tk.Label(frame_nuevo, text="Nombre del glosario:").pack()
    entrada_nombre = tk.Entry(frame_nuevo)
    entrada_nombre.pack(fill="x")
    tk.Button(frame_nuevo, text="Crear", command=crear_nuevo).pack(pady=5)
    
    # Frame para glosarios existentes
    frame_existente = tk.LabelFrame(ventana_seleccion, text="Abrir glosario existente", padx=10, pady=10)
    frame_existente.pack(pady=5, padx=10, fill="x")
    
    glosarios = listar_glosarios()
    combo_glosarios = ttk.Combobox(frame_existente, values=glosarios)
    combo_glosarios.pack(fill="x")
    if glosarios:
        combo_glosarios.set(glosarios[0])
    
    tk.Button(frame_existente, text="Abrir", command=seleccionar_existente).pack(pady=5)
    
    ventana_seleccion.mainloop()

# ------------------------
# APLICACIÓN PRINCIPAL
# ------------------------

def iniciar_aplicacion(nombre_db):
    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    # ------------------------
    # FUNCIONES
    # ------------------------

    def insertar():
        palabra = entrada_ingles.get()
        traduccion = entrada_espanol.get()
        categoria = entrada_categoria.get()
        ejemplo = entrada_ejemplo.get()
        notas = entrada_notas.get()

        if palabra and traduccion:
            cursor.execute('''
            INSERT INTO glosario (palabra_ingles, traduccion_espanol, categoria, ejemplo, notas)
            VALUES (?, ?, ?, ?, ?)
            ''', (palabra, traduccion, categoria, ejemplo, notas))
            conn.commit()
            messagebox.showinfo("Éxito", "Palabra insertada.")
            limpiar_campos()
            mostrar_todo()
        else:
            messagebox.showwarning("Campos vacíos", "Palabra y traducción son obligatorios.")

    def mostrar_todo():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM glosario ORDER BY palabra_ingles ASC")
        for fila in cursor.fetchall():
            tree.insert("", "end", values=fila)

    def buscar():
        palabra = entrada_busqueda.get()
        cursor.execute("SELECT * FROM glosario WHERE palabra_ingles LIKE ?", ('%' + palabra + '%',))
        resultados = cursor.fetchall()
        actualizar_tabla(resultados)

    def filtrar():
        cat = entrada_filtro.get()
        cursor.execute("SELECT * FROM glosario WHERE categoria = ? ORDER BY palabra_ingles ASC", (cat,))
        resultados = cursor.fetchall()
        actualizar_tabla(resultados)

    def actualizar_tabla(resultados):
        for row in tree.get_children():
            tree.delete(row)
        for fila in resultados:
            tree.insert("", "end", values=fila)

    def limpiar_campos():
        entrada_ingles.delete(0, tk.END)
        entrada_espanol.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_ejemplo.delete(0, tk.END)
        entrada_notas.delete(0, tk.END)

    def eliminar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una palabra para eliminar.")
            return
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar esta palabra?")
        if confirmacion:
            item = tree.item(seleccion)
            palabra_id = item["values"][0]
            cursor.execute("DELETE FROM glosario WHERE id = ?", (palabra_id,))
            conn.commit()
            mostrar_todo()

    def cargar_para_editar():
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una palabra para editar.")
            return
        item = tree.item(seleccion)
        valores = item["values"]
        entrada_ingles.delete(0, tk.END)
        entrada_espanol.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_ejemplo.delete(0, tk.END)
        entrada_notas.delete(0, tk.END)
        entrada_ingles.insert(0, valores[1])
        entrada_espanol.insert(0, valores[2])
        entrada_categoria.insert(0, valores[3])
        entrada_ejemplo.insert(0, valores[4])
        entrada_notas.insert(0, valores[5])
        boton_actualizar.config(state=tk.NORMAL)
        global palabra_id_editar
        palabra_id_editar = valores[0]

    def actualizar_palabra():
        palabra = entrada_ingles.get()
        traduccion = entrada_espanol.get()
        categoria = entrada_categoria.get()
        ejemplo = entrada_ejemplo.get()
        notas = entrada_notas.get()

        if palabra and traduccion:
            cursor.execute('''
            UPDATE glosario
            SET palabra_ingles = ?, traduccion_espanol = ?, categoria = ?, ejemplo = ?, notas = ?
            WHERE id = ?
            ''', (palabra, traduccion, categoria, ejemplo, notas, palabra_id_editar))
            conn.commit()
            messagebox.showinfo("Éxito", "Palabra actualizada.")
            limpiar_campos()
            mostrar_todo()
            boton_actualizar.config(state=tk.DISABLED)
        else:
            messagebox.showwarning("Campos vacíos", "Palabra y traducción son obligatorios.")

    def exportar_csv():
        ruta = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if ruta:
            cursor.execute("SELECT * FROM glosario ORDER BY palabra_ingles ASC")
            datos = cursor.fetchall()
            with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(["ID", "Inglés", "Español", "Categoría", "Ejemplo", "Notas"])
                escritor.writerows(datos)
            messagebox.showinfo("Exportado", f"Glosario exportado como CSV:\n{ruta}")

    # ------------------------
    # INTERFAZ GRÁFICA
    # ------------------------

    root = tk.Tk()
    root.title(f"Glosario Inglés - Español [{nombre_db}]")
    root.geometry("1100x650")

    frame_entrada = tk.Frame(root)
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Palabra en inglés").grid(row=0, column=0)
    tk.Label(frame_entrada, text="Traducción al español").grid(row=0, column=2)
    tk.Label(frame_entrada, text="Categoría").grid(row=1, column=0)
    tk.Label(frame_entrada, text="Ejemplo").grid(row=1, column=2)
    tk.Label(frame_entrada, text="Notas").grid(row=2, column=0)

    entrada_ingles = tk.Entry(frame_entrada, width=30)
    entrada_espanol = tk.Entry(frame_entrada, width=30)
    entrada_categoria = tk.Entry(frame_entrada, width=30)
    entrada_ejemplo = tk.Entry(frame_entrada, width=30)
    entrada_notas = tk.Entry(frame_entrada, width=63)

    entrada_ingles.grid(row=0, column=1)
    entrada_espanol.grid(row=0, column=3)
    entrada_categoria.grid(row=1, column=1)
    entrada_ejemplo.grid(row=1, column=3)
    entrada_notas.grid(row=2, column=1, columnspan=3)

    frame_botones = tk.Frame(root)
    frame_botones.pack(pady=5)

    tk.Button(frame_botones, text="Insertar palabra", command=insertar).grid(row=0, column=0, padx=5)
    boton_actualizar = tk.Button(frame_botones, text="Actualizar palabra", command=actualizar_palabra, state=tk.DISABLED)
    boton_actualizar.grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Eliminar palabra", command=eliminar).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Editar seleccionada", command=cargar_para_editar).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Exportar CSV", command=exportar_csv).grid(row=0, column=4, padx=5)

    # --- Filtros y búsqueda ---

    frame_filtro = tk.Frame(root)
    frame_filtro.pack()

    tk.Label(frame_filtro, text="Buscar palabra:").grid(row=0, column=0)
    entrada_busqueda = tk.Entry(frame_filtro)
    entrada_busqueda.grid(row=0, column=1)
    tk.Button(frame_filtro, text="Buscar", command=buscar).grid(row=0, column=2)

    tk.Label(frame_filtro, text="Filtrar por categoría:").grid(row=0, column=3, padx=10)
    entrada_filtro = tk.Entry(frame_filtro)
    entrada_filtro.grid(row=0, column=4)
    tk.Button(frame_filtro, text="Filtrar", command=filtrar).grid(row=0, column=5)

    tk.Button(frame_filtro, text="Mostrar todo", command=mostrar_todo).grid(row=0, column=6, padx=10)

    # --- Tabla de resultados ---

    cols = ("ID", "Inglés", "Español", "Categoría", "Ejemplo", "Notas")
    tree = ttk.Treeview(root, columns=cols, show="headings", height=20)
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "Notas" else 300)

    tree.pack(pady=10)

    # Mostrar contenido inicial
    mostrar_todo()

    def on_closing():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

# ------------------------
# INICIAR APLICACIÓN
# ------------------------

if __name__ == "__main__":
    seleccionar_glosario()