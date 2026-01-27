import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

IVA_ECUADOR = 0.15
ARCHIVO = "productos.txt"

COLOR_FONDO = "#eceff1"
COLOR_BLANCO = "#ffffff"
COLOR_PRIMARY = "#ff6f00"
COLOR_SUCCESS = "#2e7d32"
COLOR_TEXTO = "#37474f"
COLOR_HEADER = "#263238"

class MasterPanel:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Barrio Market - Sistema de Gestión")
        self.ventana.geometry("1180x700")
        self.ventana.config(bg=COLOR_FONDO)

        self.id_p = tk.StringVar()
        self.nombre = tk.StringVar()
        self.precio = tk.StringVar()
        self.stock = tk.StringVar()
        self.busqueda = tk.StringVar()

        self.estilos_material()
        self.setup_ui()
        self.cargar_datos_en_tabla()

    def estilos_material(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview", 
                        background=COLOR_BLANCO,
                        fieldbackground=COLOR_BLANCO,
                        foreground=COLOR_TEXTO,
                        font=("Helvetica", 10),
                        rowheight=35,
                        borderwidth=0)
        
        style.configure("Treeview.Heading", 
                        background=COLOR_FONDO,
                        foreground=COLOR_TEXTO,
                        font=("Helvetica", 10, "bold"),
                        relief="flat")
        
        style.map("Treeview", background=[('selected', COLOR_PRIMARY)])

    def setup_ui(self):
        header = tk.Frame(self.ventana, bg=COLOR_HEADER, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="🏪 BARRIO MARKET", font=("Helvetica", 18, "bold"), 
                 bg=COLOR_HEADER, fg="white").pack(side="left", padx=30)
        
        tk.Label(header, text="Panel Administrativo", font=("Helvetica", 10), 
                 bg=COLOR_HEADER, fg="#b0bec5").pack(side="left", padx=0, pady=(5,0))

        main_container = tk.Frame(self.ventana, bg=COLOR_FONDO)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        card_form = tk.Frame(main_container, bg=COLOR_BLANCO, bd=1, relief="solid")
        card_form.pack(side="left", fill="y", padx=(0, 20), ipadx=10)
        
        tk.Label(card_form, text="Nuevo Producto", font=("Helvetica", 14, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_PRIMARY).pack(pady=(15, 10), anchor="w", padx=20)

        self.crear_input_material(card_form, "Nombre del Item", self.nombre)
        self.crear_input_material(card_form, "Precio de Venta ($)", self.precio)
        self.crear_input_material(card_form, "Stock Inicial", self.stock)

        btn_container = tk.Frame(card_form, bg=COLOR_BLANCO)
        btn_container.pack(pady=10, padx=20, fill="x")

        self.crear_boton(btn_container, "GUARDAR PRODUCTO", COLOR_SUCCESS, self.registrar)
        self.crear_boton(btn_container, "ACTUALIZAR DATOS", COLOR_PRIMARY, self.actualizar)
        self.crear_boton(btn_container, "ELIMINAR", "#d32f2f", self.eliminar)
        self.crear_boton(btn_container, "LIMPIAR", "#78909c", self.limpiar_campos)

        card_table = tk.Frame(main_container, bg=COLOR_BLANCO, bd=1, relief="solid")
        card_table.pack(side="right", fill="both", expand=True)

        top_table = tk.Frame(card_table, bg=COLOR_BLANCO)
        top_table.pack(fill="x", padx=20, pady=20)

        tk.Label(top_table, text="Inventario", font=("Helvetica", 14, "bold"), 
                 bg=COLOR_BLANCO, fg=COLOR_TEXTO).pack(side="left")

        search_cont = tk.Frame(top_table, bg="#f5f5f5", bd=0, padx=10, pady=5) 
        search_cont.pack(side="right")
        
        tk.Label(search_cont, text="🔍", bg="#f5f5f5").pack(side="left")
        
        entry_search = tk.Entry(search_cont, textvariable=self.busqueda, bg="#f5f5f5", bd=0, font=("Helvetica", 10), width=25)
        entry_search.pack(side="left")
        entry_search.bind("<KeyRelease>", lambda e: self.cargar_datos_en_tabla())

        columnas = ("ID", "Producto", "Precio", "Stock", "Total Neto")
        self.tabla = ttk.Treeview(card_table, columns=columnas, show="headings", selectmode="browse")
        
        self.tabla.column("ID", width=60, anchor="center")
        self.tabla.column("Producto", width=250, anchor="w")
        self.tabla.column("Precio", width=100, anchor="center")
        self.tabla.column("Stock", width=80, anchor="center")
        self.tabla.column("Total Neto", width=120, anchor="e")

        for col in columnas:
            self.tabla.heading(col, text=col.upper())

        self.tabla.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_item)

        self.lbl_resumen = tk.Label(card_table, text="TOTAL INVENTARIO: $0.00", 
                                    font=("Helvetica", 12, "bold"), bg=COLOR_BLANCO, fg=COLOR_SUCCESS)
        self.lbl_resumen.pack(anchor="e", padx=20, pady=(0, 20))

    def crear_input_material(self, padre, titulo, var):
        frame = tk.Frame(padre, bg=COLOR_BLANCO)
        frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame, text=titulo, bg=COLOR_BLANCO, fg="#78909c", font=("Helvetica", 8, "bold")).pack(anchor="w")
        entry = tk.Entry(frame, textvariable=var, font=("Helvetica", 11), bg="#f5f5f5", bd=0, relief="flat")
        entry.pack(fill="x", ipady=8, pady=(5,0))
        tk.Frame(frame, bg=COLOR_PRIMARY, height=2).pack(fill="x")

    def crear_boton(self, padre, texto, color, comando):
        btn = tk.Button(padre, text=texto, bg=color, fg="white", font=("Helvetica", 9, "bold"),
                        command=comando, bd=0, cursor="hand2", activebackground="#37474f", pady=8)
        btn.pack(fill="x", pady=3)

    def registrar(self):
        nom, pre, sto = self.nombre.get().strip(), self.precio.get().strip(), self.stock.get().strip()
        
        if not nom or not pre or not sto:
            messagebox.showwarning("Faltan Datos", "Por favor completa todos los campos.")
            return
        
        try:
            if nom.isdigit(): raise ValueError("Nombre inválido")
            p_val, s_val = float(pre), int(sto)
            if p_val <= 0 or s_val < 0: raise ValueError("Números inválidos")
        except ValueError:
            messagebox.showerror("Error", "Revisa que el precio y stock sean números válidos.")
            return
        
        nuevo_id = random.randint(1000, 9999)
        with open(ARCHIVO, "a", encoding="utf-8") as f:
            f.write(f"{nuevo_id},{nom},{p_val},{s_val}\n")
        
        self.limpiar_campos()
        self.cargar_datos_en_tabla()
        messagebox.showinfo("Listo", "Producto agregado al inventario.")

    def cargar_datos_en_tabla(self):
        for i in self.tabla.get_children(): self.tabla.delete(i)
        
        t_neto = 0
        query = self.busqueda.get().lower()
        
        if os.path.exists(ARCHIVO):
            with open(ARCHIVO, "r", encoding="utf-8") as f:
                for linea in f:
                    d = linea.strip().split(",")
                    
                    if len(d) == 4:
                        id_p, n, p, s = d
                        
                        if query in n.lower() or query in id_p:
                            sub = float(p) * int(s)
                            t_neto += sub
                            self.tabla.insert("", "end", values=(id_p, n, f"${p}", s, f"${sub:.2f}"))
        
        self.lbl_resumen.config(text=f"VALOR TOTAL (CON IVA): ${(t_neto * (1 + IVA_ECUADOR)):.2f}")

    def seleccionar_item(self, event):
        item = self.tabla.focus()
        if item:
            v = self.tabla.item(item)['values']
            self.id_p.set(v[0])
            self.nombre.set(v[1])
            self.precio.set(str(v[2]).replace('$', ''))
            self.stock.set(v[3])

    def actualizar(self):
        if not self.id_p.get(): return
        
        lineas = []
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for l in f:
                if l.split(",")[0] == self.id_p.get():
                    lineas.append(f"{self.id_p.get()},{self.nombre.get()},{self.precio.get()},{self.stock.get()}\n")
                else:
                    lineas.append(l)
        
        with open(ARCHIVO, "w", encoding="utf-8") as f: f.writelines(lineas)
        
        self.cargar_datos_en_tabla()
        messagebox.showinfo("Actualizado", "Datos modificados correctamente.")

    def eliminar(self):
        if not self.id_p.get(): return
        
        if messagebox.askyesno("Borrar", "¿Seguro que deseas eliminar este producto?"):
            lineas = [l for l in open(ARCHIVO, "r") if l.split(",")[0] != self.id_p.get()]
            with open(ARCHIVO, "w") as f: f.writelines(lineas)
            
            self.limpiar_campos()
            self.cargar_datos_en_tabla()

    def limpiar_campos(self):
        self.id_p.set("")
        self.nombre.set("")
        self.precio.set("")
        self.stock.set("")

    def mainloop(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = MasterPanel()
    app.mainloop()

        
