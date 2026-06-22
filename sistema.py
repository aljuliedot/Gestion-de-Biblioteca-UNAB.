from werkzeug.security import generate_password_hash, check_password_hash #Esto es para la seguridad de contraseñas

class Biblioteca():
    def __init__(self):
        pass

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
        if check_password_hash(self.__contraseña, contraseña_ingresada):
            return "Sesión Iniciada"
        return "Error en la contraseña"

class Libro():
    def __init__(self):
        pass
        
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