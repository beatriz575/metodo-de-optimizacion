from manim import *
import random
import numpy as np

class Explicacion_Paper_PSO_Optuna(Scene):
    def construct(self):
        # ESCENA 1: Título y Contexto del Paper
        self.escena_1_titulo_paper()
        self.clear()
        
        # ESCENA 2: Problema de Investigación
        self.escena_2_problema_investigacion()
        self.clear()
        
        # ESCENA 3: Metodología del Estudio
        self.escena_3_metodologia()
        self.clear()
        
        # ESCENA 4: Algoritmos Comparados
        self.escena_4_algoritmos()
        self.clear()
        
        # ESCENA 5: Resultados Principales
        self.escena_5_resultados()
        self.clear()
        
        # ESCENA 6: Análisis Territorial
        self.escena_6_analisis_territorial()
        self.clear()
        
        # ESCENA 7: Discusión y Contribuciones
        self.escena_7_discusion()
        self.clear()
        
        # ESCENA 8: Conclusiones del Paper
        self.escena_8_conclusiones()
    
    def escena_1_titulo_paper(self):
        # Título del paper
        titulo = VGroup(
            Text("Análisis Comparativo de PSO y Optuna", font_size=28, color=BLUE),
            Text("para Predicción del Rendimiento Académico", font_size=24, color=WHITE),
            Text("en Educación Básica Peruana", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.15)
        titulo.to_edge(UP, buff=0.3)
        
        # Autor y afiliación
        autor = VGroup(
            Text("Beatriz Umiña Machaca", font_size=18, color=YELLOW),
            Text("Universidad Nacional del Altiplano Puno", font_size=14, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        autor.next_to(titulo, DOWN, buff=0.3)
        
        # Resumen ejecutivo del paper
        resumen = VGroup(
            Text("RESUMEN DE LA INVESTIGACIÓN:", font_size=16, color=GREEN),
            Text("• Dataset: 7,839 estudiantes de 6º grado", font_size=12),
            Text("• Fuente: Evaluación Muestral 2022 MINEDU", font_size=12),
            Text("• Cobertura: 25 regiones del Perú", font_size=12),
            Text("• Objetivo: Comparar PSO vs Optuna para predicción", font_size=12),
            Text("• Modelo: Random Forest con validación cruzada", font_size=12),
            Text("• Métricas: MSE, R², eficiencia computacional", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        resumen.move_to(UP * 0.2)
        
        # Contribución principal
        contribucion = VGroup(
            Text("CONTRIBUCIÓN PRINCIPAL:", font_size=16, color=ORANGE),
            Text("Primera comparación sistemática entre PSO y Optuna", font_size=14),
            Text("en el contexto educativo peruano, demostrando", font_size=14),
            Text("equivalencia estadística con diferencias en eficiencia", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        contribucion.move_to(DOWN * 1.2)
        
        # Importancia del estudio
        importancia = VGroup(
            Text("RELEVANCIA:", font_size=16, color=BLUE),
            Text("• Herramientas para sistemas de alerta temprana", font_size=12),
            Text("• Optimización de recursos educativos limitados", font_size=12),
            Text("• Identificación de brechas territoriales críticas", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        importancia.to_edge(DOWN, buff=0.3)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(autor))
        self.wait(1)
        self.play(Write(resumen))
        self.wait(2)
        self.play(Write(contribucion))
        self.wait(1)
        self.play(Write(importancia))
        self.wait(3)
    
    def escena_2_problema_investigacion(self):
        # Título
        titulo = Text("Problema de Investigación", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Contexto educativo peruano
        contexto = VGroup(
            Text("CONTEXTO EDUCATIVO PERUANO:", font_size=20, color=RED),
            Text("• Brechas socioeconómicas significativas", font_size=14),
            Text("• Heterogeneidades regionales extremas", font_size=14),
            Text("• Disparidades > 120 puntos entre regiones", font_size=14),
            Text("• Necesidad de modelos predictivos robustos", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        contexto.move_to(UP * 2)
        
        # Pregunta de investigación del paper
        pregunta = VGroup(
            Text("PREGUNTA DE INVESTIGACIÓN:", font_size=18, color=GREEN),
            Text("¿Cuál es la efectividad comparativa de PSO", font_size=14),
            Text("frente a Optuna en términos de precisión", font_size=14),
            Text("predictiva y eficiencia computacional para", font_size=14),
            Text("predicción del rendimiento académico?", font_size=14, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        pregunta.move_to(DOWN * 0.4)
        
        # Justificación
        justificacion = VGroup(
            Text("JUSTIFICACIÓN DEL ESTUDIO:", font_size=16, color=ORANGE),
            Text("• Instituciones educativas tienen recursos limitados", font_size=12),
            Text("• Necesidad de herramientas accesibles y eficientes", font_size=12),
            Text("• PSO: Simplicidad vs Optuna: Sofisticación", font_size=12),
            Text("• Falta de comparaciones en contexto latinoamericano", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        justificacion.move_to(DOWN * 1.2)
        
        # Hipótesis
        hipotesis = VGroup(
            Text("HIPÓTESIS:", font_size=16, color=BLUE),
            Text("Ambos métodos tendrán rendimiento predictivo similar", font_size=12),
            Text("pero diferirán en eficiencia computacional", font_size=12, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        hipotesis.to_edge(DOWN, buff=0.4)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(contexto))
        self.wait(2)
        self.play(Write(pregunta))
        self.wait(2)
        self.play(Write(justificacion))
        self.wait(1)
        self.play(Write(hipotesis))
        self.wait(3)
    
    def escena_3_metodologia(self):
        # Título
        titulo = Text("Metodología del Estudio", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Datos utilizados
        datos = VGroup(
            Text("CONJUNTO DE DATOS:", font_size=18, color=GREEN),
            Text("• Fuente: Evaluación Muestral 2022 MINEDU", font_size=12),
            Text("• Muestra: 7,839 estudiantes de 6º grado", font_size=12),
            Text("• Cobertura: 25 regiones del Perú", font_size=12),
            Text("• Variables objetivo: Puntajes lectura y matemática", font_size=12),
            Text("• Escala: 0-1000 puntos", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        datos.move_to(LEFT * 3 + UP * 0.8)
        
        # Variables predictoras
        variables = VGroup(
            Text("VARIABLES PREDICTORAS:", font_size=18, color=ORANGE),
            Text("• Sexo (Hombre/Mujer)", font_size=12),
            Text("• Lengua materna (4 categorías)", font_size=12),
            Text("• Gestión (Estatal/No estatal)", font_size=12),
            Text("• Zona (Rural/Urbana)", font_size=12),
            Text("• Nivel socioeconómico (4 niveles)", font_size=12),
            Text("• Departamento (25 categorías)", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        variables.move_to(RIGHT * 3 + UP * 0.8)
        
        # Modelo y configuración
        modelo = VGroup(
            Text("CONFIGURACIÓN DEL MODELO:", font_size=18, color=BLUE),
            Text("• Algoritmo base: Random Forest", font_size=12),
            Text("• Hiperparámetros optimizados:", font_size=12),
            Text("  - n_estimators: [10, 200]", font_size=10),
            Text("  - max_depth: [3, 20]", font_size=10),
            Text("• Validación cruzada: 5-fold", font_size=12),
            Text("• Métrica objetivo: MSE", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        modelo.move_to(LEFT * 3 + DOWN * 1.2)
        
        # Configuración de algoritmos
        config = VGroup(
            Text("CONFIGURACIÓN ALGORITMOS:", font_size=18, color=YELLOW),
            Text("PSO:", font_size=14, color=BLUE),
            Text("• 20 partículas", font_size=10),
            Text("• 50 iteraciones máximas", font_size=10),
            Text("• Librería: pyswarm", font_size=10),
            Text("Optuna:", font_size=14, color=ORANGE),
            Text("• Algoritmo TPE", font_size=10),
            Text("• 50 evaluaciones", font_size=10),
            Text("• Poda automática", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        config.move_to(RIGHT * 3 + DOWN * 1.2)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(datos))
        self.play(Write(variables))
        self.wait(2)
        self.play(Write(modelo))
        self.play(Write(config))
        self.wait(3)
    
    def escena_4_algoritmos(self):
        # Título
        titulo = Text("Algoritmos Comparados", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Línea divisoria
        linea = Line(UP * 1.5, DOWN * 2.5, color=WHITE)
        
        # PSO - Lado izquierdo
        pso_titulo = Text("PSO", font_size=24, color=BLUE)
        pso_titulo.move_to(LEFT * 3.5 + UP * 1.2)
        
        pso_desc = VGroup(
            Text("Optimización por Enjambre", font_size=12, color=BLUE),
            Text("de Partículas", font_size=12, color=BLUE)
        ).arrange(DOWN, buff=0.05)
        pso_desc.next_to(pso_titulo, DOWN, buff=0.1)
        
        pso_caracteristicas = VGroup(
            Text("CARACTERÍSTICAS:", font_size=12, color=YELLOW),
            Text("• Inspirado en comportamiento", font_size=10),
            Text("  de enjambres naturales", font_size=10),
            Text("• Búsqueda global estocástica", font_size=10),
            Text("• Simple de implementar", font_size=10, color=GREEN),
            Text("• No requiere derivadas", font_size=10),
            Text("• Paralelizable", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pso_caracteristicas.next_to(pso_desc, DOWN, buff=0.2)
        
        # Funcionamiento PSO
        pso_func = VGroup(
            Text("FUNCIONAMIENTO:", font_size=12, color=ORANGE),
            Text("1. Inicialización aleatoria", font_size=10),
            Text("2. Evaluación fitness", font_size=10),
            Text("3. Actualización pbest/gbest", font_size=10),
            Text("4. Cálculo nueva velocidad", font_size=10),
            Text("5. Actualización posición", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        pso_func.next_to(pso_caracteristicas, DOWN, buff=0.15)
        
        # Optuna - Lado derecho
        optuna_titulo = Text("Optuna", font_size=24, color=ORANGE)
        optuna_titulo.move_to(RIGHT * 3.5 + UP * 1.2)
        
        optuna_desc = VGroup(
            Text("Optimización Bayesiana", font_size=12, color=ORANGE),
            Text("(Tree-structured Parzen Estimator)", font_size=10, color=ORANGE)
        ).arrange(DOWN, buff=0.05)
        optuna_desc.next_to(optuna_titulo, DOWN, buff=0.1)
        
        optuna_caracteristicas = VGroup(
            Text("CARACTERÍSTICAS:", font_size=12, color=YELLOW),
            Text("• Usa información histórica", font_size=10),
            Text("• Convergencia más rápida", font_size=10),
            Text("• Poda automática", font_size=10, color=GREEN),
            Text("• Modelo probabilístico", font_size=10),
            Text("• Más sofisticado", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        optuna_caracteristicas.next_to(optuna_desc, DOWN, buff=0.2)
        
        # Funcionamiento Optuna
        optuna_func = VGroup(
            Text("FUNCIONAMIENTO:", font_size=12, color=ORANGE),
            Text("1. Modelo probabilístico", font_size=10),
            Text("2. Evaluación candidatos", font_size=10),
            Text("3. Construcción TPE", font_size=10),
            Text("4. Selección siguiente punto", font_size=10),
            Text("5. Actualización modelo", font_size=10)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        optuna_func.next_to(optuna_caracteristicas, DOWN, buff=0.15)
        
        # Comparación directa
        comparacion = VGroup(
            Text("COMPARACIÓN CLAVE:", font_size=16, color=YELLOW),
            Text("PSO: Simplicidad y robustez", font_size=12, color=BLUE),
            Text("Optuna: Eficiencia y sofisticación", font_size=12, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        comparacion.to_edge(DOWN, buff=0.2)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Create(linea))
        self.play(Write(pso_titulo), Write(optuna_titulo))
        self.play(Write(pso_desc), Write(optuna_desc))
        self.wait(1)
        self.play(Write(pso_caracteristicas), Write(optuna_caracteristicas))
        self.wait(1)
        self.play(Write(pso_func), Write(optuna_func))
        self.wait(1)
        self.play(Write(comparacion))
        self.wait(3)
    
    def escena_5_resultados(self):
        # Título
        titulo = Text("Resultados Principales del Paper", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Hallazgo principal
        hallazgo = VGroup(
            Text("HALLAZGO PRINCIPAL:", font_size=20, color=GREEN),
            Text("EQUIVALENCIA ESTADÍSTICA", font_size=18, color=YELLOW),
            Text("entre PSO y Optuna", font_size=16)
        ).arrange(DOWN, buff=0.1)
        hallazgo.move_to(UP * 1.5)
        
        # Resultados en lectura
        lectura = VGroup(
            Text("LECTURA:", font_size=16, color=BLUE),
            Text("                PSO        Optuna", font_size=12, color=YELLOW),
            Text("MSE:         4872±108    4872±106", font_size=12),
            Text("R²:          0.203±0.016 0.203±0.016", font_size=12),
            Text("Árboles:     116         92", font_size=12, color=GREEN),
            Text("p-value:     0.940 (no significativo)", font_size=12, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lectura.move_to(LEFT * 3 + UP * 0.2)
        
        # Resultados en matemática
        matematica = VGroup(
            Text("MATEMÁTICA:", font_size=16, color=ORANGE),
            Text("                PSO        Optuna", font_size=12, color=YELLOW),
            Text("MSE:         6650±261    6651±261", font_size=12),
            Text("R²:          0.154±0.021 0.154±0.021", font_size=12),
            Text("Árboles:     180         156", font_size=12, color=GREEN),
            Text("p-value:     0.821 (no significativo)", font_size=12, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        matematica.move_to(RIGHT * 3 + UP * 0.2)
        
        # Interpretación estadística
        interpretacion = VGroup(
            Text("INTERPRETACIÓN ESTADÍSTICA:", font_size=16, color=BLUE),
            Text("• p-values > 0.05 → No hay diferencias significativas", font_size=12),
            Text("• MSE y R² prácticamente idénticos", font_size=12),
            Text("• Optuna usa consistentemente menos árboles", font_size=12, color=GREEN),
            Text("• Ambos métodos son estadísticamente equivalentes", font_size=12, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        interpretacion.move_to(DOWN * 1)
        
        # Conclusión de resultados
        conclusion = VGroup(
            Text("CONCLUSIÓN DE RESULTADOS:", font_size=16, color=ORANGE),
            Text("Rendimiento predictivo equivalente", font_size=14),
            Text("Optuna más eficiente computacionalmente", font_size=14, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        conclusion.to_edge(DOWN, buff=0.3)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(hallazgo))
        self.wait(2)
        self.play(Write(lectura))
        self.play(Write(matematica))
        self.wait(2)
        self.play(Write(interpretacion))
        self.wait(1)
        self.play(Write(conclusion))
        self.wait(3)
    
    def escena_6_analisis_territorial(self):
        # Título
        titulo = Text("Análisis Territorial del Paper", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Categorización territorial
        categorizacion = VGroup(
            Text("CATEGORIZACIÓN TERRITORIAL:", font_size=18, color=GREEN),
            Text("Basada en cuartiles de puntaje promedio en lectura", font_size=12)
        ).arrange(DOWN, buff=0.1)
        categorizacion.move_to(UP * 1.5)
        
        # Departamentos por nivel
        nivel_optimo = VGroup(
            Text("NIVEL ÓPTIMO (Q4):", font_size=14, color=GREEN),
            Text("• Callao: 575.29 puntos", font_size=12),
            Text("• Tacna: 565.47 puntos", font_size=12),
            Text("• Arequipa: 563.16 puntos", font_size=12),
            Text("• Lima: 561.29 puntos", font_size=12),
            Text("• Moquegua: 559.73 puntos", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        nivel_optimo.move_to(LEFT * 3 + UP * 0.5)
        
        nivel_critico = VGroup(
            Text("NIVEL CRÍTICO (Q1):", font_size=14, color=RED),
            Text("• Loreto: 453.50 puntos", font_size=12),
            Text("• San Martín: 490.45 puntos", font_size=12),
            Text("• Huánuco: 497.41 puntos", font_size=12),
            Text("• Cajamarca: 498.27 puntos", font_size=12),
            Text("• Amazonas: 509.82 puntos", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        nivel_critico.move_to(RIGHT * 3 + UP * 0.5)
        
        # Brecha territorial
        brecha = VGroup(
            Text("BRECHA TERRITORIAL EXTREMA:", font_size=16, color=ORANGE),
            Text("121.79 puntos entre Callao y Loreto", font_size=14, color=YELLOW),
            Text("Equivalente a 1.7 años de escolaridad", font_size=14, color=YELLOW)
        ).arrange(DOWN, buff=0.1)
        brecha.move_to(DOWN * 0.5)
        
        # Patrones identificados
        patrones = VGroup(
            Text("PATRONES GEOGRÁFICOS IDENTIFICADOS:", font_size=14, color=BLUE),
            Text("• Corredor costero: Rendimientos óptimos", font_size=12),
            Text("• Región andina central: Rendimientos medios", font_size=12),
            Text("• Región amazónica: Rendimientos críticos", font_size=12, color=RED),
            Text("• Factores: Urbanización, desarrollo económico, acceso", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        patrones.move_to(DOWN * 1.5)
        
        # Implicaciones
        implicaciones = VGroup(
            Text("IMPLICACIONES PARA POLÍTICA EDUCATIVA:", font_size=14, color=YELLOW),
            Text("Necesidad urgente de intervenciones diferenciadas", font_size=12),
            Text("Priorización de regiones amazónicas y andinas", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        implicaciones.to_edge(DOWN, buff=0.2)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(categorizacion))
        self.wait(1)
        self.play(Write(nivel_optimo))
        self.play(Write(nivel_critico))
        self.wait(2)
        self.play(Write(brecha))
        self.wait(1)
        self.play(Write(patrones))
        self.wait(1)
        self.play(Write(implicaciones))
        self.wait(3)
    
    def escena_7_discusion(self):
        # Título
        titulo = Text("Discusión y Contribuciones", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Discusión principal
        discusion = VGroup(
            Text("DISCUSIÓN PRINCIPAL:", font_size=18, color=GREEN),
            Text("• Equivalencia estadística contrasta con literatura", font_size=12),
            Text("  que sugiere superioridad de métodos bayesianos", font_size=12),
            Text("• Atribuible a espacio de búsqueda bidimensional", font_size=12),
            Text("• R² moderado refleja naturaleza multifactorial", font_size=12),
            Text("  del rendimiento académico", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        discusion.move_to(UP * 1)
        
        # Hallazgos territoriales
        territoriales = VGroup(
            Text("HALLAZGOS TERRITORIALES:", font_size=16, color=ORANGE),
            Text("• Brecha 121.79 puntos excede reportes UNESCO", font_size=12),
            Text("• Diferencia gestión privada vs estatal: 47.19 pts", font_size=12),
            Text("• Brecha lenguas: 90 pts (castellano vs originarias)", font_size=12),
            Text("• Evidencia desigualdades estructurales profundas", font_size=12, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        territoriales.move_to(DOWN * 0.2)
        
        # Contribuciones científicas
        contribuciones = VGroup(
            Text("CONTRIBUCIONES CIENTÍFICAS:", font_size=16, color=BLUE),
            Text("• Primera comparación PSO vs Optuna en educación", font_size=12),
            Text("• Evidencia empírica de equivalencia metodológica", font_size=12),
            Text("• Framework replicable para otros contextos", font_size=12),
            Text("• Identificación de brechas críticas territoriales", font_size=12),
            Text("• Recomendaciones para recursos limitados", font_size=12, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        contribuciones.move_to(DOWN * 1.3)
        
        # Limitaciones
        limitaciones = VGroup(
            Text("LIMITACIONES DEL ESTUDIO:", font_size=14, color=YELLOW),
            Text("• Ausencia de variables de proceso educativo", font_size=11),
            Text("• Diseño transversal (no longitudinal)", font_size=11),
            Text("• Enfoque en variables sociodemográficas", font_size=11)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        limitaciones.to_edge(DOWN, buff=0.2)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(discusion))
        self.wait(2)
        self.play(Write(territoriales))
        self.wait(2)
        self.play(Write(contribuciones))
        self.wait(1)
        self.play(Write(limitaciones))
        self.wait(3)
    
    def escena_8_conclusiones(self):
        # Título
        titulo = Text("Conclusiones del Paper", font_size=32, color=BLUE)
        titulo.to_edge(UP, buff=0.3)
        
        # Conclusión principal
        conclusion_principal = VGroup(
            Text("CONCLUSIÓN PRINCIPAL:", font_size=20, color=GREEN),
            Text("PSO y Optuna son metodológicamente equivalentes", font_size=16),
            Text("para optimización en contextos educativos", font_size=16, color=YELLOW)
        ).arrange(DOWN, buff=0.1)
        conclusion_principal.move_to(UP * 1.5)
        
        # Resultados específicos
        resultados = VGroup(
            Text("RESULTADOS ESPECÍFICOS:", font_size=16, color=BLUE),
            Text("• Equivalencia estadística confirmada (p > 0.05)", font_size=12),
            Text("• Optuna 20% más eficiente computacionalmente", font_size=12, color=GREEN),
            Text("• PSO ofrece mayor simplicidad de implementación", font_size=12, color=GREEN),
            Text("• Poder predictivo moderado (R² = 0.20 y 0.15)", font_size=12),
            Text("• Brechas territoriales críticas identificadas", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        resultados.move_to(UP * 0.5)
        
        # Recomendaciones prácticas
        recomendaciones = VGroup(
            Text("RECOMENDACIONES PRÁCTICAS:", font_size=16, color=ORANGE),
            Text("• Recursos limitados → Usar PSO", font_size=12),
            Text("• Máxima eficiencia → Usar Optuna", font_size=12),
            Text("• Ambos garantizan resultados equivalentes", font_size=12, color=YELLOW),
            Text("• Implementar sistemas de alerta temprana", font_size=12),
            Text("• Políticas territorialmente diferenciadas", font_size=12)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        recomendaciones.move_to(DOWN * 0.5)
        
        # Impacto esperado
        impacto = VGroup(
            Text("IMPACTO ESPERADO:", font_size=16, color=BLUE),
            Text("• Herramientas para instituciones con recursos limitados", font_size=12),
            Text("• Optimización de inversión educativa", font_size=12),
            Text("• Reducción de brechas territoriales", font_size=12),
            Text("• Mejora en toma de decisiones basada en evidencia", font_size=12, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        impacto.move_to(DOWN * 1.4)
        
        # Mensaje final
        mensaje_final = VGroup(
            Text("MENSAJE FINAL:", font_size=16, color=YELLOW),
            Text("El estudio demuestra que la selección algorítmica", font_size=12),
            Text("puede basarse en consideraciones prácticas", font_size=12),
            Text("más que en superioridad teórica", font_size=12, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        mensaje_final.to_edge(DOWN, buff=0.2)
        
        # Animaciones
        self.play(Write(titulo))
        self.play(Write(conclusion_principal))
        self.wait(2)
        self.play(Write(resultados))
        self.wait(2)
        self.play(Write(recomendaciones))
        self.wait(2)
        self.play(Write(impacto))
        self.wait(1)
        self.play(Write(mensaje_final))
        self.wait(3)
        
        # Agradecimiento final
        agradecimiento = Text("¡Gracias por su atención!", font_size=24, color=BLUE)
        self.play(Transform(mensaje_final, agradecimiento))
        self.wait(3)

# Para renderizar el video completo:
# manim -pql video_paper.py Explicacion_Paper_PSO_Optuna

# Para renderizar escenas específicas:
# manim -pql video_paper.py Explicacion_Paper_PSO_Optuna --scene_names=escena_5_resultados