import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_excel("dataset_limpio_final.xlsx")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'], errors='coerce')

# Agrupar por departamento
departamento_mean = df.groupby("departamento")["puntaje_lectura"].mean().sort_values(ascending=False)

# Mostrar tabla en consola
print("\n📊 Promedio de puntaje en lectura por departamento:")
print(departamento_mean)

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
departamento_mean.plot(kind="bar", color="mediumseagreen", edgecolor="black")
plt.ylabel("Promedio de Puntaje en Lectura")
plt.title("Promedio de Puntaje en Lectura por Departamento")
plt.xticks(rotation=90)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("grafico_departamento_lectura.png", dpi=300)
plt.show()
