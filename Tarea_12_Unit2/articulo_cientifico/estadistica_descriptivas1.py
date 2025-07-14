import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración general
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (8, 5)

# Cargar dataset limpio
df = pd.read_excel("dataset_limpio_final.xlsx")

# Asegurar nombres de columnas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Asegurar que los puntajes son numéricos
df['puntaje_lectura'] = pd.to_numeric(df['puntaje_lectura'])
df['puntaje_matematica'] = pd.to_numeric(df['puntaje_matematica'])

# 1️⃣ Distribución de Puntajes
plt.figure()
sns.histplot(df['puntaje_lectura'], kde=True, bins=30, color='skyblue', label="Lectura")
sns.histplot(df['puntaje_matematica'], kde=True, bins=30, color='lightcoral', label="Matemática")
plt.title("Distribución de Puntajes en Lectura y Matemática")
plt.xlabel("Puntaje")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.show()

# 2️⃣ Rendimiento por Sexo (Boxplots combinados)
plt.figure()
df_melt = df.melt(id_vars="sexo", value_vars=["puntaje_lectura", "puntaje_matematica"],
                  var_name="área", value_name="puntaje")
sns.boxplot(x="sexo", y="puntaje", hue="área", data=df_melt, palette="pastel")
plt.title("Comparación de Puntajes por Sexo")
plt.ylabel("Puntaje")
plt.xlabel("Sexo")
plt.tight_layout()
plt.show()

# 3️⃣ Zona vs Lectura
plt.figure()
sns.boxplot(x="zona", y="puntaje_lectura", data=df, palette="muted")
plt.title("Puntaje en Lectura por Zona Geográfica")
plt.xlabel("Zona")
plt.ylabel("Puntaje de Lectura")
plt.tight_layout()
plt.show()

# 4️⃣ Nivel Socioeconómico vs Promedio de Puntajes
plt.figure()
df_melt2 = df.melt(id_vars="nivel_socioeconomico", value_vars=["puntaje_lectura", "puntaje_matematica"],
                   var_name="área", value_name="puntaje")
sns.barplot(x="nivel_socioeconomico", y="puntaje", hue="área", data=df_melt2,
            estimator="mean", ci=None, palette="Set2")
plt.title("Promedio de Puntajes según Nivel Socioeconómico")
plt.xlabel("Nivel Socioeconómico")
plt.ylabel("Puntaje Promedio")
plt.tight_layout()
plt.show()
