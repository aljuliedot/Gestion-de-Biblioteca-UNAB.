from werkzeug.security import generate_password_hash, check_password_hash #Esto es para la seguridad de contraseñas

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
        return "Devolucion registrada."
        
        


class Usuario():
    def __init__(self, nombre, email, contraseña):
        self._nombre = nombre
        self._email = email
        self._contraseña = generate_password_hash(contraseña)
        
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
        if check_password_hash(self._contraseña, contraseña_ingresada):
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



        


class Prestamo():
    def __init__(self):
        pass
        
class Estrategia_Recomendacion():
    def __init__(self):
        pass
       
class Historial():
    def __init__(self):
        pass
        
class Bibliotecario():
    def __init__(self, nombre, email, contraseña):
        super().__init__(nombre, email, contraseña)
        
    def agregar_libro(self, libro):
        pass
        
    def eliminar_libro(self, libro):
        pass