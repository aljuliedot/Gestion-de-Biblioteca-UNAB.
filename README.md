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
flowchart TD
  n0[+ registrar_prestamo(usuario, titulo)]
  n1[]
  n2[+ esta_prestado(): bool]
  n3[+ get_contrasena()]
  n1 -->|asocia| n2
  n0 -->|agrega  0..*| n2
  n0 -->|registra  0..*| n1
  n1 -->|asocia| n3

  n4[+ ver_historial_usuario(usuario): list]
  n5[+ ver_prestamos_activos(): list]
  n6[+ ver_historial_global(): list]
  n7[- _prestamos: list]
  n8[]

  n9[- _titulo]
  n10[- _autor]
  n11[- _genero]

  n12[+ get_editorial(): str]
  n13[+ get_genero(): str]
  n14[+ get_autor(): str]
  n15[]
  n16[+ get_titulo(): str]
  n17[- _editorial]
  n18[- _esta_prestado: bool]
  n19[+ devolver()]
  n20[+ prestar(): bool]
  n21[+ registrar_devolucion(titulo)]

  n22[+ ejecutar(libros, preferencia)]
  n23[+ ejecutar(libros, preferencia)]
  n24[+ iniciar_sesion(pass)]
  n25[+ ejecutar(libros, preferencia)]
  n26[- _libro]
  n27[- _usuario]
  n28[- _fecha]
  n29[- _esta_vigente: bool]
  n30[+ obtener_libro(): Libro]
  n31[+ obtener_usuario()]
  n32[+ obtener_fecha_inicio()]
  n33[+ set_estrategia(e)]
  n34[]
  n35[- _estrategia]
  n36[+ ejecutar_estrategia(libros, pref)]
  n37[+ terminar_prestamo()]
  n38[+ comprobar_si_esta_vigente(): bool]

  n39[]
  n40[- _prestamos: list]
  n41[- _libros: list]
  n42[+ agregar_libro(libro)]
  n43[+ buscar_libro(titulo): Libro]
  n44[+ cantidad_disponible(): int]
  n45[+ libros_disponibles(): list]
  n46[+ catalogo(): list]

  n47[+ set_nombre(n)]
  n48[+ get_email()]
  n49[+ set_email(e)]
  n50[]
  n51[- _contrasena]
  n52[+ get_nombre()]
  n53[- _nombre]
  n54[- _email]
```