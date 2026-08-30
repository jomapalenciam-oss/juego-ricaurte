
import pygame
import sys
import random
import math
import wave
import struct
import os

pygame.init()

try:
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=512
    )
    MUSICA_ACTIVA = True
except pygame.error:
    MUSICA_ACTIVA = False



ANCHO = 1200
ALTO = 760
FPS = 60

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(
    "Las Aventuras del Búho - Colegio Diocesano Ricaurte"
)

reloj = pygame.time.Clock()


NEGRO = (10, 10, 18)
BLANCO = (245, 245, 250)
GRIS = (120, 125, 140)

VERDE = (35, 115, 65)
VERDE2 = (65, 165, 85)
VERDE3 = (18, 65, 40)

AZUL = (40, 105, 175)
AZUL2 = (80, 175, 235)

MORADO = (105, 65, 160)
MORADO2 = (165, 105, 230)

ROJO = (215, 55, 70)
AMARILLO = (245, 210, 75)
NARANJA = (235, 135, 55)

CIAN = (65, 220, 210)
ARENA = (190, 145, 80)
TIERRA = (105, 70, 45)
DORADO = (255, 225, 105)


fuente_titulo = pygame.font.SysFont(
    "arial", 52, True
)

fuente_grande = pygame.font.SysFont(
    "arial", 36, True
)

fuente = pygame.font.SysFont(
    "arial", 24
)

fuente_peq = pygame.font.SysFont(
    "arial", 18
)

fuente_mini = pygame.font.SysFont(
    "arial", 15
)


MENU = 0
PERSONAJE = 1
HISTORIA = 2
JUGANDO = 3
PREGUNTA = 4
PAUSA = 5
VICTORIA = 6
DERROTA = 7

estado = MENU



jugador = pygame.Rect(
    570,
    350,
    44,
    44
)

velocidad = 4.5

vidas = 3
puntos = 0
fragmentos = 0

llave = False
nivel = 1

mensaje = ""
mensaje_t = 0

invulnerable = 0
dash_t = 0


apariencias = [

    {
        "nombre": "Búho clásico",
        "cuerpo": (48, 48, 58),
        "ojos": BLANCO,
        "pico": AMARILLO
    },

    {
        "nombre": "Búho bosque",
        "cuerpo": (75, 125, 70),
        "ojos": (225, 245, 190),
        "pico": AMARILLO
    },

    {
        "nombre": "Búho Matrix",
        "cuerpo": (45, 180, 145),
        "ojos": (180, 255, 235),
        "pico": CIAN
    },

    {
        "nombre": "Búho nocturno",
        "cuerpo": (70, 55, 105),
        "ojos": (235, 220, 255),
        "pico": AMARILLO
    }
]

apariencia = 0



NOMBRES = {

    1: "Bosque del Conocimiento",
    2: "Desierto del Tiempo",
    3: "Ciudad del Saber",
    4: "Templo de los Recuerdos",
    5: "Abismo del Conocimiento",
    6: "La Puerta de la Matrix"

}

DIFICULTAD = {

    1: "Fácil",
    2: "Fácil+",
    3: "Media",
    4: "Media+",
    5: "Difícil",
    6: "Final"

}


def P(n, c, q, a, r, e):

    return {

        "nivel": n,
        "categoria": c,
        "pregunta": q,
        "opciones": a,
        "correcta": r,
        "explicacion": e

    }


