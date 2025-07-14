import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import optuna
from pyswarm import pso
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import time
import openpyxl
warnings.filterwarnings('ignore')

class CrossValidationPSOOptuna:
    def __init__(self, excel_path, target_column='puntaje_lectura', random_state=42):
        """
        Inicializa la clase para validación cruzada con PSO y Optuna
        
        Parameters:
        -----------
        excel_path : str
            Ruta al archivo Excel con los datos
        target_column : str
            Variable objetivo ('puntaje_lectura' o 'puntaje_matematica')
        random_state : int
            Semilla para reproducibilidad
        """
        self.excel_path = excel_path
        self.target_column = target_column
        self.random_state = random_state
        self.results_pso = []
        self.results_optuna = []
        self.execution_times = {'pso': [], 'optuna': []}
        
        # Cargar y preparar datos
        self._load_data()
        self._prepare_data()
        
    def _load_data(self):
        """Carga los datos desde el archivo Excel"""
        print("Cargando datos desde Excel...")
        self.data = pd.read_excel(self.excel_path)
        print(f"Datos cargados: {self.data.shape[0]} filas, {self.data.shape[1]} columnas")
        
        # Mostrar información básica
        print("\nColumnas disponibles:")
        for i, col in enumerate(self.data.columns, 1):
            print(f"{i}. {col}")
            
    def _prepare_data(self):
        """Preprocesa los datos para el análisis"""
        print(f"\nPreparando datos para predecir: {self.target_column}")
        
        # Eliminar filas con valores faltantes en la variable objetivo
        initial_size = len(self.data)
        self.data = self.data.dropna(subset=[self.target_column])
        final_size = len(self.data)
        
        if initial_size != final_size:
            print(f"Se eliminaron {initial_size - final_size} filas con valores faltantes")
        
        # Definir características predictoras
        feature_columns = ['sexo', 'lengua_materna', 'gestion', 'zona', 
                          'nivel_socioeconomico', 'departamento']
        
        self.X = self.data[feature_columns].copy()
        self.y = self.data[self.target_column].copy()
        
        # Codificar variables categóricas
        self.label_encoders = {}
        for column in feature_columns:
            le = LabelEncoder()
            # Manejar valores faltantes
            self.X[column] = self.X[column].fillna('Missing')
            self.X[column] = le.fit_transform(self.X[column].astype(str))
            self.label_encoders[column] = le
                
        print(f"Dataset preparado: {self.X.shape[0]} muestras, {self.X.shape[1]} características")
        print(f"Variable objetivo: min={self.y.min():.2f}, max={self.y.max():.2f}, media={self.y.mean():.2f}")
        
    def pso_objective_function(self, params, X_train, y_train, X_val, y_val):
        """
        Función objetivo para PSO - Minimizar MSE en validación
        """
        n_estimators = int(np.clip(params[0], 10, 200))
        max_depth = int(np.clip(params[1], 3, 20))
        
        try:
            # Crear y entrenar modelo
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            return mean_squared_error(y_val, y_pred)
        except Exception as e:
            print(f"Error en PSO objective: {e}")
            return 1e6  # Penalización por error
    
    def optimize_with_pso(self, X_train, y_train, X_val, y_val):
        """
        Optimiza hiperparámetros usando PSO
        """
        print("   Ejecutando PSO...")
        start_time = time.time()
        
        # Definir límites para los parámetros
        lb = [10, 3]    # límites inferiores [n_estimators, max_depth]
        ub = [200, 20]  # límites superiores
        
        # Definir función objetivo para PSO
        def objective(params):
            return self.pso_objective_function(params, X_train, y_train, X_val, y_val)
        
        try:
            # Ejecutar PSO
            best_params, best_mse = pso(
                objective, 
                lb, ub,
                swarmsize=20,
                maxiter=50,
                debug=False
            )
            
            # Entrenar modelo final con mejores parámetros
            best_model = RandomForestRegressor(
                n_estimators=int(best_params[0]),
                max_depth=int(best_params[1]),
                random_state=self.random_state,
                n_jobs=-1
            )
            
            best_model.fit(X_train, y_train)
            y_pred = best_model.predict(X_val)
            
            execution_time = time.time() - start_time
            
            return {
                'n_estimators': int(best_params[0]),
                'max_depth': int(best_params[1]),
                'mse': mean_squared_error(y_val, y_pred),
                'mae': mean_absolute_error(y_val, y_pred),
                'r2': r2_score(y_val, y_pred),
                'execution_time': execution_time,
                'model': best_model
            }
        except Exception as e:
            print(f"Error en PSO: {e}")
            return None
    
    def optimize_with_optuna(self, X_train, y_train, X_val, y_val):
        """
        Optimiza hiperparámetros usando Optuna
        """
        print("   Ejecutando Optuna...")
        start_time = time.time()
        
        def objective(trial):
            n_estimators = trial.suggest_int('n_estimators', 10, 200)
            max_depth = trial.suggest_int('max_depth', 3, 20)
            
            model = RandomForestRegressor(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=self.random_state,
                n_jobs=-1
            )
            
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            return mean_squared_error(y_val, y_pred)
        
        try:
            # Crear y ejecutar estudio Optuna (silencioso)
            optuna.logging.set_verbosity(optuna.logging.WARNING)
            study = optuna.create_study(direction='minimize')
            study.optimize(objective, n_trials=100, show_progress_bar=False)
            
            # Entrenar modelo final con mejores parámetros
            best_params = study.best_params
            best_model = RandomForestRegressor(
                n_estimators=best_params['n_estimators'],
                max_depth=best_params['max_depth'],
                random_state=self.random_state,
                n_jobs=-1
            )
            
            best_model.fit(X_train, y_train)
            y_pred = best_model.predict(X_val)
            
            execution_time = time.time() - start_time
            
            return {
                'n_estimators': best_params['n_estimators'],
                'max_depth': best_params['max_depth'],
                'mse': mean_squared_error(y_val, y_pred),
                'mae': mean_absolute_error(y_val, y_pred),
                'r2': r2_score(y_val, y_pred),
                'execution_time': execution_time,
                'model': best_model
            }
        except Exception as e:
            print(f"Error en Optuna: {e}")
            return None
    
    def run_cross_validation(self, n_folds=5):
        """
        Ejecuta validación cruzada k-fold para ambos métodos
        """
        print(f"\n{'='*60}")
        print(f"INICIANDO VALIDACIÓN CRUZADA K-FOLD (k={n_folds})")
        print(f"Variable objetivo: {self.target_column}")
        print(f"Dataset: {self.X.shape[0]} muestras, {self.X.shape[1]} características")
        print(f"{'='*60}")
        
        # Configurar k-fold
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=self.random_state)
        
        fold = 1
        for train_idx, val_idx in kf.split(self.X):
            print(f"\n--- FOLD {fold}/{n_folds} ---")
            print(f"Entrenamiento: {len(train_idx)} muestras | Validación: {len(val_idx)} muestras")
            
            # Dividir datos
            X_train, X_val = self.X.iloc[train_idx], self.X.iloc[val_idx]
            y_train, y_val = self.y.iloc[train_idx], self.y.iloc[val_idx]
            
            # Optimizar con PSO
            pso_result = self.optimize_with_pso(X_train, y_train, X_val, y_val)
            if pso_result:
                pso_result['fold'] = fold
                self.results_pso.append(pso_result)
                self.execution_times['pso'].append(pso_result['execution_time'])
            
            # Optimizar con Optuna
            optuna_result = self.optimize_with_optuna(X_train, y_train, X_val, y_val)
            if optuna_result:
                optuna_result['fold'] = fold
                self.results_optuna.append(optuna_result)
                self.execution_times['optuna'].append(optuna_result['execution_time'])
            
            # Mostrar resultados del fold
            if pso_result and optuna_result:
                print(f"PSO    - MSE: {pso_result['mse']:.2f}, R²: {pso_result['r2']:.4f}, "
                      f"Tiempo: {pso_result['execution_time']:.1f}s")
                print(f"Optuna - MSE: {optuna_result['mse']:.2f}, R²: {optuna_result['r2']:.4f}, "
                      f"Tiempo: {optuna_result['execution_time']:.1f}s")
                
            fold += 1
            
        print(f"\n{'='*60}")
        print("¡VALIDACIÓN CRUZADA COMPLETADA!")
        print(f"{'='*60}")
        
    def analyze_results(self):
        """
        Analiza y compara los resultados de ambos métodos
        """
        if not self.results_pso or not self.results_optuna:
            print("Error: No hay resultados suficientes para el análisis")
            return None
            
        # Convertir resultados a DataFrames
        df_pso = pd.DataFrame(self.results_pso)
        df_optuna = pd.DataFrame(self.results_optuna)
        
        # Calcular estadísticas
        stats_pso = {
            'mse_mean': df_pso['mse'].mean(),
            'mse_std': df_pso['mse'].std(),
            'mae_mean': df_pso['mae'].mean(),
            'mae_std': df_pso['mae'].std(),
            'r2_mean': df_pso['r2'].mean(),
            'r2_std': df_pso['r2'].std(),
            'n_est_mean': df_pso['n_estimators'].mean(),
            'depth_mean': df_pso['max_depth'].mean(),
            'time_mean': df_pso['execution_time'].mean(),
            'time_std': df_pso['execution_time'].std()
        }
        
        stats_optuna = {
            'mse_mean': df_optuna['mse'].mean(),
            'mse_std': df_optuna['mse'].std(),
            'mae_mean': df_optuna['mae'].mean(),
            'mae_std': df_optuna['mae'].std(),
            'r2_mean': df_optuna['r2'].mean(),
            'r2_std': df_optuna['r2'].std(),
            'n_est_mean': df_optuna['n_estimators'].mean(),
            'depth_mean': df_optuna['max_depth'].mean(),
            'time_mean': df_optuna['execution_time'].mean(),
            'time_std': df_optuna['execution_time'].std()
        }
        
        # Pruebas estadísticas
        t_stat_mse, p_val_mse = stats.ttest_rel(df_pso['mse'], df_optuna['mse'])
        t_stat_r2, p_val_r2 = stats.ttest_rel(df_pso['r2'], df_optuna['r2'])
        t_stat_time, p_val_time = stats.ttest_rel(df_pso['execution_time'], df_optuna['execution_time'])
        
        # Intervalos de confianza (95%)
        def confidence_interval(data, confidence=0.95):
            n = len(data)
            mean = np.mean(data)
            sem = stats.sem(data)  # Standard error of mean
            h = sem * stats.t.ppf((1 + confidence) / 2., n-1)
            return mean - h, mean + h
        
        ci_pso_mse = confidence_interval(df_pso['mse'])
        ci_optuna_mse = confidence_interval(df_optuna['mse'])
        ci_pso_r2 = confidence_interval(df_pso['r2'])
        ci_optuna_r2 = confidence_interval(df_optuna['r2'])
        
        analysis_results = {
            'pso_stats': stats_pso,
            'optuna_stats': stats_optuna,
            'statistical_tests': {
                'mse_t_stat': t_stat_mse,
                'mse_p_value': p_val_mse,
                'r2_t_stat': t_stat_r2,
                'r2_p_value': p_val_r2,
                'time_t_stat': t_stat_time,
                'time_p_value': p_val_time
            },
            'confidence_intervals': {
                'pso_mse_ci': ci_pso_mse,
                'optuna_mse_ci': ci_optuna_mse,
                'pso_r2_ci': ci_pso_r2,
                'optuna_r2_ci': ci_optuna_r2
            },
            'raw_results': {
                'pso': df_pso,
                'optuna': df_optuna
            }
        }
        
        # Mostrar resumen
        self._print_summary(analysis_results)
        
        return analysis_results
    
    def _print_summary(self, results):
        """Imprime un resumen de los resultados"""
        pso_stats = results['pso_stats']
        optuna_stats = results['optuna_stats']
        tests = results['statistical_tests']
        
        print(f"\n{'='*60}")
        print("RESUMEN DE RESULTADOS - VALIDACIÓN CRUZADA")
        print(f"{'='*60}")
        
        print(f"\nPSO:")
        print(f"  MSE: {pso_stats['mse_mean']:.2f} ± {pso_stats['mse_std']:.2f}")
        print(f"  R²:  {pso_stats['r2_mean']:.4f} ± {pso_stats['r2_std']:.4f}")
        print(f"  MAE: {pso_stats['mae_mean']:.2f} ± {pso_stats['mae_std']:.2f}")
        print(f"  Tiempo: {pso_stats['time_mean']:.1f} ± {pso_stats['time_std']:.1f} segundos")
        print(f"  Parámetros promedio: n_est={pso_stats['n_est_mean']:.0f}, depth={pso_stats['depth_mean']:.1f}")
        
        print(f"\nOptuna:")
        print(f"  MSE: {optuna_stats['mse_mean']:.2f} ± {optuna_stats['mse_std']:.2f}")
        print(f"  R²:  {optuna_stats['r2_mean']:.4f} ± {optuna_stats['r2_std']:.4f}")
        print(f"  MAE: {optuna_stats['mae_mean']:.2f} ± {optuna_stats['mae_std']:.2f}")
        print(f"  Tiempo: {optuna_stats['time_mean']:.1f} ± {optuna_stats['time_std']:.1f} segundos")
        print(f"  Parámetros promedio: n_est={optuna_stats['n_est_mean']:.0f}, depth={optuna_stats['depth_mean']:.1f}")
        
        print(f"\nPRUEBAS ESTADÍSTICAS:")
        print(f"  MSE - t-test: t={tests['mse_t_stat']:.3f}, p={tests['mse_p_value']:.3f}")
        print(f"  R²  - t-test: t={tests['r2_t_stat']:.3f}, p={tests['r2_p_value']:.3f}")
        print(f"  Tiempo - t-test: t={tests['time_t_stat']:.3f}, p={tests['time_p_value']:.3f}")
        
        # Interpretación
        print(f"\nINTERPRETACIÓN:")
        if tests['mse_p_value'] > 0.05:
            print("  ✓ No hay diferencia significativa en MSE entre métodos (p > 0.05)")
        else:
            print("  ⚠ Hay diferencia significativa en MSE entre métodos (p ≤ 0.05)")
            
        if tests['r2_p_value'] > 0.05:
            print("  ✓ No hay diferencia significativa en R² entre métodos (p > 0.05)")
        else:
            print("  ⚠ Hay diferencia significativa en R² entre métodos (p ≤ 0.05)")
            
    def create_comparison_plots(self, save_path=None):
        """
        Crea gráficos comparativos de los resultados
        """
        if not self.results_pso or not self.results_optuna:
            print("Error: No hay datos suficientes para crear gráficos")
            return
            
        # Preparar datos para plotting
        df_pso = pd.DataFrame(self.results_pso)
        df_optuna = pd.DataFrame(self.results_optuna)
        
        # Combinar datos para plotting
        df_pso['method'] = 'PSO'
        df_optuna['method'] = 'Optuna'
        df_combined = pd.concat([df_pso, df_optuna], ignore_index=True)
        
        # Configurar estilo
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Crear subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Comparación PSO vs Optuna - Validación Cruzada\nVariable objetivo: {self.target_column}', 
                     fontsize=16, fontweight='bold')
        
        # MSE Boxplot
        sns.boxplot(data=df_combined, x='method', y='mse', ax=axes[0,0])
        axes[0,0].set_title('Distribución de MSE')
        axes[0,0].set_ylabel('MSE')
        
        # R² Boxplot
        sns.boxplot(data=df_combined, x='method', y='r2', ax=axes[0,1])
        axes[0,1].set_title('Distribución de R²')
        axes[0,1].set_ylabel('R²')
        
        # Tiempo de ejecución
        sns.boxplot(data=df_combined, x='method', y='execution_time', ax=axes[0,2])
        axes[0,2].set_title('Tiempo de Ejecución')
        axes[0,2].set_ylabel('Tiempo (segundos)')
        
        # MSE por fold
        axes[1,0].plot(df_pso['fold'], df_pso['mse'], 'o-', label='PSO', linewidth=2, markersize=8)
        axes[1,0].plot(df_optuna['fold'], df_optuna['mse'], 's-', label='Optuna', linewidth=2, markersize=8)
        axes[1,0].set_title('MSE por Fold')
        axes[1,0].set_xlabel('Fold')
        axes[1,0].set_ylabel('MSE')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # R² por fold
        axes[1,1].plot(df_pso['fold'], df_pso['r2'], 'o-', label='PSO', linewidth=2, markersize=8)
        axes[1,1].plot(df_optuna['fold'], df_optuna['r2'], 's-', label='Optuna', linewidth=2, markersize=8)
        axes[1,1].set_title('R² por Fold')
        axes[1,1].set_xlabel('Fold')
        axes[1,1].set_ylabel('R²')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
        
        # Hiperparámetros - n_estimators
        axes[1,2].scatter(df_pso['n_estimators'], df_pso['mse'], alpha=0.7, label='PSO', s=60)
        axes[1,2].scatter(df_optuna['n_estimators'], df_optuna['mse'], alpha=0.7, label='Optuna', s=60)
        axes[1,2].set_title('MSE vs n_estimators')
        axes[1,2].set_xlabel('n_estimators')
        axes[1,2].set_ylabel('MSE')
        axes[1,2].legend()
        axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráficos guardados en: {save_path}")
        plt.show()
        
    def generate_latex_table(self):
        """
        Genera tablas en formato LaTeX con los resultados
        """
        if not self.results_pso or not self.results_optuna:
            return "Error: No hay datos suficientes"
            
        analysis = self.analyze_results()
        pso_stats = analysis['pso_stats']
        optuna_stats = analysis['optuna_stats']
        tests = analysis['statistical_tests']
        ci = analysis['confidence_intervals']
        
        # Tabla principal de resultados
        latex_main = f"""
\\begin{{table}}[H]
\\centering
\\caption{{Resultados de validación cruzada k-fold (k=5) para PSO y Optuna - {self.target_column.replace('_', ' ').title()}}}
\\begin{{tabular}}{{|l|c|c|c|c|c|}}
\\hline
\\textbf{{Método}} & \\textbf{{MSE (μ ± σ)}} & \\textbf{{R² (μ ± σ)}} & \\textbf{{MAE (μ ± σ)}} & \\textbf{{n\\_est (μ)}} & \\textbf{{depth (μ)}} \\\\
\\hline
PSO & {pso_stats['mse_mean']:.1f} ± {pso_stats['mse_std']:.1f} & {pso_stats['r2_mean']:.4f} ± {pso_stats['r2_std']:.4f} & {pso_stats['mae_mean']:.1f} ± {pso_stats['mae_std']:.1f} & {pso_stats['n_est_mean']:.0f} & {pso_stats['depth_mean']:.1f} \\\\
Optuna & {optuna_stats['mse_mean']:.1f} ± {optuna_stats['mse_std']:.1f} & {optuna_stats['r2_mean']:.4f} ± {optuna_stats['r2_std']:.4f} & {optuna_stats['mae_mean']:.1f} ± {optuna_stats['mae_std']:.1f} & {optuna_stats['n_est_mean']:.0f} & {optuna_stats['depth_mean']:.1f} \\\\
\\hline
\\multicolumn{{6}}{{|l|}}{{\\textbf{{Análisis estadístico (pruebas t pareadas):}}}} \\\\
\\multicolumn{{6}}{{|l|}}{{MSE: t = {tests['mse_t_stat']:.3f}, p = {tests['mse_p_value']:.3f}}} \\\\
\\multicolumn{{6}}{{|l|}}{{R²: t = {tests['r2_t_stat']:.3f}, p = {tests['r2_p_value']:.3f}}} \\\\
\\multicolumn{{6}}{{|l|}}{{Tiempo: t = {tests['time_t_stat']:.3f}, p = {tests['time_p_value']:.3f}}} \\\\
\\hline
\\end{{tabular}}
\\label{{tab:cross_validation_results_{self.target_column}}}
\\end{{table}}
        """
        
        # Tabla de intervalos de confianza
        latex_ci = f"""
\\begin{{table}}[H]
\\centering
\\caption{{Intervalos de confianza (95\\%) para las métricas de rendimiento}}
\\begin{{tabular}}{{|l|c|c|}}
\\hline
\\textbf{{Método}} & \\textbf{{MSE [IC 95\\%]}} & \\textbf{{R² [IC 95\\%]}} \\\\
\\hline
PSO & [{ci['pso_mse_ci'][0]:.1f}, {ci['pso_mse_ci'][1]:.1f}] & [{ci['pso_r2_ci'][0]:.4f}, {ci['pso_r2_ci'][1]:.4f}] \\\\
Optuna & [{ci['optuna_mse_ci'][0]:.1f}, {ci['optuna_mse_ci'][1]:.1f}] & [{ci['optuna_r2_ci'][0]:.4f}, {ci['optuna_r2_ci'][1]:.4f}] \\\\
\\hline
\\end{{tabular}}
\\label{{tab:confidence_intervals_{self.target_column}}}
\\end{{table}}
        """
        
        return latex_main, latex_ci

