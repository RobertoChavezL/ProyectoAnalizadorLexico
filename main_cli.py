# main_cli.py
# Este archivo proporciona una interfaz de línea de comandos (CLI) para el analizador.
# Es útil para pruebas rápidas, automatización o entornos sin GUI.
"""
Interfaz de Línea de Comandos (CLI) para el Analizador "Natural a JSON".

Este script permite interactuar con el motor de análisis (`analyzer_core`)
directamente desde la terminal. Ofrece la posibilidad de procesar un archivo
específico pasado como argumento o entrar en un modo interactivo para
seleccionar archivos de un directorio de ejemplos.
Es ideal para pruebas rápidas, depuración y uso en entornos sin GUI.
"""
import sys
import argparse
import os
from analyzer_core import analyze_and_transform # Importamos la función principal del motor

def list_and_select_test_file(test_files_dir="ejemplos_entrada", file_extension=".txt", processed_files=None):
    """
    Lista archivos de un directorio y permite al usuario seleccionar uno para procesar.

    Muestra los archivos con una extensión específica del directorio dado.
    Permite al usuario seleccionar un archivo por número, procesar todos los
    archivos no procesados previamente en la sesión, o salir.
    Lleva un registro de los archivos ya procesados en la sesión actual
    para evitar reprocesamientos innecesarios al seleccionar "todos" o al listar.

    Args:
        test_files_dir (str, optional): Directorio donde buscar los archivos de prueba.
                                        Defaults to "ejemplos_entrada".
        file_extension (str, optional): Extensión de los archivos a listar.
                                        Defaults to ".txt".
        processed_files (set, optional): Conjunto de nombres de archivo (sin ruta)
                                         que ya han sido procesados en la sesión actual.
                                         Se utiliza para marcar visualmente y para la opción 'todos'.
                                         Defaults to None, en cuyo caso se inicializa un set vacío.

    Returns:
        tuple: (str|None, set)
            - El primer elemento es una cadena:
                - "salir": si el usuario elige salir.
                - "todos": si el usuario elige procesar todos los archivos pendientes.
                - ruta_completa_del_archivo_seleccionado: si se selecciona un archivo específico.
                - None: si ocurre un error al listar archivos o no hay archivos.
            - El segundo elemento es el conjunto `processed_files` actualizado (aunque esta función
              ya no lo modifica directamente, lo devuelve para mantener la interfaz).
    """
    if processed_files is None:
        processed_files = set()

    # Validación de la existencia del directorio de pruebas
    if not os.path.exists(test_files_dir) or not os.path.isdir(test_files_dir):
        print(f"ADVERTENCIA: Directorio de pruebas '{test_files_dir}' no encontrado.", file=sys.stderr)
        return None, processed_files

    available_files = []
    try:
        all_entries = os.listdir(test_files_dir)
        # Filtrar archivos por extensión
        for entry in all_entries:
            if entry.endswith(file_extension) and os.path.isfile(os.path.join(test_files_dir, entry)):
                available_files.append(entry)
    except OSError as e:
        print(f"Error listando archivos en '{test_files_dir}': {e}", file=sys.stderr)
        return None, processed_files

    # Si no se encuentran archivos con la extensión especificada
    if not available_files:
        print(f"No se encontraron archivos '{file_extension}' en '{test_files_dir}'.", file=sys.stderr)
        return None, processed_files

    print("\nArchivos de prueba disponibles en '{}':".format(test_files_dir))
    displayable_files = []
    # Mostrar archivos con un marcador si ya fueron procesados en la sesión
    for i, filename in enumerate(available_files):
        marker = "[✓]" if filename in processed_files else "[ ]"
        print(f"  {marker} {i+1}. {filename}")
        displayable_files.append(filename)
    
    if len(processed_files) == len(available_files) and available_files:
         print("Todos los archivos disponibles han sido procesados en esta sesión.")

    # Bucle para la selección del usuario
    while True:
        try:
            choice = input(f"Selecciona un archivo por número (1-{len(displayable_files)}), 'todos', o 's' para salir: ").strip().lower()
            if choice == 's':
                return "salir", processed_files
            if choice == 'todos':
                return "todos", processed_files
            # Intenta convertir la elección a un número
            choice_num = int(choice)
            if 1 <= choice_num <= len(displayable_files):
                selected_filename = displayable_files[choice_num - 1]
                # Devolver la ruta completa del archivo seleccionado
                return os.path.join(test_files_dir, selected_filename), processed_files
            else:
                print("Selección inválida. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número, 'todos' o 's'.")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la selección: {e}")
            return None, processed_files


