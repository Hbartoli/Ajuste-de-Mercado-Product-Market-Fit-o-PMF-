import matplotlib.pyplot as plt
import pandas as pd

def analizar_pmf(data_respuestas):
    """Calcula el porcentaje de Product-Market Fit y evalúa el resultado."""
    # Crear un DataFrame con las respuestas
    df = pd.DataFrame(data_respuestas, columns=["Respuesta"])

    # Contar frecuencias y calcular porcentajes
    conteo = df["Respuesta"].value_counts()
    porcentajes = df["Respuesta"].value_counts(normalize=True) * 100

    # Extraer el valor de 'Muy decepcionado' (columna clave para PMF)
    opcion_clave = "Muy decepcionado"
    pmf_score = porcentajes.get(opcion_clave, 0.0)

    # Determinar el estado del PMF
    tiene_pmf = pmf_score >= 40.0
    estado = (
        "✅ ¡PMF ALCANZADO! Tu producto tiene tracción."
        if tiene_pmf
        else "⚠️ SIN PMF TODAVÍA. Necesitás pivotar o iterar el producto."
    )

    # Imprimir reporte en consola
    print("--- REPORTE DE PRODUCT-MARKET FIT ---")
    for respuesta, pct in porcentajes.items():
        print(f"{respuesta}: {pct:.1f}% ({conteo[respuesta]} usuarios)")
    print("-" * 37)
    print(f"Métrica PMF (Sean Ellis Score): {pmf_score:.1f}%")
    print(f"Estado: {estado}\n")

    # Generar gráfico de barras
    graficar_resultados(porcentajes, pmf_score)


def graficar_resultados(porcentajes, pmf_score):
    """Genera un gráfico visual dinámico para el reporte."""
    plt.figure(figsize=(8, 5))

    # Colores condicionales según el resultado
    color_barras = (
        ["#2ec4b6" if idx == "Muy decepcionado" else "#cbf3f0" for idx in porcentajes.index]
        if pmf_score >= 40
        else ["#e63946" if idx == "Muy decepcionado" else "#f1faee" for idx in porcentajes.index]
    )

    # Dibujar barras
    bars = plt.bar(porcentajes.index, porcentajes.values, color=color_barras, edgecolor="black")

    # Agregar etiquetas de porcentaje sobre las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 1,
            f"{height:.1f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    # Línea de referencia del 40%
    plt.axhline(y=40, color="gray", linestyle="--", alpha=0.7, label="Umbral PMF (40%)")

    # Configuración estética
    plt.title("Test de Ajuste de Mercado (Product-Market Fit)", fontsize=14, fontweight="bold", pad=15)
    plt.ylabel("Porcentaje de Usuarios (%)")
    plt.ylim(0, max(porcentajes.values) + 10)
    plt.legend()
    plt.tight_layout()

    # Mostrar gráfico
    plt.show()


# ==========================================
# SIMULACIÓN DE DATOS (PROBÁ EL SCRIPT ACÁ)
# ==========================================
# Modificá esta lista con las respuestas reales de tus usuarios encuestados
respuestas_usuarios = (
    ["Muy decepcionado"] * 45
    + ["Algo decepcionado"] * 30
    + ["No decepcionado"] * 20
    + ["Ya no uso el producto"] * 5
)

# Ejecutar el análisis
analizar_pmf(respuestas_usuarios)