preguntas = [


    P(
        1,
        "Naturaleza",
        "¿Cuál es el animal terrestre más grande?",
        [
            "A) Elefante africano",
            "B) Rinoceronte",
            "C) Jirafa",
            "D) Hipopótamo"
        ],
        0,
        "El elefante africano es el animal terrestre más grande."
    ),

    P(
        1,
        "Geografía",
        "¿Cuál es el océano más grande?",
        [
            "A) Atlántico",
            "B) Índico",
            "C) Pacífico",
            "D) Ártico"
        ],
        2,
        "El océano Pacífico es el más grande del planeta."
    ),

    P(
        1,
        "Astronomía",
        "¿Cuál es el planeta más grande del Sistema Solar?",
        [
            "A) Marte",
            "B) Saturno",
            "C) Tierra",
            "D) Júpiter"
        ],
        3,
        "Júpiter es el planeta más grande del Sistema Solar."
    ),

    P(
        1,
        "Historia",
        "¿Dónde están las pirámides de Giza?",
        [
            "A) Grecia",
            "B) Egipto",
            "C) Italia",
            "D) Perú"
        ],
        1,
        "Las pirámides de Giza se encuentran en Egipto."
    ),

    P(
        1,
        "Colombia",
        "¿Cuál es la capital de Colombia?",
        [
            "A) Cali",
            "B) Medellín",
            "C) Bogotá",
            "D) Cartagena"
        ],
        2,
        "Bogotá es la capital de Colombia."
    ),

    P(
        1,
        "Ciencia",
        "¿Qué necesitan las plantas para realizar la fotosíntesis?",
        [
            "A) Luz solar",
            "B) Hielo",
            "C) Arena",
            "D) Metal"
        ],
        0,
        "La luz solar es fundamental para la fotosíntesis."
    ),


    # NIVEL 2
    

    P(
        2,
        "Historia",
        "¿Quién fue conocido como el Libertador de varias naciones sudamericanas?",
        [
            "A) Simón Bolívar",
            "B) Cristóbal Colón",
            "C) Napoleón Bonaparte",
            "D) Julio César"
        ],
        0,
        "Simón Bolívar tuvo un papel fundamental en varias independencias sudamericanas."
    ),

    P(
        2,
        "Astronomía",
        "¿Qué planeta es conocido como el planeta rojo?",
        [
            "A) Venus",
            "B) Marte",
            "C) Mercurio",
            "D) Neptuno"
        ],
        1,
        "Marte es conocido como el planeta rojo."
    ),

    P(
        2,
        "Ciencia",
        "¿Qué órgano bombea la sangre por el cuerpo?",
        [
            "A) Pulmón",
            "B) Cerebro",
            "C) Corazón",
            "D) Estómago"
        ],
        2,
        "El corazón bombea la sangre por el cuerpo."
    ),

    P(
        2,
        "Geografía",
        "¿Cuál es el país más grande de Sudamérica?",
        [
            "A) Colombia",
            "B) Argentina",
            "C) Brasil",
            "D) Perú"
        ],
        2,
        "Brasil es el país más grande de Sudamérica por superficie."
    ),

    P(
        2,
        "Astronomía",
        "¿Cuál es el planeta más cercano al Sol?",
        [
            "A) Venus",
            "B) Tierra",
            "C) Marte",
            "D) Mercurio"
        ],
        3,
        "Mercurio es el planeta más cercano al Sol."
    ),

    P(
        2,
        "Naturaleza",
        "¿Cuál es el animal terrestre más rápido?",
        [
            "A) León",
            "B) Guepardo",
            "C) Caballo",
            "D) Tigre"
        ],
        1,
        "El guepardo es el animal terrestre más rápido."
    ),

    # NIVEL 3
    

    P(
        3,
        "Geografía",
        "¿Cuál es el río más largo de Sudamérica?",
        [
            "A) Amazonas",
            "B) Magdalena",
            "C) Orinoco",
            "D) Paraná"
        ],
        0,
        "El río Amazonas es el principal río de Sudamérica y uno de los más largos del mundo."
    ),

    P(
        3,
        "Historia",
        "¿En qué año llegó Cristóbal Colón a América?",
        [
            "A) 1492",
            "B) 1500",
            "C) 1453",
            "D) 1510"
        ],
        0,
        "El viaje de 1492 llevó a Colón al continente americano."
    ),

    P(
        3,
        "Ciencia",
        "¿Cuál es el gas más abundante en la atmósfera terrestre?",
        [
            "A) Oxígeno",
            "B) Nitrógeno",
            "C) Hidrógeno",
            "D) Helio"
        ],
        1,
        "El nitrógeno constituye la mayor parte de la atmósfera terrestre."
    ),

    P(
        3,
        "Arte",
        "¿Quién pintó la Mona Lisa?",
        [
            "A) Miguel Ángel",
            "B) Leonardo da Vinci",
            "C) Pablo Picasso",
            "D) Vincent van Gogh"
        ],
        1,
        "La Mona Lisa fue pintada por Leonardo da Vinci."
    ),

    P(
        3,
        "Literatura",
        "¿Quién escribió Don Quijote de la Mancha?",
        [
            "A) Gabriel García Márquez",
            "B) William Shakespeare",
            "C) Miguel de Cervantes",
            "D) Julio Verne"
        ],
        2,
        "Don Quijote de la Mancha fue escrito por Miguel de Cervantes."
    ),

    P(
        3,
        "Colombia",
        "¿Cuál es el río más importante que atraviesa gran parte de Colombia?",
        [
            "A) Magdalena",
            "B) Amazonas",
            "C) Sena",
            "D) Nilo"
        ],
        0,
        "El río Magdalena es uno de los ríos más importantes de Colombia."
    ),


    # NIVEL 4
    
    

    P(
        4,
        "Ciencia",
        "¿Cuál es la unidad básica de la vida?",
        [
            "A) Átomo",
            "B) Célula",
            "C) Tejido",
            "D) Órgano"
        ],
        1,
        "La célula es considerada la unidad básica de los seres vivos."
    ),

    P(
        4,
        "Historia",
        "¿Cuál fue una de las grandes civilizaciones que construyó Machu Picchu?",
        [
            "A) Romana",
            "B) Inca",
            "C) Egipcia",
            "D) Vikinga"
        ],
        1,
        "Machu Picchu fue construido por la civilización inca."
    ),

    P(
        4,
        "Geografía",
        "¿Cuál es el país conocido por tener forma de bota?",
        [
            "A) España",
            "B) Italia",
            "C) Francia",
            "D) Portugal"
        ],
        1,
        "Italia suele describirse por su característica forma de bota."
    ),

    P(
        4,
        "Ciencia",
        "¿Qué planeta tiene los anillos más famosos del Sistema Solar?",
        [
            "A) Marte",
            "B) Venus",
            "C) Saturno",
            "D) Mercurio"
        ],
        2,
        "Saturno es famoso por su amplio sistema de anillos."
    ),

    P(
        4,
        "Música",
        "¿Cuál de estos instrumentos pertenece a la familia de las cuerdas?",
        [
            "A) Violín",
            "B) Trompeta",
            "C) Flauta",
            "D) Clarinete"
        ],
        0,
        "El violín es un instrumento de cuerda."
    ),

    P(
        4,
        "Naturaleza",
        "¿Cuál es el mamífero más grande del planeta?",
        [
            "A) Elefante africano",
            "B) Ballena azul",
            "C) Jirafa",
            "D) Orca"
        ],
        1,
        "La ballena azul es el animal más grande conocido."
    ),

    # NIVEL 5
   

    P(
        5,
        "Historia",
        "¿Qué civilización construyó el Coliseo de Roma?",
        [
            "A) Romana",
            "B) Maya",
            "C) Inca",
            "D) China"
        ],
        0,
        "El Coliseo fue construido durante el Imperio romano."
    ),

    P(
        5,
        "Geografía",
        "¿Cuál es la montaña más alta del mundo sobre el nivel del mar?",
        [
            "A) K2",
            "B) Everest",
            "C) Aconcagua",
            "D) Mont Blanc"
        ],
        1,
        "El monte Everest es la montaña más alta sobre el nivel del mar."
    ),

    P(
        5,
        "Ciencia",
        "¿Cuál es el órgano principal del sistema nervioso?",
        [
            "A) Corazón",
            "B) Cerebro",
            "C) Hígado",
            "D) Pulmón"
        ],
        1,
        "El cerebro es el órgano principal del sistema nervioso."
    ),

    P(
        5,
        "Literatura",
        "¿Quién escribió Cien años de soledad?",
        [
            "A) Gabriel García Márquez",
            "B) Mario Vargas Llosa",
            "C) Jorge Luis Borges",
            "D) Pablo Neruda"
        ],
        0,
        "Cien años de soledad fue escrita por Gabriel García Márquez."
    ),

    P(
        5,
        "Historia",
        "¿Cuál fue el nombre de la civilización que desarrolló una importante ciudad llamada Tenochtitlan?",
        [
            "A) Azteca",
            "B) Inca",
            "C) Romana",
            "D) Egipcia"
        ],
        0,
        "Tenochtitlan fue la gran capital del Imperio mexica o azteca."
    ),

    P(
        5,
        "Geografía",
        "¿Qué país tiene la mayor superficie del mundo?",
        [
            "A) Canadá",
            "B) China",
            "C) Rusia",
            "D) Estados Unidos"
        ],
        2,
        "Rusia es el país con mayor superficie terrestre."
    ),

  
    # NIVEL 6


    P(
        6,
        "Ciencia",
        "¿Cuál es el elemento químico más abundante del universo?",
        [
            "A) Oxígeno",
            "B) Hidrógeno",
            "C) Carbono",
            "D) Hierro"
        ],
        1,
        "El hidrógeno es el elemento más abundante del universo conocido."
    ),

    P(
        6,
        "Historia",
        "¿En qué país comenzó el movimiento conocido como Renacimiento?",
        [
            "A) Italia",
            "B) Francia",
            "C) Inglaterra",
            "D) Alemania"
        ],
        0,
        "El Renacimiento comenzó en las ciudades italianas."
    ),

    P(
        6,
        "Geografía",
        "¿Cuál es el continente con mayor superficie?",
        [
            "A) África",
            "B) Europa",
            "C) Asia",
            "D) Oceanía"
        ],
        2,
        "Asia es el continente más grande por superficie."
    ),

    P(
        6,
        "Astronomía",
        "¿Cómo se llama nuestra galaxia?",
        [
            "A) Andrómeda",
            "B) Vía Láctea",
            "C) Orión",
            "D) Centauro"
        ],
        1,
        "Nuestra galaxia se llama Vía Láctea."
    ),

    P(
        6,
        "Cultura general",
        "¿Cuál es el idioma con mayor número de hablantes nativos del mundo?",
        [
            "A) Español",
            "B) Inglés",
            "C) Chino mandarín",
            "D) Francés"
        ],
        2,
        "El chino mandarín tiene la mayor cantidad de hablantes nativos."
    ),

    P(
        6,
        "Matrix",
        "¿Cuál es el objetivo final del Búho en esta aventura?",
        [
            "A) Encontrar comida",
            "B) Dormir",
            "C) Conseguir la llave y escapar de la Matrix",
            "D) Construir un castillo"
        ],
        2,
        "La misión final es conseguir la llave y escapar de la Matrix."
    )
]




