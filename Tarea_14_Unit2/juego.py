import numpy as np
import pandas as pd
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Asset:
    """Clase para representar un activo financiero"""
    id: str
    retorno_esperado: float
    volatilidad: float
    beta: float
    liquidez_score: int
    sector: int
    precio_accion: float
    min_inversion: float

class CSVDataLoader:
    """Cargador especializado para archivos CSV personalizados"""
    
    @staticmethod
    def inspect_csv(file_path: str):
        """Inspeccionar la estructura del CSV"""
        try:
            df = pd.read_csv(file_path)
            print(f"📊 INSPECCIÓN DEL ARCHIVO: {file_path}")
            print(f"{'='*50}")
            print(f"📏 Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            print(f"\n📋 Columnas encontradas:")
            for i, col in enumerate(df.columns, 1):
                print(f"   {i:2d}. {col}")
            
            print(f"\n🔍 Primeras 3 filas:")
            print(df.head(3).to_string())
            
            print(f"\n📈 Tipos de datos:")
            print(df.dtypes.to_string())
            
            print(f"\n🎯 Estadísticas básicas:")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                print(df[numeric_cols].describe())
            
            return df
            
        except Exception as e:
            print(f"❌ Error inspeccionando archivo: {e}")
            return None
    
    @staticmethod
    def load_csv_auto(file_path: str) -> List[Asset]:
        """Cargar CSV con detección automática de columnas"""
        try:
            df = pd.read_csv(file_path)
            
            print(f"\n🤖 DETECCIÓN AUTOMÁTICA DE COLUMNAS")
            print(f"{'='*50}")
            
            # Mapeo automático basado en nombres de columnas
            column_mapping = {}
            
            # Patrones para cada campo
            patterns = {
                'activo_id': ['id', 'activo', 'asset', 'symbol', 'ticker', 'codigo', 'nombre'],
                'retorno_esperado': ['retorno', 'return', 'rendimiento', 'expected_return', 'ret'],
                'volatilidad': ['volatilidad', 'vol', 'volatility', 'std', 'desviacion'],
                'beta': ['beta', 'b'],
                'liquidez_score': ['liquidez', 'liquidity', 'score', 'liq'],
                'sector': ['sector', 'industry', 'categoria'],
                'precio_accion': ['precio', 'price', 'valor', 'cotizacion'],
                'min_inversion': ['min_inversion', 'minimum', 'min_inv', 'minimo']
            }
            
            for field, field_patterns in patterns.items():
                best_match = None
                for col in df.columns:
                    col_lower = col.lower().replace('_', '').replace(' ', '')
                    for pattern in field_patterns:
                        if pattern in col_lower:
                            best_match = col
                            break
                    if best_match:
                        break
                
                column_mapping[field] = best_match
                status = "✅" if best_match else "❌"
                print(f"   {status} {field}: {best_match or 'NO ENCONTRADO'}")
            
            # Procesar datos
            return CSVDataLoader._process_mapped_data(df, column_mapping)
            
        except Exception as e:
            print(f"❌ Error en detección automática: {e}")
            return []
    
    @staticmethod
    def _process_mapped_data(df: pd.DataFrame, column_mapping: Dict) -> List[Asset]:
        """Procesar datos con mapeo de columnas"""
        assets = []
        
        print(f"\n⚙️ PROCESANDO DATOS...")
        print(f"{'='*30}")
        
        for index, row in df.iterrows():
            try:
                # Obtener valores con valores por defecto
                asset_id = CSVDataLoader._get_value(row, column_mapping['activo_id'], f"A{index+1:03d}")
                retorno = CSVDataLoader._get_numeric_value(row, column_mapping['retorno_esperado'], 
                                                         np.random.uniform(5, 18))
                volatilidad = CSVDataLoader._get_numeric_value(row, column_mapping['volatilidad'], 
                                                             np.random.uniform(10, 30))
                beta = CSVDataLoader._get_numeric_value(row, column_mapping['beta'], 
                                                      np.random.uniform(0.5, 1.5))
                liquidez = CSVDataLoader._get_numeric_value(row, column_mapping['liquidez_score'], 
                                                          np.random.randint(5, 10))
                sector = CSVDataLoader._get_numeric_value(row, column_mapping['sector'], 
                                                        np.random.randint(1, 6))
                precio = CSVDataLoader._get_numeric_value(row, column_mapping['precio_accion'], 
                                                        np.random.uniform(50, 300))
                min_inv = CSVDataLoader._get_numeric_value(row, column_mapping['min_inversion'], 
                                                         np.random.uniform(2000, 8000))
                
                asset = Asset(
                    id=str(asset_id),
                    retorno_esperado=float(retorno),
                    volatilidad=float(volatilidad),
                    beta=float(beta),
                    liquidez_score=int(liquidez),
                    sector=int(sector),
                    precio_accion=float(precio),
                    min_inversion=float(min_inv)
                )
                
                assets.append(asset)
                
            except Exception as e:
                print(f"⚠️  Error procesando fila {index}: {e}")
                continue
        
        print(f"✅ Procesados {len(assets)} activos exitosamente")
        return assets
    
    @staticmethod
    def _get_value(row, column_name, default_value):
        """Obtener valor de una columna con valor por defecto"""
        if column_name and column_name in row.index:
            value = row[column_name]
            return value if pd.notna(value) else default_value
        return default_value
    
    @staticmethod
    def _get_numeric_value(row, column_name, default_value):
        """Obtener valor numérico con valor por defecto"""
        if column_name and column_name in row.index:
            value = row[column_name]
            if pd.notna(value):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    pass
        return default_value

class PortfolioOptimizer:
    """Optimizador de portafolio"""
    
    def __init__(self, assets: List[Asset], budget: float = 1000000, lambda_risk: float = 0.5):
        self.assets = assets
        self.budget = budget
        self.lambda_risk = lambda_risk
        self.n_assets = len(assets)
        
        if self.n_assets == 0:
            raise ValueError("No hay activos para optimizar")
        
        # Crear arrays numpy
        self.returns = np.array([asset.retorno_esperado/100 for asset in assets])
        self.volatilities = np.array([asset.volatilidad/100 for asset in assets])
        self.betas = np.array([asset.beta for asset in assets])
        self.prices = np.array([asset.precio_accion for asset in assets])
        self.min_investments = np.array([asset.min_inversion for asset in assets])
        self.sectors = np.array([asset.sector for asset in assets])
        
        print(f"\n🔧 OPTIMIZADOR CONFIGURADO:")
        print(f"   📊 Activos: {self.n_assets}")
        print(f"   💰 Presupuesto: S/. {self.budget:,.0f}")
        print(f"   📈 Retorno promedio: {np.mean(self.returns)*100:.1f}%")
        print(f"   📉 Volatilidad promedio: {np.mean(self.volatilities)*100:.1f}%")
        print(f"   🎯 Sectores únicos: {len(np.unique(self.sectors))}")
    
    def objective_function(self, weights: np.ndarray) -> float:
        """Función objetivo del torneo"""
        portfolio_return = np.dot(weights, self.returns)
        portfolio_variance = np.dot(weights**2, self.volatilities**2)
        utility = portfolio_return - self.lambda_risk * portfolio_variance
        return -utility  # Minimizar = maximizar utility
    
    def create_constraints(self):
        """Crear restricciones del problema"""
        constraints = []
        
        # 1. Suma de pesos = 1
        constraints.append({
            'type': 'eq',
            'fun': lambda w: np.sum(w) - 1.0
        })
        
        # 2. Diversificación sectorial (máximo 30% por sector)
        unique_sectors = np.unique(self.sectors)
        for sector in unique_sectors:
            sector_mask = (self.sectors == sector)
            constraints.append({
                'type': 'ineq',
                'fun': lambda w, mask=sector_mask: 0.30 - np.sum(w[mask])
            })
        
        # 3. Riesgo sistemático (beta ponderado ≤ 1.2)
        constraints.append({
            'type': 'ineq',
            'fun': lambda w: 1.2 - np.dot(w, self.betas)
        })
        
        return constraints
    
    def optimize(self) -> Dict:
        """Optimizar portafolio con múltiples estrategias"""
        print(f"\n⚡ EJECUTANDO OPTIMIZACIÓN...")
        print(f"{'='*40}")
        
        # Diferentes puntos de partida
        strategies = [
            ("Pesos Iguales", np.ones(self.n_assets) / self.n_assets),
            ("Basado en Retorno", self.returns / np.sum(self.returns)),
            ("Riesgo Inverso", (1/self.volatilities) / np.sum(1/self.volatilities)),
            ("Aleatorio", np.random.dirichlet(np.ones(self.n_assets)))
        ]
        
        best_result = None
        best_score = -np.inf
        
        for strategy_name, x0 in strategies:
            print(f"\n🔄 Estrategia: {strategy_name}")
            
            try:
                bounds = [(0, 1) for _ in range(self.n_assets)]
                constraints = self.create_constraints()
                
                result = minimize(
                    self.objective_function,
                    x0,
                    method='SLSQP',
                    bounds=bounds,
                    constraints=constraints,
                    options={'maxiter': 1000, 'ftol': 1e-9}
                )
                
                if result.success:
                    processed_result = self._process_results(result.x, strategy_name)
                    score = self.calculate_score(processed_result)
                    
                    print(f"   ✅ Puntaje: {score:.2f}")
                    
                    if score > best_score:
                        best_result = processed_result
                        best_score = score
                        print(f"   🏆 ¡Mejor resultado hasta ahora!")
                else:
                    print(f"   ❌ Falló: {result.message}")
                    
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                continue
        
        return best_result if best_result else {'success': False}
    
    def _process_results(self, weights: np.ndarray, strategy: str) -> Dict:
        """Procesar resultados de optimización"""
        # Limpiar pesos pequeños
        weights = np.where(weights < 0.001, 0, weights)
        if np.sum(weights) > 0:
            weights = weights / np.sum(weights)  # Renormalizar
        
        # Calcular métricas
        portfolio_return = np.dot(weights, self.returns)
        portfolio_volatility = np.sqrt(np.dot(weights**2, self.volatilities**2))
        portfolio_beta = np.dot(weights, self.betas)
        utility = portfolio_return - self.lambda_risk * (portfolio_volatility**2)
        
        # Verificar restricciones
        constraints_met = self._check_constraints(weights)
        
        # Crear detalles del portafolio
        portfolio_details = []
        for i, asset in enumerate(self.assets):
            if weights[i] > 0.001:
                portfolio_details.append({
                    'asset_id': asset.id,
                    'weight': weights[i],
                    'investment_amount': weights[i] * self.budget,
                    'expected_return': asset.retorno_esperado,
                    'volatility': asset.volatilidad,
                    'sector': asset.sector,
                    'beta': asset.beta,
                    'price': asset.precio_accion
                })
        
        return {
            'success': True,
            'strategy': strategy,
            'weights': weights,
            'portfolio_return': portfolio_return * 100,
            'portfolio_volatility': portfolio_volatility * 100,
            'portfolio_beta': portfolio_beta,
            'utility': utility,
            'constraints_met': constraints_met,
            'portfolio_details': portfolio_details,
            'n_assets_selected': len(portfolio_details)
        }
    
    def _check_constraints(self, weights: np.ndarray) -> Dict:
        """Verificar restricciones"""
        constraints = {}
        
        # Presupuesto
        constraints['presupuesto'] = abs(np.sum(weights) - 1.0) < 1e-4
        
        # Diversificación sectorial
        unique_sectors = np.unique(self.sectors)
        for sector in unique_sectors:
            sector_mask = (self.sectors == sector)
            sector_weight = np.sum(weights[sector_mask])
            constraints[f'sector_{sector}'] = sector_weight <= 0.301
        
        # Riesgo sistemático
        constraints['riesgo_sistematico'] = np.dot(weights, self.betas) <= 1.201
        
        # Mínimo de activos
        constraints['min_activos'] = np.sum(weights > 0.001) >= 5
        
        return constraints
    
    def calculate_score(self, result: Dict) -> float:
        """Calcular puntaje según reglas del torneo"""
        if not result['success']:
            return 0
        
        Rp = result['portfolio_return'] / 100
        σp = result['portfolio_volatility'] / 100
        
        # Factor de restricciones
        constraints = result['constraints_met']
        violations = sum(1 for met in constraints.values() if not met)
        
        if violations == 0:
            Fr = 1.0
        elif violations == 1:
            Fr = 0.8
        else:
            Fr = 0.6
        
        Ft = 1.5  # Factor de tiempo (entrega rápida)
        
        score = 1000 * (Rp - 0.5 * σp) * Fr * Ft
        return max(0, score)
    
    def print_results(self, result: Dict):
        """Imprimir resultados finales"""
        if not result['success']:
            print("\n❌ OPTIMIZACIÓN FALLÓ")
            return
        
        print(f"\n{'='*60}")
        print(f"🏆 RESULTADOS FINALES DEL TORNEO")
        print(f"{'='*60}")
        
        score = self.calculate_score(result)
        print(f"\n🎯 PUNTAJE FINAL: {score:.2f} puntos")
        print(f"🔧 Estrategia ganadora: {result['strategy']}")
        
        print(f"\n📊 MÉTRICAS DEL PORTAFOLIO:")
        print(f"   📈 Retorno Esperado: {result['portfolio_return']:.2f}%")
        print(f"   📉 Volatilidad: {result['portfolio_volatility']:.2f}%")
        print(f"   ⚖️  Beta: {result['portfolio_beta']:.2f}")
        print(f"   🎲 Utilidad: {result['utility']:.4f}")
        print(f"   🔢 Activos seleccionados: {result['n_assets_selected']}")
        
        print(f"\n💼 COMPOSICIÓN DEL PORTAFOLIO:")
        total_investment = 0
        for detail in sorted(result['portfolio_details'], key=lambda x: x['weight'], reverse=True):
            investment = detail['investment_amount']
            total_investment += investment
            print(f"   {detail['asset_id']:10} {detail['weight']*100:6.1f}% "
                  f"S/. {investment:>10,.0f} "
                  f"({detail['expected_return']:5.1f}% ret, {detail['volatility']:5.1f}% vol, "
                  f"β={detail['beta']:.2f})")
        
        print(f"\n💰 Inversión total: S/. {total_investment:,.0f}")
        
        # Análisis por sectores
        print(f"\n🏭 DISTRIBUCIÓN POR SECTORES:")
        sector_analysis = {}
        for detail in result['portfolio_details']:
            sector = detail['sector']
            if sector not in sector_analysis:
                sector_analysis[sector] = {'weight': 0, 'investment': 0, 'count': 0}
            sector_analysis[sector]['weight'] += detail['weight']
            sector_analysis[sector]['investment'] += detail['investment_amount']
            sector_analysis[sector]['count'] += 1
        
        for sector, data in sorted(sector_analysis.items()):
            print(f"   Sector {sector}: {data['weight']*100:5.1f}% "
                  f"(S/. {data['investment']:,.0f}, {data['count']} activos)")
        
        print(f"\n✅ VERIFICACIÓN DE RESTRICCIONES:")
        all_met = True
        for constraint, met in result['constraints_met'].items():
            status = "✅" if met else "❌"
            if not met:
                all_met = False
            constraint_name = constraint.replace('_', ' ').title()
            print(f"   {status} {constraint_name}")
        
        if all_met:
            print(f"\n🎉 ¡TODAS LAS RESTRICCIONES CUMPLIDAS!")
        else:
            print(f"\n⚠️  Algunas restricciones no se cumplieron completamente")

# Función para crear datos de ejemplo
def create_sample_data():
    """Crear datos de ejemplo para pruebas"""
    np.random.seed(42)  # Para reproducibilidad
    
    assets = []
    sectors = [1, 2, 3, 4, 5]  # 5 sectores
    
    for i in range(20):  # 20 activos de ejemplo
        asset = Asset(
            id=f"ASSET_{i+1:02d}",
            retorno_esperado=np.random.uniform(8, 20),
            volatilidad=np.random.uniform(15, 35),
            beta=np.random.uniform(0.6, 1.4),
            liquidez_score=np.random.randint(6, 10),
            sector=np.random.choice(sectors),
            precio_accion=np.random.uniform(50, 500),
            min_inversion=np.random.uniform(3000, 10000)
        )
        assets.append(asset)
    
    return assets

# Función principal simplificada
def run_optimization(file_path=None):
    """Ejecutar optimización con archivo CSV o datos de ejemplo"""
    print("🚀 OPTIMABATTLE ARENA - OPTIMIZADOR DE PORTAFOLIO")
    print("=" * 60)
    
    if file_path:
        # Cargar desde archivo CSV
        print(f"📁 Cargando datos desde: {file_path}")
        assets = CSVDataLoader.load_csv_auto(file_path)
    else:
        # Usar datos de ejemplo
        print("📊 Usando datos de ejemplo...")
        assets = create_sample_data()
    
    if not assets:
        print("❌ No se pudieron cargar los activos")
        return
    
    # Mostrar resumen
    print(f"\n📋 RESUMEN DE ACTIVOS:")
    print(f"   Total: {len(assets)} activos")
    print(f"   Retorno promedio: {np.mean([a.retorno_esperado for a in assets]):.1f}%")
    print(f"   Volatilidad promedio: {np.mean([a.volatilidad for a in assets]):.1f}%")
    print(f"   Sectores únicos: {len(set(a.sector for a in assets))}")
    
    # Optimizar
    try:
        optimizer = PortfolioOptimizer(assets)
        result = optimizer.optimize()
        optimizer.print_results(result)
        
        return result
        
    except Exception as e:
        print(f"❌ Error en optimización: {e}")
        return None

# Para ejecutar con datos de ejemplo
if __name__ == "__main__":
    # Ejecutar con datos de ejemplo
    result = run_optimization()
    
    # Para ejecutar con archivo CSV, usar:
    # result = run_optimization("tu_archivo.csv")