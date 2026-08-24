import pandas as pd
import streamlit as str

# Configuración de la página web
st.set_page_config(page_title="Test de Ajuste de Mercado (PMF)", page_icon="📊", layout="centered")

st.title("📊 Test de Ajuste de Mercado (Product-Market Fit)")
st.write(
    "Mapeá la tracción de tu producto usando la **Regla del 40% de Sean Ellis**. "
    "Si el 40% o más de tus usuarios elegidos responde 'Muy decepcionado', tenés PMF."
)

# 1. Simulación de entrada de datos (Podés conectar un archivo real después)
st.sidebar.header("⚙️ Configuración de Datos")
st.sidebar.write("Simulación de respuestas recibidas:")

muy_dec = st.sidebar.slider("Muy decepcionado", 0, 100, 45)
algo_dec = st.sidebar.slider("Algo decepcionado", 0, 100, 30)
no_dec = st.sidebar.slider("No decepcionado", 0, 100, 20)
ya_no_usa = st.sidebar.slider("Ya no usa el producto", 0, 100, 5)

# Generar la lista de respuestas según los sliders
respuestas_usuarios = (
    ["Muy decepcionado"] * muy_dec
    + ["Algo decepcionado"] * algo_dec
    + ["No decepcionado"] * no_dec
    + ["Ya no uso el producto"] * ya_no_usa
)

# 2. Procesamiento de los datos con Pandas
df = pd.DataFrame(respuestas_usuarios, columns=["Respuesta"])
conteo = df["Respuesta"].value_counts()
porcentajes = df["Respuesta"].value_counts(normalize=True) * 100

# Asegurar que todas las opciones existan en el índice para evitar errores visuales
todas_opciones = ["Muy decepcionado", "Algo decepcionado", "No decepcionado", "Ya no uso el producto"]
porcentajes = porcentajes.reindex(todas_opciones, fill_value=0.0)

# Extraer la métrica clave
pmf_score = porcentajes.get("Muy decepcionado", 0.0)

# 3. Mostrar métricas y diagnóstico en pantalla
st.subheader("📈 Resultado del Análisis")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Métrica PMF (Sean Ellis Score)", value=f"{pmf_score:.1f}%", delta=f"{pmf_score - 40:.1f}% vs Umbral")

with col2:
    if pmf_score >= 40.0:
        st.success("✅ **¡PMF ALCANZADO!** Tu producto tiene tracción real en el mercado.")
    else:
        st.error("⚠️ **SIN PMF TODAVÍA.** Necesitás iterar, hablar con usuarios o pivotar.")

# 4. Gráfico interactivo nativo de Streamlit (Sin usar Matplotlib)
st.write("### Distribución de Respuestas (%)")
st.bar_chart(porcentajes)

# 5. Tabla detallada de datos de control
st.write("### 📋 Desglose de Datos")
df_reporte = pd.DataFrame({"Porcentaje (%)": porcentajes, "Total Usuarios": conteo.reindex(todas_opciones, fill_value=0)})
st.dataframe(df_reporte)
