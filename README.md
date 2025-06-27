README - Snake Game

# Video URL: https://youtu.be/3nYibiPcCRU 

Descripción:
Este proyecto es una implementación del clásico juego Snake en la terminal de Windows. Usa caracteres Unicode para representar el tablero, la serpiente y la fruta, y reproduce sonidos al comer fruta y al terminar el juego.

Requisitos:

* Python 3.10 o superior (probado en Python 3.13 en Windows)
* Módulos estándar de Python (no requieren instalación adicional):

  * os, shutil, random, time, msvcrt, copy, winsound
* Dependencias externas (instalar con pip):

  * pyfiglet (para mostrar títulos ASCII)

Instalación:

1. Clonar o descargar el repositorio.
2. Crear y activar un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```
3. Instalar la dependencia:

   ```bash
   pip install -r requirements.txt
   ```

Estructura de archivos:

```
/Final_Project
  |-- project.py         # Código fuente principal
  |-- requirements.txt   # Dependencias externas
  |-- README.txt         # Este archivo de documentación
  |-- Audio/             # Carpeta con archivos .wav
      |-- Explosion.wav
      |-- Pickup_Coin.wav
      |-- Blip_Select.wav
```

Uso:

1. Ejecutar el juego:

   ```bash
   python project.py
   ```
2. En el menú principal:

   * Presiona `S` para iniciar el juego.
   * Presiona `Q` para salir del programa.
3. Controles dentro del juego:

   * `W`: mover arriba
   * `S`: mover abajo
   * `A`: mover izquierda
   * `D`: mover derecha
   * `ESC`: salir al menú principal o terminar el juego
4. Al terminar (Game Over):

   * Presiona `R` para reiniciar.
   * Presiona `M` para volver al menú principal.
   * Presiona `Q` o `ESC` para salir.

Personalización:

* Puedes cambiar el tamaño del tablero modificando los parámetros de `Board(width, height)`.
* Los sonidos se definen en el diccionario `AUDIO` al inicio del código; reemplázalos por tus propios archivos .wav si lo deseas.
* La fuente ASCII de los títulos usa `doom`; puedes cambiarla en la función `set_text()`.

Licencia:
Este proyecto es de código abierto y se distribuye bajo la licencia MIT.
