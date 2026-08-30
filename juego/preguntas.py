"""Banco de preguntas y selección aleatoria sin repeticiones.

IMPORTANTE: las opciones se guardan SIN la letra ("A)", "B)"...).
La letra se genera al dibujar, después de barajar, para que siempre
coincida con la posición real en pantalla.
"""

import random

from juego.config import NIVEL_MAX


def P(nivel, categoria, enunciado, opciones, correcta, explicacion):
    """Crea una pregunta.

    `correcta` es el índice (0-3) de la respuesta correcta dentro de `opciones`.
    """
    return {
        "nivel": nivel,
        "categoria": categoria,
        "pregunta": enunciado,
        "opciones": opciones,
        "correcta": correcta,
        "explicacion": explicacion,
    }


BANCO = [

    # ------------------------------------------------------------------
    # NIVEL 1 - Bosque del Conocimiento (Fácil)
    # ------------------------------------------------------------------

    P(1, "Naturaleza",
      "¿Cuál es el animal terrestre más grande?",
      ["Elefante africano", "Rinoceronte", "Jirafa", "Hipopótamo"], 0,
      "El elefante africano es el animal terrestre más grande."),

    P(1, "Geografía",
      "¿Cuál es el océano más grande?",
      ["Atlántico", "Índico", "Pacífico", "Ártico"], 2,
      "El océano Pacífico es el más grande del planeta."),

    P(1, "Astronomía",
      "¿Cuál es el planeta más grande del Sistema Solar?",
      ["Marte", "Saturno", "Tierra", "Júpiter"], 3,
      "Júpiter es el planeta más grande del Sistema Solar."),

    P(1, "Historia",
      "¿Dónde están las pirámides de Giza?",
      ["Grecia", "Egipto", "Italia", "Perú"], 1,
      "Las pirámides de Giza se encuentran en Egipto."),

    P(1, "Colombia",
      "¿Cuál es la capital de Colombia?",
      ["Cali", "Medellín", "Bogotá", "Cartagena"], 2,
      "Bogotá es la capital de Colombia."),

    P(1, "Ciencia",
      "¿Qué necesitan las plantas para realizar la fotosíntesis?",
      ["Luz solar", "Hielo", "Arena", "Metal"], 0,
      "La luz solar es fundamental para la fotosíntesis."),

    P(1, "Matemáticas",
      "¿Cuántos días tiene un año que no es bisiesto?",
      ["360", "365", "366", "370"], 1,
      "Un año común tiene 365 días; el bisiesto tiene 366."),

    P(1, "Naturaleza",
      "¿Cuántas patas tiene una araña?",
      ["Seis", "Ocho", "Diez", "Cuatro"], 1,
      "Las arañas son arácnidos y tienen ocho patas."),

    P(1, "Ciencia",
      "¿Qué pigmento da el color verde a las hojas de las plantas?",
      ["La clorofila", "La melanina", "El caroteno", "La hemoglobina"], 0,
      "La clorofila da el color verde y captura la luz para la fotosíntesis."),

    P(1, "Astronomía",
      "¿Qué astro nos da luz y calor durante el día?",
      ["La Luna", "Marte", "El Sol", "Venus"], 2,
      "El Sol es la estrella que ilumina y calienta la Tierra."),

    P(1, "Ciencia",
      "¿Qué sentido usamos principalmente para escuchar?",
      ["La vista", "El olfato", "El gusto", "El oído"], 3,
      "El oído es el sentido que nos permite percibir los sonidos."),

    P(1, "Naturaleza",
      "¿Qué animal es conocido popularmente como el rey de la selva?",
      ["El tigre", "El león", "El oso", "El lobo"], 1,
      "El león recibe tradicionalmente el apodo de rey de la selva."),

    # ------------------------------------------------------------------
    # NIVEL 2 - Desierto del Tiempo (Fácil+)
    # ------------------------------------------------------------------

    P(2, "Historia",
      "¿Quién fue conocido como el Libertador de varias naciones sudamericanas?",
      ["Simón Bolívar", "Cristóbal Colón", "Napoleón Bonaparte", "Julio César"], 0,
      "Simón Bolívar tuvo un papel fundamental en varias independencias sudamericanas."),

    P(2, "Astronomía",
      "¿Qué planeta es conocido como el planeta rojo?",
      ["Venus", "Marte", "Mercurio", "Neptuno"], 1,
      "Marte es conocido como el planeta rojo por el óxido de hierro de su suelo."),

    P(2, "Ciencia",
      "¿Qué órgano bombea la sangre por el cuerpo?",
      ["Pulmón", "Cerebro", "Corazón", "Estómago"], 2,
      "El corazón bombea la sangre por todo el cuerpo."),

    P(2, "Geografía",
      "¿Cuál es el país más grande de Sudamérica?",
      ["Colombia", "Argentina", "Brasil", "Perú"], 2,
      "Brasil es el país más grande de Sudamérica por superficie."),

    P(2, "Astronomía",
      "¿Cuál es el planeta más cercano al Sol?",
      ["Venus", "Tierra", "Marte", "Mercurio"], 3,
      "Mercurio es el planeta más cercano al Sol."),

    P(2, "Naturaleza",
      "¿Cuál es el animal terrestre más rápido?",
      ["León", "Guepardo", "Caballo", "Tigre"], 1,
      "El guepardo alcanza más de 100 km/h en carreras cortas."),

    P(2, "Ciencia",
      "¿Cuántos huesos tiene aproximadamente el cuerpo humano adulto?",
      ["106", "156", "206", "306"], 2,
      "El esqueleto de un adulto tiene alrededor de 206 huesos."),

    P(2, "Ciencia",
      "¿En qué estado se encuentra el agua a 0 °C o menos?",
      ["Sólido", "Líquido", "Gaseoso", "Plasma"], 0,
      "Por debajo de 0 °C el agua se congela y pasa a estado sólido."),

    P(2, "Ciencia",
      "¿Qué instrumento se usa para medir la temperatura?",
      ["La balanza", "El termómetro", "El barómetro", "La brújula"], 1,
      "El termómetro mide la temperatura."),

    P(2, "Colombia",
      "¿Cuál es la moneda oficial de Colombia?",
      ["El bolívar", "El sol", "El peso colombiano", "El real"], 2,
      "La moneda oficial de Colombia es el peso colombiano."),

    P(2, "Ciencia",
      "¿Qué gas toman las plantas del aire para hacer la fotosíntesis?",
      ["Oxígeno", "Nitrógeno", "Helio", "Dióxido de carbono"], 3,
      "Las plantas absorben dióxido de carbono y liberan oxígeno."),

    P(2, "Matemáticas",
      "¿Cuántos lados tiene un hexágono?",
      ["Cinco", "Seis", "Siete", "Ocho"], 1,
      "El prefijo hexa- significa seis: un hexágono tiene seis lados."),

    # ------------------------------------------------------------------
    # NIVEL 3 - Ciudad del Saber (Media)
    # ------------------------------------------------------------------

    P(3, "Geografía",
      "¿Cuál es el río más largo de Sudamérica?",
      ["Amazonas", "Magdalena", "Orinoco", "Paraná"], 0,
      "El Amazonas es el principal río de Sudamérica y uno de los más largos del mundo."),

    P(3, "Historia",
      "¿En qué año llegó Cristóbal Colón a América?",
      ["1492", "1500", "1453", "1510"], 0,
      "El viaje de 1492 llevó a Colón al continente americano."),

    P(3, "Ciencia",
      "¿Cuál es el gas más abundante en la atmósfera terrestre?",
      ["Oxígeno", "Nitrógeno", "Hidrógeno", "Helio"], 1,
      "El nitrógeno constituye cerca del 78 % de la atmósfera."),

    P(3, "Arte",
      "¿Quién pintó la Mona Lisa?",
      ["Miguel Ángel", "Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"], 1,
      "La Mona Lisa fue pintada por Leonardo da Vinci."),

    P(3, "Literatura",
      "¿Quién escribió Don Quijote de la Mancha?",
      ["Gabriel García Márquez", "William Shakespeare", "Miguel de Cervantes",
       "Julio Verne"], 2,
      "Don Quijote de la Mancha fue escrito por Miguel de Cervantes."),

    P(3, "Colombia",
      "¿Cuál es el río más importante que atraviesa gran parte de Colombia?",
      ["Magdalena", "Amazonas", "Sena", "Nilo"], 0,
      "El río Magdalena recorre el país de sur a norte y es su principal arteria fluvial."),

    P(3, "Geografía",
      "¿Cuál es la capital de Argentina?",
      ["Santiago", "Montevideo", "Buenos Aires", "Lima"], 2,
      "Buenos Aires es la capital de Argentina."),

    P(3, "Ciencia",
      "¿Qué científico formuló la teoría de la relatividad?",
      ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Marie Curie"], 1,
      "Albert Einstein publicó la relatividad especial en 1905 y la general en 1915."),

    P(3, "Matemáticas",
      "¿Cuál es el resultado de 7 × 8?",
      ["54", "56", "48", "64"], 1,
      "7 × 8 = 56."),

    P(3, "Colombia",
      "¿En qué año ocurrió el Grito de Independencia de Colombia?",
      ["1810", "1819", "1492", "1886"], 0,
      "El Grito de Independencia se dio el 20 de julio de 1810."),

    P(3, "Ciencia",
      "¿Qué parte de la célula contiene el material genético?",
      ["La membrana", "El citoplasma", "El núcleo", "La pared celular"], 2,
      "El núcleo guarda el ADN en las células eucariotas."),

    P(3, "Ciencia",
      "¿Cuál es el único metal que es líquido a temperatura ambiente?",
      ["Plomo", "Mercurio", "Aluminio", "Estaño"], 1,
      "El mercurio es líquido a temperatura ambiente."),

    # ------------------------------------------------------------------
    # NIVEL 4 - Templo de los Recuerdos (Media+)
    # ------------------------------------------------------------------

    P(4, "Ciencia",
      "¿Cuál es la unidad básica de la vida?",
      ["Átomo", "Célula", "Tejido", "Órgano"], 1,
      "La célula es la unidad básica estructural y funcional de los seres vivos."),

    P(4, "Historia",
      "¿Qué civilización construyó Machu Picchu?",
      ["Romana", "Inca", "Egipcia", "Vikinga"], 1,
      "Machu Picchu fue construido por la civilización inca."),

    P(4, "Geografía",
      "¿Cuál es el país conocido por tener forma de bota?",
      ["España", "Italia", "Francia", "Portugal"], 1,
      "Italia suele describirse por su característica forma de bota."),

    P(4, "Astronomía",
      "¿Qué planeta tiene los anillos más famosos del Sistema Solar?",
      ["Marte", "Venus", "Saturno", "Mercurio"], 2,
      "Saturno es famoso por su amplio sistema de anillos."),

    P(4, "Música",
      "¿Cuál de estos instrumentos pertenece a la familia de las cuerdas?",
      ["Violín", "Trompeta", "Flauta", "Clarinete"], 0,
      "El violín es un instrumento de cuerda frotada."),

    P(4, "Naturaleza",
      "¿Cuál es el mamífero más grande del planeta?",
      ["Elefante africano", "Ballena azul", "Jirafa", "Orca"], 1,
      "La ballena azul es el animal más grande conocido."),

    P(4, "Ciencia",
      "¿Cuál es la fórmula química del agua?",
      ["CO2", "O2", "H2O", "NaCl"], 2,
      "El agua se compone de dos átomos de hidrógeno y uno de oxígeno: H2O."),

    P(4, "Literatura",
      "¿Quién escribió la obra Romeo y Julieta?",
      ["William Shakespeare", "Miguel de Cervantes", "Homero", "Dante Alighieri"], 0,
      "Romeo y Julieta es una tragedia de William Shakespeare."),

    P(4, "Ciencia",
      "¿Cuál es el hueso más largo del cuerpo humano?",
      ["El húmero", "La tibia", "El fémur", "La clavícula"], 2,
      "El fémur, en el muslo, es el hueso más largo del cuerpo."),

    P(4, "Colombia",
      "¿Qué cordillera atraviesa Colombia dividiéndose en tres ramales?",
      ["Los Alpes", "Los Andes", "Los Pirineos", "El Himalaya"], 1,
      "La cordillera de los Andes entra a Colombia y se divide en tres ramales."),

    P(4, "Astronomía",
      "¿Cuál es el único satélite natural de la Tierra?",
      ["Fobos", "Europa", "Titán", "La Luna"], 3,
      "La Luna es el único satélite natural de la Tierra."),

    P(4, "Ciencia",
      "¿Cómo se llama el proceso por el que el agua líquida pasa a vapor?",
      ["Condensación", "Evaporación", "Solidificación", "Sublimación"], 1,
      "La evaporación convierte el agua líquida en vapor de agua."),

    # ------------------------------------------------------------------
    # NIVEL 5 - Abismo del Conocimiento (Difícil)
    # ------------------------------------------------------------------

    P(5, "Historia",
      "¿Qué civilización construyó el Coliseo de Roma?",
      ["Romana", "Maya", "Inca", "China"], 0,
      "El Coliseo fue construido durante el Imperio romano."),

    P(5, "Geografía",
      "¿Cuál es la montaña más alta del mundo sobre el nivel del mar?",
      ["K2", "Everest", "Aconcagua", "Mont Blanc"], 1,
      "El monte Everest, con 8.849 m, es la montaña más alta sobre el nivel del mar."),

    P(5, "Ciencia",
      "¿Cuál es el órgano principal del sistema nervioso?",
      ["Corazón", "Cerebro", "Hígado", "Pulmón"], 1,
      "El cerebro es el órgano principal del sistema nervioso central."),

    P(5, "Literatura",
      "¿Quién escribió Cien años de soledad?",
      ["Gabriel García Márquez", "Mario Vargas Llosa", "Jorge Luis Borges",
       "Pablo Neruda"], 0,
      "Cien años de soledad fue escrita por el colombiano Gabriel García Márquez."),

    P(5, "Historia",
      "¿Qué civilización desarrolló la ciudad de Tenochtitlan?",
      ["Azteca", "Inca", "Romana", "Egipcia"], 0,
      "Tenochtitlan fue la gran capital del Imperio mexica o azteca."),

    P(5, "Geografía",
      "¿Qué país tiene la mayor superficie del mundo?",
      ["Canadá", "China", "Rusia", "Estados Unidos"], 2,
      "Rusia es el país con mayor superficie terrestre del planeta."),

    P(5, "Ciencia",
      "¿Cuál es el número atómico del carbono?",
      ["4", "6", "8", "12"], 1,
      "El carbono tiene 6 protones, por lo que su número atómico es 6."),

    P(5, "Historia",
      "¿En qué año llegó el ser humano a la Luna por primera vez?",
      ["1957", "1961", "1969", "1975"], 2,
      "La misión Apolo 11 alunizó el 20 de julio de 1969."),

    P(5, "Geografía",
      "¿Cuál es el desierto cálido más grande del mundo?",
      ["Sahara", "Atacama", "Gobi", "Kalahari"], 0,
      "El Sahara, en el norte de África, es el desierto cálido más extenso."),

    P(5, "Astronomía",
      "¿Quién propuso el modelo heliocéntrico del Sistema Solar?",
      ["Ptolomeo", "Aristóteles", "Nicolás Copérnico", "Johannes Kepler"], 2,
      "Copérnico propuso que los planetas giran alrededor del Sol."),

    P(5, "Geografía",
      "¿Cuál es la capital de Australia?",
      ["Sídney", "Melbourne", "Canberra", "Brisbane"], 2,
      "La capital de Australia es Canberra, no Sídney."),

    P(5, "Ciencia",
      "¿Qué tipo de roca se forma por el enfriamiento del magma?",
      ["Sedimentaria", "Metamórfica", "Ígnea", "Caliza"], 2,
      "Las rocas ígneas se forman al enfriarse y solidificarse el magma."),

    # ------------------------------------------------------------------
    # NIVEL 6 - La Puerta de la Matrix (Final)
    # ------------------------------------------------------------------

    P(6, "Ciencia",
      "¿Cuál es el elemento químico más abundante del universo?",
      ["Oxígeno", "Hidrógeno", "Carbono", "Hierro"], 1,
      "El hidrógeno es el elemento más abundante del universo conocido."),

    P(6, "Historia",
      "¿En qué país comenzó el movimiento conocido como Renacimiento?",
      ["Italia", "Francia", "Inglaterra", "Alemania"], 0,
      "El Renacimiento comenzó en las ciudades italianas del siglo XIV."),

    P(6, "Geografía",
      "¿Cuál es el continente con mayor superficie?",
      ["África", "Europa", "Asia", "Oceanía"], 2,
      "Asia es el continente más grande por superficie y población."),

    P(6, "Astronomía",
      "¿Cómo se llama nuestra galaxia?",
      ["Andrómeda", "Vía Láctea", "Orión", "Centauro"], 1,
      "Nuestra galaxia se llama Vía Láctea."),

    P(6, "Cultura general",
      "¿Cuál es el idioma con mayor número de hablantes nativos del mundo?",
      ["Español", "Inglés", "Chino mandarín", "Francés"], 2,
      "El chino mandarín tiene la mayor cantidad de hablantes nativos."),

    P(6, "Astronomía",
      "¿Qué unidad se usa para medir distancias entre estrellas?",
      ["El kilómetro", "La milla náutica", "El año luz", "El metro cúbico"], 2,
      "Un año luz es la distancia que recorre la luz en un año."),

    P(6, "Ciencia",
      "¿Quién desarrolló la teoría de la evolución por selección natural?",
      ["Gregor Mendel", "Charles Darwin", "Louis Pasteur", "Alexander Fleming"], 1,
      "Charles Darwin publicó El origen de las especies en 1859."),

    P(6, "Geografía",
      "¿En qué océano está la fosa de las Marianas, el punto más profundo?",
      ["Atlántico", "Índico", "Pacífico", "Ártico"], 2,
      "La fosa de las Marianas está en el océano Pacífico."),

    P(6, "Historia",
      "¿En qué siglo ocurrió la Revolución Francesa?",
      ["Siglo XVI", "Siglo XVII", "Siglo XVIII", "Siglo XIX"], 2,
      "La Revolución Francesa comenzó en 1789, en el siglo XVIII."),

    P(6, "Ciencia",
      "¿Qué órgano del cuerpo humano produce la insulina?",
      ["El hígado", "El páncreas", "El riñón", "El bazo"], 1,
      "El páncreas produce la insulina, que regula el azúcar en la sangre."),

    P(6, "Ciencia",
      "¿Qué nombre recibe el conjunto de todos los seres vivos y su entorno?",
      ["La atmósfera", "La litosfera", "La biosfera", "La hidrosfera"], 2,
      "La biosfera es el conjunto de los seres vivos y el medio en que habitan."),

    P(6, "Matrix",
      "¿Cuál es el objetivo final del Búho en esta aventura?",
      ["Encontrar comida", "Dormir", "Conseguir la llave y escapar de la Matrix",
       "Construir un castillo"], 2,
      "La misión final es conseguir la llave dorada y escapar de la Matrix."),
]


