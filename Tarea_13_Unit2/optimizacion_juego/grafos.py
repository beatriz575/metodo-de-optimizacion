import tkinter as tk
from tkinter import messagebox, ttk
import random
from collections import Counter
import networkx as nx
from itertools import combinations

# Configuración del juego
DULCES = ["🍋 Limón", "🍐 Pera", "🥚 Huevo"]
DULCES_SIMPLES = ["limon", "pera", "huevo"]
EMOJIS = {"limon": "🍋", "pera": "🍐", "huevo": "🥚"}
COLORES = {
    "limon": "#FFE135",
    "pera": "#90EE90", 
    "huevo": "#F0E68C"
}

class JuegoSobrevivientes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("🎯 Juego de Sobrevivientes - Optimizado")
        self.ventana.configure(bg="#f0f8ff")
        self.ventana.geometry("1000x800")
        
        # Variables del juego
        self.estudiantes_n1 = []
        self.estudiantes_n2 = []
        self.estadisticas = {"nivel1": [], "nivel2": []}
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Título principal
        titulo = tk.Label(
            self.ventana, 
            text="🎮 SIMULADOR DE SOBREVIVIENTES OPTIMIZADO", 
            font=("Arial", 20, "bold"), 
            bg="#f0f8ff",
            fg="#2c3e50"
        )
        titulo.pack(pady=15)
        
        # Instrucciones
        instrucciones = tk.Label(
            self.ventana,
            text="Para sobrevivir necesitas: 🍋 Limón + 🍐 Pera + 🥚 Huevo = 🍭 Chupetín + 🎁 Comodín",
            font=("Arial", 12),
            bg="#f0f8ff",
            fg="#34495e"
        )
        instrucciones.pack(pady=(0, 10))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Crear pestañas
        self.crear_nivel1()
        self.crear_nivel2()
        self.crear_estadisticas()
        
    def crear_nivel1(self):
        # Frame para Nivel 1
        frame_n1 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(frame_n1, text="🔹 Nivel 1: Cooperación Individual")
        
        # Configuración
        config_frame = tk.LabelFrame(frame_n1, text="⚙️ Configuración", font=("Arial", 12, "bold"), bg="white")
        config_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(config_frame, text="Número de estudiantes:", font=("Arial", 11), bg="white").pack(side="left", padx=5)
        self.entry_n1 = tk.Entry(config_frame, width=8, font=("Arial", 12), justify="center")
        self.entry_n1.pack(side="left", padx=5)
        self.entry_n1.insert(0, "6")
        
        tk.Button(config_frame, text="🎲 Repartir Dulces", font=("Arial", 11), 
                 command=self.repartir_nivel_1, bg="#3498db", fg="white").pack(side="left", padx=5)
        tk.Button(config_frame, text="🧠 Aplicar Estrategia", font=("Arial", 11), 
                 command=self.estrategia_nivel_1, bg="#e74c3c", fg="white").pack(side="left", padx=5)
        tk.Button(config_frame, text="🔄 Simular 100 veces", font=("Arial", 11), 
                 command=self.simular_nivel_1, bg="#27ae60", fg="white").pack(side="left", padx=5)
        
        # Estudiantes
        self.frame_dulces_n1 = tk.Frame(frame_n1, bg="white")
        self.frame_dulces_n1.pack(fill="x", padx=10, pady=5)
        
        # Resultados
        resultado_frame = tk.LabelFrame(frame_n1, text="📊 Resultados", font=("Arial", 12, "bold"), bg="white")
        resultado_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.resultado_n1 = tk.Text(resultado_frame, height=12, wrap="word", font=("Courier", 10),
                                   bg="#f8f9fa", relief="sunken", borderwidth=2)
        scrollbar1 = tk.Scrollbar(resultado_frame, orient="vertical", command=self.resultado_n1.yview)
        self.resultado_n1.configure(yscrollcommand=scrollbar1.set)
        
        self.resultado_n1.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")
        
    def crear_nivel2(self):
        # Frame para Nivel 2
        frame_n2 = tk.Frame(self.notebook, bg="white")
        self.notebook.add(frame_n2, text="🔸 Nivel 2: Grupos de 3")
        
        # Configuración
        config_frame = tk.LabelFrame(frame_n2, text="⚙️ Configuración", font=("Arial", 12, "bold"), bg="white")
        config_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(config_frame, text="Número de estudiantes:", font=("Arial", 11), bg="white").pack(side="left", padx=5)
        self.entry_n2 = tk.Entry(config_frame, width=8, font=("Arial", 12), justify="center")
        self.entry_n2.pack(side="left", padx=5)
        self.entry_n2.insert(0, "9")
        
        tk.Button(config_frame, text="🎲 Repartir Dulces", font=("Arial", 11), 
                 command=self.repartir_nivel_2, bg="#3498db", fg="white").pack(side="left", padx=5)
        tk.Button(config_frame, text="🧠 Formar Grupos", font=("Arial", 11), 
                 command=self.estrategia_nivel_2, bg="#e74c3c", fg="white").pack(side="left", padx=5)
        tk.Button(config_frame, text="🔄 Simular 100 veces", font=("Arial", 11), 
                 command=self.simular_nivel_2, bg="#27ae60", fg="white").pack(side="left", padx=5)
        
        # Estudiantes
        self.frame_dulces_n2 = tk.Frame(frame_n2, bg="white")
        self.frame_dulces_n2.pack(fill="x", padx=10, pady=5)
        
        # Resultados
        resultado_frame = tk.LabelFrame(frame_n2, text="📊 Resultados", font=("Arial", 12, "bold"), bg="white")
        resultado_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.resultado_n2 = tk.Text(resultado_frame, height=12, wrap="word", font=("Courier", 10),
                                   bg="#f8f9fa", relief="sunken", borderwidth=2)
        scrollbar2 = tk.Scrollbar(resultado_frame, orient="vertical", command=self.resultado_n2.yview)
        self.resultado_n2.configure(yscrollcommand=scrollbar2.set)
        
        self.resultado_n2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
    def crear_estadisticas(self):
        # Frame para Estadísticas
        frame_stats = tk.Frame(self.notebook, bg="white")
        self.notebook.add(frame_stats, text="📈 Estadísticas")
        
        self.stats_text = tk.Text(frame_stats, height=20, wrap="word", font=("Courier", 10),
                                 bg="#f8f9fa", relief="sunken", borderwidth=2)
        scrollbar_stats = tk.Scrollbar(frame_stats, orient="vertical", command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=scrollbar_stats.set)
        
        self.stats_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar_stats.pack(side="right", fill="y")
        
        # Botón para limpiar estadísticas
        tk.Button(frame_stats, text="🗑️ Limpiar Estadísticas", font=("Arial", 11), 
                 command=self.limpiar_estadisticas, bg="#f39c12", fg="white").pack(pady=5)
    
    def repartir_estudiantes(self, n):
        """Reparte dulces aleatoriamente a los estudiantes"""
        return [random.choices(DULCES_SIMPLES, k=2) for _ in range(n)]
    
    def mostrar_estudiantes(self, estudiantes, frame, nivel):
        """Muestra los estudiantes y sus dulces en la interfaz"""
        for widget in frame.winfo_children():
            widget.destroy()
            
        for i, dulces in enumerate(estudiantes):
            # Crear caja para cada estudiante
            caja = tk.Frame(frame, bg="#ffffff", relief="solid", borderwidth=2, padx=8, pady=8)
            caja.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="nsew")
            
            # Nombre del estudiante
            tk.Label(caja, text=f"👤 Est. {i+1}", font=("Arial", 10, "bold"), bg="#ffffff").pack()
            
            # Dulces del estudiante
            dulces_frame = tk.Frame(caja, bg="#ffffff")
            dulces_frame.pack()
            
            for dulce in dulces:
                dulce_label = tk.Label(dulces_frame, text=f"{EMOJIS[dulce]}", 
                                     font=("Arial", 16), bg=COLORES[dulce], 
                                     relief="raised", borderwidth=1, padx=5, pady=2)
                dulce_label.pack(side="left", padx=2)
            
            # Mostrar qué le falta
            tiene = set(dulces)
            falta = set(DULCES_SIMPLES) - tiene
            if falta:
                falta_text = ", ".join([EMOJIS[d] for d in falta])
                tk.Label(caja, text=f"Falta: {falta_text}", font=("Arial", 8), 
                        bg="#ffffff", fg="#e74c3c").pack()
            else:
                tk.Label(caja, text="¡Completo! 🎉", font=("Arial", 8), 
                        bg="#ffffff", fg="#27ae60").pack()
    
    # =============== NIVEL 1 ===============
    def repartir_nivel_1(self):
        try:
            n = int(self.entry_n1.get())
            if n < 2:
                raise ValueError("Mínimo 2 estudiantes")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        self.estudiantes_n1 = self.repartir_estudiantes(n)
        self.mostrar_estudiantes(self.estudiantes_n1, self.frame_dulces_n1, 1)
        
        # Mostrar resumen inicial
        self.resultado_n1.delete("1.0", tk.END)
        self.resultado_n1.insert(tk.END, f"🎲 Dulces repartidos a {n} estudiantes\n")
        self.resultado_n1.insert(tk.END, "=" * 50 + "\n\n")
        
        completos = sum(1 for dulces in self.estudiantes_n1 if set(dulces) == set(DULCES_SIMPLES))
        if completos > 0:
            self.resultado_n1.insert(tk.END, f"🎉 ¡{completos} estudiante(s) ya tienen todos los dulces!\n\n")
    
    def estrategia_nivel_1(self):
        if not self.estudiantes_n1:
            messagebox.showerror("Error", "Primero reparte los dulces")
            return
        
        n = len(self.estudiantes_n1)
        texto = f"🧠 ESTRATEGIA NIVEL 1 - {n} estudiantes\n"
        texto += "=" * 50 + "\n\n"
        
        # Crear grafo para encontrar pares óptimos
        G = nx.Graph()
        for i in range(n):
            G.add_node(i)
        
        # Agregar aristas entre estudiantes que pueden ayudarse
        for i in range(n):
            for j in range(i + 1, n):
                dulces_combinados = set(self.estudiantes_n1[i]) | set(self.estudiantes_n1[j])
                if set(DULCES_SIMPLES).issubset(dulces_combinados):
                    G.add_edge(i, j)
        
        # Encontrar el emparejamiento máximo
        matching = nx.max_weight_matching(G, maxcardinality=True)
        sobrevivientes = set()
        usados = set()
        
        texto += "🤝 FASE 1: Emparejamiento directo\n"
        texto += "-" * 30 + "\n"
        
        for i, j in matching:
            dulces_i = set(self.estudiantes_n1[i])
            dulces_j = set(self.estudiantes_n1[j])
            falta_i = set(DULCES_SIMPLES) - dulces_i
            falta_j = set(DULCES_SIMPLES) - dulces_j
            
            # Determinar quién ayuda a quién
            if len(falta_i) <= len(falta_j):
                ayudado, ayudante = i, j
                falta = falta_i
            else:
                ayudado, ayudante = j, i
                falta = falta_j
            
            texto += f"✅ Est. {ayudado+1} ← Est. {ayudante+1}\n"
            texto += f"   Recibe: {[EMOJIS[d] for d in falta]}\n"
            texto += f"   🍭 Obtiene chupetín + comodín\n\n"
            
            sobrevivientes.add(ayudado)
            usados.update([i, j])
        
        # Usar comodines para ayudar a más estudiantes
        texto += "🎁 FASE 2: Uso de comodines\n"
        texto += "-" * 30 + "\n"
        
        comodines_disponibles = list(sobrevivientes)
        for superviviente in comodines_disponibles:
            for estudiante in range(n):
                if estudiante in usados:
                    continue
                    
                dulces_actuales = set(self.estudiantes_n1[estudiante])
                falta = list(set(DULCES_SIMPLES) - dulces_actuales)
                
                if len(falta) <= 1:  # Solo puede ayudar si falta 1 dulce o menos
                    if falta:
                        dulce_dado = falta[0]
                        texto += f"🎁 Est. {superviviente+1} da {EMOJIS[dulce_dado]} → Est. {estudiante+1}\n"
                        texto += f"   ✨ Est. {estudiante+1} sobrevive con comodín\n\n"
                        sobrevivientes.add(estudiante)
                    else:
                        texto += f"   ✨ Est. {estudiante+1} ya tenía todos los dulces\n\n"
                        sobrevivientes.add(estudiante)
                    
                    usados.add(estudiante)
                    break
        
        # Resumen final
        porcentaje = (len(sobrevivientes) / n) * 100
        texto += f"📊 RESUMEN FINAL\n"
        texto += "=" * 30 + "\n"
        texto += f"🎯 Sobrevivientes: {len(sobrevivientes)} de {n} ({porcentaje:.1f}%)\n"
        texto += f"💀 Eliminados: {n - len(sobrevivientes)}\n"
        
        if sobrevivientes:
            texto += f"🏆 Sobrevivientes: {sorted([f'Est. {i+1}' for i in sobrevivientes])}\n"
        
        self.resultado_n1.delete("1.0", tk.END)
        self.resultado_n1.insert(tk.END, texto)
        
        # Guardar estadística
        self.estadisticas["nivel1"].append({
            "estudiantes": n,
            "sobrevivientes": len(sobrevivientes),
            "porcentaje": porcentaje
        })
        
        self.actualizar_estadisticas()
    
    def simular_nivel_1(self):
        """Simula el nivel 1 muchas veces para obtener estadísticas"""
        try:
            n = int(self.entry_n1.get())
            if n < 2:
                raise ValueError("Mínimo 2 estudiantes")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        simulaciones = 100
        resultados = []
        
        for _ in range(simulaciones):
            estudiantes = self.repartir_estudiantes(n)
            sobrevivientes = self.calcular_sobrevivientes_nivel1(estudiantes)
            resultados.append(len(sobrevivientes))
        
        # Estadísticas
        promedio = sum(resultados) / len(resultados)
        maximo = max(resultados)
        minimo = min(resultados)
        
        texto = f"🔄 SIMULACIÓN NIVEL 1 - {simulaciones} iteraciones\n"
        texto += "=" * 50 + "\n"
        texto += f"👥 Estudiantes por simulación: {n}\n"
        texto += f"📊 Promedio de sobrevivientes: {promedio:.2f}\n"
        texto += f"🏆 Máximo sobrevivientes: {maximo}\n"
        texto += f"💀 Mínimo sobrevivientes: {minimo}\n"
        texto += f"📈 Tasa de supervivencia: {(promedio/n)*100:.1f}%\n\n"
        
        # Distribución
        from collections import Counter
        distribucion = Counter(resultados)
        texto += "📊 DISTRIBUCIÓN DE RESULTADOS:\n"
        texto += "-" * 30 + "\n"
        for sobrevivientes in sorted(distribucion.keys()):
            frecuencia = distribucion[sobrevivientes]
            barra = "█" * (frecuencia // 2)
            texto += f"{sobrevivientes:2d} sobrevivientes: {frecuencia:2d} veces {barra}\n"
        
        self.resultado_n1.delete("1.0", tk.END)
        self.resultado_n1.insert(tk.END, texto)
    
    def calcular_sobrevivientes_nivel1(self, estudiantes):
        """Calcula los sobrevivientes para el nivel 1 sin mostrar detalles"""
        n = len(estudiantes)
        G = nx.Graph()
        for i in range(n):
            G.add_node(i)
        
        for i in range(n):
            for j in range(i + 1, n):
                dulces_combinados = set(estudiantes[i]) | set(estudiantes[j])
                if set(DULCES_SIMPLES).issubset(dulces_combinados):
                    G.add_edge(i, j)
        
        matching = nx.max_weight_matching(G, maxcardinality=True)
        sobrevivientes = set()
        usados = set()
        
        for i, j in matching:
            dulces_i = set(estudiantes[i])
            dulces_j = set(estudiantes[j])
            falta_i = set(DULCES_SIMPLES) - dulces_i
            falta_j = set(DULCES_SIMPLES) - dulces_j
            
            if len(falta_i) <= len(falta_j):
                sobrevivientes.add(i)
            else:
                sobrevivientes.add(j)
            usados.update([i, j])
        
        # Usar comodines
        comodines_disponibles = list(sobrevivientes)
        for superviviente in comodines_disponibles:
            for estudiante in range(n):
                if estudiante in usados:
                    continue
                dulces_actuales = set(estudiantes[estudiante])
                falta = list(set(DULCES_SIMPLES) - dulces_actuales)
                if len(falta) <= 1:
                    sobrevivientes.add(estudiante)
                    usados.add(estudiante)
                    break
        
        return sobrevivientes
    
    # =============== NIVEL 2 ===============
    def repartir_nivel_2(self):
        try:
            n = int(self.entry_n2.get())
            if n < 3:
                raise ValueError("Mínimo 3 estudiantes")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        self.estudiantes_n2 = self.repartir_estudiantes(n)
        self.mostrar_estudiantes(self.estudiantes_n2, self.frame_dulces_n2, 2)
        
        # Mostrar resumen inicial
        self.resultado_n2.delete("1.0", tk.END)
        self.resultado_n2.insert(tk.END, f"🎲 Dulces repartidos a {n} estudiantes\n")
        self.resultado_n2.insert(tk.END, "=" * 50 + "\n\n")
        
        # Analizar dulces totales
        contador_total = Counter()
        for dulces in self.estudiantes_n2:
            contador_total.update(dulces)
        
        self.resultado_n2.insert(tk.END, "📊 Dulces totales disponibles:\n")
        for dulce in DULCES_SIMPLES:
            self.resultado_n2.insert(tk.END, f"   {EMOJIS[dulce]}: {contador_total[dulce]}\n")
        self.resultado_n2.insert(tk.END, "\n")
    
    def estrategia_nivel_2(self):
        if not self.estudiantes_n2:
            messagebox.showerror("Error", "Primero reparte los dulces")
            return
        
        n = len(self.estudiantes_n2)
        texto = f"🧠 ESTRATEGIA NIVEL 2 - {n} estudiantes\n"
        texto += "=" * 50 + "\n\n"
        
        # Encontrar la mejor combinación de grupos de 3
        mejor_grupos = self.encontrar_mejores_grupos(self.estudiantes_n2)
        
        if mejor_grupos:
            texto += f"🎯 GRUPOS ÓPTIMOS ENCONTRADOS: {len(mejor_grupos)}\n"
            texto += "-" * 40 + "\n"
            
            total_sobrevivientes = 0
            for i, grupo in enumerate(mejor_grupos):
                est1, est2, est3 = grupo
                dulces_grupo = (self.estudiantes_n2[est1] + 
                               self.estudiantes_n2[est2] + 
                               self.estudiantes_n2[est3])
                contador = Counter(dulces_grupo)
                
                texto += f"🥇 GRUPO {i+1}: Est. {est1+1}, Est. {est2+1}, Est. {est3+1}\n"
                texto += f"   Dulces totales: "
                for dulce in DULCES_SIMPLES:
                    texto += f"{EMOJIS[dulce]}×{contador[dulce]} "
                texto += f"\n"
                
                # Verificar si pueden sobrevivir
                if all(contador[dulce] >= 2 for dulce in DULCES_SIMPLES):
                    texto += f"   ✅ ¡Grupo sobrevive! 🍭 + 2 comodines\n"
                    total_sobrevivientes += 3
                else:
                    texto += f"   ❌ No cumplen requisitos\n"
                texto += "\n"
            
            porcentaje = (total_sobrevivientes / n) * 100
            texto += f"📊 RESUMEN FINAL\n"
            texto += "=" * 30 + "\n"
            texto += f"🎯 Sobrevivientes: {total_sobrevivientes} de {n} ({porcentaje:.1f}%)\n"
            texto += f"💀 Eliminados: {n - total_sobrevivientes}\n"
            
        else:
            texto += "❌ No se encontraron grupos válidos\n"
            texto += "💡 Sugerencia: Intenta con más estudiantes\n"
        
        self.resultado_n2.delete("1.0", tk.END)
        self.resultado_n2.insert(tk.END, texto)
        
        # Guardar estadística
        sobrevivientes = sum(3 for grupo in mejor_grupos 
                           if self.grupo_puede_sobrevivir(grupo, self.estudiantes_n2))
        self.estadisticas["nivel2"].append({
            "estudiantes": n,
            "sobrevivientes": sobrevivientes,
            "porcentaje": (sobrevivientes / n) * 100 if n > 0 else 0
        })
        
        self.actualizar_estadisticas()
    
    def encontrar_mejores_grupos(self, estudiantes):
        """Encuentra la mejor combinación de grupos de 3 estudiantes"""
        n = len(estudiantes)
        if n < 3:
            return []
        
        # Generar todas las combinaciones posibles de 3 estudiantes
        todas_combinaciones = list(combinations(range(n), 3))
        
        # Filtrar solo las que pueden sobrevivir
        grupos_validos = []
        for grupo in todas_combinaciones:
            if self.grupo_puede_sobrevivir(grupo, estudiantes):
                grupos_validos.append(grupo)
        
        # Encontrar la combinación que maximice sobrevivientes sin solapamiento
        return self.optimizar_grupos(grupos_validos)
    
    def grupo_puede_sobrevivir(self, grupo, estudiantes):
        """Verifica si un grupo de 3 puede sobrevivir"""
        dulces_grupo = []
        for est in grupo:
            dulces_grupo.extend(estudiantes[est])
        
        contador = Counter(dulces_grupo)
        return all(contador[dulce] >= 2 for dulce in DULCES_SIMPLES)
    
    def optimizar_grupos(self, grupos_validos):
        """Encuentra la combinación óptima de grupos sin solapamiento"""
        if not grupos_validos:
            return []
        
        # Usar programación dinámica para encontrar la mejor combinación
        # Por simplicidad, usar un enfoque greedy
        grupos_seleccionados = []
        estudiantes_usados = set()
        
        for grupo in grupos_validos:
            if not any(est in estudiantes_usados for est in grupo):
                grupos_seleccionados.append(grupo)
                estudiantes_usados.update(grupo)
        
        return grupos_seleccionados
    
    def simular_nivel_2(self):
        """Simula el nivel 2 muchas veces"""
        try:
            n = int(self.entry_n2.get())
            if n < 3:
                raise ValueError("Mínimo 3 estudiantes")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        
        simulaciones = 100
        resultados = []
        
        for _ in range(simulaciones):
            estudiantes = self.repartir_estudiantes(n)
            grupos = self.encontrar_mejores_grupos(estudiantes)
            sobrevivientes = len(grupos) * 3
            resultados.append(sobrevivientes)
        
        # Estadísticas
        promedio = sum(resultados) / len(resultados)
        maximo = max(resultados)
        minimo = min(resultados)
        
        texto = f"🔄 SIMULACIÓN NIVEL 2 - {simulaciones} iteraciones\n"
        texto += "=" * 50 + "\n"
        texto += f"👥 Estudiantes por simulación: {n}\n"
        texto += f"📊 Promedio de sobrevivientes: {promedio:.2f}\n"
        texto += f"🏆 Máximo sobrevivientes: {maximo}\n"
        texto += f"💀 Mínimo sobrevivientes: {minimo}\n"
        texto += f"📈 Tasa de supervivencia: {(promedio/n)*100:.1f}%\n\n"
        
        # Distribución
        from collections import Counter
        distribucion = Counter(resultados)
        texto += "📊 DISTRIBUCIÓN DE RESULTADOS:\n"
        texto += "-" * 30 + "\n"
        for sobrevivientes in sorted(distribucion.keys()):
            frecuencia = distribucion[sobrevivientes]
            barra = "█" * (frecuencia // 2)
            texto += f"{sobrevivientes:2d} sobrevivientes: {frecuencia:2d} veces {barra}\n"
            self.resultado_n2.delete("1.0", tk.END)
        self.resultado_n2.insert(tk.END, texto)
    
    # =============== ESTADÍSTICAS ===============
    def actualizar_estadisticas(self):
        """Actualiza la pestaña de estadísticas"""
        self.stats_text.delete("1.0", tk.END)
        
        texto = "📈 ESTADÍSTICAS GENERALES\n"
        texto += "=" * 50 + "\n\n"
        
        # Estadísticas Nivel 1
        if self.estadisticas["nivel1"]:
            texto += "🔹 NIVEL 1 - Cooperación Individual\n"
            texto += "-" * 35 + "\n"
            
            total_sims = len(self.estadisticas["nivel1"])
            promedio_est = sum(s["estudiantes"] for s in self.estadisticas["nivel1"]) / total_sims
            promedio_sobr = sum(s["sobrevivientes"] for s in self.estadisticas["nivel1"]) / total_sims
            promedio_porc = sum(s["porcentaje"] for s in self.estadisticas["nivel1"]) / total_sims
            
            texto += f"📊 Total simulaciones: {total_sims}\n"
            texto += f"👥 Promedio estudiantes: {promedio_est:.1f}\n"
            texto += f"🎯 Promedio sobrevivientes: {promedio_sobr:.1f}\n"
            texto += f"📈 Tasa promedio supervivencia: {promedio_porc:.1f}%\n\n"
            
            # Últimas 5 simulaciones
            texto += "🕐 Últimas 5 simulaciones:\n"
            for i, sim in enumerate(self.estadisticas["nivel1"][-5:], 1):
                texto += f"   {i}. {sim['estudiantes']} est. → {sim['sobrevivientes']} sobrev. ({sim['porcentaje']:.1f}%)\n"
            texto += "\n"
        
        # Estadísticas Nivel 2
        if self.estadisticas["nivel2"]:
            texto += "🔸 NIVEL 2 - Grupos de 3\n"
            texto += "-" * 25 + "\n"
            
            total_sims = len(self.estadisticas["nivel2"])
            promedio_est = sum(s["estudiantes"] for s in self.estadisticas["nivel2"]) / total_sims
            promedio_sobr = sum(s["sobrevivientes"] for s in self.estadisticas["nivel2"]) / total_sims
            promedio_porc = sum(s["porcentaje"] for s in self.estadisticas["nivel2"]) / total_sims
            
            texto += f"📊 Total simulaciones: {total_sims}\n"
            texto += f"👥 Promedio estudiantes: {promedio_est:.1f}\n"
            texto += f"🎯 Promedio sobrevivientes: {promedio_sobr:.1f}\n"
            texto += f"📈 Tasa promedio supervivencia: {promedio_porc:.1f}%\n\n"
            
            # Últimas 5 simulaciones
            texto += "🕐 Últimas 5 simulaciones:\n"
            for i, sim in enumerate(self.estadisticas["nivel2"][-5:], 1):
                texto += f"   {i}. {sim['estudiantes']} est. → {sim['sobrevivientes']} sobrev. ({sim['porcentaje']:.1f}%)\n"
            texto += "\n"
        
        # Comparación entre niveles
        if self.estadisticas["nivel1"] and self.estadisticas["nivel2"]:
            texto += "⚖️ COMPARACIÓN ENTRE NIVELES\n"
            texto += "-" * 30 + "\n"
            
            eficiencia_n1 = sum(s["porcentaje"] for s in self.estadisticas["nivel1"]) / len(self.estadisticas["nivel1"])
            eficiencia_n2 = sum(s["porcentaje"] for s in self.estadisticas["nivel2"]) / len(self.estadisticas["nivel2"])
            
            texto += f"📊 Eficiencia Nivel 1: {eficiencia_n1:.1f}%\n"
            texto += f"📊 Eficiencia Nivel 2: {eficiencia_n2:.1f}%\n"
            
            if eficiencia_n1 > eficiencia_n2:
                texto += f"🏆 Nivel 1 es más eficiente por {eficiencia_n1 - eficiencia_n2:.1f}%\n"
            elif eficiencia_n2 > eficiencia_n1:
                texto += f"🏆 Nivel 2 es más eficiente por {eficiencia_n2 - eficiencia_n1:.1f}%\n"
            else:
                texto += f"⚖️ Ambos niveles tienen la misma eficiencia\n"
        
        self.stats_text.insert(tk.END, texto)
    
    def limpiar_estadisticas(self):
        """Limpia todas las estadísticas"""
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres limpiar todas las estadísticas?")
        if respuesta:
            self.estadisticas = {"nivel1": [], "nivel2": []}
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert(tk.END, "📊 Estadísticas limpiadas\n\n")
            self.stats_text.insert(tk.END, "💡 Ejecuta algunas simulaciones para generar nuevas estadísticas.")

# =============== FUNCIÓN PRINCIPAL ===============
def main():
    """Función principal que inicia la aplicación"""
    ventana = tk.Tk()
    app = JuegoSobrevivientes(ventana)
    ventana.mainloop()

if __name__ == "__main__":
    main()