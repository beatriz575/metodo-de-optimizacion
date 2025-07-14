import random
from collections import defaultdict, Counter
from itertools import combinations, permutations
import copy

class JuegoSupervivenciaColaborativo:
    def __init__(self):
        self.dulces = ['limon', 'pera', 'huevo']
        
    def generar_dulces_aleatorios(self, cantidad):
        """Genera una cantidad específica de dulces aleatorios"""
        return [random.choice(self.dulces) for _ in range(cantidad)]
    
    def puede_formar_chupetin_individual(self, dulces_jugador, comodines=0):
        """
        Verifica si un jugador puede formar chupetín individualmente
        Ronda 1: Necesita 1 limón, 1 pera, 1 huevo
        """
        contador = Counter(dulces_jugador)
        comodines_usados = 0
        
        # Verificar cuántos tipos diferentes faltan
        for dulce in self.dulces:
            if contador[dulce] == 0:  # No tiene este tipo
                if comodines_usados < comodines:
                    comodines_usados += 1
                else:
                    return False, comodines  # No puede formar
        
        return True, comodines - comodines_usados
    
    def encontrar_intercambios_optimos(self, jugadores_data):
        """
        Encuentra los intercambios óptimos entre jugadores para maximizar supervivientes
        jugadores_data: lista de {'id': int, 'dulces': list, 'comodines': int}
        """
        n = len(jugadores_data)
        mejor_resultado = {'supervivientes': [], 'intercambios': []}
        max_supervivientes = 0
        
        # Probar diferentes combinaciones de intercambios
        for intentos in range(min(1000, 3**n)):  # Limitar búsqueda para eficiencia
            # Copiar estado inicial
            jugadores_temp = copy.deepcopy(jugadores_data)
            intercambios_realizados = []
            
            # Intentar intercambios aleatorios
            for _ in range(random.randint(0, n//2)):
                # Seleccionar dos jugadores al azar
                if len(jugadores_temp) < 2:
                    break
                    
                j1, j2 = random.sample(range(len(jugadores_temp)), 2)
                
                # Intentar intercambio beneficioso
                intercambio = self.intentar_intercambio(jugadores_temp[j1], jugadores_temp[j2])
                if intercambio:
                    intercambios_realizados.append(intercambio)
            
            # Evaluar supervivientes después de intercambios
            supervivientes = []
            for jugador in jugadores_temp:
                puede_sobrevivir, comodines_restantes = self.puede_formar_chupetin_individual(
                    jugador['dulces'], jugador['comodines']
                )
                if puede_sobrevivir:
                    supervivientes.append({
                        'id': jugador['id'],
                        'dulces_usados': [d for d in self.dulces],  # 1 de cada tipo
                        'comodines_restantes': comodines_restantes + 1,  # +1 por formar chupetín
                        'dulces_sobrantes': self.calcular_sobrantes(jugador['dulces'])
                    })
            
            # Actualizar mejor resultado si es mejor
            if len(supervivientes) > max_supervivientes:
                max_supervivientes = len(supervivientes)
                mejor_resultado = {
                    'supervivientes': supervivientes,
                    'intercambios': intercambios_realizados
                }
        
        return mejor_resultado
    
    def intentar_intercambio(self, jugador1, jugador2):
        """
        Intenta hacer un intercambio beneficioso entre dos jugadores
        Retorna información del intercambio si se realizó, None si no
        """
        contador1 = Counter(jugador1['dulces'])
        contador2 = Counter(jugador2['dulces'])
        
        # Buscar intercambios mutuamente beneficiosos
        for dulce1 in self.dulces:
            for dulce2 in self.dulces:
                if dulce1 != dulce2 and contador1[dulce1] > 0 and contador2[dulce2] > 0:
                    # Simular intercambio
                    temp_contador1 = contador1.copy()
                    temp_contador2 = contador2.copy()
                    
                    temp_contador1[dulce1] -= 1
                    temp_contador1[dulce2] += 1
                    temp_contador2[dulce2] -= 1
                    temp_contador2[dulce1] += 1
                    
                    # Verificar si mejora las posibilidades de ambos
                    mejora1 = self.evaluar_mejora(contador1, temp_contador1, jugador1['comodines'])
                    mejora2 = self.evaluar_mejora(contador2, temp_contador2, jugador2['comodines'])
                    
                    if mejora1 and mejora2:
                        # Realizar intercambio
                        jugador1['dulces'].remove(dulce1)
                        jugador1['dulces'].append(dulce2)
                        jugador2['dulces'].remove(dulce2)
                        jugador2['dulces'].append(dulce1)
                        
                        return {
                            'jugador1': jugador1['id'],
                            'jugador2': jugador2['id'],
                            'intercambio': f"J{jugador1['id']} da {dulce1} por {dulce2} de J{jugador2['id']}"
                        }
        
        return None
    
    def evaluar_mejora(self, contador_antes, contador_despues, comodines):
        """Evalúa si un intercambio mejora las posibilidades de supervivencia"""
        # Calcular tipos únicos antes y después
        tipos_antes = sum(1 for count in contador_antes.values() if count > 0)
        tipos_despues = sum(1 for count in contador_despues.values() if count > 0)
        
        # Calcular comodines necesarios antes y después
        comodines_necesarios_antes = max(0, 3 - tipos_antes)
        comodines_necesarios_despues = max(0, 3 - tipos_despues)
        
        # Mejora si necesita menos comodines o puede sobrevivir cuando antes no podía
        puede_antes = comodines_necesarios_antes <= comodines
        puede_despues = comodines_necesarios_despues <= comodines
        
        return (not puede_antes and puede_despues) or (puede_antes and puede_despues and comodines_necesarios_despues < comodines_necesarios_antes)
    
    def calcular_sobrantes(self, dulces_jugador):
        """Calcula dulces sobrantes después de formar un chupetín"""
        contador = Counter(dulces_jugador)
        sobrantes = []
        
        # Remover 1 de cada tipo (para formar chupetín)
        for dulce in self.dulces:
            if contador[dulce] > 1:
                sobrantes.extend([dulce] * (contador[dulce] - 1))
        
        return sobrantes
    
    def simular_ronda1_colaborativa(self, num_jugadores, dulces_por_jugador=2):
        """Simula la primera ronda con estrategia colaborativa"""
        print(f"\n=== RONDA 1 COLABORATIVA ===")
        print(f"Jugadores: {num_jugadores}")
        print(f"Dulces por jugador: {dulces_por_jugador}")
        print("🤝 COLABORACIÓN REQUERIDA: Con solo 2 dulces, necesitan intercambiar para sobrevivir")
        print("Regla: 1 limón + 1 pera + 1 huevo = 1 chupetín + 1 comodín")
        
        # Generar jugadores
        jugadores = []
        for i in range(num_jugadores):
            dulces = self.generar_dulces_aleatorios(dulces_por_jugador)
            jugadores.append({
                'id': i+1,
                'dulces': dulces,
                'comodines': 0
            })
            print(f"Jugador {i+1}: {dulces}")
        
        # Mostrar análisis individual (todos deberían fallar)
        print(f"\n--- Análisis Individual (sin colaboración) ---")
        supervivientes_individuales = 0
        for jugador in jugadores:
            puede, _ = self.puede_formar_chupetin_individual(jugador['dulces'], jugador['comodines'])
            if puede:
                supervivientes_individuales += 1
            tipos_unicos = len(set(jugador['dulces']))
            print(f"Jugador {jugador['id']}: {tipos_unicos}/3 tipos únicos - {'✓' if puede else '✗'}")
        
        print(f"Supervivientes sin colaboración: {supervivientes_individuales}/{num_jugadores}")
        
        # Encontrar estrategia colaborativa óptima
        print(f"\n--- Optimizando Intercambios ---")
        resultado_optimo = self.encontrar_intercambios_optimos(jugadores)
        
        print(f"\n--- Intercambios Realizados ---")
        if resultado_optimo['intercambios']:
            for intercambio in resultado_optimo['intercambios']:
                print(f"🔄 {intercambio['intercambio']}")
        else:
            print("No se realizaron intercambios beneficiosos")
        
        print(f"\n--- Resultado Final Ronda 1 ---")
        supervivientes = resultado_optimo['supervivientes']
        for superviviente in supervivientes:
            print(f"✓ Jugador {superviviente['id']} SOBREVIVE")
            print(f"  Comodines: {superviviente['comodines_restantes']}")
            print(f"  Dulces sobrantes: {superviviente['dulces_sobrantes']}")
        
        print(f"\n🎯 Supervivientes con colaboración: {len(supervivientes)}/{num_jugadores}")
        print(f"📈 Mejora: +{len(supervivientes) - supervivientes_individuales} supervivientes")
        
        return supervivientes
    
    def simular_ronda2_colaborativa(self, supervivientes_ronda1, dulces_adicionales=2):
        """Simula la segunda ronda con estrategia colaborativa"""
        print(f"\n=== RONDA 2 COLABORATIVA ===")
        print(f"Supervivientes de ronda anterior: {len(supervivientes_ronda1)}")
        print(f"Dulces adicionales por jugador: {dulces_adicionales}")
        print("Regla: 2 limón + 2 pera + 2 huevo = 1 chupetín + 2 comodines")
        
        # Preparar jugadores para ronda 2
        jugadores_r2 = []
        for superviviente in supervivientes_ronda1:
            dulces_nuevos = self.generar_dulces_aleatorios(dulces_adicionales)
            dulces_totales = superviviente['dulces_sobrantes'] + dulces_nuevos
            
            jugadores_r2.append({
                'id': superviviente['id'],
                'dulces': dulces_totales,
                'comodines': superviviente['comodines_restantes']
            })
            
            print(f"Jugador {superviviente['id']}: {dulces_totales} (comodines: {superviviente['comodines_restantes']})")
        
        # Aplicar lógica colaborativa para ronda 2
        # (Aquí podrías expandir con lógica específica para la ronda 2)
        
        print(f"\n🚧 Ronda 2 en desarrollo - Se necesita lógica específica para 2 de cada tipo")
        return []
    
    def analizar_distribucion_inicial(self, num_jugadores, num_simulaciones=1000):
        """Analiza la distribución inicial de dulces y posibilidades de colaboración"""
        print(f"\n=== ANÁLISIS DE DISTRIBUCIONES ===")
        
        distribucion_tipos = {1: 0, 2: 0, 3: 0}  # Jugadores con 1, 2 o 3 tipos únicos
        total_simulaciones = 0
        
        for _ in range(num_simulaciones):
            jugadores = []
            for i in range(num_jugadores):
                dulces = self.generar_dulces_aleatorios(2)
                tipos_unicos = len(set(dulces))
                distribucion_tipos[tipos_unicos] += 1
            total_simulaciones += num_jugadores
        
        print(f"Distribución promedio en {num_simulaciones} simulaciones:")
        for tipos, cantidad in distribucion_tipos.items():
            porcentaje = (cantidad / total_simulaciones) * 100
            print(f"  {tipos} tipo(s) único(s): {porcentaje:.1f}%")
        
        # Calcular probabilidad teórica
        # P(2 tipos únicos) = P(dulce1 ≠ dulce2) = 2/3
        print(f"\nProbabilidad teórica:")
        print(f"  1 tipo único (ej: limón, limón): 33.3%")
        print(f"  2 tipos únicos (ej: limón, pera): 66.7%")
        print(f"  3 tipos únicos: 0% (imposible con 2 dulces)")
        
        print(f"\n💡 Insight: ~67% de jugadores tendrán 2 tipos únicos")
        print(f"   Necesitan intercambiar para conseguir el 3er tipo")

def main():
    juego = JuegoSupervivenciaColaborativo()
    
    print("🍭 JUEGO DE SUPERVIVENCIA COLABORATIVO 🍭")
    print("🤝 La clave está en la colaboración estratégica")
    
    # Análisis de distribuciones
    juego.analizar_distribucion_inicial(20)
    
    # Simular un juego colaborativo
    num_jugadores = int(input("\n¿Cuántos jugadores? (recomendado: 6-12 para ver intercambios): "))
    
    supervivientes_r1 = juego.simular_ronda1_colaborativa(num_jugadores)
    
    if supervivientes_r1:
        print(f"\n🎉 {len(supervivientes_r1)} jugadores avanzan a la Ronda 2!")
        
        respuesta = input("\n¿Continuar con Ronda 2? (s/n): ")
        if respuesta.lower() == 's':
            supervivientes_finales = juego.simular_ronda2_colaborativa(supervivientes_r1)
    else:
        print(f"\n💀 Nadie logró formar alianzas exitosas en la Ronda 1")
    
    print(f"\n🧠 ESTRATEGIAS CLAVE:")
    print(f"1. Identifica quién tiene qué tipos de dulces")
    print(f"2. Busca intercambios mutuamente beneficiosos")
    print(f"3. Usa comodines estratégicamente")
    print(f"4. Forma alianzas temporales para sobrevivir")

if __name__ == "__main__":
    main()