# Las Aventuras del Búho — Escape de la Matrix

Juego educativo tipo *quiz* con exploración, desarrollado en Python con
**pygame** para el **Colegio Diocesano Ricaurte**.

El Búho ha despertado dentro de una "Matrix educativa". Para escapar debe
recorrer 6 niveles, reunir en cada uno 4 fragmentos del conocimiento
respondiendo preguntas de cultura general, conseguir la llave dorada y cruzar
la puerta final.

---

## Instalación

Requiere **Python 3.8 o superior**.

```bash
# 1. Clonar el repositorio
git clone https://github.com/JOSESPALENCIAT/juego-ricaurte.git
cd juego-ricaurte

# 2. (Recomendado) crear un entorno virtual
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

---

## Cómo se juega

| Tecla | Acción |
|---|---|
| `W` `A` `S` `D` o flechas | Mover al búho |
| `ESPACIO` | Impulso rápido (dash) |
| `E` | Interactuar con un fragmento o con la puerta |
| `1` `2` `3` `4` o `A` `B` `C` `D` | Responder una pregunta |
| Clic del ratón | Responder una pregunta |
| `P` | Pausa |
| `C` (en el menú) | Personalizar el búho |
| `ENTER` | Confirmar / continuar |
| `ESC` | Salir del juego |

### Objetivo

1. En cada nivel hay **4 fragmentos** (rombos cian). Acércate y pulsa `E`.
2. Responde la pregunta correctamente para recoger el fragmento.
3. Con los 4 fragmentos, la **puerta** se ilumina en dorado. Ve hacia ella y
   pulsa `E` para pasar al siguiente nivel.
4. En el **nivel 6**, el cuarto fragmento te da la **llave dorada**. Cruza la
   puerta final y habrás escapado.

### Reglas

- Empiezas con **3 vidas**.
- **Fallar una pregunta NO cuesta vidas**: resta 50 puntos, te muestra la
  explicación y puedes volver a intentarlo con otra pregunta. La idea es que
  equivocarse sea parte del aprendizaje, no un castigo.
- **Las vidas se pierden con las trampas** (cuadros rojos) y con los
  **guardianes** (círculos morados). Tras recibir un golpe hay 1,5 s de
  invulnerabilidad, indicados con el parpadeo del búho.
- Las **monedas doradas** dan 25 puntos y no tienen riesgo.
- Acertar da `100 + nivel × 35` puntos.

### Niveles

| Nº | Nombre | Dificultad |
|---|---|---|
| 1 | Bosque del Conocimiento | Fácil |
| 2 | Desierto del Tiempo | Fácil+ |
| 3 | Ciudad del Saber | Media |
| 4 | Templo de los Recuerdos | Media+ |
| 5 | Abismo del Conocimiento | Difícil |
| 6 | La Puerta de la Matrix | Final |

---

## Contenido educativo

El banco tiene **72 preguntas**, 12 por nivel, con dificultad creciente y
repartidas en las categorías: Ciencia, Historia, Geografía, Astronomía,
Naturaleza, Literatura, Arte, Música, Matemáticas, Colombia y Cultura general.

Cada pregunta incluye una **explicación**, que se muestra tanto al acertar como
al fallar, para reforzar el aprendizaje en ambos casos.

Las preguntas de un nivel no se repiten hasta que se han visto todas.

### Añadir o cambiar preguntas

Todas están en [`juego/preguntas.py`](juego/preguntas.py). Para añadir una,
copia el formato:

```python
P(3, "Ciencia",
  "¿Cuál es el gas más abundante en la atmósfera terrestre?",
  ["Oxígeno", "Nitrógeno", "Hidrógeno", "Helio"], 1,
  "El nitrógeno constituye cerca del 78 % de la atmósfera."),
```

Los parámetros son: nivel (1-6), categoría, enunciado, lista de 4 opciones,
índice de la respuesta correcta (0-3) y explicación.

> **No escribas las letras `A)`, `B)`...** en las opciones. El juego baraja el
> orden en cada partida y añade la letra al dibujar, para que siempre coincida
> con la posición real en pantalla.

---

## Estructura del proyecto

```
juego-ricaurte/
├── main.py              Punto de entrada
├── requirements.txt     Dependencias
├── README.md
└── juego/
    ├── config.py        Constantes: colores, estados, reglas, geometría
    ├── preguntas.py     Banco de 72 preguntas + selección sin repetición
    ├── estado.py        Clase Juego: todo el estado y las reglas
    ├── nivel.py         Generación de fragmentos, enemigos, trampas y monedas
    ├── bucle.py         Bucle principal, eventos y despacho de pantallas
    ├── fuentes.py       Carga de tipografías
    ├── audio.py         Música generada por código
    ├── dibujo.py        Utilidades de dibujo y sprite del búho
    ├── escenario.py     Fondos de nivel y objetos
    ├── hud.py           Marcador, barra de progreso y avisos
    └── pantallas.py     Menú, historia, pregunta, pausa, victoria, derrota
```

### Cómo está organizado

- **`estado.py` es el único módulo que modifica datos.** Los módulos de dibujo
  (`escenario`, `hud`, `pantallas`, `dibujo`) reciben el estado y solo pintan.
  Así se sabe siempre dónde buscar un cambio de comportamiento.
- Todos los movimientos y temporizadores usan **delta-time** (segundos reales),
  no número de frames, así que el juego va igual de rápido en cualquier equipo.
- Las posiciones se guardan en **coma flotante** y se redondean solo al dibujar,
  para no perder precisión en las diagonales.
- No hay variables globales: el estado vive en la clase `Juego`.

---

## Música

La banda sonora se **genera por código** (ondas senoidales sobre progresiones
de acordes), una pista distinta por nivel. Los `.wav` se escriben en la carpeta
temporal del sistema, **nunca dentro del repositorio**, y quedan cacheados: la
primera vez que entras a un nivel hay una pequeña pausa mientras se genera.

Si el equipo no tiene tarjeta de sonido, el juego funciona igual, sin música.

---

## Modo desarrollo

Los atajos para saltar niveles están **desactivados por defecto**, para que en
la entrega no se pueda terminar el juego sin responder. Para activarlos:

```powershell
# Windows PowerShell
$env:BUHO_DEBUG = "1"
python main.py
```

```bash
# Linux / macOS
BUHO_DEBUG=1 python main.py
```

Con `BUHO_DEBUG=1` quedan disponibles:

| Atajo | Efecto |
|---|---|
| `F6` | Saltar al nivel 6 |
| `F7` | Saltar al nivel 6 con la llave |
| `python main.py nivel6` | Arrancar en el nivel 6 |
| `python main.py final` | Arrancar en el nivel 6 con la llave |

Cuando el modo está activo, el menú lo indica en rojo.

---

## Créditos

Juego creado por:

- Jose Palencia
- Juan Piñero
- Juan José Rodríguez
- Carlos Fernández

**Colegio Diocesano Ricaurte**
