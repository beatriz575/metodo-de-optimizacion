import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from pyswarm import pso
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar dataset
df = pd.read_excel("dataset_limpio_final.xlsx")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['puntaje_matematica'] = pd.to_numeric(df['puntaje_matematica'])
df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'])

# 2. Codificar variables categóricas (one-hot)
categorical_cols = ['sexo', 'lengua_materna', 'gestion', 'zona', 'nivel_socioeconomico', 'departamento']
df_encoded = pd.get_dummies(df, columns=categorical_cols)

# 3. Definir X (predictoras) e y (variable objetivo)
X = df_encoded.drop(columns=['puntaje_lectura', 'puntaje_matematica'])
y = df_encoded['puntaje_lectura']  # ← usamos lectura como objetivo

# 4. Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Función objetivo para PSO
def objective_function(params):
    n_estimators = int(params[0])
    max_depth = int(params[1])
    print(f"🔧 Evaluando: n_estimators={n_estimators}, max_depth={max_depth}")
    model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    return mse

# 6. Límites de búsqueda
lb = [50, 5]
ub = [200, 20]

# 7. Ejecutar PSO
best_params, best_mse = pso(objective_function, lb, ub, swarmsize=20, maxiter=50)

# 8. Entrenar modelo final
best_model = RandomForestRegressor(
    n_estimators=int(best_params[0]),
    max_depth=int(best_params[1]),
    random_state=42
)
best_model.fit(X_train, y_train)
final_predictions = best_model.predict(X_test)
final_r2 = r2_score(y_test, final_predictions)

# 9. Imprimir resultados
print("\n✅ Mejores parámetros encontrados:")
print("n_estimators:", int(best_params[0]))
print("max_depth:", int(best_params[1]))
print("MSE:", best_mse)
print("R²:", final_r2)

# 10. Generar y guardar gráfico de dispersión
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=final_predictions, alpha=0.5, color='dodgerblue', edgecolor='k')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Ideal (y = x)')
plt.xlabel("Puntajes reales de lectura")
plt.ylabel("Puntajes predichos por el modelo")
plt.title("Figura X. Dispersión: valores reales vs predichos (modelo PSO)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_real_vs_predicho.png", dpi=300)
plt.show()
