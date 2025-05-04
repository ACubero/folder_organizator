# Organizador de Archivos por Extensión

Este script de Python te ayuda a organizar los archivos dentro de una carpeta y todas sus subcarpetas, moviéndolos automáticamente a nuevas carpetas nombradas según su extensión.

## Características

*   Pide al usuario la ruta de la carpeta a organizar.
*   Recorre recursivamente todas las subcarpetas.
*   Identifica la extensión de cada archivo (o los etiqueta como "sin_extension").
*   Crea una subcarpeta con el nombre de la extensión (ej: `txt`, `jpg`, `pdf`, `sin_extension`) dentro de la carpeta de origen.
*   Mueve cada archivo a la carpeta de la extensión correspondiente.
*   Maneja conflictos de nombres añadiendo sufijos (`_1`, `_2`, etc.) si ya existe un archivo con el mismo nombre en el destino.
*   **Opcionalmente:** Pregunta al inicio si deseas eliminar las carpetas o subcarpetas que queden vacías después de mover los archivos (las nuevas carpetas de extensión y la carpeta de origen principal no se eliminan).

## Requisitos

*   Python 3 (las librerías `os` y `shutil` son estándar).

## Cómo Usar

1.  Guarda el código del script como `organizador_archivos.py`.
2.  Abre una terminal o línea de comandos.
3.  Navega hasta la carpeta donde guardaste el script.
4.  Ejecuta el script con el siguiente comando:

    ```bash
    python organizador_archivos.py
    ```
5.  El script te pedirá que introduzcas la ruta completa de la carpeta que deseas organizar. Introduce la ruta y presiona Enter.
6.  A continuación, te preguntará si deseas eliminar las carpetas vacías al finalizar. Responde `s` (o `si`/`yes`) si quieres limpiarlas, o `n` (o cualquier otra cosa) si prefieres conservarlas.
7.  El script comenzará a procesar los archivos, mostrando mensajes sobre los movimientos.
8.  Una vez completado el movimiento (y opcionalmente la limpieza), el script finalizará.

## Manejo de Duplicados

Si al intentar mover un archivo, ya existe un archivo con el mismo nombre en la carpeta de destino, el script añadirá automáticamente un sufijo numérico al nuevo archivo antes de moverlo (ej: `mi_foto.jpg` se convertiría en `mi_foto_1.jpg`, `mi_foto_2.jpg`, etc.).

## Eliminación de Carpetas Vacías (Opcional)

Si seleccionas la opción de eliminar carpetas vacías, el script recorrerá de nuevo la estructura original y eliminará cualquier carpeta que haya quedado *completamente* vacía después de que sus archivos hayan sido movidos.

**Importante:**
*   La carpeta principal que especificaste no será eliminada, aunque quede vacía.
*   Las **nuevas carpetas** creadas para las extensiones (ej: `txt`, `jpg`) **tampoco serán eliminadas**, incluso si por alguna razón quedaran vacías. Solo se eliminan las subcarpetas *originales* que queden vacías.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.