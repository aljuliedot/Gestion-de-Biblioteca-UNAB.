"""
Controlador de escritorio para el Sistema de Gestión de Biblioteca usando PyWebView.
Conecta la lógica de negocio en Python (sistema.py) con la interfaz de usuario moderna (web/).

Se ejecuta: python interfaz_webview.py
"""
import os
import webview
from sistema import (Biblioteca, Libro, Usuario,
                     Estrategia_Autor, Estrategia_Genero, Recomendacion,
                     Historial)

ARCHIVO = "biblioteca.json"

class Api:
    def __init__(self):
        self.biblioteca = Biblioteca()
        self.usuario = Usuario("Invitado", "invitado@biblioteca.com", "1234")
        # Persistencia: primero intento cargar lo guardado.
        self.biblioteca.cargar_desde_json(ARCHIVO)
        # Si no había nada guardado, cargo libros de ejemplo (solo la 1a vez).
        if not self.biblioteca.catalogo():
            self._precargar_libros()
            self.biblioteca.guardar_en_json(ARCHIVO)

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

    def get_libros(self):
        """Retorna todos los libros del catálogo como diccionarios para JS."""
        return [libro.to_dict() for libro in self.biblioteca.catalogo()]

    def agregar_libro(self, titulo, autor, genero, editorial):
        """Lógica para agregar un nuevo libro desde la UI."""
        if not titulo:
            return {"success": False, "message": "El título no puede estar vacío."}
        nuevo = Libro(titulo, autor, genero, editorial)
        self.biblioteca.agregar_libro(nuevo)
        self.biblioteca.guardar_en_json(ARCHIVO)
        return {"success": True, "message": f"Libro '{titulo}' agregado y guardado."}

    def prestar_libro(self, titulo):
        """Lógica para registrar un préstamo."""
        msg = self.biblioteca.registrar_prestamo(self.usuario, titulo)
        self.biblioteca.guardar_en_json(ARCHIVO)
        success = "registrado" in msg.lower()
        return {"success": success, "message": msg}

    def devolver_libro(self, titulo):
        """Lógica para registrar una devolución."""
        msg = self.biblioteca.registrar_devolucion(titulo)
        self.biblioteca.guardar_en_json(ARCHIVO)
        return {"success": True, "message": msg}

    def get_historial(self, solo_activos):
        """Retorna el historial de préstamos formateado para JS."""
        historial = Historial(self.biblioteca._prestamos)
        if solo_activos:
            prestamos = historial.ver_prestamos_activos()
        else:
            prestamos = historial.ver_historial_global()

        datos = []
        for p in prestamos:
            datos.append({
                "libro": p.obtener_libro().get_titulo(),
                "usuario": p.obtener_usuario().get_nombre(),
                "fecha": str(p.obtener_fecha_inicio()),
                "esta_vigente": p.comprobar_si_esta_vigente()
            })
        return datos

    def recomendar_libro(self, criterio, pref):
        """Lógica para buscar recomendaciones según la preferencia."""
        if not pref:
            return {"success": False, "message": "Escribí una preferencia."}
        
        estrategia = Estrategia_Autor() if criterio == "Autor" else Estrategia_Genero()
        recomendador = Recomendacion(estrategia)
        resultado = recomendador.ejecutar_estrategia(self.biblioteca.catalogo(), pref)
        
        if resultado:
            return {
                "success": True,
                "libro": resultado.to_dict()
            }
        else:
            return {"success": False, "message": "No se encontraron libros con esa preferencia."}


if __name__ == "__main__":
    api = Api()
    
    # Obtenemos la ruta absoluta al archivo index.html local
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "web", "index.html")
    
    # Configuramos e iniciamos la ventana de PyWebView
    window = webview.create_window(
        title="Gestión de Biblioteca UNAB",
        url=html_path,
        js_api=api,
        width=1000,
        height=680,
        min_size=(900, 600),
        background_color="#1E1E2E"
    )
    webview.start(debug=True)
