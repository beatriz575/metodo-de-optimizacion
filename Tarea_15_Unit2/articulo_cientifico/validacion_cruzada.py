import pandas as pd
import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import optuna
from pyswarm import pso
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Cargar y preparar datos
def load_and_prepare_data():
    df = pd.read_excel("C:/beatrizumiña/metodo-de-optimizacion/Tarea_15_Unit2/articulo_cientifico/dataset_limpio_final.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Limpiar datos - ahora incluimos tanto lectura como matemática
    df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'], errors='coerce')
    df['puntaje_matematica'] = pd.to_numeric(df['puntaje_matematica'], errors='coerce')
    
    # Eliminar filas con valores faltantes en las variables objetivo
    df = df.dropna(subset=['puntaje_lectura', 'puntaje_matematica'])
    
    # Variables predictoras según tu paper
    categorical_vars = [
        'sexo', 
        'lengua_materna', 
        'gestion', 
        'zona', 
        'nivel_socioeconomico',  # Cambiado de 'niv_socioec' según tu paper
        'departamento'
    ]
    
    # Verificar qué columnas existen realmente
    available_vars = [var for var in categorical_vars if var in df.columns]
    missing_vars = [var for var in categorical_vars if var not in df.columns]
    
    print(f"Variables disponibles: {available_vars}")
    if missing_vars:
        print(f"Variables faltantes: {missing_vars}")
        print(f"Columnas disponibles en el dataset: {list(df.columns)}")
    
    # Codificar variables categóricas
    le_dict = {}
    for var in available_vars:
        le = LabelEncoder()
        df[var] = le.fit_transform(df[var].astype(str))
        le_dict[var] = le
    
    # Preparar X e y para ambas variables objetivo
    X = df[available_vars]
    y_lectura = df['puntaje_lectura']
    y_matematica = df['puntaje_matematica']
    
    return X, y_lectura, y_matematica, le_dict, available_vars

# Función objetivo para PSO
def pso_objective(params, X, y, cv_folds):
    n_estimators = int(params[0])
    max_depth = int(params[1])
    
    try:
        rf = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
        
        scores = cross_val_score(rf, X, y, cv=cv_folds, 
                               scoring='neg_mean_squared_error', n_jobs=-1)
        return -scores.mean()  # PSO minimiza, por eso negativo
    except Exception as e:
        print(f"Error en PSO objective: {e}")
        return 10000  # Penalización por error

# Optimización con PSO usando validación cruzada
def optimize_with_pso(X, y, cv_folds, n_particles=20, max_iter=50):
    print("Optimizando con PSO...")
    
    # Definir límites de búsqueda
    lower_bounds = [10, 3]     # n_estimators_min, max_depth_min
    upper_bounds = [200, 20]   # n_estimators_max, max_depth_max
    
    # Optimización PSO
    def objective_wrapper(params):
        return pso_objective(params, X, y, cv_folds)
    
    try:
        best_params, best_score = pso(objective_wrapper, lower_bounds, upper_bounds,
                                      swarmsize=n_particles, maxiter=max_iter)
        
        best_n_estimators = int(best_params[0])
        best_max_depth = int(best_params[1])
        
        return {
            'n_estimators': best_n_estimators,
            'max_depth': best_max_depth,
            'cv_score': best_score
        }
    except Exception as e:
        print(f"Error en PSO optimization: {e}")
        # Retornar valores por defecto si falla
        return {
            'n_estimators': 100,
            'max_depth': 10,
            'cv_score': 10000.0
        }

# Función objetivo para Optuna
def optuna_objective(trial, X, y, cv_folds):
    n_estimators = trial.suggest_int('n_estimators', 10, 200)
    max_depth = trial.suggest_int('max_depth', 3, 20)
    
    try:
        rf = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
            n_jobs=-1
        )
        
        scores = cross_val_score(rf, X, y, cv=cv_folds, 
                               scoring='neg_mean_squared_error', n_jobs=-1)
        return -scores.mean()
    except Exception as e:
        print(f"Error en Optuna objective: {e}")
        return 10000.0

# Optimización con Optuna usando validación cruzada
def optimize_with_optuna(X, y, cv_folds, n_trials=100):
    print("Optimizando con Optuna...")
    
    try:
        # Suprimir logs de Optuna
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        
        study = optuna.create_study(direction='minimize')
        study.optimize(lambda trial: optuna_objective(trial, X, y, cv_folds), 
                       n_trials=n_trials)
        
        return {
            'n_estimators': study.best_params['n_estimators'],
            'max_depth': study.best_params['max_depth'],
            'cv_score': study.best_value
        }
    except Exception as e:
        print(f"Error en Optuna optimization: {e}")
        # Retornar valores por defecto si falla
        return {
            'n_estimators': 50,
            'max_depth': 7,
            'cv_score': 10000.0
        }

