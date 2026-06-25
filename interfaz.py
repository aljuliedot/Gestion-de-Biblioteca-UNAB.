"""
Interfaz grafica de escritorio para el Sistema de Gestion de Biblioteca.

Hecha con CustomTkinter. NO modifica ninguna clase: solo USA las clases de
sistema.py (Biblioteca, Libro, Usuario, el patron Strategy y el Historial).

Requiere:  pip install customtkinter
Se ejecuta: python interfaz.py
"""
import customtkinter as ctk

from sistema import (Biblioteca, Libro, Usuario,
                     Estrategia_Autor, Estrategia_Genero, Recomendacion,
                     Historial)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#2FA8A0"
ACCENT_HOVER = "#268C85"
CARD = "#2B2B2B"
OK_COLOR = "#3BA776"
WARN_COLOR = "#C25E5E"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestion de Biblioteca")
        self.geometry("960x620")
        self.minsize(820, 540)

        # ---------- LOGICA (las clases del proyecto) ----------
        self.biblioteca = Biblioteca()
        self.usuario = Usuario("Invitado", "invitado@biblioteca.com", "1234")
        self._precargar_libros()

        # ---------- LAYOUT ----------
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._construir_sidebar()
        self._construir_contenido()
        self._construir_status()

        self.mostrar_catalogo()

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
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="Biblioteca UNAB",
                     font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(26, 20))

        self._btn_nav("Catalogo", self.mostrar_catalogo, 1)
        self._btn_nav("Agregar libro", self.mostrar_agregar, 2)
        self._btn_nav("Recomendar", self.mostrar_recomendar, 3)
        self._btn_nav("Historial", self.mostrar_historial, 4)

        ctk.CTkLabel(self.sidebar, text="Gestion de Biblioteca\nProgramacion Avanzada",
                     font=ctk.CTkFont(size=11), text_color="gray60",
                     justify="left").grid(row=7, column=0, padx=20, pady=18, sticky="sw")

    def _btn_nav(self, texto, comando, fila):
        ctk.CTkButton(self.sidebar, text=texto, command=comando,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      height=40, anchor="w",
                      font=ctk.CTkFont(size=14)).grid(
            row=fila, column=0, padx=16, pady=6, sticky="ew")

    # ============ contenido ============
    def _construir_contenido(self):
        self.contenido = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=24, pady=20)
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=1)

    def _construir_status(self):
        self.status = ctk.CTkLabel(self, text="Listo.", anchor="w",
                                   font=ctk.CTkFont(size=12), text_color="gray70")
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 8))

    def _status(self, texto, color="gray70"):
        self.status.configure(text=texto, text_color=color)

    def _limpiar(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _titulo(self, texto):
        ctk.CTkLabel(self.contenido, text=texto,
                     font=ctk.CTkFont(size=24, weight="bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 14))

    # ============ VISTA: catalogo ============
    def mostrar_catalogo(self):
        self._limpiar()
        disp = self.biblioteca.cantidad_disponible()
        total = len(self.biblioteca.catalogo())
        self._titulo(f"Catalogo  ({disp}/{total} disponibles)")

        lista = ctk.CTkScrollableFrame(self.contenido, fg_color="transparent")
        lista.grid(row=1, column=0, sticky="nsew")
        lista.grid_columnconfigure(0, weight=1)

        libros = self.biblioteca.catalogo()
        if not libros:
            ctk.CTkLabel(lista, text="La biblioteca esta vacia.",
                         text_color="gray60").grid(row=0, column=0, pady=20)
            return
        for i, libro in enumerate(libros):
            self._tarjeta_libro(lista, libro, i)

    def _tarjeta_libro(self, padre, libro, fila):
        card = ctk.CTkFrame(padre, fg_color=CARD, corner_radius=10)
        card.grid(row=fila, column=0, sticky="ew", pady=6, padx=2)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=libro.get_titulo(),
                     font=ctk.CTkFont(size=15, weight="bold"), anchor="w").grid(
            row=0, column=0, sticky="w", padx=16, pady=(12, 0))
        sub = f"{libro.get_autor()}  -  {libro.get_genero()}  -  {libro.get_editorial()}"
        ctk.CTkLabel(card, text=sub, font=ctk.CTkFont(size=12),
                     text_color="gray65", anchor="w").grid(
            row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        prestado = libro.esta_prestado()
        ctk.CTkLabel(card, text="Prestado" if prestado else "Disponible",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=WARN_COLOR if prestado else OK_COLOR).grid(
            row=0, column=1, rowspan=2, padx=10)

        titulo = libro.get_titulo()
        if prestado:
            ctk.CTkButton(card, text="Devolver", width=110, fg_color=WARN_COLOR,
                          hover_color="#A84A4A",
                          command=lambda t=titulo: self.accion_devolver(t)).grid(
                row=0, column=2, rowspan=2, padx=(6, 14))
        else:
            ctk.CTkButton(card, text="Prestar", width=110, fg_color=ACCENT,
                          hover_color=ACCENT_HOVER,
                          command=lambda t=titulo: self.accion_prestar(t)).grid(
                row=0, column=2, rowspan=2, padx=(6, 14))

    def accion_prestar(self, titulo):
        msg = self.biblioteca.registrar_prestamo(self.usuario, titulo)
        self._status(msg, OK_COLOR if "registrado" in msg else WARN_COLOR)
        self.mostrar_catalogo()

    def accion_devolver(self, titulo):
        msg = self.biblioteca.registrar_devolucion(titulo)
        self._status(msg, OK_COLOR)
        self.mostrar_catalogo()

    # ============ VISTA: agregar ============
    def mostrar_agregar(self):
        self._limpiar()
        self._titulo("Agregar libro")
        form = ctk.CTkFrame(self.contenido, fg_color=CARD, corner_radius=10)
        form.grid(row=1, column=0, sticky="new", pady=4)
        form.grid_columnconfigure(0, weight=1)

        self.entries = {}
        for campo in ["Titulo", "Autor", "Genero", "Editorial"]:
            ctk.CTkLabel(form, text=campo, anchor="w").grid(sticky="w", padx=20, pady=(14, 2))
            entry = ctk.CTkEntry(form, height=36, placeholder_text=f"Ingrese {campo.lower()}...")
            entry.grid(sticky="ew", padx=20)
            self.entries[campo] = entry

        ctk.CTkButton(form, text="Agregar al catalogo", height=40,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      command=self.accion_agregar).grid(sticky="ew", padx=20, pady=22)

    def accion_agregar(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}
        if not datos["Titulo"]:
            self._status("El titulo no puede estar vacio.", WARN_COLOR)
            return
        self.biblioteca.agregar_libro(
            Libro(datos["Titulo"], datos["Autor"], datos["Genero"], datos["Editorial"]))
        self._status(f"Libro '{datos['Titulo']}' agregado.", OK_COLOR)
        self.mostrar_catalogo()

    # ============ VISTA: recomendar (Strategy) ============
    def mostrar_recomendar(self):
        self._limpiar()
        self._titulo("Recomendar un libro")
        panel = ctk.CTkFrame(self.contenido, fg_color=CARD, corner_radius=10)
        panel.grid(row=1, column=0, sticky="new", pady=4)
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(panel, text="Criterio (estrategia)", anchor="w").grid(
            sticky="w", padx=20, pady=(16, 2))
        self.opt_criterio = ctk.CTkOptionMenu(panel, values=["Autor", "Genero"],
                                              fg_color=ACCENT, button_color=ACCENT_HOVER)
        self.opt_criterio.grid(sticky="ew", padx=20, pady=(0, 10))

        ctk.CTkLabel(panel, text="Preferencia", anchor="w").grid(
            sticky="w", padx=20, pady=(6, 2))
        self.entry_pref = ctk.CTkEntry(panel, height=36,
                                       placeholder_text="Ej: Borges  /  Novela")
        self.entry_pref.grid(sticky="ew", padx=20)

        ctk.CTkButton(panel, text="Buscar recomendacion", height=40,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      command=self.accion_recomendar).grid(sticky="ew", padx=20, pady=18)

        self.lbl_resultado = ctk.CTkLabel(panel, text="", font=ctk.CTkFont(size=14),
                                          wraplength=520, justify="left")
        self.lbl_resultado.grid(sticky="w", padx=20, pady=(0, 18))

    def accion_recomendar(self):
        criterio = self.opt_criterio.get()
        pref = self.entry_pref.get().strip()
        if not pref:
            self._status("Escribi una preferencia.", WARN_COLOR)
            return
        estrategia = Estrategia_Autor() if criterio == "Autor" else Estrategia_Genero()
        recomendador = Recomendacion(estrategia)
        resultado = recomendador.ejecutar_estrategia(self.biblioteca.catalogo(), pref)
        if resultado:
            self.lbl_resultado.configure(text=f"Recomendacion:\n{resultado}", text_color=OK_COLOR)
            self._status("Recomendacion encontrada.", OK_COLOR)
        else:
            self.lbl_resultado.configure(
                text="No se encontraron libros con esa preferencia.", text_color=WARN_COLOR)
            self._status("Sin resultados.", WARN_COLOR)

    # ============ VISTA: historial ============
    def mostrar_historial(self, solo_activos=False):
        self._limpiar()
        self._titulo("Historial de prestamos")

        # Barra de filtros
        filtros = ctk.CTkFrame(self.contenido, fg_color="transparent")
        filtros.grid(row=0, column=0, sticky="e")
        ctk.CTkButton(filtros, text="Todos", width=90,
                      fg_color=ACCENT if not solo_activos else "gray30",
                      hover_color=ACCENT_HOVER,
                      command=lambda: self.mostrar_historial(False)).grid(row=0, column=0, padx=4)
        ctk.CTkButton(filtros, text="Activos", width=90,
                      fg_color=ACCENT if solo_activos else "gray30",
                      hover_color=ACCENT_HOVER,
                      command=lambda: self.mostrar_historial(True)).grid(row=0, column=1, padx=4)

        lista = ctk.CTkScrollableFrame(self.contenido, fg_color="transparent")
        lista.grid(row=1, column=0, sticky="nsew")
        lista.grid_columnconfigure(0, weight=1)

        # Creamos el Historial con los prestamos de la biblioteca.
        # (Accedemos a _prestamos directamente porque no tocamos la clase Biblioteca.)
        historial = Historial(self.biblioteca._prestamos)
        if solo_activos:
            prestamos = historial.ver_prestamos_activos()
        else:
            prestamos = historial.ver_historial_global()

        if not prestamos:
            ctk.CTkLabel(lista, text="No hay prestamos para mostrar.",
                         text_color="gray60").grid(row=0, column=0, pady=20)
            return

        for i, prestamo in enumerate(prestamos):
            card = ctk.CTkFrame(lista, fg_color=CARD, corner_radius=10)
            card.grid(row=i, column=0, sticky="ew", pady=6, padx=2)
            card.grid_columnconfigure(0, weight=1)
            vigente = prestamo.comprobar_si_esta_vigente()
            ctk.CTkLabel(card, text=str(prestamo), font=ctk.CTkFont(size=13),
                         anchor="w", justify="left").grid(
                row=0, column=0, sticky="w", padx=16, pady=12)
            ctk.CTkLabel(card, text="En curso" if vigente else "Devuelto",
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=WARN_COLOR if vigente else OK_COLOR).grid(
                row=0, column=1, padx=14)


if __name__ == "__main__":
    app = App()
    app.mainloop()