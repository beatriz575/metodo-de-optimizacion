import pandas as pd
ruta = "Reporte del consumo de energía eléctrica (kWh-mes) - 202201 - 202501.csv"
df = pd.read_csv(ruta)

df_split = df.iloc[:, 0].str.split(",", expand=True)

df_split.columns = [
    "FECHA_CORTE", "FECHA_EMISION", "MES_FACTURACION", "COD_EMPRESA", "RAZON_SOCIAL",
    "GRUPO", "COD_SIS_ELECTR", "COD_TARIFA", "ATARIFA", "USO", "SUMINISTROS", "PROMEDIO_CONSUMO"
]

df_split["FECHA_EMISION"] = df_split["FECHA_EMISION"].str.replace('"', '')
df_split["MES_FACTURACION"] = df_split["MES_FACTURACION"].str.replace('"', '')
df_split["ATARIFA"] = df_split["ATARIFA"].str.strip().str.replace('"', '')

df_split["SUMINISTROS"] = pd.to_numeric(df_split["SUMINISTROS"], errors='coerce')
df_split["PROMEDIO_CONSUMO"] = pd.to_numeric(df_split["PROMEDIO_CONSUMO"], errors='coerce')

df_clean = df_split.dropna()

print(df_clean.info())
print(df_clean.head())

from sklearn.model_selection import train_test_split


y = df_clean["PROMEDIO_CONSUMO"]

X = df_clean.drop("PROMEDIO_CONSUMO", axis=1)

X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)

#########################################
from lazypredict.Supervised import LazyRegressor

reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)


models, predictions = reg.fit(X_train, X_test, y_train, y_test)


print("\n📊 Resultados de LazyPredict:\n")
print(models)

#######################################
import numpy as np

import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def objective(trial):
    n_estimators = trial.suggest_int("n_estimators", 50, 300)
    max_depth = trial.suggest_int("max_depth", 5, 30)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 10)
    min_samples_leaf = trial.suggest_int("min_samples_leaf", 1, 10)

    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return rmse


study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=30)

print("\n✅ Mejores hiperparámetros encontrados por Optuna:")
print(study.best_params)


best_model = RandomForestRegressor(**study.best_params, random_state=42)
best_model.fit(X_train, y_train)
from sklearn.metrics import mean_absolute_error, r2_score

preds = best_model.predict(X_test)
mse = mean_squared_error(y_test, preds)
rmse_final = np.sqrt(mse)
mae = mean_absolute_error(y_test, preds)
r2 = r2_score(y_test, preds)


print("\n📈 Evaluación del Modelo Optimizado:")
print(f"✅ RMSE: {rmse_final:.2f}")
print(f"✅ MAE:  {mae:.2f}")
print(f"✅ R²:   {r2:.4f}")

######################################

import matplotlib.pyplot as plt

# real vs predicho
plt.figure(figsize=(8, 6))
plt.scatter(y_test, preds, alpha=0.6, color='royalblue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r')
plt.xlabel("Valor Real")
plt.ylabel("Valor Predicho")
plt.title("📍 Real vs Predicho")
plt.grid(True)
plt.tight_layout()
plt.show()


errors = y_test - preds

plt.figure(figsize=(8, 5))
plt.hist(errors, bins=30, color='orange', edgecolor='black')
plt.xlabel("Error (Real - Predicho)")
plt.ylabel("Frecuencia")
plt.title("📊 Distribución del error de predicción")
plt.grid(True)
plt.tight_layout()
plt.show()

# linea temporal sie l orden imprta
plt.figure(figsize=(10, 6))
plt.plot(y_test.values[:50], label='Real', marker='o')
plt.plot(preds[:50], label='Predicho', marker='x')
plt.title("🕒 Predicción vs Real (primeras 50 muestras)")
plt.xlabel("Índice")
plt.ylabel("Consumo promedio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

####################
import optuna.visualization.matplotlib as optuna_vis

# Evolución del valor objetivo (RMSE) a lo largo de las iteraciones
optuna_vis.plot_optimization_history(study)
plt.title("📉 Evolución del RMSE durante la optimización")
plt.tight_layout()
plt.show()
#########################
optuna_vis.plot_param_importances(study)
plt.title("🧪 Importancia de los hiperparámetros")
plt.tight_layout()
plt.show()
###########################3
optuna.visualization.matplotlib.plot_slice(study, params=["n_estimators", "max_depth", "min_samples_split", "min_samples_leaf"])
plt.suptitle("📊 Efecto de cada hiperparámetro en el RMSE", fontsize=14)
plt.tight_layout()
plt.show()
