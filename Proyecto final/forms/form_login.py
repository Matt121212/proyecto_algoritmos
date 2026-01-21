import tkinter as tk
from tkinter import ttk, messagebox
import basica.generic as utl
from forms.form_crud import MasterPanel
import os

COLOR_FONDO_VENTANA = "#F3F4F6"
COLOR_CARD_BG = "#FFFFFF"
COLOR_CARD_BORDER = "#E5E7EB"
COLOR_TEXTO_TITULO = "#111827"
COLOR_TEXTO_LABEL = "#6B7280"
COLOR_INPUT_BG = "#F9FAFB"
COLOR_INPUT_BORDER = "#D1D5DB"
COLOR_INPUT_FOCUS = "#3B82F6"
COLOR_BOTON = "#2563EB"
COLOR_BOTON_HOVER = "#1D4ED8"

FONT_TITLE = ('Segoe UI', 20, 'bold')
FONT_SUBTITLE = ('Segoe UI', 11)
FONT_LABEL = ('Segoe UI', 9, 'bold')
FONT_INPUT = ('Segoe UI', 11)
FONT_BUTTON = ('Segoe UI', 11, 'bold')

class App:
    def verificar(self, event=None):
        usu = self.usuario.get()
        password = self.password.get()
        if usu == "admin123" and password == "admin123":
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(message="Credenciales incorrectas", title="Error de Acceso")

    def on_enter_btn(self, e):
        self.btn_login.config(bg=COLOR_BOTON_HOVER)

    def on_leave_btn(self, e):
        self.btn_login.config(bg=COLOR_BOTON)

    def on_focus_in(self, event, entry_frame):
        entry_frame.config(highlightbackground=COLOR_INPUT_FOCUS, highlightcolor=COLOR_INPUT_FOCUS)

    def on_focus_out(self, event, entry_frame):
        entry_frame.config(highlightbackground=COLOR_INPUT_BORDER, highlightcolor=COLOR_INPUT_BORDER)

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Barrio Market | Acceso Seguro")
        self.ventana.geometry("420x650")
        self.ventana.config(bg=COLOR_FONDO_VENTANA)
        self.ventana.resizable(width=False, height=False)
        utl.centrar_ventana(self.ventana, 420, 650)

        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_logo = os.path.join(directorio_actual, "..", "imagenes", "logo2.jpeg")

        logo = None
        if os.path.exists(ruta_logo):
            try:
                logo = utl.leer_imagen(ruta_logo, (120, 120))
            except Exception as e:
                print(f"Error al leer imagen: {e}")
                logo = None

        card = tk.Frame(self.ventana, bg=COLOR_CARD_BG, bd=0, 
                        highlightthickness=1, highlightbackground=COLOR_CARD_BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=550)
        
        if logo:
            lbl_logo = tk.Label(card, image=logo, bg=COLOR_CARD_BG)
            lbl_logo.pack(pady=(40, 15))
        else:
            tk.Label(card, text="🛒", font=("Segoe UI", 60), fg=COLOR_TEXTO_TITULO, bg=COLOR_CARD_BG).pack(pady=(40, 15))

        tk.Label(card, text="BARRIO MARKET", font=FONT_TITLE, 
                 fg=COLOR_TEXTO_TITULO, bg=COLOR_CARD_BG).pack(pady=(0, 5))
        
        tk.Label(card, text="Bienvenido de nuevo", font=FONT_SUBTITLE, 
                 fg=COLOR_TEXTO_LABEL, bg=COLOR_CARD_BG).pack(pady=(0, 35))

        tk.Label(card, text="USUARIO", font=FONT_LABEL, fg=COLOR_TEXTO_LABEL, 
                 bg=COLOR_CARD_BG, anchor="w").pack(fill=tk.X, padx=30, pady=(0, 5))
        
        self.frame_user = tk.Frame(card, bg=COLOR_INPUT_BG, bd=0, 
                                   highlightthickness=1, highlightbackground=COLOR_INPUT_BORDER)
        self.frame_user.pack(fill=tk.X, padx=30, pady=(0, 20), ipady=2)

        self.usuario = tk.Entry(self.frame_user, font=FONT_INPUT, bg=COLOR_INPUT_BG, 
                                fg=COLOR_TEXTO_TITULO, bd=0, relief=tk.FLAT)
        self.usuario.pack(fill=tk.X, padx=10, pady=8)
        
        self.usuario.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.frame_user))
        self.usuario.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.frame_user))

        tk.Label(card, text="CONTRASEÑA", font=FONT_LABEL, fg=COLOR_TEXTO_LABEL, 
                 bg=COLOR_CARD_BG, anchor="w").pack(fill=tk.X, padx=30, pady=(0, 5))
        
        self.frame_pass = tk.Frame(card, bg=COLOR_INPUT_BG, bd=0, 
                                   highlightthickness=1, highlightbackground=COLOR_INPUT_BORDER)
        self.frame_pass.pack(fill=tk.X, padx=30, pady=(0, 30), ipady=2)

        self.password = tk.Entry(self.frame_pass, font=FONT_INPUT, bg=COLOR_INPUT_BG, 
                                 fg=COLOR_TEXTO_TITULO, bd=0, relief=tk.FLAT, show="●")
        self.password.pack(fill=tk.X, padx=10, pady=8)

        self.password.bind("<FocusIn>", lambda e: self.on_focus_in(e, self.frame_pass))
        self.password.bind("<FocusOut>", lambda e: self.on_focus_out(e, self.frame_pass))

        self.btn_login = tk.Button(card, text="Entrar", font=FONT_BUTTON, 
                                   bg=COLOR_BOTON, fg="white", 
                                   bd=0, cursor="hand2", activebackground=COLOR_BOTON_HOVER,
                                   activeforeground="white", command=self.verificar)
        self.btn_login.pack(fill=tk.X, padx=30, ipady=10)

        self.btn_login.bind("<Enter>", self.on_enter_btn)
        self.btn_login.bind("<Leave>", self.on_leave_btn)
        self.ventana.bind("<Return>", self.verificar)

        self.usuario.focus_set()

        self.ventana.mainloop()

if __name__ == "__main__":
    App()
