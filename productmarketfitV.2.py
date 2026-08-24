import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="Test de Ajuste de Mercado (PMF)", page_icon="📊", layout="centered")

st.title("📊 Test de Ajuste de Mercado (Product-Market Fit)")
st.write(
    "Mapeá la tracción de tu producto usando la **Regla del 40% de Sean Ellis**. "
    "Si el 40% o más de tus usuarios elegidos responde 'Muy decepcionado', tienes PMF."
)

# --- BARRA LATERAL: ENTRADA DE DATOS ---
st.sidebar.header("⚙️ Entrada de Datos")

# Selector del origen de los datos
origen_datos = st.sidebar.radio("Selecciona el origen de los datos:", ("Simulador manual", "Subir archivo (CSV / Excel)"))

todas_opciones = ["Muy decepcionado", "Algo decepcionado", "No decepcionado", "Ya no uso el producto"]
respuestas_usuarios = []

if origen_datos == "Simulador manual":
    st.sidebar.write("---")
    muy_dec = st.sidebar.slider("Muy decepcionado", 0, 100, 45)
    algo_dec = st.sidebar.slider("Algo decepcionado", 0, 100, 30)
    no_dec = st.sidebar.slider("No decepcionado", 0, 100, 20)
    ya_no_usa = st.sidebar.slider("Ya no usa el producto", 0, 100, 5)

    respuestas_usuarios = (
        ["Muy decepcionado"] * muy_dec
        + ["Algo decepcionado"] * algo_dec
        + ["No decepcionado"] * no_dec
        + ["Ya no uso el producto"] * ya_no_usa
    )
    df_origen = pd.DataFrame(respuestas_usuarios, columns=["Respuesta"])

else:
    st.sidebar.write("---")
    archivo_cargado = st.sidebar.file_uploader("Subí tu archivo Excel o CSV", type=["csv", "xlsx"])

    if archivo_cargado is not None:
        try:
            if archivo_cargado.name.endswith(".csv"):
                df_origen = pd.read_csv(archivo_cargado)
            else:
                df_origen = pd.read_excel(archivo_cargado)

            columna_seleccionada = st.sidebar.selectbox("Seleccioná la columna de la encuesta:", df_origen.columns)
            df_origen = df_origen.rename(columns={columna_seleccionada: "Respuesta"})
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
            df_origen = pd.DataFrame(columns=["Respuesta"])
    else:
        st.info("💡 Subí un archivo en la barra lateral para procesar tus métricas reales.")
        df_origen = pd.DataFrame(columns=["Respuesta"])

# --- PROCESAMIENTO Y MÉTRICAS ---
if not df_origen.empty and "Respuesta" in df_origen.columns:
    # Limpieza básica y conteo
    conteo = df_origen["Respuesta"].value_counts()
    conteo_completo = conteo.reindex(todas_opciones, fill_value=0)

    total_respuestas = len(df_origen)

    if total_respuestas > 0:
        porcentajes = (conteo_completo / total_respuestas) * 100
        pmf_score = percentages = porcentajes.get("Muy decepcionado", 0.0)

        # UI de Resultados
        st.subheader("📈 Resultado del Análisis")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Métrica PMF (Sean Ellis Score)",
                value=f"{pmf_score:.1f}%",
                delta=f"{pmf_score - 40:.1f}% vs Umbral",
            )
        with col2:
            if pmf_score >= 40.0:
                st.success("✅ **¡PMF ALCANZADO!** Tu producto tiene tracción real en el mercado.")
            else:
                st.error("⚠️ **SIN PMF TODAVÍA.** Necesitas iterar, hablar con usuarios o pivotar.")

        # Gráfico
        st.write("### Distribución de Respuestas (%)")
        st.bar_chart(porcentajes)

        # Desglose numérico
        st.write("### 📋 Desglose de Datos")
        df_reporte = pd.DataFrame({"Porcentaje (%)": porcentajes, "Total Usuarios": conteo_completo})
        st.dataframe(df_reporte)

        # Plan de acción dinámico
        st.subheader("💡 Plan de acción recomendado")
        if pmf_score >= 40.0:
            st.markdown(
                "- **Duplicá la apuesta en canales de crecimiento:** El motor principal funciona. Enfócate en adquisición masiva.\n"
                "- **Protegé el core:** Analizá qué características ama el grupo 'Muy decepcionado' y no las rompas.\n"
                "- **Monitoreá el NPS:** Asegurá que el crecimiento no diluya la experiencia del usuario."
            )
        else:
            st.markdown(
                "- **Entrevistá al segmento intermedio:** Preguntale al grupo 'Algo decepcionado' qué le falta al producto para ser indispensable.\n"
                "- **Ajustá el posicionamiento:** Es posible que estés vendiendo el producto al público objetivo equivocado.\n"
                "- **Frena la inversión en marketing:** Inyectar capital sin PMF acelerará la pérdida de usuarios (*churn*)."
            )
    else:
        st.warning("El archivo no contiene respuestas válidas.")
