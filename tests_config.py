# tests_config.py - Configuración de Tests Vocacionales

from typing import Dict, List, Tuple
import random
import json

# Sistema de puntuación: A=5, B=4, C=3, D=2, E=1
PUNTUACION_VALORES = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1}

# TESTS_CONFIG - Mantener la configuración completa de tu main.py
TESTS_CONFIG = {
    "general": {
        "titulo": "Test Vocacional General",
        "descripcion": "Descubre tus áreas de interés profesional",
        "instrucciones": "Responde honestamente cada pregunta. No hay respuestas correctas o incorrectas.",
        "preguntas": [
            {"id": 1, "texto": "¿Disfrutas resolver problemas matemáticos y lógicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Te interesa comprender cómo funcionan las cosas y los fenómenos naturales?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Disfrutas trabajar con tecnología y computadoras?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te gusta diseñar, construir o crear cosas nuevas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Te interesa el mundo de los negocios y las finanzas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Disfrutas realizar experimentos científicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te gusta analizar datos y estadísticas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Te interesa entender cómo funcionan los mercados económicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Disfrutas programar o aprender lenguajes de programación?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te gusta trabajar en proyectos de construcción o mecánicos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Te interesa la innovación y las nuevas tecnologías?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Disfrutas gestionar proyectos y organizar recursos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te gusta estudiar organismos vivos y ecosistemas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Te interesa optimizar procesos y mejorar la eficiencia?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Disfrutas aprender sobre química y reacciones químicas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te gusta trabajar con circuitos y sistemas eléctricos?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Te interesa el marketing y las estrategias de ventas?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Disfrutas desarrollar aplicaciones o software?",
                "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                            {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                            {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te gusta analizar problemas complejos y encontrar soluciones creativas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Te interesa la gestión financiera y las inversiones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Disfrutas trabajar en laboratorios y realizar investigaciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te gusta diseñar estructuras y planificar infraestructuras?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Te interesa la inteligencia artificial y el machine learning?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Disfrutas liderar equipos y tomar decisiones estratégicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te gusta trabajar con física y entender las leyes del universo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Te interesa la automatización y robótica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Disfrutas analizar balances financieros y contabilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te gusta la biotecnología y la genética?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Te interesa la ciberseguridad y protección de sistemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Disfrutas trabajar en la optimización de producción industrial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 31, "texto": "¿Te gusta emprender y crear tu propio negocio?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 32, "texto": "¿Te interesa el medio ambiente y la sostenibilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 33, "texto": "¿Disfrutas diseñar interfaces y experiencias de usuario?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 34, "texto": "¿Te gusta analizar el comportamiento del consumidor?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 35, "texto": "¿Te interesa trabajar con energías renovables?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 36, "texto": "¿Disfrutas trabajar con bases de datos y gestión de información?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 37, "texto": "¿Te gusta investigar nuevos materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 38, "texto": "¿Te interesa la logística y cadena de suministro?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 39, "texto": "¿Disfrutas desarrollar videojuegos o aplicaciones interactivas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 40, "texto": "¿Te gusta analizar tendencias económicas y hacer proyecciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    },
    
    "tecnologia": {
        "titulo": "Test de Tecnología",
        "descripcion": "Evalúa tu afinidad con carreras tecnológicas",
        "instrucciones": "Este test te ayudará a identificar si las carreras tecnológicas son para ti.",
        "preguntas": [
            {"id": 1, "texto": "¿Te interesa aprender lenguajes de programación?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 2, "texto": "¿Disfrutas resolver problemas usando lógica y algoritmos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 3, "texto": "¿Te gusta estar al día con las últimas tecnologías?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 4, "texto": "¿Disfrutas diseñar y desarrollar aplicaciones o sitios web?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 5, "texto": "¿Te interesa la inteligencia artificial y el aprendizaje automático?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 6, "texto": "¿Disfrutas trabajar con bases de datos y gestión de información?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 7, "texto": "¿Te gusta la ciberseguridad y proteger sistemas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 8, "texto": "¿Te interesa desarrollar videojuegos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 9, "texto": "¿Disfrutas configurar y administrar redes de computadoras?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 10, "texto": "¿Te gusta analizar y visualizar grandes volúmenes de datos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 11, "texto": "¿Te interesa el cloud computing y servicios en la nube?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 12, "texto": "¿Disfrutas automatizar tareas usando scripts o programas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 13, "texto": "¿Te gusta diseñar interfaces de usuario atractivas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 14, "texto": "¿Te interesa el desarrollo móvil (apps para celulares)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 15, "texto": "¿Disfrutas debuggear (encontrar y corregir errores) en código?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 16, "texto": "¿Te gusta trabajar con hardware y componentes de computadoras?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 17, "texto": "¿Te interesa el Internet de las Cosas (IoT)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 18, "texto": "¿Disfrutas optimizar el rendimiento de aplicaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 19, "texto": "¿Te gusta la realidad virtual y aumentada?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 20, "texto": "¿Te interesa el blockchain y las criptomonedas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 21, "texto": "¿Disfrutas participar en hackathons o competencias de programación?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 22, "texto": "¿Te gusta trabajar con APIs y servicios web?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 23, "texto": "¿Te interesa DevOps y la integración continua?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 24, "texto": "¿Disfrutas aprender nuevos frameworks y librerías?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 25, "texto": "¿Te gusta el desarrollo backend (servidor)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 26, "texto": "¿Te interesa el testing y aseguramiento de calidad?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 27, "texto": "¿Disfrutas el trabajo colaborativo con control de versiones (Git)?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 28, "texto": "¿Te gusta crear soluciones innovadoras con tecnología?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 29, "texto": "¿Te interesa la arquitectura de software?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 30, "texto": "¿Disfrutas mantenerte actualizado con tendencias tecnológicas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]}
        ]
    },
    
    "ciencias": {
        "titulo": "Test de Ciencias",
        "descripcion": "Descubre tu vocación científica",
        "instrucciones": "Responde según tu interés real en actividades científicas.",
        "preguntas": [
            {"id": 1, "texto": "¿Te gusta realizar experimentos y descubrir cómo funcionan las cosas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Te interesa estudiar organismos vivos y ecosistemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Disfrutas trabajar en laboratorios?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te gusta la química y las reacciones químicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Te interesa la física y las leyes del universo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Disfrutas investigar y formular hipótesis?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te gusta la biotecnología y la genética?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Te interesa la astronomía y el espacio?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Disfrutas analizar datos experimentales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te gusta la medicina y ayudar a la salud de las personas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Te interesa la ecología y conservación ambiental?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Disfrutas usar el método científico para resolver problemas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te gusta la microbiología y el estudio de microorganismos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Te interesa la neurociencia y el cerebro humano?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Disfrutas investigar sobre materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te gusta la farmacología y el desarrollo de medicamentos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Te interesa la geología y el estudio de la Tierra?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Disfrutas estudiar el comportamiento animal?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te gusta la bioquímica y procesos moleculares?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Te interesa la climatología y cambio climático?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Disfrutas la investigación en laboratorio por largas horas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te gusta leer artículos científicos y papers?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Te interesa la nanotecnología?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Disfrutas usar microscopios y equipos especializados?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te gusta contribuir al avance del conocimiento científico?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Te interesa la oceanografía y vida marina?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Disfrutas analizar muestras y hacer mediciones precisas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te gusta la paleontología y el estudio de fósiles?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Te interesa la toxicología y sustancias químicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Disfrutas participar en proyectos de investigación científica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    },
    
    "ingenieria": {
        "titulo": "Test de Ingeniería",
        "descripcion": "Evalúa tu aptitud para carreras de ingeniería",
        "instrucciones": "Este test mide tu afinidad con el pensamiento ingenieril.",
        "preguntas": [
            {"id": 1, "texto": "¿Disfrutas diseñar y construir cosas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 2, "texto": "¿Te gusta resolver problemas técnicos complejos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 3, "texto": "¿Te interesa el diseño de estructuras y edificaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 4, "texto": "¿Disfrutas trabajar con máquinas y mecanismos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 5, "texto": "¿Te gusta la electricidad y los circuitos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 6, "texto": "¿Te interesa optimizar procesos industriales?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 7, "texto": "¿Disfrutas usar herramientas de diseño CAD?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 8, "texto": "¿Te gusta la robótica y automatización?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 9, "texto": "¿Te interesa la ingeniería ambiental y sostenibilidad?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 10, "texto": "¿Disfrutas calcular y hacer cálculos técnicos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 11, "texto": "¿Te gusta trabajar con materiales y sus propiedades?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 12, "texto": "¿Te interesa la gestión de proyectos de ingeniería?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 13, "texto": "¿Disfrutas hacer prototipos y pruebas?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 14, "texto": "¿Te gusta la termodinámica y transferencia de calor?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 15, "texto": "¿Te interesa el control de calidad en manufactura?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 16, "texto": "¿Disfrutas diseñar sistemas de producción?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 17, "texto": "¿Te gusta la mecánica de fluidos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 18, "texto": "¿Te interesa el diseño de vehículos y transporte?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 19, "texto": "¿Disfrutas trabajar con energías renovables?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 20, "texto": "¿Te gusta el análisis estructural?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 21, "texto": "¿Te interesa la construcción de infraestructura?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 22, "texto": "¿Disfrutas hacer simulaciones y modelado?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 23, "texto": "¿Te gusta la ingeniería biomédica?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 24, "texto": "¿Te interesa el tratamiento de aguas y residuos?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 25, "texto": "¿Disfrutas innovar y mejorar diseños existentes?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 26, "texto": "¿Te gusta la logística y cadena de suministro?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 27, "texto": "¿Te interesa el diseño de sistemas de telecomunicaciones?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 28, "texto": "¿Disfrutas trabajar en proyectos multidisciplinarios?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 29, "texto": "¿Te gusta resolver problemas de ingeniería en campo?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]},
            
            {"id": 30, "texto": "¿Te interesa contribuir al desarrollo tecnológico?",
             "opciones": [{"valor": "A", "texto": "Mucho"}, {"valor": "B", "texto": "Bastante"}, 
                         {"valor": "C", "texto": "Algo"}, {"valor": "D", "texto": "Poco"}, 
                         {"valor": "E", "texto": "Nada"}]}
        ]
    },
    
    "economia": {
        "titulo": "Test de Economía",
        "descripcion": "Descubre tu afinidad con carreras económicas y de negocios",
        "instrucciones": "Responde según tu interés en temas económicos y financieros.",
        "preguntas": [
            {"id": 1, "texto": "¿Te interesa entender cómo funcionan los mercados y las finanzas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 2, "texto": "¿Disfrutas analizar datos financieros y balances?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 3, "texto": "¿Te gusta gestionar negocios y organizaciones?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 4, "texto": "¿Te interesa el marketing y estrategias de ventas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 5, "texto": "¿Disfrutas hacer inversiones y análisis de riesgo?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 6, "texto": "¿Te gusta emprender y crear negocios propios?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 7, "texto": "¿Te interesa la contabilidad y registros financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 8, "texto": "¿Disfrutas negociar y cerrar acuerdos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 9, "texto": "¿Te gusta liderar equipos y tomar decisiones empresariales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 10, "texto": "¿Te interesa el comercio internacional?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 11, "texto": "¿Disfrutas analizar el comportamiento del consumidor?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 12, "texto": "¿Te gusta gestionar recursos humanos?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 13, "texto": "¿Te interesa la banca y servicios financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 14, "texto": "¿Disfrutas hacer proyecciones y planificación estratégica?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 15, "texto": "¿Te gusta la economía global y políticas económicas?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 16, "texto": "¿Te interesa la consultoría empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 17, "texto": "¿Disfrutas trabajar con presupuestos y planeación financiera?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 18, "texto": "¿Te gusta el análisis de mercados y competencia?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 19, "texto": "¿Te interesa la gestión de proyectos empresariales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 20, "texto": "¿Disfrutas leer sobre finanzas y economía?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 21, "texto": "¿Te gusta el e-commerce y negocios digitales?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 22, "texto": "¿Te interesa la auditoría y control interno?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 23, "texto": "¿Disfrutas optimizar costos y mejorar rentabilidad?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 24, "texto": "¿Te gusta la gestión de la calidad empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 25, "texto": "¿Te interesa la responsabilidad social empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 26, "texto": "¿Disfrutas trabajar con indicadores de desempeño (KPIs)?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 27, "texto": "¿Te gusta la gestión de marcas y branding?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 28, "texto": "¿Te interesa el análisis económico y estadístico?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 29, "texto": "¿Disfrutas asistir a eventos de networking empresarial?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]},
            
            {"id": 30, "texto": "¿Te gusta tomar decisiones basadas en datos financieros?",
             "opciones": [{"valor": "A", "texto": "Totalmente de acuerdo"}, {"valor": "B", "texto": "De acuerdo"}, 
                         {"valor": "C", "texto": "Neutral"}, {"valor": "D", "texto": "En desacuerdo"}, 
                         {"valor": "E", "texto": "Totalmente en desacuerdo"}]}
        ]
    }
}

# MAPEO_PREGUNTAS_GENERAL - Copiar de tu main.py
MAPEO_PREGUNTAS_GENERAL = {
    # === BLOQUE 1: MATEMÁTICAS & LÓGICA ===
    1: {"matematicas": 1.0, "logica": 0.9, "analitico": 0.7, "resolucion": 0.6},
    7: {"analitico": 1.0, "datos": 0.9, "matematicas": 0.7, "estadistica": 0.6},
    19: {"analitico": 1.0, "resolucion": 1.0, "logica": 0.8, "creatividad": 0.7},
    
    # === BLOQUE 2: CIENCIAS NATURALES ===
    2: {"ciencias": 1.0, "curiosidad": 0.8, "investigacion": 0.7, "naturaleza": 0.5},
    6: {"ciencias": 1.0, "investigacion": 1.0, "metodico": 0.8, "laboratorio": 0.7},
    13: {"biologia": 1.0, "ciencias": 0.9, "naturaleza": 0.8, "ecologia": 0.6},
    15: {"quimica": 1.0, "ciencias": 0.9, "laboratorio": 0.8, "investigacion": 0.6},
    21: {"investigacion": 1.0, "ciencias": 0.9, "paciencia": 0.7, "metodico": 0.7},
    25: {"fisica": 1.0, "ciencias": 0.9, "teorico": 0.8, "matematicas": 0.7},
    28: {"biotecnologia": 1.0, "biologia": 0.8, "ciencias": 0.8, "innovacion": 0.6},
    
    # === BLOQUE 3: TECNOLOGÍA & PROGRAMACIÓN ===
    3: {"tecnologia": 1.0, "practico": 0.7, "digital": 0.8},
    9: {"programacion": 1.0, "tecnologia": 0.9, "logica": 0.8, "algoritmos": 0.7},
    11: {"innovacion": 1.0, "tecnologia": 0.9, "futuro": 0.8, "tendencias": 0.6},
    18: {"programacion": 1.0, "desarrollo": 1.0, "tecnologia": 0.9, "creatividad": 0.5},
    23: {"ia": 1.0, "tecnologia": 0.9, "programacion": 0.8, "matematicas": 0.7},
    29: {"seguridad": 1.0, "tecnologia": 0.9, "proteccion": 0.8, "sistemas": 0.7},
    33: {"ux": 1.0, "diseno": 0.9, "tecnologia": 0.8, "creatividad": 0.8, "usuario": 0.7},
    36: {"datos": 1.0, "tecnologia": 0.9, "organizacion": 0.8, "analitico": 0.7},
    39: {"gaming": 1.0, "programacion": 0.9, "creatividad": 0.9, "tecnologia": 0.8},
    
    # === BLOQUE 4: INGENIERÍA & CONSTRUCCIÓN ===
    4: {"diseno": 1.0, "creatividad": 0.9, "ingenieria": 0.7, "construccion": 0.6},
    10: {"construccion": 1.0, "ingenieria": 0.9, "practico": 0.9, "mecanico": 0.7},
    14: {"optimizacion": 1.0, "ingenieria": 0.8, "analitico": 0.7, "eficiencia": 0.8},
    16: {"electrica": 1.0, "ingenieria": 0.9, "tecnico": 0.9, "sistemas": 0.7},
    22: {"civil": 1.0, "ingenieria": 0.9, "diseno": 0.8, "construccion": 0.7, "estructural": 0.8},
    26: {"automatizacion": 1.0, "robotica": 0.9, "ingenieria": 0.8, "tecnologia": 0.7},
    30: {"industrial": 1.0, "ingenieria": 0.9, "produccion": 0.9, "optimizacion": 0.7},
    35: {"energia": 1.0, "renovables": 0.9, "ingenieria": 0.8, "ambiental": 0.7, "sostenibilidad": 0.8},
    37: {"materiales": 1.0, "ciencias": 0.8, "investigacion": 0.8, "innovacion": 0.6},
    
    # === BLOQUE 5: NEGOCIOS & ECONOMÍA ===
    5: {"negocios": 1.0, "finanzas": 0.8, "estrategia": 0.7, "empresarial": 0.6},
    8: {"economia": 1.0, "mercados": 0.9, "negocios": 0.8, "analitico": 0.6},
    12: {"liderazgo": 1.0, "gestion": 0.9, "organizacion": 0.9, "negocios": 0.6},
    17: {"marketing": 1.0, "comunicacion": 0.9, "negocios": 0.8, "creatividad": 0.7, "ventas": 0.8},
    20: {"finanzas": 1.0, "inversion": 0.9, "negocios": 0.8, "analitico": 0.7, "riesgo": 0.6},
    24: {"liderazgo": 1.0, "decision": 0.9, "estrategia": 0.8, "negocios": 0.7},
    27: {"contabilidad": 1.0, "finanzas": 0.8, "detalle": 0.9, "negocios": 0.7, "numeros": 0.8},
    31: {"emprendimiento": 1.0, "negocios": 0.9, "innovacion": 0.8, "riesgo": 0.7, "liderazgo": 0.6},
    34: {"consumidor": 1.0, "marketing": 0.9, "psicologia": 0.7, "negocios": 0.6, "investigacion": 0.5},
    38: {"logistica": 1.0, "cadena": 0.9, "organizacion": 0.8, "optimizacion": 0.7, "negocios": 0.6},
    40: {"economia": 1.0, "proyeccion": 0.9, "analitico": 0.8, "tendencias": 0.7, "finanzas": 0.6},
    
    # === BLOQUE 6: SOSTENIBILIDAD & MEDIO AMBIENTE ===
    32: {"ambiental": 1.0, "sostenibilidad": 1.0, "responsabilidad": 0.9, "ecologia": 0.8, "futuro": 0.6},
}

# ================================
# PERFILES VOCACIONALES MEJORADOS
# ================================

PERFILES_DETALLADOS = {
    "desarrollador_software": {
        "nombre": "Desarrollador/a de Software",
        "indicadores_clave": {
            "tecnologia": (72, 100),      # ✅ Cambiado de 70
            "programacion": (75, 100),    # Igual
            "logica": (70, 100),          # Igual
        },
        "indicadores_secundarios": {
            "analitico": (65, 100),       # ✅ Cambiado de 60
            "resolucion": (65, 100),      # Igual
            "creatividad": (50, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería de Software",
                "match_base": 95,
                "factores": {
                    "programacion": 0.35,
                    "tecnologia": 0.30,
                    "logica": 0.20,
                    "creatividad": 0.15
                }
            },
            {
                "nombre": "Ingeniería de Sistemas",
                "match_base": 92,
                "factores": {
                    "tecnologia": 0.35,
                    "programacion": 0.30,
                    "analitico": 0.20,
                    "organizacion": 0.15
                }
            },
            {
                "nombre": "Ciencia de Datos",
                "match_base": 88,
                "factores": {
                    "datos": 0.35,
                    "programacion": 0.30,
                    "analitico": 0.25,
                    "matematicas": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil muestra una fuerte inclinación hacia el desarrollo de software. Destacas en pensamiento lógico, resolución de problemas y tienes la creatividad necesaria para diseñar soluciones innovadoras.",
        "fortalezas_especificas": [
            "Pensamiento algorítmico y estructurado",
            "Capacidad de abstracción de problemas complejos",
            "Aprendizaje continuo de nuevas tecnologías",
            "Creatividad aplicada a soluciones técnicas"
        ],
        "areas_desarrollo": [
            "Comunicación técnica con equipos no técnicos",
            "Gestión de proyectos y plazos",
            "Habilidades de presentación",
            "Trabajo colaborativo en equipos grandes"
        ],
        "campo_laboral": [
            "Empresas de tecnología (startups y corporaciones)",
            "Desarrollo de aplicaciones móviles y web",
            "Consultoría tecnológica",
            "Investigación y desarrollo (I+D)",
            "Trabajo remoto/freelance con proyectos globales"
        ]
    },
    
    "cientifico_investigador": {
        "nombre": "Científico/a Investigador/a",
        "indicadores_clave": {
            "ciencias": (75, 100),        # Igual
            "investigacion": (75, 100),   # Igual
            "metodico": (68, 100),
        },
        "indicadores_secundarios": {
            "curiosidad": (65, 100),      # ✅ Cambiado de 70
            "paciencia": (60, 100),       # ✅ Cambiado de 65
            "laboratorio": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Biología",
                "match_base": 90,
                "factores": {
                    "biologia": 0.40,
                    "investigacion": 0.30,
                    "naturaleza": 0.20,
                    "metodico": 0.10
                }
            },
            {
                "nombre": "Química",
                "match_base": 88,
                "factores": {
                    "quimica": 0.40,
                    "laboratorio": 0.25,
                    "investigacion": 0.25,
                    "analitico": 0.10
                }
            },
            {
                "nombre": "Biotecnología",
                "match_base": 92,
                "factores": {
                    "biotecnologia": 0.35,
                    "biologia": 0.25,
                    "innovacion": 0.20,
                    "investigacion": 0.20
                }
            }
        ],
        "descripcion": "Tienes un perfil científico sólido con gran curiosidad intelectual. Te apasiona entender cómo funciona el mundo natural y tienes la disciplina necesaria para la investigación rigurosa.",
        "fortalezas_especificas": [
            "Método científico riguroso",
            "Pensamiento crítico y analítico",
            "Atención meticulosa al detalle",
            "Capacidad para trabajo experimental sistemático"
        ],
        "areas_desarrollo": [
            "Aplicación comercial de investigaciones",
            "Comunicación científica para público general",
            "Gestión de financiamiento y grants",
            "Networking en comunidad científica"
        ],
        "campo_laboral": [
            "Universidades e institutos de investigación",
            "Laboratorios farmacéuticos",
            "Centros de biotecnología",
            "Organizaciones ambientales",
            "Docencia e investigación académica"
        ]
    },
    
    "ingeniero_constructor": {
        "nombre": "Ingeniero/a de Construcción e Infraestructura",
        "indicadores_clave": {
            "ingenieria": (70, 100),
            "practico": (70, 100),
            "diseno": (65, 100)
        },
        "indicadores_secundarios": {
            "matematicas": (62, 100),
            "organizacion": (60, 100),
            "construccion": (65, 100)
        },
        "carreras": [
            {
                "nombre": "Ingeniería Civil",
                "match_base": 95,
                "factores": {
                    "civil": 0.40,
                    "construccion": 0.25,
                    "diseno": 0.20,
                    "matematicas": 0.15
                }
            },
            {
                "nombre": "Ingeniería Mecánica",
                "match_base": 90,
                "factores": {
                    "ingenieria": 0.35,
                    "practico": 0.30,
                    "diseno": 0.20,
                    "tecnico": 0.15
                }
            },
            {
                "nombre": "Arquitectura",
                "match_base": 85,
                "factores": {
                    "diseno": 0.40,
                    "creatividad": 0.25,
                    "construccion": 0.20,
                    "estetico": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil indica una fuerte vocación por crear infraestructura y soluciones tangibles. Combinas habilidades técnicas con visión espacial y capacidad de materializar proyectos.",
        "fortalezas_especificas": [
            "Pensamiento espacial y visual desarrollado",
            "Capacidad de planificación a gran escala",
            "Comprensión de sistemas físicos complejos",
            "Enfoque práctico orientado a resultados"
        ],
        "areas_desarrollo": [
            "Herramientas digitales avanzadas (BIM, CAD 3D)",
            "Sostenibilidad y construcción verde",
            "Gestión de equipos multidisciplinarios",
            "Innovación en materiales"
        ],
        "campo_laboral": [
            "Empresas constructoras",
            "Consultoras de ingeniería",
            "Sector público (infraestructura)",
            "Desarrollo inmobiliario",
            "Consultoría independiente"
        ]
    },
    
    "estratega_negocios": {
        "nombre": "Estratega de Negocios",
        "indicadores_clave": {
            "negocios": (72, 100),
            "estrategia": (70, 100),
            "analitico": (65, 100)
        },
        "indicadores_secundarios": {
            "liderazgo": (62, 100),
            "decision": (65, 100),
            "comunicacion": (60, 100)
        },
        "carreras": [
            {
                "nombre": "Administración de Empresas",
                "match_base": 93,
                "factores": {
                    "negocios": 0.35,
                    "liderazgo": 0.25,
                    "organizacion": 0.20,
                    "estrategia": 0.20
                }
            },
            {
                "nombre": "Economía",
                "match_base": 90,
                "factores": {
                    "economia": 0.40,
                    "analitico": 0.30,
                    "proyeccion": 0.20,
                    "matematicas": 0.10
                }
            },
            {
                "nombre": "Finanzas",
                "match_base": 91,
                "factores": {
                    "finanzas": 0.40,
                    "analitico": 0.30,
                    "inversion": 0.20,
                    "riesgo": 0.10
                }
            }
        ],
        "descripcion": "Tienes un perfil orientado al mundo empresarial con fuerte capacidad analítica. Destacas en pensamiento estratégico y toma de decisiones basadas en datos.",
        "fortalezas_especificas": [
            "Visión estratégica de negocios",
            "Análisis cuantitativo y financiero",
            "Toma de decisiones bajo incertidumbre",
            "Comprensión de dinámicas de mercado"
        ],
        "areas_desarrollo": [
            "Habilidades técnicas (programación básica, BI)",
            "Innovación disruptiva y digital",
            "Gestión del cambio organizacional",
            "Pensamiento de diseño (design thinking)"
        ],
        "campo_laboral": [
            "Consultoría estratégica",
            "Banca de inversión",
            "Empresas corporativas (estrategia, finanzas)",
            "Startups (como CFO o estratega)",
            "Analista financiero"
        ]
    },
    
    "innovador_tecnologico": {
        "nombre": "Innovador/a Tecnológico/a",
        "indicadores_clave": {
            "tecnologia": (70, 100),
            "innovacion": (75, 100),
            "creatividad": (70, 100)
        },
        "indicadores_secundarios": {
            "futuro": (65, 100),
            "ia": (58, 100),
            "programacion": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería en Inteligencia Artificial",
                "match_base": 94,
                "factores": {
                    "ia": 0.40,
                    "programacion": 0.25,
                    "matematicas": 0.20,
                    "innovacion": 0.15
                }
            },
            {
                "nombre": "Ingeniería Mecatrónica",
                "match_base": 90,
                "factores": {
                    "tecnologia": 0.30,
                    "ingenieria": 0.30,
                    "automatizacion": 0.25,
                    "innovacion": 0.15
                }
            },
            {
                "nombre": "Diseño de Productos Digitales",
                "match_base": 87,
                "factores": {
                    "diseno": 0.35,
                    "ux": 0.30,
                    "tecnologia": 0.20,
                    "creatividad": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil combina creatividad con habilidades técnicas avanzadas. Te atrae crear soluciones innovadoras que integran múltiples disciplinas y tecnologías emergentes.",
        "fortalezas_especificas": [
            "Pensamiento interdisciplinario",
            "Adaptabilidad a nuevas tecnologías",
            "Visión de futuro y tendencias",
            "Creatividad aplicada a soluciones técnicas"
        ],
        "areas_desarrollo": [
            "Profundización en fundamentos teóricos",
            "Metodologías de investigación formal",
            "Gestión de proyectos de I+D",
            "Comercialización de innovaciones"
        ],
        "campo_laboral": [
            "Departamentos de I+D",
            "Startups tecnológicas",
            "Empresas de robótica e IA",
            "Laboratorios de innovación",
            "Emprendimiento tecnológico"
        ]
    },
    
    "ingeniero_ambiental": {
        "nombre": "Ingeniero/a Ambiental",
        "indicadores_clave": {
            "ambiental": (75, 100),
            "sostenibilidad": (75, 100),
            "ingenieria": (65, 100)
        },
        "indicadores_secundarios": {
            "ciencias": (60, 100),
            "responsabilidad": (70, 100),
            "energia": (55, 100),
        },
        "carreras": [
            {
                "nombre": "Ingeniería Ambiental",
                "match_base": 95,
                "factores": {
                    "ambiental": 0.40,
                    "sostenibilidad": 0.30,
                    "ingenieria": 0.20,
                    "ciencias": 0.10
                }
            },
            {
                "nombre": "Ingeniería en Energías Renovables",
                "match_base": 92,
                "factores": {
                    "energia": 0.40,
                    "sostenibilidad": 0.30,
                    "tecnologia": 0.20,
                    "futuro": 0.10
                }
            },
            {
                "nombre": "Ciencias Ambientales",
                "match_base": 88,
                "factores": {
                    "ambiental": 0.35,
                    "ciencias": 0.35,
                    "investigacion": 0.20,
                    "naturaleza": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil muestra una fuerte conciencia ambiental combinada con habilidades técnicas. Te motiva crear soluciones sostenibles para los desafíos ambientales actuales.",
        "fortalezas_especificas": [
            "Conciencia ambiental y sostenibilidad",
            "Pensamiento sistémico",
            "Capacidad de integrar ciencia e ingeniería",
            "Visión de largo plazo"
        ],
        "areas_desarrollo": [
            "Política pública y regulación ambiental",
            "Tecnologías emergentes en energía",
            "Análisis de ciclo de vida",
            "Comunicación de impacto ambiental"
        ],
        "campo_laboral": [
            "Consultoras ambientales",
            "Empresas de energías renovables",
            "ONGs ambientales",
            "Sector público (medio ambiente)",
            "Certificación y auditoría ambiental"
        ]
    },
    "comunicador_creativo": {
        "nombre": "Comunicador/a Creativo/a",
        "indicadores_clave": {
            "comunicacion": (70, 100),
            "creatividad": (72, 100),
            "marketing": (65, 100)
        },
        "indicadores_secundarios": {
            "diseno": (60, 100),
            "ventas": (55, 100),
            "ux": (50, 100)
        },
        "carreras": [
            {
                "nombre": "Comunicación Social",
                "match_base": 92,
                "factores": {
                    "comunicacion": 0.40,
                    "creatividad": 0.30,
                    "marketing": 0.20,
                    "ventas": 0.10
                }
            },
            {
                "nombre": "Diseño Gráfico",
                "match_base": 90,
                "factores": {
                    "diseno": 0.40,
                    "creatividad": 0.35,
                    "ux": 0.15,
                    "tecnologia": 0.10
                }
            },
            {
                "nombre": "Publicidad y Marketing",
                "match_base": 94,
                "factores": {
                    "marketing": 0.40,
                    "creatividad": 0.30,
                    "comunicacion": 0.20,
                    "negocios": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil destaca en comunicación, creatividad y conexión con audiencias. Tienes habilidad para transmitir ideas de forma impactante y generar contenido que resuena con las personas.",
        "fortalezas_especificas": [
            "Creatividad aplicada a la comunicación",
            "Capacidad de storytelling y narrativa",
            "Comprensión de audiencias y tendencias",
            "Habilidades visuales y estéticas"
        ],
        "areas_desarrollo": [
            "Análisis de datos y métricas",
            "Herramientas digitales avanzadas",
            "Estrategia de negocios",
            "Gestión de proyectos"
        ],
        "campo_laboral": [
            "Agencias de publicidad y marketing",
            "Departamentos de comunicación corporativa",
            "Producción de contenido digital",
            "Diseño de marca y branding",
            "Consultoría creativa"
        ]
    },
    
    "analista_datos": {
        "nombre": "Analista de Datos",
        "indicadores_clave": {
            "datos": (75, 100),
            "analitico": (73, 100),
            "matematicas": (68, 100)
        },
        "indicadores_secundarios": {
            "estadistica": (65, 100),
            "programacion": (55, 100),
            "logica": (60, 100)
        },
        "carreras": [
            {
                "nombre": "Ciencia de Datos",
                "match_base": 95,
                "factores": {
                    "datos": 0.40,
                    "analitico": 0.30,
                    "programacion": 0.20,
                    "matematicas": 0.10
                }
            },
            {
                "nombre": "Estadística",
                "match_base": 92,
                "factores": {
                    "estadistica": 0.40,
                    "matematicas": 0.30,
                    "analitico": 0.20,
                    "datos": 0.10
                }
            },
            {
                "nombre": "Business Intelligence",
                "match_base": 88,
                "factores": {
                    "datos": 0.35,
                    "analitico": 0.30,
                    "negocios": 0.20,
                    "tecnologia": 0.15
                }
            }
        ],
        "descripcion": "Tu perfil combina fuerte capacidad analítica con habilidades matemáticas y pasión por los datos. Destacas en encontrar patrones, hacer proyecciones y convertir datos en insights accionables.",
        "fortalezas_especificas": [
            "Análisis cuantitativo avanzado",
            "Interpretación de datos complejos",
            "Pensamiento estadístico",
            "Visualización de información"
        ],
        "areas_desarrollo": [
            "Programación avanzada (Python, R)",
            "Machine Learning aplicado",
            "Comunicación de insights a no técnicos",
            "Big Data y herramientas cloud"
        ],
        "campo_laboral": [
            "Empresas de tecnología y fintech",
            "Consultoras de análisis",
            "Departamentos de Business Intelligence",
            "Investigación de mercados",
            "Gobierno y políticas públicas"
        ]
    },
    
    "gestor_proyectos": {
        "nombre": "Gestor/a de Proyectos",
        "indicadores_clave": {
            "organizacion": (72, 100),
            "liderazgo": (70, 100),
            "gestion": (70, 100)
        },
        "indicadores_secundarios": {
            "comunicacion": (65, 100),
            "estrategia": (60, 100),
            "negocios": (55, 100)
        },
        "carreras": [
            {
                "nombre": "Administración de Empresas",
                "match_base": 90,
                "factores": {
                    "gestion": 0.35,
                    "liderazgo": 0.30,
                    "negocios": 0.20,
                    "organizacion": 0.15
                }
            },
            {
                "nombre": "Ingeniería Industrial",
                "match_base": 88,
                "factores": {
                    "organizacion": 0.35,
                    "optimizacion": 0.30,
                    "gestion": 0.20,
                    "ingenieria": 0.15
                }
            },
            {
                "nombre": "Gestión de Proyectos",
                "match_base": 93,
                "factores": {
                    "gestion": 0.40,
                    "organizacion": 0.30,
                    "liderazgo": 0.20,
                    "estrategia": 0.10
                }
            }
        ],
        "descripcion": "Tu perfil destaca en organización, liderazgo y coordinación de recursos. Tienes la capacidad de planificar, ejecutar y entregar proyectos cumpliendo objetivos y plazos.",
        "fortalezas_especificas": [
            "Planificación estratégica",
            "Coordinación de equipos multidisciplinarios",
            "Gestión de recursos y presupuestos",
            "Resolución de conflictos"
        ],
        "areas_desarrollo": [
            "Metodologías ágiles (Scrum, Kanban)",
            "Herramientas de gestión de proyectos",
            "Habilidades técnicas específicas",
            "Negociación y manejo de stakeholders"
        ],
        "campo_laboral": [
            "Project Manager en empresas de cualquier sector",
            "Consultoría de gestión",
            "Coordinación de proyectos de desarrollo",
            "Startups y empresas tecnológicas",
            "ONGs y sector público"
        ]
    },
    "perfil_exploratorio": {
        "nombre": "Perfil en Exploración Vocacional",
        "indicadores_clave": {},
        "indicadores_secundarios": {},
        "carreras": [
            {"nombre": "Se recomienda realizar tests adicionales específicos", "afinidad": 0},
            {"nombre": "Consultar con orientador vocacional profesional", "afinidad": 0},
            {"nombre": "Explorar diferentes áreas mediante cursos introductorios", "afinidad": 0}
        ],
        "descripcion": "Tus respuestas no muestran una orientación clara hacia un perfil específico. Esto puede deberse a que aún estás explorando tus intereses o las respuestas presentan inconsistencias. Te recomendamos reflexionar más sobre las actividades que realmente disfrutas.",
        "fortalezas_especificas": [
            "Apertura a múltiples opciones profesionales",
            "Flexibilidad en intereses vocacionales",
            "Oportunidad de descubrir nuevas pasiones",
            "Capacidad de exploración sin límites preconcebidos"
        ],
        "areas_desarrollo": [
            "Definir intereses más específicos",
            "Realizar tests vocacionales especializados por área",
            "Probar actividades prácticas en diferentes campos",
            "Conversar con profesionales de distintas carreras",
            "Reflexionar sobre experiencias pasadas que te motivaron"
        ],
        "campo_laboral": []
    }
}

# ================================
# FUNCIONES DE CÁLCULO
# ================================

def calcular_puntajes_dimensiones(respuestas: dict) -> Dict[str, float]:
    """
    Calcula puntajes normalizados para cada dimensión vocacional
    basándose en el mapeo de preguntas
    """
    dimensiones = {}
    conteos = {}
    
    for pregunta, respuesta in respuestas.items():
        num_pregunta = int(pregunta.split("_")[1])
        puntos = PUNTUACION_VALORES.get(respuesta, 3)  # 1-5
        
        if num_pregunta in MAPEO_PREGUNTAS_GENERAL:
            pesos = MAPEO_PREGUNTAS_GENERAL[num_pregunta]
            
            for dimension, peso in pesos.items():
                if dimension not in dimensiones:
                    dimensiones[dimension] = 0
                    conteos[dimension] = 0
                
                dimensiones[dimension] += puntos * peso
                conteos[dimension] += peso
    
    # Normalizar a escala 0-100
    puntajes_normalizados = {}
    for dimension, suma in dimensiones.items():
        if conteos[dimension] > 0:
            promedio = suma / conteos[dimension]  # 1-5
            puntajes_normalizados[dimension] = round((promedio / 5) * 100, 2)
    
    return puntajes_normalizados

def detectar_contradicciones_dimensiones(puntajes: Dict[str, float]) -> int:
    """
    Detecta contradicciones graves en las dimensiones del usuario
    Retorna el número de contradicciones encontradas
    """
    contradicciones = 0
    
    # Definir pares de dimensiones que deberían ser consistentes
    pares_relacionados = [
        ("programacion", "tecnologia", 25),
        ("programacion", "desarrollo", 20),
        ("ciencias", "investigacion", 25),
        ("biologia", "ciencias", 20),
        ("quimica", "ciencias", 20),
        ("fisica", "ciencias", 20),
        ("ingenieria", "matematicas", 30),
        ("finanzas", "negocios", 25),
        ("marketing", "comunicacion", 25),
        ("liderazgo", "gestion", 20),
        ("datos", "analitico", 25),
        ("ia", "programacion", 30),
        ("ux", "diseno", 20),
        ("ambiental", "sostenibilidad", 15),
    ]
    
    for dim1, dim2, umbral in pares_relacionados:
        val1 = puntajes.get(dim1, 0)
        val2 = puntajes.get(dim2, 0)
        
        if val1 > 30 or val2 > 30:
            diferencia = abs(val1 - val2)
            
            if diferencia > umbral:
                if (val1 > 70 and val2 < 40) or (val2 > 70 and val1 < 40):
                    contradicciones += 1
    
    return contradicciones

def identificar_perfil_optimo(puntajes: Dict[str, float]) -> Tuple[str, float]:
    """
    Identifica el perfil con VALIDACIÓN ESTRICTA + DETECTOR DE CONTRADICCIONES
    """
    # Detectar contradicciones graves
    contradicciones = detectar_contradicciones_dimensiones(puntajes)
    if contradicciones > 3:
        return "perfil_exploratorio", 0
    
    scores_perfiles = {}
    
    for perfil_id, perfil in PERFILES_DETALLADOS.items():
        if not perfil.get("indicadores_clave") or len(perfil["indicadores_clave"]) == 0:
            scores_perfiles[perfil_id] = 0
            continue
        
        cumple_requisitos_minimos = True
        score_indicadores_clave = 0
        indicadores_cumplidos = 0
        
        for indicador, (min_val, max_val) in perfil["indicadores_clave"].items():
            puntaje_usuario = puntajes.get(indicador, 0)
            
            if puntaje_usuario < min_val * 0.7:
                cumple_requisitos_minimos = False
                break
            
            if min_val <= puntaje_usuario <= max_val:
                score_indicadores_clave += 100
                indicadores_cumplidos += 1
            elif puntaje_usuario < min_val:
                diferencia = min_val - puntaje_usuario
                score_indicadores_clave += max(0, 100 - (diferencia * 2.5))
            else:
                score_indicadores_clave += 88
                indicadores_cumplidos += 1
        
        if not cumple_requisitos_minimos:
            scores_perfiles[perfil_id] = 0
            continue
        
        porcentaje_cumplimiento = (indicadores_cumplidos / len(perfil["indicadores_clave"])) * 100
        if porcentaje_cumplimiento < 70:
            scores_perfiles[perfil_id] = 0
            continue
        
        # Evaluar indicadores secundarios
        score_secundarios = 0
        for indicador, (min_val, max_val) in perfil.get("indicadores_secundarios", {}).items():
            puntaje_usuario = puntajes.get(indicador, 0)
            
            if min_val <= puntaje_usuario <= max_val:
                score_secundarios += 55
            elif puntaje_usuario >= min_val * 0.8:
                score_secundarios += 35
        
        # Calcular score normalizado
        total_posible = (
            len(perfil["indicadores_clave"]) * 100 +
            len(perfil.get("indicadores_secundarios", {})) * 55
        )
        
        if total_posible > 0:
            score_final = ((score_indicadores_clave + score_secundarios) / total_posible) * 100
            
            dimensiones_fuertes = sum(1 for v in puntajes.values() if v >= 68)
            if dimensiones_fuertes < 3:
                score_final *= 0.82
            elif dimensiones_fuertes >= 6:
                score_final *= 1.05
            
            if contradicciones > 0:
                score_final *= (1 - (contradicciones * 0.08))
            
            scores_perfiles[perfil_id] = round(min(score_final, 100), 2)
        else:
            scores_perfiles[perfil_id] = 0
    
    if not scores_perfiles or max(scores_perfiles.values()) < 50:
        return "perfil_exploratorio", max(scores_perfiles.values(), default=0)
    
    mejor_perfil = max(scores_perfiles, key=scores_perfiles.get)
    return mejor_perfil, scores_perfiles[mejor_perfil]

def calcular_match_carreras(perfil_data: dict, puntajes: Dict[str, float]) -> List[dict]:
    """
    Calcula match con VALIDACIÓN REALISTA de coherencia
    """
    carreras_con_match = []
    
    for carrera in perfil_data["carreras"]:
        match_base = carrera["match_base"]
        
        factores_cumplidos = 0
        factores_fuertes = 0
        suma_ajustes = 0
        
        for factor, peso in carrera["factores"].items():
            puntaje_factor = puntajes.get(factor, 0)
            
            if puntaje_factor >= 45:
                factores_cumplidos += 1
                
                if puntaje_factor >= 70:
                    factores_fuertes += 1
                
                ajuste = ((puntaje_factor - 50) / 50) * peso * 8
                suma_ajustes += ajuste
            else:
                suma_ajustes -= peso * 5
        
        porcentaje_cumplimiento = (factores_cumplidos / len(carrera["factores"])) * 100
        porcentaje_fuertes = (factores_fuertes / len(carrera["factores"])) * 100
        
        if porcentaje_cumplimiento < 50:
            match_calculado = match_base * 0.6
        elif porcentaje_cumplimiento < 75:
            match_calculado = match_base * 0.85 + suma_ajustes
        else:
            match_calculado = match_base + suma_ajustes
            
            if porcentaje_fuertes >= 50:
                match_calculado *= 1.05
        
        match_calculado = max(35, min(97, match_calculado))
        
        carreras_con_match.append({
            "nombre": carrera["nombre"],
            "afinidad": round(match_calculado, 2)
        })
    
    return sorted(carreras_con_match, key=lambda x: x["afinidad"], reverse=True)

def calcular_resultados_test(tipo_test: str, respuestas: dict) -> dict:
    """
    Función principal mejorada de cálculo de resultados
    """
    puntuacion_total = sum(PUNTUACION_VALORES.get(v, 0) for v in respuestas.values())
    total_preguntas = len(respuestas)
    puntuacion_maxima = total_preguntas * 5
    porcentaje_global = round((puntuacion_total / puntuacion_maxima) * 100, 2)
    
    puntajes_dimensiones = calcular_puntajes_dimensiones(respuestas)
    
    perfil_id, score_ajuste = identificar_perfil_optimo(puntajes_dimensiones)
    
    if perfil_id == "perfil_exploratorio":
        return {
            "puntuacion_total": puntuacion_total,
            "puntuacion_maxima": puntuacion_maxima,
            "porcentaje_afinidad": score_ajuste,
            "porcentaje_global": porcentaje_global,
            "nivel": "Exploratoria",
            "mensaje": "Tus respuestas indican que aún estás explorando tus intereses vocacionales. "
                    "Te recomendamos realizar tests adicionales específicos o reflexionar más sobre "
                    "las actividades que realmente te apasionan.",
            "area_principal": "En Exploración",
            "carreras_recomendadas": [
                {"nombre": "Realiza tests específicos por área", "afinidad": 0},
                {"nombre": "Consulta con un orientador vocacional", "afinidad": 0}
            ],
            "fortalezas": [
                "Apertura a explorar diferentes opciones",
                "Flexibilidad en intereses",
                "Oportunidad de descubrir nuevas pasiones"
            ],
            "areas_desarrollo": [
                "Definir intereses más específicos",
                "Probar actividades prácticas en diferentes áreas",
                "Realizar tests vocacionales especializados"
            ],
            "campo_laboral": [],
            "puntajes_dimensiones": puntajes_dimensiones,
            "perfil_identificado": "exploratorio",
            "score_ajuste": score_ajuste
        }
    
    perfil_data = PERFILES_DETALLADOS[perfil_id]
    carreras_recomendadas = calcular_match_carreras(perfil_data, puntajes_dimensiones)
    
    if score_ajuste >= 75:
        nivel = "Excelente"
        claridad = "muy clara"
    elif score_ajuste >= 60:
        nivel = "Buena"
        claridad = "clara"
    elif score_ajuste >= 45:
        nivel = "Moderada"
        claridad = "moderada"
    else:
        nivel = "Exploratoria"
        claridad = "en exploración"
    
    mensaje = f"{perfil_data['descripcion']}\n\nTu orientación vocacional es {claridad} hacia este perfil (ajuste: {score_ajuste}%). "
    
    if score_ajuste >= 70:
        mensaje += "Las carreras recomendadas tienen un alto nivel de compatibilidad con tus intereses y habilidades."
    elif score_ajuste >= 50:
        mensaje += "Te recomendamos explorar más sobre las carreras sugeridas para validar tu interés."
    else:
        mensaje += "Considera tomar tests adicionales o explorar otras áreas para clarificar tu vocación."
    
    return {
        "puntuacion_total": puntuacion_total,
        "puntuacion_maxima": puntuacion_maxima,
        "porcentaje_afinidad": score_ajuste,
        "porcentaje_global": porcentaje_global,
        "nivel": nivel,
        "mensaje": mensaje,
        "area_principal": perfil_data["nombre"],
        "carreras_recomendadas": carreras_recomendadas[:5],
        "fortalezas": perfil_data["fortalezas_especificas"],
        "areas_desarrollo": perfil_data["areas_desarrollo"],
        "campo_laboral": perfil_data.get("campo_laboral", []),
        "puntajes_dimensiones": puntajes_dimensiones,
        "perfil_identificado": perfil_id,
        "score_ajuste": score_ajuste
    }