usadas = {
    1: set(),
    2: set(),
    3: set(),
    4: set(),
    5: set(),
    6: set()
}



fragmentos_nivel = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: []
}

enemigos = []
monedas = []
particulas = []
trampas = []

puerta = pygame.Rect(
    1080,
    650,
    55,
    65
)



def mostrar_mensaje(t, segundos=2.5):

    global mensaje
    global mensaje_t

    mensaje = t
    mensaje_t = segundos



def nueva_pregunta():

    disponibles = [

        (i, p)
        for i, p in enumerate(preguntas)

        if p["nivel"] == nivel
        and i not in usadas[nivel]

    ]

    if not disponibles:

        usadas[nivel].clear()

        disponibles = [

            (i, p)
            for i, p in enumerate(preguntas)

            if p["nivel"] == nivel

        ]

    if not disponibles:

        return None

    i, pregunta = random.choice(
        disponibles
    )

    usadas[nivel].add(i)

    opciones = [

        (texto_opcion, j == pregunta["correcta"])

        for j, texto_opcion
        in enumerate(
            pregunta["opciones"]
        )

    ]

    random.shuffle(opciones)

    nueva = pregunta.copy()

    nueva["opciones"] = [

        x[0]
        for x in opciones

    ]

    nueva["correcta"] = next(

        j
        for j, x in enumerate(opciones)
        if x[1]

    )

    return nueva




def crear_nivel():

    global fragmentos_nivel
    global enemigos
    global monedas
    global trampas
    global puerta

    fragmentos_nivel[nivel] = [

        pygame.Rect(

            random.randint(100, 1030),
            random.randint(130, 600),
            22,
            22

        )

        for _ in range(4)

    ]

    for r in fragmentos_nivel[nivel]:

        while r.colliderect(
            jugador.inflate(180, 180)
        ):

            r.topleft = (

                random.randint(100, 1030),
                random.randint(130, 600)

            )

    monedas = [

        pygame.Rect(

            random.randint(80, 1080),
            random.randint(120, 650),
            14,
            14

        )

        for _ in range(12)

    ]

    enemigos = []

    cantidad_enemigos = max(
        1,
        nivel
    )

    for _ in range(cantidad_enemigos):

        enemigos.append({

            "rect": pygame.Rect(

                random.randint(120, 1000),
                random.randint(130, 620),
                34,
                34

            ),

            "vx": random.choice(
                [-2, -1.5, 1.5, 2]
            ),

            "vy": random.choice(
                [-1.5, 1.5]
            )

        })

    trampas = []

    for _ in range(nivel + 2):

        trampas.append(

            pygame.Rect(

                random.randint(100, 1050),
                random.randint(130, 620),
                35,
                35

            )

        )

    puerta = pygame.Rect(
        1080,
        650,
        55,
        65
    )

    jugador.center = (
        100,
        110
    )




musica_cache = {}

NOTAS = {

    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88

}


def crear_wav_musica(n):

    nombre_archivo = (
        f"matrix_classical_{n}.wav"
    )

    ruta = os.path.join(

        os.path.dirname(
            os.path.abspath(__file__)
        ),

        nombre_archivo

    )

    if os.path.exists(ruta):

        return ruta

    try:

        sr = 44100
        duracion = 10.0

        total = int(
            sr * duracion
        )

        datos = []

        progresiones = [

            ["C", "E", "G", "C"],
            ["A", "C", "E", "A"],
            ["D", "F", "A", "D"],
            ["G", "B", "D", "G"],
            ["E", "G", "B", "E"],
            ["C", "F", "A", "C"]

        ]

        progresion = progresiones[
            (n - 1) % len(progresiones)
        ]

        bpm = 68 + n * 3

        beat = 60 / bpm

        for k in range(total):

            t = k / sr

            indice = int(
                t / beat
            )

            nota = NOTAS[
                progresion[
                    indice % len(progresion)
                ]
            ]

            frecuencia = nota

            if indice % 4 == 2:

                frecuencia *= 2

            valor = (

                0.15
                * math.sin(

                    2
                    * math.pi
                    * frecuencia
                    * t

                )

            )

            valor += (

                0.07
                * math.sin(

                    2
                    * math.pi
                    * (frecuencia / 2)
                    * t

                )

            )

            if indice % 2 == 1:

                valor += (

                    0.035
                    * math.sin(

                        2
                        * math.pi
                        * (frecuencia * 1.5)
                        * t

                    )

                )

            ataque = min(
                1,
                t / 0.2
            )

            salida = min(
                1,
                (duracion - t) / 0.7
            )

            envolvente = (
                ataque * salida
            )

            muestra = int(

                max(

                    -1,
                    min(
                        1,
                        valor * envolvente
                    )

                )
                * 32767

            )

            datos.append(

                struct.pack(
                    "<hh",
                    muestra,
                    muestra
                )

            )

        with wave.open(
            ruta,
            "wb"
        ) as wf:

            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)

            wf.writeframes(
                b"".join(datos)
            )

        return ruta

    except Exception:

        return None


def cambiar_musica():

    if not MUSICA_ACTIVA:
        return

    try:

        if nivel in musica_cache:

            ruta = musica_cache[nivel]

        else:

            ruta = crear_wav_musica(
                nivel
            )

            musica_cache[nivel] = ruta

        if ruta:

            pygame.mixer.music.load(
                ruta
            )

            pygame.mixer.music.set_volume(
                0.22
            )

            pygame.mixer.music.play(
                -1
            )

    except Exception:

        pass




def texto(
    txt,
    f,
    c,
    x,
    y,
    centro=True
):

    surf = f.render(
        txt,
        True,
        c
    )

    if centro:

        r = surf.get_rect(
            center=(x, y)
        )

    else:

        r = surf.get_rect(
            topleft=(x, y)
        )

    pantalla.blit(
        surf,
        r
    )