# Evaluación detallada con validación cruzada
def detailed_cv_evaluation(X, y, params, method_name, n_folds=5):
    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)
    
    mse_scores = []
    r2_scores = []
    
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        rf = RandomForestRegressor(
            n_estimators=params['n_estimators'],
            max_depth=params['max_depth'],
            random_state=42,
            n_jobs=-1
        )
        
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_test)
        
        mse_scores.append(mean_squared_error(y_test, y_pred))
        r2_scores.append(r2_score(y_test, y_pred))
    
    return {
        'method': method_name,
        'mse_mean': np.mean(mse_scores),
        'mse_std': np.std(mse_scores),
        'r2_mean': np.mean(r2_scores),
        'r2_std': np.std(r2_scores),
        'mse_scores': mse_scores,
        'r2_scores': r2_scores,
        'params': params
    }

# Análisis estadístico de significancia
def statistical_analysis(pso_results, optuna_results):
    try:
        # Test t para diferencias en MSE
        t_stat_mse, p_val_mse = stats.ttest_rel(pso_results['mse_scores'], 
                                               optuna_results['mse_scores'])
        
        # Test t para diferencias en R²
        t_stat_r2, p_val_r2 = stats.ttest_rel(pso_results['r2_scores'], 
                                             optuna_results['r2_scores'])
        
        return {
            'mse_ttest': {'t_stat': t_stat_mse, 'p_value': p_val_mse},
            'r2_ttest': {'t_stat': t_stat_r2, 'p_value': p_val_r2}
        }
    except Exception as e:
        print(f"Error en análisis estadístico: {e}")
        return {
            'mse_ttest': {'t_stat': 0.0, 'p_value': 1.0},
            'r2_ttest': {'t_stat': 0.0, 'p_value': 1.0}
        }

# Estadísticas descriptivas
def calcular_estadisticas_descriptivas(df):
    """Calcula estadísticas descriptivas para lectura y matemática"""
    estadisticas = {}
    
    for materia in ['puntaje_lectura', 'puntaje_matematica']:
        if materia in df.columns:
            serie = pd.to_numeric(df[materia], errors='coerce').dropna()
            
            estadisticas[materia] = {
                'n': len(serie),
                'media': serie.mean(),
                'std': serie.std(),
                'min': serie.min(),
                'q25': serie.quantile(0.25),
                'mediana': serie.median(),
                'q75': serie.quantile(0.75),
                'max': serie.max(),
                'cv': serie.std() / serie.mean()
            }
    
    return estadisticas

# Análisis por variables categóricas
def analisis_por_categorias(df, variables_disponibles):
    """Realiza análisis descriptivo por categorías"""
    resultados = {}
    
    for var in variables_disponibles:
        if var in df.columns:
            print(f"\n--- Análisis por {var.upper()} ---")
            
            # Para lectura
            if 'puntaje_lectura' in df.columns:
                grupo_lectura = df.groupby(var)['puntaje_lectura'].agg(['mean', 'std', 'count'])
                print(f"Lectura por {var}:")
                print(grupo_lectura.round(2))
                resultados[f'{var}_lectura'] = grupo_lectura
            
            # Para matemática
            if 'puntaje_matematica' in df.columns:
                grupo_matematica = df.groupby(var)['puntaje_matematica'].agg(['mean', 'std', 'count'])
                print(f"Matemática por {var}:")
                print(grupo_matematica.round(2))
                resultados[f'{var}_matematica'] = grupo_matematica
    
    return resultados

