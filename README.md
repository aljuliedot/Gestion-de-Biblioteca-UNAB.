# Sistema de Gestión de Biblioteca

## Integrantes

- Pereyra Joaquín Gabriel.
- Mateo Joaquín Rivero Correa.
- Jorge Ordoñez.
- Aldana Gonzalez.

## Descripción

Este repositorio contiene un Sistema de Gestión de Biblioteca, en el cual se podrá gestionar usuarios, libros y prestamos. Su función principal sería la recomendación de libros, en la que cada usuario dependiendo del contenido que lea se le dará posibles sugerencias para llevar. 

Este proyecto fue programado con el lenguaje de programación Python junto con el uso del paradigma de Programación Orientada a Objetos. Se hizo de esta manera para controlar mejor cada clase y debido a la facilidad de codificar con este lenguaje.

## Instrucciones de Uso

> [!IMPORTANT]
> Para la función correcta del código, se debe instalar los siguientes módulos: ***datetime***, ***werkzeug.security*** y ***customtkinter.***

[EN CONSTRUCCIÓN]

## Diagrama de Clases

```mermaid
classDiagram
class "+ registrar_prestamo(usuario, titulo)" {
}
class "+ esta_prestado(): bool" {
}
class "+ get_contrasena()" {
}
class "+ ver_historial_usuario(usuario): list" {
}
class "+ ver_prestamos_activos(): list" {
}
class "+ ver_historial_global(): list" {
}
class "- _prestamos: list" {
}
class "" {
}
class "- _titulo" {
}
class "- _autor" {
}
class "- _genero" {
}
class "+ get_editorial(): str" {
}
class "+ get_genero(): str" {
}
class "+ get_autor(): str" {
}
class "+ get_titulo(): str" {
}
class "- _editorial" {
}
class "- _esta_prestado: bool" {
}
class "+ devolver()" {
}
class "+ prestar(): bool" {
}
class "+ registrar_devolucion(titulo)" {
}
class "+ ejecutar(libros, preferencia)" {
}
class "+ iniciar_sesion(pass)" {
}
class "- _libro" {
}
class "- _usuario" {
}
class "- _fecha" {
}
class "- _esta_vigente: bool" {
}
class "+ obtener_libro(): Libro" {
}
class "+ obtener_usuario()" {
}
class "+ obtener_fecha_inicio()" {
}
class "+ set_estrategia(e)" {
}
class "- _estrategia" {
}
class "+ ejecutar_estrategia(libros, pref)" {
}
class "+ terminar_prestamo()" {
}
class "+ comprobar_si_esta_vigente(): bool" {
}
class "- _libros: list" {
}
class "+ agregar_libro(libro)" {
}
class "+ buscar_libro(titulo): Libro" {
}
class "+ cantidad_disponible(): int" {
}
class "+ libros_disponibles(): list" {
}
class "+ catalogo(): list" {
}
class "+ set_nombre(n)" {
}
class "+ get_email()" {
}
class "+ set_email(e)" {
}
class "- _contrasena" {
}
class "+ get_nombre()" {
}
class "- _nombre" {
}
class "- _email" {
}
"" --> "+ esta_prestado(): bool" : asocia
"+ registrar_prestamo(usuario, titulo)" o--> "+ esta_prestado(): bool" : agrega  0..*
"+ registrar_prestamo(usuario, titulo)" o--> "" : registra  0..*
"" --> "+ get_contrasena()" : asocia
```