def dibujar_buho():

    x, y = jugador.center

    apariencia_actual = (
        apariencias[apariencia]
    )

    cuerpo = apariencia_actual[
        "cuerpo"
    ]

    ojos = apariencia_actual[
        "ojos"
    ]

    pico = apariencia_actual[
        "pico"
    ]

    # Sombra

    pygame.draw.ellipse(
        pantalla,
        (0, 0, 0),
        (
            x - 24,
            y + 18,
            48,
            12
        )
    )

    # Cuerpo

    pygame.draw.ellipse(
        pantalla,
        cuerpo,
        (
            x - 22,
            y - 5,
            44,
            52
        )
    )

    # Alas

    pygame.draw.ellipse(
        pantalla,
        cuerpo,
        (
            x - 34,
            y + 3,
            23,
            34
        )
    )

    pygame.draw.ellipse(
        pantalla,
        cuerpo,
        (
            x + 11,
            y + 3,
            23,
            34
        )
    )

    # Cabeza

    pygame.draw.circle(
        pantalla,
        cuerpo,
        (
            x,
            y - 20
        ),
        28
    )

    # Orejas

    pygame.draw.polygon(
        pantalla,
        cuerpo,
        [

            (
                x - 23,
                y - 36
            ),

            (
                x - 16,
                y - 60
            ),

            (
                x - 3,
                y - 37
            )

        ]
    )

    pygame.draw.polygon(
        pantalla,
        cuerpo,
        [

            (
                x + 23,
                y - 36
            ),

            (
                x + 16,
                y - 60
            ),

            (
                x + 3,
                y - 37
            )

        ]
    )

    # Ojos

    for ex in (
        x - 10,
        x + 10
    ):

        pygame.draw.circle(
            pantalla,
            ojos,
            (
                ex,
                y - 20
            ),
            9
        )

        pygame.draw.circle(
            pantalla,
            (15, 15, 20),
            (
                ex,
                y - 20
            ),
            4
        )

    # Pico

    pygame.draw.polygon(
        pantalla,
        pico,
        [

            (
                x - 6,
                y - 7
            ),

            (
                x + 6,
                y - 7
            ),

            (
                x,
                y + 5
            )

        ]
    )

    # Brillo

    pygame.draw.circle(
        pantalla,
        BLANCO,
        (
            x - 12,
            y - 23
        ),
        2
    )

    # Dash

    if dash_t > 0:

        pygame.draw.circle(
            pantalla,
            CIAN,
            (
                x,
                y
            ),
            34,
            2
        )



def arbol(x, y, s=1):

    pygame.draw.rect(

        pantalla,
        (75, 48, 30),

        (

            x - 8 * s,
            y + 5 * s,
            16 * s,
            45 * s

        )

    )

    pygame.draw.circle(

        pantalla,
        VERDE3,
        (
            x,
            y
        ),
        int(30 * s)

    )

    pygame.draw.circle(

        pantalla,
        VERDE,
        (

            int(x - 20 * s),
            int(y + 4 * s)

        ),
        int(24 * s)

    )

    pygame.draw.circle(

        pantalla,
        VERDE2,
        (

            int(x + 18 * s),
            int(y + 2 * s)

        ),
        int(22 * s)

    )