class BancoPreguntas:
    """Entrega preguntas de un nivel sin repetir hasta agotar el banco."""

    def __init__(self, banco=None, rng=None):
        self.banco = BANCO if banco is None else banco
        self.rng = rng or random
        self.por_nivel = {n: [] for n in range(1, NIVEL_MAX + 1)}

        for pregunta in self.banco:
            self.por_nivel.setdefault(pregunta["nivel"], []).append(pregunta)

        self.usadas = {n: set() for n in self.por_nivel}

    def reiniciar(self):
        """Olvida el historial de preguntas usadas (partida nueva)."""
        for vistas in self.usadas.values():
            vistas.clear()

    def siguiente(self, nivel):
        """Devuelve una pregunta del nivel con las opciones ya barajadas.

        Devuelve None si el nivel no tiene preguntas.
        """
        disponibles = self.por_nivel.get(nivel, [])
        if not disponibles:
            return None

        vistas = self.usadas[nivel]
        sin_usar = [p for p in disponibles if id(p) not in vistas]

        if not sin_usar:
            vistas.clear()
            sin_usar = disponibles

        original = self.rng.choice(sin_usar)
        vistas.add(id(original))

        # Barajamos manteniendo la marca de cuál era la correcta.
        marcadas = [
            (texto, i == original["correcta"])
            for i, texto in enumerate(original["opciones"])
        ]
        self.rng.shuffle(marcadas)

        pregunta = dict(original)
        pregunta["opciones"] = [texto for texto, _ in marcadas]
        pregunta["correcta"] = next(
            i for i, (_, es_correcta) in enumerate(marcadas) if es_correcta
        )
        return pregunta
