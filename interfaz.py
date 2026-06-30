"""
Interfaz gráfica de escritorio para el Sistema de Gestión de Biblioteca.
 
Hecha con CustomTkinter. Usa las clases de sistema.py.
Rediseño premium con paleta de colores moderna y UX mejorada.

Requiere:  pip install customtkinter
Se ejecuta: python interfaz.py
"""
import customtkinter as ctk
 
from sistema import (Biblioteca, Libro, Usuario,
                     Estrategia_Autor, Estrategia_Genero, Recomendacion,
                     Historial)
 
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
 
# Paleta de colores Premium (Catppuccin Mocha/Slate)
BG_MAIN = "#1E1E2E"       # Fondo principal de la ventana
BG_SIDEBAR = "#11111B"    # Fondo del panel lateral
ACCENT = "#89B4FA"        # Azul pastel vibrante
ACCENT_HOVER = "#74C7EC"  # Azul claro al pasar el cursor
CARD = "#252538"          # Fondo de las tarjetas
OK_COLOR = "#A6E3A1"      # Verde esmeralda para disponibles/devueltos
WARN_COLOR = "#F38BA8"    # Rojo suave para prestados/alertas
TEXT_COLOR = "#CDD6F4"    # Texto primario
MUTED_COLOR = "#A6ADC8"   # Texto secundario/desvanecido
ARCHIVO = "biblioteca.json"
 
 
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Biblioteca UNAB")
        self.geometry("980x640")
        self.minsize(850, 560)
        self.configure(fg_color=BG_MAIN)
 
        # ---------- LOGICA (las clases del proyecto) ----------
        self.biblioteca = Biblioteca()
        self.usuario = Usuario("Invitado", "invitado@biblioteca.com", "1234")
        # Persistencia: primero intento cargar lo guardado.
        self.biblioteca.cargar_desde_json(ARCHIVO)
        # Si no habia nada guardado, cargo libros de ejemplo (solo la 1a vez).
        if not self.biblioteca.catalogo():
            self._precargar_libros()
            self.biblioteca.guardar_en_json(ARCHIVO)
 
        # ---------- LAYOUT ----------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.nav_buttons = {}  # Guardar referencias de botones de navegación
        
        self._construir_sidebar()
        self._construir_contenido()
        self._construir_status()
 
        self.mostrar_catalogo()
        self._seleccionar_nav("Catalogo")
 
    def _precargar_libros(self):
        ejemplos = [
            ("Rayuela", "Cortazar", "Novela", "Sudamericana"),
            ("El Aleph", "Borges", "Cuento", "Emece"),
            ("Ficciones", "Borges", "Cuento", "Sur"),
            ("Cien Anios de Soledad", "Garcia Marquez", "Novela", "Sudamericana"),
            ("Bestiario", "Cortazar", "Cuento", "Sudamericana"),
        ]
        for datos in ejemplos:
            self.biblioteca.agregar_libro(Libro(*datos))
 
    # ============ sidebar ============
    def _construir_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color=BG_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
 
        ctk.CTkLabel(self.sidebar, text="Biblioteca UNAB",
                     text_color=ACCENT,
                     font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(26, 20))
 
        self._btn_nav("Catalogo", self.mostrar_catalogo, 1)
        self._btn_nav("Agregar libro", self.mostrar_agregar, 2)
        self._btn_nav("Recomendar", self.mostrar_recomendar, 3)
        self._btn_nav("Historial", self.mostrar_historial, 4)
 
        ctk.CTkLabel(self.sidebar, text="Gestión de Biblioteca\nProgramación Avanzada",
                     font=ctk.CTkFont(family="Segoe UI", size=11), text_color=MUTED_COLOR,
                     justify="left").grid(row=7, column=0, padx=20, pady=18, sticky="sw")
 
    def _btn_nav(self, texto, comando, fila):
        btn = ctk.CTkButton(
            self.sidebar, text=texto, 
            command=lambda: [comando(), self._seleccionar_nav(texto)],
            fg_color="transparent", text_color=MUTED_COLOR,
            hover_color="#252538", height=40, corner_radius=8, anchor="w",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
        )
        btn.grid(row=fila, column=0, padx=16, pady=4, sticky="ew")
        self.nav_buttons[texto] = btn

    def _seleccionar_nav(self, texto_activo):
        for texto, btn in self.nav_buttons.items():
            if texto == texto_activo:
                btn.configure(fg_color=ACCENT, text_color="#11111B", hover_color=ACCENT_HOVER)
            else:
                btn.configure(fg_color="transparent", text_color=MUTED_COLOR, hover_color="#252538")
 
    # ============ contenido ============
    def _construir_contenido(self):
        self.contenido = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=1)
 
    def _construir_status(self):
        self.status = ctk.CTkLabel(self, text="Listo.", anchor="w",
                                   font=ctk.CTkFont(family="Segoe UI", size=12), text_color=MUTED_COLOR)
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 8))
 
    def _status(self, texto, color=MUTED_COLOR):
        self.status.configure(text=texto, text_color=color)
 
    def _limpiar(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()
 
    def _titulo(self, texto):
        ctk.CTkLabel(self.contenido, text=texto, text_color=TEXT_COLOR,
                     font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 18))
 
    # ============ VISTA: catalogo ============
    def mostrar_catalogo(self):
        self._limpiar()
        disp = self.biblioteca.cantidad_disponible()
        total = len(self.biblioteca.catalogo())
        self._titulo(f"Catálogo  ({disp}/{total} disponibles)")
 
        lista = ctk.CTkScrollableFrame(self.contenido, fg_color="transparent")
        lista.grid(row=1, column=0, sticky="nsew")
        lista.grid_columnconfigure(0, weight=1)
 
        libros = self.biblioteca.catalogo()
        if not libros:
            ctk.CTkLabel(lista, text="La biblioteca está vacía.",
                         text_color=MUTED_COLOR,
                         font=ctk.CTkFont(family="Segoe UI", size=13)).grid(row=0, column=0, pady=20)
            return
        for i, libro in enumerate(libros):
            self._tarjeta_libro(lista, libro, i)
 
    def _tarjeta_libro(self, padre, libro, fila):
        card = ctk.CTkFrame(padre, fg_color=CARD, corner_radius=12)
        card.grid(row=fila, column=0, sticky="ew", pady=6, padx=2)
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, minsize=100)
 
        # Contenedor de texto
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.grid(row=0, column=0, sticky="w", padx=16, pady=12)
        
        ctk.CTkLabel(text_frame, text=libro.get_titulo(),
                     font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), 
                     text_color=TEXT_COLOR, anchor="w").pack(anchor="w")
                     
        sub = f"Autor: {libro.get_autor()}   |   Género: {libro.get_genero()}   |   Editorial: {libro.get_editorial()}"
        ctk.CTkLabel(text_frame, text=sub, 
                     font=ctk.CTkFont(family="Segoe UI", size=12),
                     text_color=MUTED_COLOR, anchor="w").pack(anchor="w", pady=(2, 0))
 
        prestado = libro.esta_prestado()
        estado_texto = "● Prestado" if prestado else "● Disponible"
        estado_color = WARN_COLOR if prestado else OK_COLOR
        
        ctk.CTkLabel(card, text=estado_texto,
                     font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                     text_color=estado_color).grid(row=0, column=1, padx=10, sticky="e")
 
        titulo = libro.get_titulo()
        if prestado:
            btn = ctk.CTkButton(card, text="Devolver", width=110, height=32,
                                fg_color=WARN_COLOR, hover_color="#E07A97", text_color="#11111B",
                                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                corner_radius=8,
                                command=lambda t=titulo: self.accion_devolver(t))
            btn.grid(row=0, column=2, padx=(6, 16))
        else:
            btn = ctk.CTkButton(card, text="Prestar", width=110, height=32,
                                fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#11111B",
                                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                                corner_radius=8,
                                command=lambda t=titulo: self.accion_prestar(t))
            btn.grid(row=0, column=2, padx=(6, 16))
 
    def accion_prestar(self, titulo):
        msg = self.biblioteca.registrar_prestamo(self.usuario, titulo)
        self.biblioteca.guardar_en_json(ARCHIVO)
        self._status(msg, OK_COLOR if "registrado" in msg.lower() else WARN_COLOR)
        self.mostrar_catalogo()
 
    def accion_devolver(self, titulo):
        msg = self.biblioteca.registrar_devolucion(titulo)
        self.biblioteca.guardar_en_json(ARCHIVO)
        self._status(msg, OK_COLOR)
        self.mostrar_catalogo()
 
    # ============ VISTA: agregar ============
    def mostrar_agregar(self):
        self._limpiar()
        self._titulo("Agregar libro")
        
        form = ctk.CTkFrame(self.contenido, fg_color=CARD, corner_radius=12)
        form.grid(row=1, column=0, sticky="new", pady=4)
        form.grid_columnconfigure(0, weight=1)
 
        self.entries = {}
        for i, campo in enumerate(["Titulo", "Autor", "Genero", "Editorial"]):
            lbl = ctk.CTkLabel(form, text=campo, text_color=TEXT_COLOR,
                               font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
            lbl.grid(sticky="w", padx=20, pady=(14 if i==0 else 8, 2))
            
            entry = ctk.CTkEntry(form, height=36, placeholder_text=f"Ingrese {campo.lower()}...",
                                 fg_color=BG_MAIN, border_color="#45475A", text_color=TEXT_COLOR,
                                 placeholder_text_color="#585B70", border_width=1, corner_radius=8)
            entry.grid(sticky="ew", padx=20)
            self.entries[campo] = entry
 
        ctk.CTkButton(form, text="Agregar al catálogo", height=40,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#11111B",
                      font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                      corner_radius=8,
                      command=self.accion_agregar).grid(sticky="ew", padx=20, pady=22)
 
    def accion_agregar(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        if not datos["Titulo"]:
            self._status("El título no puede estar vacío.", WARN_COLOR)
            self.entries["Titulo"].configure(border_color=WARN_COLOR)
            return
            
        self.entries["Titulo"].configure(border_color="#45475A")
        self.biblioteca.agregar_libro(
            Libro(datos["Titulo"], datos["Autor"], datos["Genero"], datos["Editorial"]))
        self.biblioteca.guardar_en_json(ARCHIVO)
        self._status(f"Libro '{datos['Titulo']}' agregado y guardado.", OK_COLOR)
        self.mostrar_catalogo()
        self._seleccionar_nav("Catalogo")
 
    # ============ VISTA: recomendar (Strategy) ============
    def mostrar_recomendar(self):
        self._limpiar()
        self._titulo("Recomendar un libro")
        
        panel = ctk.CTkFrame(self.contenido, fg_color=CARD, corner_radius=12)
        panel.grid(row=1, column=0, sticky="new", pady=4)
        panel.grid_columnconfigure(0, weight=1)
 
        lbl_crit = ctk.CTkLabel(panel, text="Criterio (estrategia)", text_color=TEXT_COLOR,
                                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        lbl_crit.grid(sticky="w", padx=20, pady=(16, 2))
        
        self.opt_criterio = ctk.CTkOptionMenu(
            panel, values=["Autor", "Genero"],
            fg_color=BG_MAIN, button_color=ACCENT, button_hover_color=ACCENT_HOVER,
            text_color=TEXT_COLOR, dropdown_fg_color=CARD, dropdown_text_color=TEXT_COLOR,
            corner_radius=8, height=36
        )
        self.opt_criterio.grid(sticky="ew", padx=20, pady=(0, 10))
 
        lbl_pref = ctk.CTkLabel(panel, text="Preferencia", text_color=TEXT_COLOR,
                                font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"))
        lbl_pref.grid(sticky="w", padx=20, pady=(6, 2))
        
        self.entry_pref = ctk.CTkEntry(
            panel, height=36, placeholder_text="Ej: Borges  /  Novela",
            fg_color=BG_MAIN, border_color="#45475A", text_color=TEXT_COLOR,
            placeholder_text_color="#585B70", border_width=1, corner_radius=8
        )
        self.entry_pref.grid(sticky="ew", padx=20)
 
        ctk.CTkButton(panel, text="Buscar recomendación", height=40,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#11111B",
                      font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
                      corner_radius=8,
                      command=self.accion_recomendar).grid(sticky="ew", padx=20, pady=18)
 
        # Contenedor para la tarjeta de resultado
        self.rec_container = ctk.CTkFrame(panel, fg_color="transparent")
        self.rec_container.grid(sticky="ew", row=6, column=0, pady=(0, 4))
 
    def accion_recomendar(self):
        criterio = self.opt_criterio.get()
        pref = self.entry_pref.get().strip()
        if not pref:
            self._status("Escribí una preferencia.", WARN_COLOR)
            self.entry_pref.configure(border_color=WARN_COLOR)
            return
            
        self.entry_pref.configure(border_color="#45475A")
        estrategia = Estrategia_Autor() if criterio == "Autor" else Estrategia_Genero()
        recomendador = Recomendacion(estrategia)
        resultado = recomendador.ejecutar_estrategia(self.biblioteca.catalogo(), pref)
        
        # Limpiar contenedor de resultado anterior
        for widget in self.rec_container.winfo_children():
            widget.destroy()
            
        if resultado:
            card = ctk.CTkFrame(self.rec_container, fg_color=BG_MAIN, corner_radius=10, 
                                border_color="#45475A", border_width=1)
            card.pack(fill="x", padx=20, pady=(0, 20))
            
            ctk.CTkLabel(card, text="★ RECOMENDACIÓN SUGERIDA ★", 
                         font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), 
                         text_color=ACCENT).pack(anchor="w", padx=16, pady=(12, 4))
                         
            ctk.CTkLabel(card, text=resultado.get_titulo(), 
                         font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), 
                         text_color=TEXT_COLOR).pack(anchor="w", padx=16, pady=(0, 2))
                         
            sub = f"Autor: {resultado.get_autor()}   |   Género: {resultado.get_genero()}   |   Editorial: {resultado.get_editorial()}"
            ctk.CTkLabel(card, text=sub, 
                         font=ctk.CTkFont(family="Segoe UI", size=12), 
                         text_color=MUTED_COLOR).pack(anchor="w", padx=16, pady=(0, 12))
                         
            self._status("Recomendación encontrada.", OK_COLOR)
        else:
            card = ctk.CTkFrame(self.rec_container, fg_color=BG_MAIN, corner_radius=10, 
                                border_color=WARN_COLOR, border_width=1)
            card.pack(fill="x", padx=20, pady=(0, 20))
            
            ctk.CTkLabel(card, text="No se encontraron libros con esa preferencia.", 
                         font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
                         text_color=WARN_COLOR).pack(anchor="w", padx=16, pady=16)
                         
            self._status("Sin resultados.", WARN_COLOR)
 
    # ============ VISTA: historial ============
    def mostrar_historial(self, solo_activos=False):
        self._limpiar()
        self._titulo("Historial de préstamos")
 
        # Barra de filtros
        filtros = ctk.CTkFrame(self.contenido, fg_color="transparent")
        filtros.grid(row=0, column=0, sticky="e", pady=(0, 14))
        
        btn_todos = ctk.CTkButton(
            filtros, text="Todos", width=90, height=32, corner_radius=8,
            fg_color=ACCENT if not solo_activos else CARD,
            text_color="#11111B" if not solo_activos else TEXT_COLOR,
            hover_color=ACCENT_HOVER if not solo_activos else "#313244",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.mostrar_historial(False)
        )
        btn_todos.grid(row=0, column=0, padx=4)
        
        btn_activos = ctk.CTkButton(
            filtros, text="Activos", width=90, height=32, corner_radius=8,
            fg_color=ACCENT if solo_activos else CARD,
            text_color="#11111B" if solo_activos else TEXT_COLOR,
            hover_color=ACCENT_HOVER if solo_activos else "#313244",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            command=lambda: self.mostrar_historial(True)
        )
        btn_activos.grid(row=0, column=1, padx=4)
 
        lista = ctk.CTkScrollableFrame(self.contenido, fg_color="transparent")
        lista.grid(row=1, column=0, sticky="nsew")
        lista.grid_columnconfigure(0, weight=1)
 
        historial = Historial(self.biblioteca._prestamos)
        if solo_activos:
            prestamos = historial.ver_prestamos_activos()
        else:
            prestamos = historial.ver_historial_global()
 
        if not prestamos:
            ctk.CTkLabel(lista, text="No hay préstamos para mostrar.",
                         text_color=MUTED_COLOR,
                         font=ctk.CTkFont(family="Segoe UI", size=13)).grid(row=0, column=0, pady=20)
            return
 
        for i, prestamo in enumerate(prestamos):
            card = ctk.CTkFrame(lista, fg_color=CARD, corner_radius=12)
            card.grid(row=i, column=0, sticky="ew", pady=6, padx=2)
            card.grid_columnconfigure(0, weight=1)
            
            libro_titulo = prestamo.obtener_libro().get_titulo()
            usuario_nombre = prestamo.obtener_usuario().get_nombre()
            fecha = prestamo.obtener_fecha_inicio()
            vigente = prestamo.comprobar_si_esta_vigente()
            
            # Contenedor de texto
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.grid(row=0, column=0, sticky="w", padx=16, pady=12)
            
            ctk.CTkLabel(info_frame, text=libro_titulo, 
                         font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                         text_color=TEXT_COLOR, anchor="w").pack(anchor="w")
                         
            sub = f"Prestado a: {usuario_nombre}   |   Fecha: {fecha}"
            ctk.CTkLabel(info_frame, text=sub, 
                         font=ctk.CTkFont(family="Segoe UI", size=12), 
                         text_color=MUTED_COLOR, anchor="w").pack(anchor="w", pady=(2, 0))
                         
            # Estado
            estado_texto = "● En curso" if vigente else "✓ Devuelto"
            estado_color = WARN_COLOR if vigente else OK_COLOR
            ctk.CTkLabel(card, text=estado_texto,
                         font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                         text_color=estado_color).grid(row=0, column=1, padx=20, sticky="e")
 
 
if __name__ == "__main__":
    app = App()
    app.mainloop()