from werkzeug.security import generate_password_hash, check_password_hash #Esto es para la seguridad de contraseñas
from datetime import date #Esto para controlar fechas

class Biblioteca():
    def __init__(self):
        self._libros = []                    # lista de objetos Libro  (agregacion)
        self._prestamos = []                 # lista de objetos Prestamo
 
    # ---- Gestion de libros ----
    def agregar_libro(self, libro):
        self._libros.append(libro)
 
    def buscar_libro(self, titulo):
        for libro in self._libros:
            if libro.get_titulo().lower() == titulo.lower():
                return libro
        return None                          # no lo encontro
 
    def catalogo(self):
        return self._libros
 
    def libros_disponibles(self):
        return [libro for libro in self._libros if not libro.esta_prestado()]
 
    def cantidad_disponible(self):
        return len(self.libros_disponibles())
 
    # ---- Gestion de prestamos ----
    # Fijate que la Biblioteca NO toca los datos internos del Libro:
    # le PIDE (libro.prestar()). Eso es encapsulamiento bien hecho.
    
    def registrar_prestamo(self, usuario, titulo):
        libro = self.buscar_libro(titulo)
        
        if libro is None:
            return "El libro no existe en la biblioteca."
       
        if not libro.prestar():              # intenta marcarlo como prestado
            return "El libro ya esta prestado."
       
        # Crea el prestamo. OJO: Prestamo es la clase de tu companero/a;
        # tiene que tener __init__(self, usuario, libro).
       
        prestamo = Prestamo(usuario, libro)
        self._prestamos.append(prestamo)
        return "Prestamo registrado."
 
    def registrar_devolucion(self, titulo):
        libro = self.buscar_libro(titulo)
        if libro is None:
            return "El libro no existe en la biblioteca."
        
        libro.devolver()
        
        # CONEXIÓN INTERNA: Busca el préstamo activo de este libro y lo da por terminado
        for prestamo in self._prestamos:
            if prestamo.obtener_libro().get_titulo().lower() == titulo.lower() and prestamo.comprobar_si_esta_vigente():
                prestamo.terminar_prestamo()
                break
                
        return "Devolucion registrada."
        
    def guardar_en_json(self, archivo="biblioteca.json"):
        datos = [libro.to_dict() for libro in self._libros]
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)

    def cargar_desde_json(self, archivo="biblioteca.json"):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except FileNotFoundError:
            return  # primera ejecucion: todavia no hay archivo
        self._libros = [Libro.from_dict(d) for d in datos]    


class Usuario():
    def __init__(self, nombre, email, contraseña):
        self._nombre = nombre
        self._email = email
        self._contraseña = generate_password_hash(contraseña) # Se define una contraseña y genera un hash para mejor protección.

# Se crea getter y setter para el encapsulamiento de datos
        
    def get_nombre(self):
        return self._nombre
    
    def set_nombre(self, nombre):
        self._nombre = nombre
        
    def get_email(self):
        return self._email 
        
    def set_email(self, email):
        self._email = email
        
    def get_contraseña(self):
        return self._contraseña
        
    def set_contraseña(self, contraseña):
        self._contraseña = generate_password_hash(contraseña)
        
    def iniciar_sesion(self, contraseña_ingresada):
        if check_password_hash(self._contraseña, contraseña_ingresada): #Se compara la contraseña ingresada con la hasheada.
            return "Sesión Iniciada"
        return "Error en la contraseña"

class Libro():
    #  Clase "simple": guarda sus datos y conoce su propio estado
    #  (prestado / disponible). Encapsulamiento: atributos privados (_).
    def __init__(self, titulo, autor, genero, editorial):
        self._titulo = titulo
        self._autor = autor
        self._genero = genero
        self._editorial = editorial
        self._esta_prestado = False          # un libro nuevo arranca disponible
 
    # ---- Getters ----
    def get_titulo(self):
        return self._titulo
 
    def get_autor(self):
        return self._autor
 
    def get_genero(self):
        return self._genero
 
    def get_editorial(self):
        return self._editorial
 
    def esta_prestado(self):
        return self._esta_prestado
 
    # ---- Comportamiento ----
    def prestar(self):
        if self._esta_prestado:
            return False                     # ya estaba prestado, no se puede
        self._esta_prestado = True
        return True
 
    def devolver(self):
        self._esta_prestado = False
 
    def __str__(self):
        estado = "Prestado" if self._esta_prestado else "Disponible"
        return f"'{self._titulo}' - {self._autor} ({self._genero}) [{estado}]"

    def to_dict(self):
        # Devuelve los datos del libro como diccionario (para guardar en JSON).
        return {
            "titulo": self._titulo,
            "autor": self._autor,
            "genero": self._genero,
            "editorial": self._editorial,
            "esta_prestado": self._esta_prestado,
        }

    @staticmethod
    def from_dict(datos):
        # Reconstruye un Libro a partir de un diccionario (al cargar el JSON).
        libro = Libro(datos["titulo"], datos["autor"], datos["genero"], datos["editorial"])
        if datos.get("esta_prestado"):
            libro.prestar()
        return libro

