"""
Menu interactivo de consola para el Sistema de Gestion de Biblioteca.
Usa las clases de sistema.py. Ahora con persistencia: los libros se guardan
en un archivo JSON y se cargan automaticamente al abrir el programa.
"""
from sistema import Biblioteca, Libro, Usuario, Historial
 
USUARIO = Usuario("Invitado", "invitado@biblioteca.com", "1234")
ARCHIVO = "biblioteca.json"
 
 
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
    biblio.guardar_en_json(ARCHIVO)          # persistimos el cambio
    print(f"-> Libro '{titulo}' agregado y guardado.")
 
 
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
    print("-> No se encontro ese libro." if libro is None else f"-> Encontrado: {libro}")
 
 
def opcion_disponibles(biblio):
    disponibles = biblio.libros_disponibles()
    print(f"Disponibles ({biblio.cantidad_disponible()}):")
    if not disponibles:
        print("   (ninguno)")
    for libro in disponibles:
        print("   ", libro)
 
 
def opcion_prestar(biblio):
    titulo = input("Titulo a prestar: ")
    print("->", biblio.registrar_prestamo(USUARIO, titulo))
    biblio.guardar_en_json(ARCHIVO)          # persistimos el cambio de estado
 
 
def opcion_devolver(biblio):
    titulo = input("Titulo a devolver: ")
    print("->", biblio.registrar_devolucion(titulo))
    biblio.guardar_en_json(ARCHIVO)
 
 
def opcion_historial_global(biblio):
    Historial(biblio._prestamos).ver_historial_global()
 
 
def opcion_prestamos_activos(biblio):
    Historial(biblio._prestamos).ver_prestamos_activos()
 
 
def main():
    biblio = Biblioteca()
    biblio.cargar_desde_json(ARCHIVO)        # carga lo guardado al iniciar
    opciones = {
        "1": opcion_agregar, "2": opcion_catalogo, "3": opcion_buscar,
        "4": opcion_disponibles, "5": opcion_prestar, "6": opcion_devolver,
        "7": opcion_historial_global, "8": opcion_prestamos_activos,
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
 