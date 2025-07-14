import pandas as pd

# Cargar dataset ya limpio
df = pd.read_excel("dataset_limpio_final.xlsx")

# Asegurar que los nombres están bien formateados
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# 1️⃣ Estadísticas para variables numéricas
print("🔢 Estadísticas descriptivas para 'puntaje_lectura' y 'puntaje_matematica':")
print(df[['puntaje_lectura', 'puntaje_matematica']].describe())

# Coeficiente de variación
cv_lectura = df['puntaje_lectura'].std() / df['puntaje_lectura'].mean()
cv_matematica = df['puntaje_matematica'].std() / df['puntaje_matematica'].mean()
print(f"\n📈 Coeficiente de variación:")
print(f"Lectura: {cv_lectura:.4f}")
print(f"Matemática: {cv_matematica:.4f}")

# 2️⃣ Estadísticas para variables categóricas
categorical_cols = [
    'sexo', 'lengua_materna', 'gestion',
    'zona', 'nivel_socioeconomico', 'departamento'
]

for col in categorical_cols:
    print(f"\n📊 Frecuencia de '{col}':")
    print(df[col].value_counts())
    
    print(f"\n📉 Porcentaje de '{col}':")
    print((df[col].value_counts(normalize=True) * 100).round(2))