def run_analysis_for_cli(source_name, content):
    """
    Ejecuta el análisis del contenido proporcionado y muestra los resultados en la CLI.

    Invoca la función `analyze_and_transform` del `analyzer_core` y luego
    imprime los tokens, el árbol de parseo (si se generó), el JSON resultante
    (si no hubo errores), un resumen de errores (si los hubo) y estadísticas
    del análisis. También ofrece la opción de guardar el JSON generado.

    Args:
        source_name (str): Un nombre identificador para la fuente del contenido
                           (ej. nombre de archivo), usado en los mensajes.
        content (str): El contenido textual a analizar.
    """
    print("\n" + "═"*70)
    title_text = f"Iniciando Análisis para: '{source_name}'"
    print(f"║ {title_text.center(70-4)} ║")
    print("═"*70)

    # Llamada al motor de análisis. Devuelve 6 valores:
    # json_string, tokens_string, parsetree_lisp_string, parsetree_qt_model, error_summary_string, stats_dict
    json_s, tokens_s, tree_lisp_s, _qt_model, errors_s, stats_data = analyze_and_transform(source_name, content)

    # Mostrar siempre los tokens reconocidos
    print(tokens_s)

    # Mostrar errores si existen
    if errors_s:
        print(errors_s, file=sys.stderr) # Errores a stderr
    
    # Imprimir árbol LISP si está disponible y no hubo errores críticos que impidieran su generación
    if not errors_s and tree_lisp_s:
        print(tree_lisp_s)

    # Procesar y mostrar JSON y estadísticas si no hubo errores y se generó JSON
    if json_s and not errors_s: # Si se generó JSON y no hubo errores reportados por el analizador
        print("--- JSON Generado ---")
        print(json_s)
        print("---------------------")

        # Mostrar estadísticas del análisis
        if stats_data:
            print("\n--- Estadísticas del Análisis ---")
            print(f"  Tiempo de análisis: {stats_data['tiempo_analisis_seg']:.4f} segundos")
            print(f"  Comandos procesados: {stats_data['comandos_procesados']}")
            print(f"  Tokens enviados al parser: {stats_data['tokens_al_parser']}")
            print(f"  Errores léxicos: {stats_data['errores_lexicos']}")
            print(f"  Errores sintácticos: {stats_data['errores_sintacticos']}")
            print("-------------------------------\n")
        print("Proceso completado. JSON generado.")

        # Opción para guardar el JSON generado
        save_choice = input("¿Desea guardar este JSON en un archivo? (s/n): ").strip().lower()
        if save_choice == 's':
            default_output_filename = os.path.splitext(os.path.basename(source_name))[0] + "_output.json"
            output_filename = input(f"Ingrese nombre para el archivo JSON (default: {default_output_filename}): ").strip()
            if not output_filename:
                output_filename = default_output_filename
            try:
                # Crear directorio de salida si no existe
                output_dir = "salidas_json_cli"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                full_output_path = os.path.join(output_dir, output_filename)

                with open(full_output_path, "w", encoding="utf-8") as outfile:
                    outfile.write(json_s)
                print(f"JSON guardado en '{full_output_path}'")
            except Exception as e:
                print(f"Error al guardar el archivo JSON: {e}", file=sys.stderr)

    elif errors_s: # Si hubo errores reportados por el analizador
        print("\nEl proceso finalizó con errores. No se generó JSON.", file=sys.stderr)
    else: # No hubo errores, pero tampoco se generó JSON (ej. entrada vacía o solo comentarios)
        print("\nAnálisis completado. No se generó JSON (entrada vacía o solo comentarios).")
        if stats_data: # Mostrar estadísticas incluso si no se generó JSON (ej. para entrada vacía)
            print("\n--- Estadísticas del Análisis ---")
            print(f"  Tiempo de análisis: {stats_data['tiempo_analisis_seg']:.4f} segundos")
            # ... (podrías repetir el bloque de estadísticas aquí si es relevante)
            print(f"  Comandos procesados: {stats_data['comandos_procesados']}")


