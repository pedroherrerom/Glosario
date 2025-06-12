glosario.py

Crea una base de datos llamada glosario.db, en ella se guarda: palabra en español, traducción en inglés, tipo de palabra (sustantivo, adjetivo, etc). Además genera una interfaz gráfica para que sea más comodo introducir las palabras.

El programa original es una aplicación de escritorio para gestionar un glosario de palabras inglés-español, utilizando:

SQLite como base de datos.

Tkinter para la interfaz gráfica.

CSV para exportar datos.

  Funcionalidades Principales:

✅ Gestión de palabras:

Añadir nuevas palabras (inglés, español, categoría, ejemplo, notas).

Editar palabras existentes.

Eliminar palabras.

Buscar palabras por término o categoría.

✅ Visualización de datos:

Tabla con todas las palabras.

Filtrado por categoría.

Búsqueda por palabra en inglés.

✅ Exportación:

Guardar el glosario completo en formato CSV.

----------------------------------------------------------------------

glosario_multiples.py

Descripción General:
Mantiene todas las funcionalidades del original, pero añade:

Selección de múltiples glosarios.

Ventana inicial mejorada (más grande y organizada).

Posibilidad de crear nuevos glosarios con nombre personalizado.

Nuevas Funcionalidades:

🚀 Pantalla de inicio con dos opciones:

Crear nuevo glosario (el usuario elige el nombre).

Abrir glosario existente (lista desplegable con bases de datos .db disponibles).

🚀 Múltiples glosarios:

Ahora puedes tener varios archivos .db (ej: vocabulario.db, tecnicismos.db).

Al iniciar la app, puedes elegir cuál editar.

🚀 Interfaz más amigable:

Ventana inicial más grande

Diseño mejor organizado con secciones claras.

Mensajes más descriptivos.

----------------------------------------------------------------------

juego_vocabulario.py

Juego para practicar el vocabulario en inglés y español:

Proporciona una palabra aleatoria de la base de datos glosario.db, y el usuario debe proporcionar la traducción

Funcionalidades:

Versión 1.1
- Modos de juego: traducción de español a inglés y de inglés a español.
- Tipo de palabra: permite elegir el tipo de palabra que aparece en el juego, entre sustantivos, adjetivos, adverbios / conectores, verbos o todas a la vez.

Versión 1.2
- Elimina las palabras acertadas y solo muestra las incorrectas.
- Muestra cuantas palabras hay en la base de datos de ese tipo y cuantas faltan por acertar
