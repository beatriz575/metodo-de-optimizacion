import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import optuna

# Cargar y preparar datos
df = pd.read_excel("dataset_limpio_final.xlsx")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'], errors='coerce')
df['puntaje_matematica'] = pd.to_numeric(df['puntaje_matematica'], errors='coerce')

# Codificar variables categóricas
categorical_cols = ['sexo', 'lengua_materna', 'gestion', 'zona', 'nivel_socioeconomico', 'departamento']
df_encoded = pd.get_dummies(df, columns=categorical_cols)

# Variable objetivo
X = df_encoded.drop(columns=['puntaje_lectura', 'puntaje_matematica'])
y = df_encoded['puntaje_lectura']

# División del dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Función objetivo para Optuna
def objective(trial):
    n_estimators = trial.suggest_int("n_estimators", 50, 200)
    max_depth = trial.suggest_int("max_depth", 5, 20)

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse  # Queremos minimizar MSE

# Optimización con Optuna
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)
# Mejor modelo encontrado
best_params = study.best_params
best_model = RandomForestRegressor(
    n_estimators=best_params["n_estimators"],
    max_depth=best_params["max_depth"],
    random_state=42
)
best_model.fit(X_train, y_train)
y_pred = best_model.predict(X_test)

# Métricas finales
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n✅ Resultados del modelo optimizado con Optuna:")
print("Mejores hiperparámetros encontrados:", best_params)
print("MSE:", mse)
print("R²:", r2)