def main_cli():
    """
    Función principal para la ejecución de la interfaz de línea de comandos.

    Configura el parser de argumentos para aceptar un archivo de entrada opcional.
    Si se proporciona un archivo, lo procesa directamente.
    Si no, entra en un modo interactivo que permite al usuario seleccionar
    archivos de un directorio de ejemplos para analizar.
    """
    # Mensaje de advertencia para indicar que es una versión de prueba/depuración
    print("*"*70)
    print("*" + " ".center(68) + "*")
    print("*" + "MODO DE PRÁCTICA/DEPURACIÓN - INTERFAZ DE LÍNEA DE COMANDOS (CLI)".center(68) + "*")
    print("*" + "Esta versión es para pruebas y no representa la aplicación final.".center(68) + "*")
    print("*" + " ".center(68) + "*")
    print("*"*70)

    default_examples_dir = "ejemplos_entrada"
    if not os.path.exists(default_examples_dir):
        try:
            os.makedirs(default_examples_dir)
            print(f"INFO: Directorio '{default_examples_dir}' creado. Coloca tus archivos .txt de prueba aquí.")
        except OSError as e:
            print(f"ADVERTENCIA: No se pudo crear el directorio '{default_examples_dir}': {e}", file=sys.stderr)

    # Configuración del parser de argumentos de línea de comandos
    arg_parser = argparse.ArgumentParser(
        description='Analizador (CLI) para lenguaje "Natural a JSON".',
        formatter_class=argparse.RawTextHelpFormatter
    )
    arg_parser.add_argument(
        'input_file', nargs='?', type=str, default=None,
        help='(Opcional) Archivo de entrada a procesar directamente.'
    )
    args = arg_parser.parse_args()

    # Conjunto para rastrear archivos procesados durante la sesión interactiva
    processed_in_session = set()

    # Si se proporciona un archivo como argumento, procesarlo directamente
    if args.input_file:
        source_name = args.input_file
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            run_analysis_for_cli(source_name, content)
        except FileNotFoundError:
            print(f"Error Crítico: Archivo '{args.input_file}' no encontrado.", file=sys.stderr); sys.exit(1)
        except Exception as e:
            print(f"Error Crítico al leer archivo '{args.input_file}': {e}", file=sys.stderr); sys.exit(1)
    else: # Modo interactivo si no se proporciona un archivo
        while True:
            print("\n" + "="*70)
            print("MODO INTERACTIVO CLI - SELECCIÓN DE ARCHIVO".center(70))
            print("="*70)
            
            # Obtener la selección del usuario (archivo, 'todos', 'salir', o None)
            selection_result, temp_processed = list_and_select_test_file(default_examples_dir, processed_files=processed_in_session)
            # `temp_processed` no se usa aquí ya que `list_and_select_test_file` no modifica `processed_in_session`
            # list_and_select_test_file ya no modifica processed_in_session directamente

            if selection_result == "salir" or selection_result is None:
                print("Saliendo del modo interactivo.")
                break
            
            files_to_process_this_round = []
            # Si el usuario elige 'todos'
            if selection_result == "todos":
                print("\nProcesando todos los archivos no procesados en '{}'...".format(default_examples_dir))
                all_files_in_dir = [os.path.join(default_examples_dir, f) 
                                    for f in os.listdir(default_examples_dir) 
                                    if f.endswith(".txt") and os.path.isfile(os.path.join(default_examples_dir, f))]
                
                # Añadir a la lista de procesamiento solo los que no han sido procesados en esta sesión
                for file_path in all_files_in_dir:
                    if os.path.basename(file_path) not in processed_in_session:
                        files_to_process_this_round.append(file_path)
                
                if not files_to_process_this_round and all_files_in_dir:
                     print("Todos los archivos ya habían sido procesados en esta sesión.")
                elif not all_files_in_dir:
                     print(f"No se encontraron archivos .txt en '{default_examples_dir}'.")
            else: # Si se seleccionó un archivo específico
                files_to_process_this_round.append(selection_result)

            # Procesar los archivos seleccionados (puede ser uno o varios si fue 'todos')
            for file_path_to_process in files_to_process_this_round:
                filename_only = os.path.basename(file_path_to_process)
                try:
                    # Leer contenido del archivo
                    with open(file_path_to_process, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Ejecutar el análisis
                    run_analysis_for_cli(filename_only, content) # Usar filename_only para source_name
                    processed_in_session.add(filename_only) # Marcar como procesado
                except Exception as e:
                    print(f"Error procesando '{filename_only}': {e}", file=sys.stderr)
            
            if selection_result != "salir":
                cont = input("\n¿Desea procesar otro archivo o ver la lista? (s/n): ").strip().lower()
                # Salir del bucle interactivo si el usuario no quiere continuar
                if cont != 's':
                    print("Saliendo del modo interactivo.")
                    break
            else:
                break

if __name__ == '__main__':
    main_cli()