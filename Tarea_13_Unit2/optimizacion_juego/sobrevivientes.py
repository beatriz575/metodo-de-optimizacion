import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter

# Tipos de dulces disponibles
DULCES = ["limon", "pera", "huevo"]

# Repartir 2 dulces a cada estudiante
def repartir_dulces_estudiantes(n):
    return [random.choices(DULCES, k=2) for _ in range(n)]

# NIVEL 1 - Individual con cooperación detallada
def optimizar_nivel_1(estudiantes):
    total_dulces = sum(estudiantes, [])
    texto = ""
    for i, dulces in enumerate(estudiantes):
        texto += f"🎒 Estudiante {i+1}: {dulces}\n"

    disponibles = {i: set(dulces) for i, dulces in enumerate(estudiantes)}
    usados = set()
    sobrevivientes = []
    comodines = []
    historial = []

    # Buscar combinaciones entre pares
    for i in range(len(estudiantes)):
        if i in usados:
            continue
        propios = disponibles[i]
        for j in range(len(estudiantes)):
            if i == j or j in usados:
                continue
            combinados = propios | disponibles[j]
            if set(DULCES).issubset(combinados):
                faltantes = set(DULCES) - propios
                historial.append(
                    f"\n✅ Estudiante {i+1} sobrevivió al intercambiar con Estudiante {j+1}.\n"
                    f"   🔄 Intercambio: obtuvo {list(faltantes)} de Est. {j+1}\n"
                    f"   🍭 Obtuvo un chupetín y un comodín.\n"
                )
                sobrevivientes.append(i)
                usados.add(i)
                usados.add(j)
                comodines.append(i)
                break

    # Usar comodines para ayudar a otros
    ayudados = set()
    for i in comodines:
        for j in range(len(estudiantes)):
            if j in usados or j in ayudados:
                continue
            actuales = disponibles[j]
            faltantes = list(set(DULCES) - actuales)
            if faltantes:
                dulce_dado = faltantes[0]
                disponibles[j].add(dulce_dado)
                historial.append(
                    f"🎁 Est. {i+1} usó su comodín para dar '{dulce_dado}' a Est. {j+1}.\n"
                )
                ayudados.add(j)
                break

    # Verificar si los ayudados sobrevivieron
    for j in ayudados:
        if set(DULCES).issubset(disponibles[j]):
            historial.append(f"✨ Est. {j+1} también sobrevivió gracias al comodín recibido.\n")

    texto += "\n🧠 Estrategia aplicada:\n" + "".join(historial)
    return texto

def iniciar_nivel_1(entry):
    try:
        n = int(entry.get())
        if n < 2:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido de estudiantes (mínimo 2).")
        return

    estudiantes = repartir_dulces_estudiantes(n)
    resultado = optimizar_nivel_1(estudiantes)
    messagebox.showinfo("Resultado Nivel 1", resultado)

# NIVEL 2 - Juego grupal
def optimizar_nivel_2(participantes):
    grupo = repartir_dulces_estudiantes(participantes)
    total = sum(grupo, [])
    conteo = Counter(total)

    texto = ""
    for i, dulces in enumerate(grupo):
        texto += f"Estudiante {i+1}: {dulces}\n"

    texto += f"\nTotal de dulces: {dict(conteo)}\n"

    if all(conteo[d] >= 2 for d in DULCES):
        texto += "\n✅ El grupo sobrevivió (1 chupetín grupal + 2 comodines)\n"
        posibles_sets = min(conteo["limon"], conteo["pera"], conteo["huevo"])
        if posibles_sets >= 2:
            texto += "🎉 ¡Además lograron otro set con los comodines!\n"
        else:
            texto += "🧠 Comodines usados para apoyar a completar un segundo set.\n"
    else:
        texto += "\n❌ El grupo no sobrevivió. Faltan dulces suficientes.\n"

    return texto

def iniciar_nivel_2(entry):
    try:
        n = int(entry.get())
        if n < 3:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Número mínimo: 3 estudiantes.")
        return

    resultado = optimizar_nivel_2(n)
    messagebox.showinfo("Resultado Nivel 2", resultado)

# Interfaz principal
def interfaz_principal():
    ventana = tk.Tk()
    ventana.title("🎮 Juego de Sobrevivientes")
    ventana.config(bg="lightcyan", padx=20, pady=20)

    tk.Label(ventana, text="🎯 JUEGO DE SOBREVIVIENTES", font=("Arial", 16, "bold"), bg="lightcyan").pack(pady=10)

    # NIVEL 1
    marco1 = tk.Frame(ventana, bg="lightblue", padx=10, pady=10, relief="groove", borderwidth=2)
    marco1.pack(pady=10, fill="x")
    tk.Label(marco1, text="🔹 Nivel 1: Individual con cooperación", font=("Arial", 13, "bold"), bg="lightblue").pack()
    frame_entry1 = tk.Frame(marco1, bg="lightblue")
    frame_entry1.pack(pady=5)
    tk.Label(frame_entry1, text="Cantidad de estudiantes:", bg="lightblue").pack(side="left")
    entry1 = tk.Entry(frame_entry1, width=5)
    entry1.pack(side="left", padx=5)
    tk.Button(marco1, text="Jugar Nivel 1", bg="lightgreen", command=lambda: iniciar_nivel_1(entry1)).pack(pady=5)

    # NIVEL 2
    marco2 = tk.Frame(ventana, bg="lightyellow", padx=10, pady=10, relief="groove", borderwidth=2)
    marco2.pack(pady=10, fill="x")
    tk.Label(marco2, text="🔸 Nivel 2: Juego Grupal", font=("Arial", 13, "bold"), bg="lightyellow").pack()
    frame_entry2 = tk.Frame(marco2, bg="lightyellow")
    frame_entry2.pack(pady=5)
    tk.Label(frame_entry2, text="Número de participantes (mín. 3):", bg="lightyellow").pack(side="left")
    entry2 = tk.Entry(frame_entry2, width=5)
    entry2.pack(side="left", padx=5)
    tk.Button(marco2, text="Jugar Nivel 2", bg="orange", command=lambda: iniciar_nivel_2(entry2)).pack(pady=5)

    ventana.mainloop()

interfaz_principal()
