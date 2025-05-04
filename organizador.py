import os
import shutil
import sys
import time # Para añadir un pequeño retraso si es necesario (opcional, no incluido por defecto)

def organizar_archivos_por_extension():
    """
    Pide al usuario una ruta de carpeta, la recorre recursivamente,
    mueve cada archivo a una subcarpeta dentro de la carpeta de origen
    nombrada según su extensión, manejando duplicados.
    Finalmente, opcionalmente elimina las carpetas vacías restantes.
    """
    print("--- Organizador de Archivos por Extensión ---")

    # 1. Pedir la ruta de la carpeta al usuario
    carpeta_origen = input("Por favor, introduce la ruta de la carpeta a organizar: ")

    # Validar que la ruta existe y es una carpeta
    if not os.path.exists(carpeta_origen):
        print(f"Error: La ruta '{carpeta_origen}' no existe.")
        sys.exit(1)
    if not os.path.isdir(carpeta_origen):
        print(f"Error: La ruta '{carpeta_origen}' no es una carpeta válida.")
        sys.exit(1)

    # Obtener la ruta absoluta de la carpeta de origen para comparaciones seguras
    carpeta_origen_abs = os.path.abspath(carpeta_origen)

    print(f"\nIniciando la organización de la carpeta: {carpeta_origen}")

    # Conjunto para almacenar las rutas absolutas de las carpetas de extensión creadas
    # Las excluiremos de la limpieza posterior aunque queden vacías
    carpetas_extension_creadas = set()

    # 2. Recorrer la carpeta y subcarpetas (Top-Down para mover archivos)
    # os.walk(..., topdown=True) es el comportamiento por defecto
    print("\nMoviendo archivos...")
    archivos_procesados_count = 0

    # Capturamos posibles errores durante el walk (como permisos)
    try:
        for ruta_actual, directorios, archivos in os.walk(carpeta_origen_abs, topdown=True):

            # Evitar procesar los archivos que ya están DENTRO de una carpeta de extensión
            # ya que estas carpetas se crean directamente en la carpeta_origen_abs
            if os.path.abspath(ruta_actual) in carpetas_extension_creadas:
                 # print(f"Saltando directorio de extensión ya creado: {ruta_actual}") # Descomentar para depurar
                 continue # No procesar subdirectorios que ya son carpetas de destino

            # Procesar cada archivo encontrado en la carpeta actual
            for nombre_archivo in archivos:
                ruta_completa_origen = os.path.join(ruta_actual, nombre_archivo)

                # Asegurarse de que es un archivo real y no está en una de las carpetas de extensión ya creadas
                if not os.path.isfile(ruta_completa_origen):
                    continue

                # Evitar procesar archivos que ya están en una carpeta de extensión
                # Esto es una doble verificación, aunque el 'continue' de arriba debería bastar
                if os.path.dirname(os.path.abspath(ruta_completa_origen)) in carpetas_extension_creadas:
                     # print(f"Saltando archivo ya en carpeta de extensión: {ruta_completa_origen}") # Descomentar para depurar
                     continue


                # 3. Obtener la extensión del archivo
                nombre_base, extension = os.path.splitext(nombre_archivo)

                # Limpiar la extensión (quitar el punto inicial, convertir a minúsculas)
                if extension:
                    nombre_carpeta_extension = extension[1:].lower()
                    # Manejar casos como .tar.gz, donde splitext solo da '.gz'
                    # Si quieres una carpeta 'gz' para .tar.gz, el código actual es correcto.
                    # Si quieres una carpeta 'tar.gz', necesitarías una lógica diferente.
                    # Dejamos el comportamiento actual (extensión simple).
                else:
                    nombre_carpeta_extension = "sin_extension"

                # 4. Determinar la carpeta de destino
                # Las nuevas carpetas de extensión se crearán DENTRO de la carpeta de origen principal
                carpeta_destino_base = os.path.join(carpeta_origen_abs, nombre_carpeta_extension)

                # 5. Crear la carpeta de destino si no existe y añadirla a nuestro conjunto
                try:
                    os.makedirs(carpeta_destino_base, exist_ok=True)
                    carpetas_extension_creadas.add(os.path.abspath(carpeta_destino_base)) # Añadir la ruta absoluta
                except OSError as e:
                    print(f"Error al crear la carpeta '{carpeta_destino_base}': {e}")
                    continue

                # 6. Determinar la ruta completa de destino para el archivo
                ruta_completa_destino_inicial = os.path.join(carpeta_destino_base, nombre_archivo)
                ruta_completa_destino = ruta_completa_destino_inicial # Ruta de trabajo

                # 7. Manejar posibles conflictos de nombre
                contador = 1
                # Mientras el archivo ya exista en la ubicación de destino
                while os.path.exists(ruta_completa_destino):
                    nuevo_nombre_archivo = f"{nombre_base}_{contador}{extension}"
                    ruta_completa_destino = os.path.join(carpeta_destino_base, nuevo_nombre_archivo)
                    contador += 1

                # 8. Mover el archivo
                # Comprobar si el archivo ya está en la ubicación de destino resuelta
                # Esto puede pasar si el script se ejecuta varias veces
                if os.path.abspath(ruta_completa_origen) == os.path.abspath(ruta_completa_destino):
                     print(f"Saltando: '{ruta_completa_origen}' ya está en su ubicación destino resuelta.")
                     continue

                try:
                    print(f"Moviendo '{ruta_completa_origen}' a '{ruta_completa_destino}'")
                    shutil.move(ruta_completa_origen, ruta_completa_destino)
                    archivos_procesados_count += 1

                except shutil.Error as e:
                    print(f"Error al mover '{ruta_completa_origen}': {e}")
                except Exception as e:
                    print(f"Ocurrió un error inesperado al mover '{ruta_completa_origen}': {e}")

    except Exception as e:
        print(f"\nOcurrió un error durante el recorrido de archivos: {e}")


    print(f"\nProceso de movimiento de archivos completado. Se procesaron {archivos_procesados_count} archivos.")

    # 9. Preguntar al usuario si desea eliminar carpetas vacías
    respuesta = input("¿Deseas eliminar las carpetas o subcarpetas vacías que queden (excepto las de extensión creada)? (s/n): ").lower().strip()

    if respuesta in ['s', 'si', 'yes']:
        print("\nEliminando carpetas vacías...")
        carpetas_eliminadas_count = 0
        errores_eliminacion_count = 0

        # 10. Recorrer la carpeta de nuevo (Bottom-Up para eliminar directorios)
        # topdown=False es crucial aquí para eliminar primero los subdirectorios
        try:
            # Creamos una copia de la lista de directorios para evitar problemas
            # si os.rmdir modifica el sistema de archivos mientras os.walk itera
            # Aunque os.walk con topdown=False es más seguro, es una buena práctica
            for ruta_actual, directorios, archivos in os.walk(carpeta_origen_abs, topdown=False):

                # 11. Comprobar si la carpeta está vacía
                # os.listdir() lista los contenidos de un directorio
                # Si está vacía, la lista es []
                if not directorios and not archivos: # O simplemente: if not os.listdir(ruta_actual):

                    # 12. NO eliminar la carpeta de origen principal ni las carpetas de extensión creadas
                    if os.path.abspath(ruta_actual) == carpeta_origen_abs:
                        # print(f"Saltando la carpeta raíz: {ruta_actual}") # Descomentar para depurar
                        continue # No eliminar la carpeta que el usuario especificó

                    if os.path.abspath(ruta_actual) in carpetas_extension_creadas:
                        # print(f"Saltando carpeta de extensión creada: {ruta_actual}") # Descomentar para depurar
                        continue # No eliminar las carpetas que creamos para extensiones

                    # Si está vacía y no es la raíz ni una carpeta de extensión creada, intentar eliminar
                    try:
                        os.rmdir(ruta_actual)
                        print(f"Carpeta vacía eliminada: {ruta_actual}")
                        carpetas_eliminadas_count += 1
                    except OSError as e:
                        # Esto puede ocurrir si la carpeta no está realmente vacía (ej: archivo oculto, permisos)
                        # o si otro proceso la modificó entre la comprobación y el rmdir
                        print(f"No se pudo eliminar la carpeta '{ruta_actual}': {e}")
                        errores_eliminacion_count += 1
                    except Exception as e:
                         print(f"Ocurrió un error inesperado al eliminar '{ruta_actual}': {e}")
                         errores_eliminacion_count += 1

        except Exception as e:
            print(f"\nOcurrió un error durante la eliminación de carpetas vacías: {e}")


        print(f"\nProceso de eliminación de carpetas vacías completado.")
        print(f"Carpetas vacías eliminadas: {carpetas_eliminadas_count}")
        if errores_eliminacion_count > 0:
             print(f"Errores al intentar eliminar carpetas: {errores_eliminacion_count}")

    else:
        print("\nLas carpetas vacías no serán eliminadas.")


    print("\n--- Proceso General Finalizado ---")

# Bloque principal para ejecutar la función
if __name__ == "__main__":
    organizar_archivos_por_extension()