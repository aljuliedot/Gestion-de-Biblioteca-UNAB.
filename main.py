"""
Menu interactivo de consola para el Sistema de Gestion de Biblioteca.
Este archivo NO modifica ninguna clase: solo USA las clases de sistema.py.
Separar el menu (interfaz) de las clases (logica) es buena practica de diseno.
"""
from sistema import Biblioteca, Libro, Usuario, Historial
 
# Usuario de sesion. Sirve para registrar los prestamos: asi se crean objetos
# Prestamo y el Historial despues tiene datos reales para mostrar.
USUARIO = Usuario("Invitado", "invitado@biblioteca.com", "1234")
 
 
def mostrar_menu():
    print("\n" + "=" * 42)
    print("     SISTEMA DE GESTION DE BIBLIOTECA")
    print("=" * 42)
    print(" 1. Agregar libro")
    print(" 2. Ver catalogo completo")
    print(" 3. Buscar libro")
    print(" 4. Ver libros disponibles")
    print(" 5. Prestar libro")
    print(" 6. Devolver libro")
    print(" 7. Ver historial global")
    print(" 8. Ver prestamos activos")
    print(" 0. Salir")
    print("=" * 42)
 
 
def opcion_agregar(biblio):
    titulo = input("Titulo: ")
    autor = input("Autor: ")
    genero = input("Genero: ")
    editorial = input("Editorial: ")
    biblio.agregar_libro(Libro(titulo, autor, genero, editorial))
    print(f"-> Libro '{titulo}' agregado.")
 
 
def opcion_catalogo(biblio):
    libros = biblio.catalogo()
    if not libros:
        print("-> La biblioteca esta vacia.")
        return
    print("Catalogo:")
    for libro in libros:
        print("   ", libro)
 
 
def opcion_buscar(biblio):
    titulo = input("Titulo a buscar: ")
    libro = biblio.buscar_libro(titulo)
    if libro is None:
        print("-> No se encontro ese libro.")
    else:
        print("-> Encontrado:", libro)
 
 
def opcion_disponibles(biblio):
    disponibles = biblio.libros_disponibles()
    print(f"Disponibles ({biblio.cantidad_disponible()}):")
    if not disponibles:
        print("   (ninguno)")
    for libro in disponibles:
        print("   ", libro)
 
 
def opcion_prestar(biblio):
    titulo = input("Titulo a prestar: ")
    # Usamos registrar_prestamo (no libro.prestar() directo) para que se cree
    # un objeto Prestamo. Eso es lo que despues lee el Historial.
    print("->", biblio.registrar_prestamo(USUARIO, titulo))
 
 
def opcion_devolver(biblio):
    titulo = input("Titulo a devolver: ")
    print("->", biblio.registrar_devolucion(titulo))
 
 
def opcion_historial_global(biblio):
    # Le pasamos al Historial la lista de prestamos de la biblioteca.
    # (Lo ideal seria un metodo get_prestamos() en Biblioteca; aca, como no
    #  tocamos esa clase, accedemos a _prestamos directamente.)
    historial = Historial(biblio._prestamos)
    historial.ver_historial_global()
 
 
def opcion_prestamos_activos(biblio):
    historial = Historial(biblio._prestamos)
    historial.ver_prestamos_activos()
 
 
def main():
    biblio = Biblioteca()
    opciones = {
        "1": opcion_agregar,
        "2": opcion_catalogo,
        "3": opcion_buscar,
        "4": opcion_disponibles,
        "5": opcion_prestar,
        "6": opcion_devolver,
        "7": opcion_historial_global,
        "8": opcion_prestamos_activos,
    }
 
    while True:
        mostrar_menu()
        eleccion = input("Elegi una opcion: ").strip()
        if eleccion == "0":
            print("Hasta luego!")
            break
        accion = opciones.get(eleccion)
        if accion:
            accion(biblio)
        else:
            print("-> Opcion invalida, intenta de nuevo.")
 
 
if __name__ == "__main__":
    main()
 