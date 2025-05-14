# Proyecto: Analizador "Natural a JSON"

## Integrantes
*   Carlos Verastegui Cruz
*   Roberto Chavez Lopez

## Información del Curso
*   Materia: Programación de Sistemas de Base 1
*   Profesor: Muñoz Quintero Dante Adolfo
*   Institución: Universidad Autónoma de Tamaulipas
*   Semestre: 8° I
*   Fecha de Entrega del Proyecto: 13 de Mayo de 2025

## Descripción del Proyecto
"Natural a JSON" es una herramienta de software diseñada para convertir instrucciones estructuradas escritas en un subconjunto del español a formato JSON válido. El proyecto aplica los principios del análisis léxico y sintáctico para interpretar los comandos de entrada, validarlos según una gramática formal, y generar la estructura JSON correspondiente.

El sistema ofrece dos interfaces de usuario:
1.  Una Interfaz de Línea de Comandos (CLI) para pruebas rápidas, procesamiento de archivos por lotes y uso en entornos sin GUI.
2.  Una Interfaz Gráfica de Usuario (GUI) desarrollada con PyQt5, que proporciona una experiencia más visual e interactiva para la entrada de comandos, carga de archivos, y visualización de los resultados del análisis (tokens, árbol de parseo, JSON generado y errores).

El lenguaje de entrada permite definir objetos y listas JSON mediante comandos simples como "CREAR OBJETO <nombre> CON <clave>:<valor>, ..." y "CREAR LISTA <nombre> CON ELEMENTOS <valor1>, ...". Soporta tipos de datos como strings, números (enteros y decimales) y booleanos, además de identificadores con caracteres del español y comentarios.

## Estructura del Repositorio



├── NaturalToJson.g4 # Archivo de gramática ANTLR v4 para el lenguaje
├── analyzer_core.py # Módulo con la lógica central del analizador y listeners
├── main_cli.py # Script para la Interfaz de Línea de Comandos
├── main_gui.py # Script para la Interfaz Gráfica de Usuario (PyQt5)
├── generated/ # Carpeta con el código Python generado por ANTLR
│ ├── NaturalToJsonLexer.py
│ ├── NaturalToJsonParser.py
│ ├── NaturalToJsonListener.py
│ ├── NaturalToJsonVisitor.py (si se generó)
│ └── ... (otros archivos .tokens, .interp)
├── ejemplos_entrada/ # Carpeta con archivos .txt de ejemplo para probar
│ ├── ejemplo_complejo.txt
│ ├── ejemplo_con_error_lexico.txt
│ ├── ... (archivos de prueba)
├── salidas_json/ # (Opcional) Carpeta donde se pueden guardar los JSON generados
└── README.md # Este archivo

## Requisitos Previos
Para ejecutar este proyecto o regenerar el analizador desde la gramática, necesitarás:
1.  Python 3: Versión 3.7 o superior.
2.  Java Development Kit (JDK): Versión 8 o superior (solo necesario para ejecutar la herramienta ANTLR y regenerar los archivos del analizador desde ".g4").
3.  ANTLR 4 Python runtime: Instalar usando pip:
    pip install antlr4-python3-runtime    
4.  PyQt5: Para la interfaz gráfica. Instalar usando pip:
    pip install PyQt5    
5.  (Opcional) Herramienta ANTLR 4: El archivo JAR de ANTLR (ej. "antlr-4.13.2-complete.jar") si deseas regenerar el lexer/parser desde el archivo "NaturalToJson.g4". Puedes descargarlo desde [antlr.org](https://www.antlr.org/download.html).

## Instrucciones para Regenerar el Analizador desde la Gramática (Opcional)
Si realizas cambios en "NaturalToJson.g4" y necesitas regenerar los archivos Python del lexer y parser:
1.  Asegúrate de tener el JAR de ANTLR 4 (ej. "antlr-4.13.2-complete.jar") en la raíz del proyecto o en una ubicación accesible.
2.  Abre una terminal o símbolo del sistema en la raíz del proyecto.
3.  Ejecuta el siguiente comando (ajusta el nombre del JAR si es diferente):
    java -jar antlr-4.13.2-complete.jar NaturalToJson.g4 -Dlanguage=Python3 -o generated -visitor -listener
    Esto generará/actualizará los archivos en la carpeta "generated/".

## Instrucciones para Ejecutar la Aplicación

### 1. Interfaz Gráfica de Usuario (GUI)
Para la experiencia más completa e interactiva:
1.  Abre una terminal o símbolo del sistema en la raíz del proyecto.
2.  Ejecuta el siguiente comando:
    python main_gui.py
    Esto abrirá la ventana de la aplicación. Desde allí podrás:
    *   Escribir comandos directamente.
    *   Cargar archivos ".txt" desde la carpeta "ejemplos_entrada/" o cualquier otra ubicación.
    *   Analizar la entrada y ver los tokens, el árbol de parseo, el JSON generado y los errores.
    *   Guardar tu entrada o el JSON resultante.
    *   Acceder a la ayuda con ejemplos de sintaxis.

### 2. Interfaz de Línea de Comandos (CLI)
Para pruebas rápidas o uso sin entorno gráfico:
1.  Abre una terminal o símbolo del sistema en la raíz del proyecto.
2.  Para procesar un archivo específico:
    python main_cli.py ejemplos_entrada/nombre_del_archivo.txt
    Reemplaza "nombre_del_archivo.txt" con el archivo que deseas analizar.
3.  Para modo interactivo:
    python main_cli.py
    Esto te presentará un menú para seleccionar archivos de la carpeta "ejemplos_entrada/" o procesarlos todos.

## Breve Descripción del Lenguaje "Natural a JSON"
El lenguaje permite definir:
*   Objetos: "CREAR OBJETO <nombreObjeto> CON <clave1>:<valor1>, <clave2>:<valor2>, ..."
*   Listas: "CREAR LISTA <nombreLista> CON ELEMENTOS <valor1>, <valor2>, ..."

Tipos de datos soportados para los valores:
*   Strings: ""texto entre comillas""
*   Números: "123", "-45", "3.14", "-0.05"
*   Booleanos: "VERDADERO", "FALSO" (insensible a mayúsculas/minúsculas)

Identificadores (para nombres y claves) pueden contener letras (incluyendo ñ, acentos), números y guion bajo, iniciando con letra o guion bajo. Son sensibles a mayúsculas/minúsculas.

Comentarios de una línea inician con "//".