def fondo_nivel():

    if nivel == 1:

        pantalla.fill(
            (14, 45, 29)
        )

        pygame.draw.rect(

            pantalla,
            (25, 90, 48),
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        posiciones = [

            (100, 150),
            (250, 100),
            (420, 170),
            (650, 115),
            (900, 150),
            (1080, 240),
            (180, 610),
            (430, 620),
            (780, 610),
            (1040, 560)

        ]

        for p in posiciones:

            arbol(
                *p,
                1
            )

        pygame.draw.rect(

            pantalla,
            (105, 75, 48),
            (
                80,
                330,
                1050,
                80
            ),
            border_radius=30

        )

        pygame.draw.rect(

            pantalla,
            (55, 115, 170),
            (
                70,
                95,
                190,
                105
            ),
            border_radius=20

        )

    elif nivel == 2:

        pantalla.fill(
            (95, 62, 35)
        )

        pygame.draw.rect(

            pantalla,
            ARENA,
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        pygame.draw.rect(

            pantalla,
            (225, 185, 110),
            (
                80,
                330,
                1050,
                75
            ),
            border_radius=30

        )

        for x, y in [

            (230, 150),
            (500, 130),
            (850, 170),
            (1020, 500),
            (260, 570),
            (760, 600)

        ]:

            pygame.draw.circle(

                pantalla,
                (160, 115, 60),
                (
                    x,
                    y
                ),
                65

            )

        pygame.draw.ellipse(

            pantalla,
            AZUL,
            (
                70,
                100,
                190,
                100
            )

        )

    elif nivel == 3:

        pantalla.fill(
            (12, 12, 35)
        )

        pygame.draw.rect(

            pantalla,
            (25, 30, 75),
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        for x in range(
            100,
            1150,
            100
        ):

            pygame.draw.line(

                pantalla,
                (45, 70, 130),
                (
                    x,
                    100
                ),
                (
                    x,
                    700
                ),
                1

            )

        for y in range(
            120,
            700,
            60
        ):

            pygame.draw.line(

                pantalla,
                (45, 70, 130),
                (
                    50,
                    y
                ),
                (
                    1150,
                    y
                ),
                1

            )

        for _ in range(25):

            x = random.randint(
                50,
                1150
            )

            y = random.randint(
                90,
                700
            )

            pygame.draw.circle(

                pantalla,
                CIAN,
                (
                    x,
                    y
                ),
                2

            )

    elif nivel == 4:

        pantalla.fill(
            (35, 22, 52)
        )

        pygame.draw.rect(

            pantalla,
            (70, 42, 88),
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        for x in range(
            100,
            1150,
            120
        ):

            pygame.draw.rect(

                pantalla,
                (100, 60, 115),
                (
                    x,
                    150,
                    50,
                    420
                ),
                border_radius=12

            )

        pygame.draw.rect(

            pantalla,
            (45, 28, 60),
            (
                80,
                330,
                1050,
                80
            ),
            border_radius=25

        )

    elif nivel == 5:

        pantalla.fill(
            (8, 8, 20)
        )

        pygame.draw.rect(

            pantalla,
            (25, 15, 45),
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        for i in range(15):

            x = 70 + i * 75

            pygame.draw.line(

                pantalla,
                MORADO,
                (
                    x,
                    100
                ),
                (
                    x + random.randint(
                        -30,
                        30
                    ),
                    700
                ),
                2

            )

        for i in range(12):

            y = 120 + i * 50

            pygame.draw.line(

                pantalla,
                (45, 35, 80),
                (
                    50,
                    y
                ),
                (
                    1150,
                    y
                ),
                1

            )

    else:

        pantalla.fill(
            (5, 10, 14)
        )

        pygame.draw.rect(

            pantalla,
            (10, 40, 42),
            (
                35,
                80,
                1130,
                630
            ),
            border_radius=28

        )

        # Código Matrix

        for x in range(
            70,
            1150,
            55
        ):

            yy = (

                pygame.time.get_ticks()
                // 8
                + x * 7

            ) % 620 + 90

            texto(

                "1",
                fuente_mini,
                CIAN,
                x,
                yy,
                False

            )




def dibujar_objetos():

    # --------------------------------------------------------
    # MONEDAS
    # --------------------------------------------------------

    for r in monedas:

        pygame.draw.circle(
            pantalla,
            DORADO,
            r.center,
            8
        )

        pygame.draw.circle(
            pantalla,
            AMARILLO,
            r.center,
            4
        )

  

    for r in fragmentos_nivel[nivel]:

        pygame.draw.polygon(

            pantalla,
            CIAN,

            [

                (
                    r.centerx,
                    r.y - 5
                ),

                (
                    r.right,
                    r.centery
                ),

                (
                    r.centerx,
                    r.bottom + 5
                ),

                (
                    r.x,
                    r.centery
                )

            ]

        )

        pygame.draw.polygon(

            pantalla,
            BLANCO,

            [

                (
                    r.centerx,
                    r.y + 1
                ),

                (
                    r.right - 7,
                    r.centery
                ),

                (
                    r.centerx,
                    r.bottom - 1
                ),

                (
                    r.x + 7,
                    r.centery
                )

            ]

        )

    

    for r in trampas:

        pygame.draw.rect(

            pantalla,
            (100, 20, 35),
            r,
            border_radius=7

        )

        pygame.draw.line(

            pantalla,
            ROJO,
            r.topleft,
            r.bottomright,
            3

        )

        pygame.draw.line(

            pantalla,
            ROJO,
            r.topright,
            r.bottomleft,
            3

        )

   

    for enemigo in enemigos:

        r = enemigo["rect"]

        pygame.draw.circle(

            pantalla,
            (80, 45, 105),
            r.center,
            18

        )

        pygame.draw.circle(

            pantalla,
            ROJO,
            (
                r.centerx - 6,
                r.centery - 4
            ),
            4

        )

        pygame.draw.circle(

            pantalla,
            ROJO,
            (
                r.centerx + 6,
                r.centery - 4
            ),
            4

        )

   

    pygame.draw.rect(

        pantalla,
        (20, 25, 30),
        puerta,
        border_radius=8

    )

    # La puerta se muestra dorada cuando puede abrirse

    if nivel == 6 and llave and fragmentos >= 4:

        color_puerta = DORADO

    elif nivel < 6 and fragmentos >= 4:

        color_puerta = DORADO

    else:

        color_puerta = GRIS

    pygame.draw.rect(

        pantalla,
        color_puerta,
        puerta,
        3,
        border_radius=8

    )

    pygame.draw.circle(

        pantalla,
        color_puerta,
        puerta.center,
        7

    )

   

    if nivel == 6:

        if llave and fragmentos >= 4:

            texto(

                "ABIERTA",
                fuente_mini,
                VERDE2,
                puerta.centerx,
                puerta.y - 18

            )

        else:

            texto(

                "BLOQUEADA",
                fuente_mini,
                ROJO,
                puerta.centerx,
                puerta.y - 18

            )




def interfaz():

    pygame.draw.rect(

        pantalla,
        (8, 10, 18),
        (
            0,
            0,
            ANCHO,
            70
        )

    )

    texto(

        f"VIDAS: {vidas}",
        fuente,
        ROJO,
        25,
        20,
        False

    )

    texto(

        f"PUNTOS: {puntos}",
        fuente,
        DORADO,
        180,
        20,
        False

    )

    texto(

        f"FRAGMENTOS: {fragmentos}/4",
        fuente,
        BLANCO,
        360,
        20,
        False

    )

    texto(

        f"NIVEL {nivel}/6",
        fuente,
        CIAN,
        610,
        20,
        False

    )

    texto(

        NOMBRES[nivel],
        fuente_peq,
        BLANCO,
        790,
        22,
        False

    )

  

    pygame.draw.rect(

        pantalla,
        (45, 45, 60),
        (
            25,
            650,
            260,
            16
        ),
        border_radius=8

    )

    pygame.draw.rect(

        pantalla,
        CIAN,
        (
            25,
            650,
            min(
                260,
                65 * fragmentos
            ),
            16
        ),
        border_radius=8

    )

    texto(

        "E: interactuar   ESPACIO: impulso   P: pausa",
        fuente_mini,
        GRIS,
        305,
        650,
        False

    )

    # Llave

    if nivel == 6:

        texto(

            "LLAVE: " + (
                "SI"
                if llave
                else "NO"
            ),

            fuente_mini,

            DORADO
            if llave
            else GRIS,

            1000,
            650,
            False

        )



def dibujar_mensaje():

    global mensaje_t

    if mensaje and mensaje_t > 0:

        pygame.draw.rect(

            pantalla,
            (15, 15, 25),
            (
                250,
                575,
                700,
                55
            ),
            border_radius=15

        )

        texto(

            mensaje,
            fuente_peq,
            BLANCO,
            600,
            602

        )

        mensaje_t -= 1 / FPS




pregunta_actual = None
objeto_actual = None


def objeto_cercano():

    for r in fragmentos_nivel[nivel]:

        if jugador.colliderect(
            r.inflate(55, 55)
        ):

            return (
                "fragmento",
                r
            )

    if jugador.colliderect(
        puerta.inflate(45, 45)
    ):

        return (
            "puerta",
            puerta
        )

    return None


def recibir_daño(causa):

    global vidas
    global invulnerable
    global estado

    if invulnerable > 0:

        return

    vidas -= 1

    invulnerable = 1.5

    mostrar_mensaje(
        "¡Cuidado! Has perdido una vida."
    )

    if vidas <= 0:

        estado = DERROTA


def abrir_pregunta():

    global pregunta_actual
    global estado

    pregunta_actual = nueva_pregunta()

    if pregunta_actual:

        estado = PREGUNTA




def responder(i):

    global vidas
    global puntos
    global fragmentos
    global estado
    global objeto_actual
    global llave
    global pregunta_actual

    # Seguridad

    if pregunta_actual is None:

        estado = JUGANDO

        return

   

    if i != pregunta_actual["correcta"]:

        vidas -= 1

        mostrar_mensaje(

            "Incorrecto: "
            + pregunta_actual["explicacion"]

        )

        if vidas <= 0:

            estado = DERROTA

        else:

            estado = JUGANDO

        return

  

    puntos += (
        100
        + nivel * 35
    )

    mostrar_mensaje(

        f"¡Correcto! +{100 + nivel * 35} puntos"

    )

   

    if (

        objeto_actual
        and objeto_actual[0] == "fragmento"

    ):

        r = objeto_actual[1]

        if r in fragmentos_nivel[nivel]:

            fragmentos_nivel[nivel].remove(r)

            fragmentos += 1

          

            if nivel == 6 and fragmentos >= 4:

                fragmentos = 4

                llave = True

                mostrar_mensaje(

                    "¡LLAVE DORADA CONSEGUIDA! "
                    "Ve a la puerta final y presiona E."

                )

            elif fragmentos >= 4:

                mostrar_mensaje(

                    "¡Conseguiste los 4 fragmentos! "
                    "Busca la puerta."

                )

  

    elif (

        objeto_actual
        and objeto_actual[0] == "puerta"

    ):

        if nivel == 6:

            llave = True

    pregunta_actual = None

    estado = JUGANDO


def avanzar_nivel():

    global nivel
    global fragmentos
    global llave
    global estado

    if nivel < 6:

        nivel += 1

        fragmentos = 0

        llave = False

        crear_nivel()

        cambiar_musica()

        mostrar_mensaje(

            f"¡Nivel {nivel}! "
            f"{NOMBRES[nivel]}"

        )

    else:

      

        if fragmentos >= 4 and llave:

            estado = VICTORIA

        elif fragmentos >= 4:

            llave = True

            mostrar_mensaje(

                "¡Tienes los 4 fragmentos! "
                "Has obtenido la llave final."

            )

        else:

            mostrar_mensaje(

                f"Necesitas los 4 fragmentos. "
                f"{fragmentos}/4"

            )




def menu():

    pantalla.fill(
        (8, 9, 17)
    )

    # Estrellas

    for i in range(45):

        x = (
            i * 83 + 40
        ) % ANCHO

        y = (
            i * 47 + 70
        ) % 600

        pygame.draw.circle(

            pantalla,
            (80, 90, 115),
            (
                x,
                y
            ),
            1 + (i % 2)

        )

    texto(

        "LAS AVENTURAS",
        fuente_titulo,
        BLANCO,
        600,
        75

    )

    texto(

        "DEL BÚHO",
        fuente_titulo,
        DORADO,
        600,
        135

    )

    texto(

        "Juego creado por",
        fuente_peq,
        GRIS,
        600,
        190

    )

    texto(

        "Colegio Diocesano Ricaurte",
        fuente_grande,
        DORADO,
        600,
        230

    )

    jugador.center = (
        600,
        335
    )

    dibujar_buho()

    texto(

        "ESCAPE DE LA MATRIX",
        fuente_grande,
        CIAN,
        600,
        430

    )

    pygame.draw.rect(

        pantalla,
        (35, 35, 55),
        (
            330,
            465,
            540,
            60
        ),
        border_radius=18

    )

    texto(

        "ENTER  •  Comenzar aventura",
        fuente,
        BLANCO,
        600,
        495

    )

    texto(

        "C  •  Personalizar personaje",
        fuente_peq,
        GRIS,
        600,
        550

    )

    texto(

        "WASD / FLECHAS  •  Moverse",
        fuente_peq,
        GRIS,
        600,
        580

    )

    texto(

        "P  •  Pausa     ESC  •  Salir",
        fuente_peq,
        GRIS,
        600,
        610

    )




def pantalla_personaje():

    pantalla.fill(
        (13, 14, 25)
    )

    texto(

        "PERSONALIZA TU BÚHO",
        fuente_titulo,
        DORADO,
        600,
        70

    )

    texto(

        "Usa ← → para cambiar y ENTER para confirmar",
        fuente_peq,
        GRIS,
        600,
        115

    )

    for i, a in enumerate(
        apariencias
    ):

        x = 180 + i * 270

        r = pygame.Rect(

            x,
            170,
            230,
            340

        )

        pygame.draw.rect(

            pantalla,
            (35, 35, 52),
            r,
            border_radius=20

        )

        if i == apariencia:

            pygame.draw.rect(

                pantalla,
                CIAN,
                r,
                4,
                border_radius=20

            )

        texto(

            a["nombre"],
            fuente_peq,
            BLANCO,
            x + 115,
            205

        )

        cx = x + 115
        cy = 335

        pygame.draw.ellipse(

            pantalla,
            a["cuerpo"],
            (
                cx - 35,
                cy - 5,
                70,
                80
            )

        )

        pygame.draw.circle(

            pantalla,
            a["cuerpo"],
            (
                cx,
                cy - 40
            ),
            42

        )

        for ex in (

            cx - 15,
            cx + 15

        ):

            pygame.draw.circle(

                pantalla,
                a["ojos"],
                (
                    ex,
                    cy - 43
                ),
                13

            )

            pygame.draw.circle(

                pantalla,
                NEGRO,
                (
                    ex,
                    cy - 43
                ),
                6

            )

        pygame.draw.polygon(

            pantalla,
            a["pico"],

            [

                (
                    cx - 8,
                    cy - 25
                ),

                (
                    cx + 8,
                    cy - 25
                ),

                (
                    cx,
                    cy - 10
                )

            ]

        )

        if i == apariencia:

            texto(

                "ELEGIDO",
                fuente_peq,
                CIAN,
                x + 115,
                475

            )




def historia():

    pantalla.fill(
        (8, 9, 17)
    )

    texto(

        "LA ÚLTIMA PUERTA",
        fuente_titulo,
        DORADO,
        600,
        90

    )

    lineas = [

        "El Búho ha despertado dentro de una Matrix educativa.",

        "Los guardianes han escondido fragmentos del conocimiento.",

        "Cada respuesta correcta abre un nuevo camino.",

        "Pero los desafíos se harán cada vez más difíciles.",

        "",

        "Supera los 6 niveles, consigue la llave dorada",

        "y encuentra la puerta final para escapar.",

        "",

        "Las preguntas pondrán a prueba tus conocimientos",

        "de historia, ciencia, geografía, cultura y naturaleza."

    ]

    for i, linea in enumerate(
        lineas
    ):

        if i in (

            0,
            1,
            2,
            3,
            5,
            6,
            8,
            9

        ):

            f = fuente

        else:

            f = fuente_peq

        texto(

            linea,
            f,
            BLANCO,
            600,
            170 + i * 40

        )

    texto(

        "ENTER  •  Comenzar",
        fuente,
        DORADO,
        600,
        665

    )



def pregunta_screen():

    pantalla.fill(
        (8, 9, 18)
    )

    texto(

        f"DESAFÍO — NIVEL {nivel}",
        fuente_grande,
        CIAN,
        600,
        70

    )

    texto(

        pregunta_actual["categoria"],
        fuente_peq,
        DORADO,
        600,
        110

    )

    pygame.draw.rect(

        pantalla,
        (27, 28, 45),
        (
            80,
            145,
            1040,
            490
        ),
        border_radius=25

    )

    palabras = (
        pregunta_actual["pregunta"]
        .split()
    )

    lineas = []
    actual = ""

    for palabra in palabras:

        prueba = (

            actual
            + " "
            + palabra

        ).strip()

        if fuente.size(
            prueba
        )[0] > 900:

            lineas.append(
                actual
            )

            actual = palabra

        else:

            actual = prueba

    if actual:

        lineas.append(
            actual
        )

    for i, linea in enumerate(
        lineas
    ):

        texto(

            linea,
            fuente,
            BLANCO,
            600,
            195 + i * 32

        )

    botones = [

        pygame.Rect(

            145,
            300 + i * 72,
            910,
            56

        )

        for i in range(4)

    ]

    mouse = pygame.mouse.get_pos()

    for i, r in enumerate(
        botones
    ):

        color = (

            (60, 90, 125)
            if r.collidepoint(mouse)
            else (45, 45, 65)

        )

        pygame.draw.rect(

            pantalla,
            color,
            r,
            border_radius=14

        )

        pygame.draw.rect(

            pantalla,
            (100, 105, 135),
            r,
            2,
            border_radius=14

        )

        texto(

            pregunta_actual["opciones"][i],
            fuente,
            BLANCO,
            r.x + 20,
            r.y + 15,
            False

        )

    texto(

        "Haz clic en una respuesta",
        fuente_peq,
        GRIS,
        600,
        670

    )

    return botones




def pausa():

    pantalla.fill(
        (8, 8, 15)
    )

    texto(

        "PAUSA",
        fuente_titulo,
        DORADO,
        600,
        180

    )

    texto(

        "P  •  Continuar",
        fuente,
        BLANCO,
        600,
        300

    )

    texto(

        "ESC  •  Salir",
        fuente,
        GRIS,
        600,
        350

    )



def victoria():

    pantalla.fill(
        (5, 25, 22)
    )

    # Estrellas

    for i in range(50):

        x = (
            i * 97 + 30
        ) % ANCHO

        y = (
            i * 53 + 20
        ) % ALTO

        pygame.draw.circle(

            pantalla,
            DORADO,
            (
                x,
                y
            ),
            1 + (i % 3)

        )

    texto(

        "¡ESCAPASTE DE LA MATRIX!",
        fuente_titulo,
        DORADO,
        600,
        65

    )

    texto(

        "LA AVENTURA HA TERMINADO",
        fuente_grande,
        CIAN,
        600,
        120

    )

    texto(

        "La llave abrió la última puerta.",
        fuente,
        BLANCO,
        600,
        165

    )

    texto(

        f"PUNTUACIÓN FINAL: {puntos}",
        fuente_grande,
        DORADO,
        600,
        215

    )

    pygame.draw.line(

        pantalla,
        CIAN,
        (
            350,
            255
        ),
        (
            850,
            255
        ),
        3

    )

    texto(

        "CRÉDITOS",
        fuente_titulo,
        BLANCO,
        600,
        295

    )

    texto(

        "Juego creado por",
        fuente_peq,
        GRIS,
        600,
        340

    )

    texto(

        "JOSE PALENCIA",
        fuente,
        BLANCO,
        600,
        385

    )

    texto(

        "JUAN PIÑERO",
        fuente,
        BLANCO,
        600,
        425

    )

    texto(

        "JUAN JOSE RODRIGUEZ",
        fuente,
        BLANCO,
        600,
        465

    )

    texto(

        "CARLOS FERNANDEZ",
        fuente,
        BLANCO,
        600,
        505

    )

    pygame.draw.line(

        pantalla,
        MORADO2,
        (
            400,
            540
        ),
        (
            800,
            540
        ),
        2

    )

    texto(

        "Colegio Diocesano Ricaurte",
        fuente_grande,
        DORADO,
        600,
        580

    )

    texto(

        "¡Gracias por jugar!",
        fuente,
        CIAN,
        600,
        625

    )

    texto(

        "ENTER  •  Jugar otra vez",
        fuente_peq,
        GRIS,
        600,
        680

    )




def derrota():

    pantalla.fill(
        (45, 8, 18)
    )

    texto(

        "EL BÚHO HA CAÍDO",
        fuente_titulo,
        ROJO,
        600,
        190

    )

    texto(

        "Los guardianes de la Matrix fueron demasiado fuertes.",
        fuente,
        BLANCO,
        600,
        290

    )

    texto(

        f"Puntuación: {puntos}",
        fuente_grande,
        DORADO,
        600,
        370

    )

    texto(

        "ENTER  •  Intentar nuevamente",
        fuente,
        BLANCO,
        600,
        500

    )




def ir_al_nivel_final():

    global nivel
    global fragmentos
    global llave
    global estado
    global vidas

    nivel = 6

    fragmentos = 4

    llave = False

    vidas = 3

    crear_nivel()

    cambiar_musica()

    jugador.center = (
        100,
        110
    )

    estado = JUGANDO

    mostrar_mensaje(

        "¡Has llegado al NIVEL 6! "
        "Encuentra los fragmentos."

    )




def ir_al_final_completo():

    global nivel
    global fragmentos
    global llave
    global estado
    global vidas

    nivel = 6

    fragmentos = 4

    llave = True

    vidas = 3

    crear_nivel()

    cambiar_musica()

    jugador.center = (
        100,
        110
    )

    estado = JUGANDO

    mostrar_mensaje(

        "MODO PRUEBA: NIVEL 6 CON LLAVE. "
        "Ve a la puerta."

    )




def reiniciar():

    global vidas
    global puntos
    global fragmentos
    global nivel
    global llave
    global estado
    global mensaje
    global mensaje_t
    global invulnerable
    global dash_t
    global pregunta_actual
    global objeto_actual

    vidas = 3

    puntos = 0

    fragmentos = 0

    nivel = 1

    llave = False

    mensaje = ""

    mensaje_t = 0

    invulnerable = 0

    dash_t = 0

    pregunta_actual = None

    objeto_actual = None

    for s in usadas.values():

        s.clear()

    crear_nivel()

    cambiar_musica()

    jugador.center = (
        100,
        110
    )

    estado = HISTORIA




crear_nivel()


if len(sys.argv) > 1:

    argumento = sys.argv[1].lower()

    if argumento == "nivel6":

        nivel = 6

        fragmentos = 0

        llave = False

        vidas = 3

        crear_nivel()

        cambiar_musica()

        jugador.center = (
            100,
            110
        )

        estado = JUGANDO

    elif argumento == "final":

        nivel = 6

        fragmentos = 4

        llave = True

        vidas = 3

        crear_nivel()

        cambiar_musica()

        jugador.center = (
            100,
            110
        )

        estado = JUGANDO




ejecutando = True

while ejecutando:

    dt = (
        reloj.tick(FPS)
        / 1000.0
    )

   

    for e in pygame.event.get():

        if e.type == pygame.QUIT:

            ejecutando = False

        elif e.type == pygame.KEYDOWN:

            if e.key == pygame.K_ESCAPE:

                ejecutando = False

          

            elif e.key == pygame.K_F6:

                ir_al_nivel_final()

           

            elif e.key == pygame.K_F7:

                ir_al_final_completo()

       

            elif estado == MENU:

                if e.key == pygame.K_RETURN:

                    reiniciar()

                elif e.key == pygame.K_c:

                    estado = PERSONAJE

       

            elif estado == PERSONAJE:

                if e.key == pygame.K_LEFT:

                    apariencia = (

                        apariencia - 1
                    ) % len(apariencias)

                elif e.key == pygame.K_RIGHT:

                    apariencia = (

                        apariencia + 1
                    ) % len(apariencias)

                elif e.key == pygame.K_RETURN:

                    estado = MENU

         
            elif estado == HISTORIA:

                if e.key == pygame.K_RETURN:

                    estado = JUGANDO

        

            elif estado == JUGANDO:

                if e.key == pygame.K_p:

                    estado = PAUSA

              

                elif e.key == pygame.K_e:

                    objeto_actual = (
                        objeto_cercano()
                    )

                    if objeto_actual:

                       
                        if objeto_actual[0] == "fragmento":

                            abrir_pregunta()

                        

                        elif objeto_actual[0] == "puerta":

                            
                            if nivel < 6:

                                if fragmentos >= 4:

                                    avanzar_nivel()

                                else:

                                    mostrar_mensaje(

                                        f"Necesitas los 4 "
                                        f"fragmentos. "
                                        f"Tienes {fragmentos}/4."

                                    )

                            

                            else:

                                # Ya tiene todo

                                if (
                                    fragmentos >= 4
                                    and llave
                                ):

                                    mostrar_mensaje(

                                        "¡LA PUERTA FINAL SE ABRE!"

                                    )

                                    estado = VICTORIA

                                # Tiene los fragmentos pero
                                # por seguridad no tiene llave

                                elif fragmentos >= 4:

                                    llave = True

                                    mostrar_mensaje(

                                        "¡LLAVE DORADA CONSEGUIDA! "
                                        "Presiona E nuevamente."

                                    )

                                # No tiene todos los fragmentos

                                else:

                                    mostrar_mensaje(

                                        "La puerta final está "
                                        "bloqueada. Necesitas los "
                                        f"4 fragmentos ({fragmentos}/4)."

                                    )

            

                elif (

                    e.key == pygame.K_n
                    and fragmentos >= 4

                ):

                    if nivel < 6:

                        avanzar_nivel()

                    elif llave:

                        estado = VICTORIA


                elif (

                    e.key == pygame.K_SPACE
                    and dash_t <= 0

                ):

                    dash_t = 0.22

           

            elif estado == PAUSA:

                if e.key == pygame.K_p:

                    estado = JUGANDO

          

            elif estado in (

                VICTORIA,
                DERROTA

            ):

                if e.key == pygame.K_RETURN:

                    reiniciar()

        
        elif (

            e.type == pygame.MOUSEBUTTONDOWN
            and estado == PREGUNTA

        ):

            botones = pregunta_screen()

            for i, r in enumerate(
                botones
            ):

                if r.collidepoint(
                    e.pos
                ):

                    responder(i)

   

    if estado == JUGANDO:

        teclas = pygame.key.get_pressed()

        dx = (

            teclas[pygame.K_d]
            or teclas[pygame.K_RIGHT]

        ) - (

            teclas[pygame.K_a]
            or teclas[pygame.K_LEFT]

        )

        dy = (

            teclas[pygame.K_s]
            or teclas[pygame.K_DOWN]

        ) - (

            teclas[pygame.K_w]
            or teclas[pygame.K_UP]

        )

        if dx and dy:

            dx *= 0.707

            dy *= 0.707

        multiplicador = (

            2.2
            if dash_t > 0
            else 1

        )

        jugador.x += int(

            dx
            * velocidad
            * multiplicador

        )

        jugador.y += int(

            dy
            * velocidad
            * multiplicador

        )

        jugador.clamp_ip(

            pygame.Rect(

                55,
                85,
                ANCHO - 110,
                ALTO - 155

            )

        )

      


        for r in monedas[:]:

            if jugador.colliderect(
                r.inflate(12, 12)
            ):

                monedas.remove(r)

                puntos += 25

      

        for r in trampas:

            if jugador.colliderect(r):

                recibir_daño(
                    "trampa"
                )

    
    

        for enemigo in enemigos:

            r = enemigo["rect"]

            r.x += int(
                enemigo["vx"]
            )

            r.y += int(
                enemigo["vy"]
            )

            if (

                r.left < 70
                or r.right > 1130

            ):

                enemigo["vx"] *= -1

            if (

                r.top < 95
                or r.bottom > 640

            ):

                enemigo["vy"] *= -1

            if jugador.colliderect(
                r.inflate(-5, -5)
            ):

                recibir_daño(
                    "enemigo"
                )

        if invulnerable > 0:

            invulnerable -= dt

        if dash_t > 0:

            dash_t -= dt



    if estado == MENU:

        menu()

    elif estado == PERSONAJE:

        pantalla_personaje()

    elif estado == HISTORIA:

        historia()

    elif estado == JUGANDO:

        fondo_nivel()

        dibujar_objetos()

        if (

            invulnerable <= 0
            or int(
                invulnerable * 12
            ) % 2 == 0

        ):

            dibujar_buho()

        interfaz()

        obj = objeto_cercano()

        if obj:

            if obj[0] == "fragmento":

                texto(

                    "E • Responder desafío",
                    fuente_peq,
                    DORADO,
                    600,
                    610

                )

            elif obj[0] == "puerta":

                if nivel == 6 and llave:

                    texto(

                        "E • ABRIR PUERTA FINAL",
                        fuente_peq,
                        VERDE2,
                        600,
                        610

                    )

                else:

                    texto(

                        "E • Interactuar con la puerta",
                        fuente_peq,
                        DORADO,
                        600,
                        610

                    )

        elif fragmentos >= 4:

            if nivel == 6 and llave:

                texto(

                    "¡LLAVE CONSEGUIDA! Busca la puerta final.",
                    fuente_peq,
                    DORADO,
                    600,
                    610

                )

            else:

                texto(

                    "¡Ya tienes los 4 fragmentos! Busca la puerta.",
                    fuente_peq,
                    DORADO,
                    600,
                    610

                )

        dibujar_mensaje()

    elif estado == PREGUNTA:

        pregunta_screen()

    elif estado == PAUSA:

        pausa()

    elif estado == VICTORIA:

        victoria()

    elif estado == DERROTA:

        derrota()

    pygame.display.flip()



if MUSICA_ACTIVA:

    try:

        pygame.mixer.music.stop()

    except:

        pass

pygame.quit()

sys.exit()