# Función principal mejorada
def main():
    try:
        # Cargar datos
        X, y_lectura, y_matematica, le_dict, variables_disponibles = load_and_prepare_data()
        print(f"Dataset cargado: {X.shape[0]} muestras, {X.shape[1]} características")
        print(f"Variables utilizadas: {variables_disponibles}")
        
        # Cargar dataframe original para estadísticas descriptivas
        df_original = pd.read_excel("C:/beatrizumiña/metodo-de-optimizacion/Tarea_15_Unit2/articulo_cientifico/dataset_limpio_final.xlsx")
        df_original.columns = df_original.columns.str.strip().str.lower().str.replace(" ", "_")
        
        # Estadísticas descriptivas
        print("\n" + "="*60)
        print("ESTADÍSTICAS DESCRIPTIVAS")
        print("="*60)
        
        estadisticas = calcular_estadisticas_descriptivas(df_original)
        for materia, stats in estadisticas.items():
            print(f"\n{materia.upper().replace('_', ' ')}:")
            print(f"  n: {stats['n']}")
            print(f"  Media: {stats['media']:.2f}")
            print(f"  Desv. Estándar: {stats['std']:.2f}")
            print(f"  Mínimo: {stats['min']:.2f}")
            print(f"  Q1: {stats['q25']:.2f}")
            print(f"  Mediana: {stats['mediana']:.2f}")
            print(f"  Q3: {stats['q75']:.2f}")
            print(f"  Máximo: {stats['max']:.2f}")
            print(f"  Coef. Variación: {stats['cv']:.4f}")
        
        # Análisis por categorías
        print("\n" + "="*60)
        print("ANÁLISIS POR CATEGORÍAS")
        print("="*60)
        analisis_categorias = analisis_por_categorias(df_original, variables_disponibles)
        
        # Configurar validación cruzada
        cv_folds = KFold(n_splits=5, shuffle=True, random_state=42)
        
        # ========== ANÁLISIS PARA LECTURA ==========
        print("\n" + "="*60)
        print("OPTIMIZACIÓN PARA PUNTAJE DE LECTURA")
        print("="*60)
        
        # Optimizar con PSO para lectura
        pso_best_lectura = optimize_with_pso(X, y_lectura, cv_folds)
        print(f"PSO Lectura - Mejores parámetros: {pso_best_lectura}")
        
        # Optimizar con Optuna para lectura
        optuna_best_lectura = optimize_with_optuna(X, y_lectura, cv_folds, n_trials=50)
        print(f"Optuna Lectura - Mejores parámetros: {optuna_best_lectura}")
        
        # Evaluación detallada para lectura
        print("Realizando evaluación detallada para lectura...")
        pso_results_lectura = detailed_cv_evaluation(X, y_lectura, pso_best_lectura, "PSO")
        optuna_results_lectura = detailed_cv_evaluation(X, y_lectura, optuna_best_lectura, "Optuna")
        
        # Análisis estadístico para lectura
        stats_results_lectura = statistical_analysis(pso_results_lectura, optuna_results_lectura)
        
        # ========== ANÁLISIS PARA MATEMÁTICA ==========
        print("\n" + "="*60)
        print("OPTIMIZACIÓN PARA PUNTAJE DE MATEMÁTICA")
        print("="*60)
        
        # Optimizar con PSO para matemática
        pso_best_matematica = optimize_with_pso(X, y_matematica, cv_folds)
        print(f"PSO Matemática - Mejores parámetros: {pso_best_matematica}")
        
        # Optimizar con Optuna para matemática
        optuna_best_matematica = optimize_with_optuna(X, y_matematica, cv_folds, n_trials=50)
        print(f"Optuna Matemática - Mejores parámetros: {optuna_best_matematica}")
        
        # Evaluación detallada para matemática
        print("Realizando evaluación detallada para matemática...")
        pso_results_matematica = detailed_cv_evaluation(X, y_matematica, pso_best_matematica, "PSO")
        optuna_results_matematica = detailed_cv_evaluation(X, y_matematica, optuna_best_matematica, "Optuna")
        
        # Análisis estadístico para matemática
        stats_results_matematica = statistical_analysis(pso_results_matematica, optuna_results_matematica)
        
        # ========== IMPRIMIR RESULTADOS FINALES ==========
        print("\n" + "="*80)
        print("RESULTADOS FINALES DE VALIDACIÓN CRUZADA")
        print("="*80)
        
        # Resultados para Lectura
        print("\n" + "-"*40)
        print("PUNTAJE DE LECTURA")
        print("-"*40)
        
        print(f"\nPSO:")
        print(f"  MSE: {pso_results_lectura['mse_mean']:.2f} ± {pso_results_lectura['mse_std']:.2f}")
        print(f"  R²: {pso_results_lectura['r2_mean']:.4f} ± {pso_results_lectura['r2_std']:.4f}")
        print(f"  Parámetros: n_estimators={pso_results_lectura['params']['n_estimators']}, max_depth={pso_results_lectura['params']['max_depth']}")
        
        print(f"\nOptuna:")
        print(f"  MSE: {optuna_results_lectura['mse_mean']:.2f} ± {optuna_results_lectura['mse_std']:.2f}")
        print(f"  R²: {optuna_results_lectura['r2_mean']:.4f} ± {optuna_results_lectura['r2_std']:.4f}")
        print(f"  Parámetros: n_estimators={optuna_results_lectura['params']['n_estimators']}, max_depth={optuna_results_lectura['params']['max_depth']}")
        
        print(f"\nAnálisis Estadístico (Lectura):")
        print(f"  Diferencia en MSE - t-stat: {stats_results_lectura['mse_ttest']['t_stat']:.4f}, p-value: {stats_results_lectura['mse_ttest']['p_value']:.4f}")
        print(f"  Diferencia en R² - t-stat: {stats_results_lectura['r2_ttest']['t_stat']:.4f}, p-value: {stats_results_lectura['r2_ttest']['p_value']:.4f}")
        
        # Resultados para Matemática
        print("\n" + "-"*40)
        print("PUNTAJE DE MATEMÁTICA")
        print("-"*40)
        
        print(f"\nPSO:")
        print(f"  MSE: {pso_results_matematica['mse_mean']:.2f} ± {pso_results_matematica['mse_std']:.2f}")
        print(f"  R²: {pso_results_matematica['r2_mean']:.4f} ± {pso_results_matematica['r2_std']:.4f}")
        print(f"  Parámetros: n_estimators={pso_results_matematica['params']['n_estimators']}, max_depth={pso_results_matematica['params']['max_depth']}")
        
        print(f"\nOptuna:")
        print(f"  MSE: {optuna_results_matematica['mse_mean']:.2f} ± {optuna_results_matematica['mse_std']:.2f}")
        print(f"  R²: {optuna_results_matematica['r2_mean']:.4f} ± {optuna_results_matematica['r2_std']:.4f}")
        print(f"  Parámetros: n_estimators={optuna_results_matematica['params']['n_estimators']}, max_depth={optuna_results_matematica['params']['max_depth']}")
        
        print(f"\nAnálisis Estadístico (Matemática):")
        print(f"  Diferencia en MSE - t-stat: {stats_results_matematica['mse_ttest']['t_stat']:.4f}, p-value: {stats_results_matematica['mse_ttest']['p_value']:.4f}")
        print(f"  Diferencia en R² - t-stat: {stats_results_matematica['r2_ttest']['t_stat']:.4f}, p-value: {stats_results_matematica['r2_ttest']['p_value']:.4f}")
        
        # Interpretación de resultados
        print(f"\n" + "="*60)
        print("INTERPRETACIÓN DE RESULTADOS")
        print("="*60)
        
        alpha = 0.05
        
        print("\nLECTURA:")
        if stats_results_lectura['mse_ttest']['p_value'] < alpha:
            print(f"  Existe diferencia estadísticamente significativa en MSE (p < {alpha})")
        else:
            print(f"  No existe diferencia estadísticamente significativa en MSE (p ≥ {alpha})")
            
        if stats_results_lectura['r2_ttest']['p_value'] < alpha:
            print(f"  Existe diferencia estadísticamente significativa en R² (p < {alpha})")
        else:
            print(f"  No existe diferencia estadísticamente significativa en R² (p ≥ {alpha})")
        
        print("\nMATEMÁTICA:")
        if stats_results_matematica['mse_ttest']['p_value'] < alpha:
            print(f"  Existe diferencia estadísticamente significativa en MSE (p < {alpha})")
        else:
            print(f"  No existe diferencia estadísticamente significativa en MSE (p ≥ {alpha})")
            
        if stats_results_matematica['r2_ttest']['p_value'] < alpha:
            print(f"  Existe diferencia estadísticamente significativa en R² (p < {alpha})")
        else:
            print(f"  No existe diferencia estadísticamente significativa en R² (p ≥ {alpha})")
        
        # Resumen final
        print(f"\n" + "="*60)
        print("RESUMEN EJECUTIVO")
        print("="*60)
        
        mejor_lectura = "PSO" if pso_results_lectura['r2_mean'] > optuna_results_lectura['r2_mean'] else "Optuna"
        mejor_matematica = "PSO" if pso_results_matematica['r2_mean'] > optuna_results_matematica['r2_mean'] else "Optuna"
        
        print(f"Mejor rendimiento en Lectura: {mejor_lectura}")
        print(f"Mejor rendimiento en Matemática: {mejor_matematica}")
        
        # Calcular eficiencia computacional
        eficiencia_lectura_pso = pso_results_lectura['params']['n_estimators']
        eficiencia_lectura_optuna = optuna_results_lectura['params']['n_estimators']
        eficiencia_matematica_pso = pso_results_matematica['params']['n_estimators']
        eficiencia_matematica_optuna = optuna_results_matematica['params']['n_estimators']
        
        print(f"\nEficiencia Computacional:")
        print(f"  Lectura - PSO: {eficiencia_lectura_pso} árboles, Optuna: {eficiencia_lectura_optuna} árboles")
        print(f"  Matemática - PSO: {eficiencia_matematica_pso} árboles, Optuna: {eficiencia_matematica_optuna} árboles")
        
        return {
            'lectura': {
                'pso': pso_results_lectura,
                'optuna': optuna_results_lectura,
                'stats': stats_results_lectura
            },
            'matematica': {
                'pso': pso_results_matematica,
                'optuna': optuna_results_matematica,
                'stats': stats_results_matematica
            },
            'estadisticas_descriptivas': estadisticas,
            'analisis_categorias': analisis_categorias
        }
        
    except Exception as e:
        print(f"Error en función main: {e}")
        return None

if __name__ == "__main__":
    resultados_completos = main()