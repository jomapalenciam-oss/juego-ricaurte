"""Las Aventuras del Búho — Escape de la Matrix.

Juego educativo del Colegio Diocesano Ricaurte.

Uso:
    python main.py

Atajos de desarrollo (solo con la variable de entorno BUHO_DEBUG=1):
    python main.py nivel6    -> empieza en el nivel 6
    python main.py final     -> empieza en el nivel 6 con la llave
"""

import sys

from juego.bucle import Aplicacion


def main(argumentos=None):
    argumentos = sys.argv[1:] if argumentos is None else argumentos

    app = Aplicacion()

    if argumentos and not app.aplicar_argumento(argumentos[0]):
        print("Argumento ignorado: %r. Los atajos de prueba requieren "
              "BUHO_DEBUG=1 (ver README)." % argumentos[0], file=sys.stderr)

    app.ejecutar()
    return 0


if __name__ == "__main__":
    sys.exit(main())