def main():
    """
    Función principal para ejecutar el análisis completo
    """
    print("="*80)
    print("ANÁLISIS DE VALIDACIÓN CRUZADA - PSO vs OPTUNA")
    print("Dataset: Evaluación Muestral 2022 - MINEDU Perú")
    print("="*80)
    
    # Ruta al archivo Excel
    excel_path = 'dataset_limpio_final.xlsx'
    
    # Ejecutar análisis para puntaje de lectura
    print("\n" + "="*40)
    print("ANÁLISIS PARA PUNTAJE DE LECTURA")
    print("="*40)
    
    cv_lectura = CrossValidationPSOOptuna(excel_path, 'puntaje_lectura')
    cv_lectura.run_cross_validation(n_folds=5)
    results_lectura = cv_lectura.analyze_results()
    
    # Crear gráficos
    cv_lectura.create_comparison_plots('validacion_cruzada_lectura.png')
    
    # Generar tablas LaTeX
    latex_main_lectura, latex_ci_lectura = cv_lectura.generate_latex_table()
    
    # Opcionalmente, ejecutar también para matemática
    ejecutar_matematica = input("\n¿Deseas ejecutar también el análisis para matemática? (s/n): ").lower().strip()
    
    if ejecutar_matematica == 's':
        print("\n" + "="*40)
        print("ANÁLISIS PARA PUNTAJE DE MATEMÁTICA")
        print("="*40)
        
        cv_matematica = CrossValidationPSOOptuna(excel_path, 'puntaje_matematica')
        cv_matematica.run_cross_validation(n_folds=5)
        results_matematica = cv_matematica.analyze_results()
        
        # Crear gráficos
        cv_matematica.create_comparison_plots('validacion_cruzada_matematica.png')
        
        # Generar tablas LaTeX
        latex_main_matematica, latex_ci_matematica = cv_matematica.generate_latex_table()
        
        print("\n" + "="*60)
        print("TABLAS LATEX PARA MATEMÁTICA:")
        print("="*60)
        print(latex_main_matematica)
        print(latex_ci_matematica)
    
    # Mostrar tablas LaTeX para lectura
    print("\n" + "="*60)
    print("TABLAS LATEX PARA LECTURA:")
    print("="*60)
    print(latex_main_lectura)
    print(latex_ci_lectura)
    
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("Archivos generados:")
    print("- validacion_cruzada_lectura.png")
    if ejecutar_matematica == 's':
        print("- validacion_cruzada_matematica.png")
    print("="*80)
    
    return results_lectura

if __name__ == "__main__":
    results = main()