class Prestamo():
    def __init__(self, usuario, libro):
        self._usuario = usuario                        # Guarda el objeto Usuario
        self._libro = libro                            # Guarda el objeto Libro
        self._fecha = date.today()              # Fecha del prestamo
        self._esta_vigente = True                      # El préstamo arranca activo

    # - Métodos para Obtener Datos -
    def obtener_usuario(self):
        return self._usuario

    def obtener_libro(self):
        return self._libro

    def obtener_fecha_inicio(self):
        return self._fecha

    def comprobar_si_esta_vigente(self):
        return self._esta_vigente

    # - Acciones -
    def terminar_prestamo(self):
        """Se ejecuta cuando el usuario devuelve el libro."""
        self._esta_vigente = False

    def __str__(self):
        estado = "En curso" if self._esta_vigente else "Devuelto"
        return f"Préstamo: {self._usuario.get_nombre()} tiene '{self._libro.get_titulo()}' | Fecha: {self._fecha} | Estado: {estado}"
        
        
class Estrategia_Recomendacion():
    def ejecutar(self, libros: list, preferencia): #se le da la lista de libros de la clase Biblioteca a todas las recomendaciones
        pass

class Estrategia_Autor(Estrategia_Recomendacion):
    def ejecutar(self, libros:list, preferencia):
        encontrado = False
        for libro in libros:
            if preferencia.lower() == libro.get_autor().lower(): #Compara las variables en minusculas para no hacer diferencias con mayusculas
                print("La recomendación según el autor es la siguiente", libro)
                encontrado = True
                return libro
        if not encontrado:
            print("No se encontraron libros en base a esa recomendación.")
            return None
    
class Estrategia_Genero(Estrategia_Recomendacion):
    def ejecutar(self, libros: list, preferencia):
        encontrado = False
        for libro in libros:
            if preferencia.lower()== libro.get_genero().lower():
                print("La recomendación según el género del libro es la siguiente:", libro)
                encontrado = True
                return libro
        if not encontrado:
            print("No se encontraron libros en base a esa recomendación.")
            return None
    
class Recomendacion(): #Almacenamos las estrategias y la usamos en ejecutar_estrategia
    def __init__(self, estrategia):
        self._estrategia = estrategia
     
    def set_estrategia(self, estrategia):
        self._estrategia = estrategia
        
    def ejecutar_estrategia(self, libros: list, preferencia):
        return self._estrategia.ejecutar(libros, preferencia)
       
class Historial():
    def __init__(self, prestamos_biblioteca: list):
        # Recibe la lista de préstamos de la clase Biblioteca para analizarla.
        self._prestamos = prestamos_biblioteca
        
    def ver_historial_global(self):
        # Muestra absolutamente todos los préstamos registrados (activos y devueltos)
        if not self._prestamos:
            print("No hay registros en el historial global.")
            return []
        
        print("\n--- HISTORIAL GLOBAL DE PRÉSTAMOS ---")
        for prestamo in self._prestamos:
            print(prestamo) # Usa el __str__ que ya definieron en Prestamo
        return self._prestamos

    def ver_historial_usuario(self, usuario: Usuario):
        """Filtra y muestra solo los préstamos que pertenecen a un usuario específico."""
        historial_usuario = []
        for prestamo in self._prestamos:
            # Comparamos los objetos o los emails para saber si es el mismo usuario
            if prestamo.obtener_usuario().get_email() == usuario.get_email():
                historial_usuario.append(prestamo)
                
        print(f"\n--- HISTORIAL DE: {usuario.get_nombre().upper()} ---")
        if not historial_usuario:
            print("Este usuario no tiene préstamos registrados.")
        else:
            for prestamo in historial_usuario:
                print(prestamo)
                
        return historial_usuario

    def ver_prestamos_activos(self):
       # Muestra solo los libros que están prestados actualmente (sin devolver).
        activos = [p for p in self._prestamos if p.comprobar_si_esta_vigente()]
        
        print("\n--- PRÉSTAMOS ACTIVOS (SIN DEVOLVER) ---")
        if not activos:
            print("No hay préstamos activos en este momento.")
        else:
            for prestamo in activos:
                print(prestamo)
        return activos
