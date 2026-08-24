import io
import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="Test de Ajuste de Mercado (PMF)", page_icon="📊", layout="centered")

# --- INITIALIZAR ESTADO DE LA SESIÓN (Base de datos temporal en vivo) ---
if "votos_formulario" not in st.session_state:
    # Datos iniciales precargados para que la app no empiece vacía
    st.session_state.votos_formulario = {
        "Muy decepcionado": 12,
        "Algo decepcionado": 8,
        "No decepcionado": 4,
        "Ya no uso el producto": 1,
    }

st.title("📊 Test de Ajuste de Mercado (Product-Market Fit)")
st.write(
    "Mapeá la tracción de tu producto usando la **Regla del 40% de Sean Ellis**. "
    "Si el 40% o más de tus usuarios elegidos responde 'Muy decepcionado', tienes PMF."
)

# --- BARRA LATERAL: ENTRADA DE DATOS ---
st.sidebar.header("⚙️ Entrada de Datos")

origen_datos = st.sidebar.radio(
    "Selecciona el origen de los datos:",
    ("Formulario Web en Vivo", "Simulador manual", "Subir archivo (CSV / Excel)"),
)

todas_opciones = ["Muy decepcionado", "Algo decepcionado", "No decepcionado", "Ya no uso el producto"]
df_origen = pd.DataFrame(columns=["Respuesta"])

# OPCIÓN 1: FORMULARIO WEB EN VIVO
if origen_datos == "Formulario Web en Vivo":
    st.sidebar.write("---")
    st.sidebar.info("👉 Completá el formulario del centro de la pantalla para simular la experiencia del usuario.")

    # Renderizar el formulario interactivo en el cuerpo principal
    st.subheader("📝 Encuesta de Satisfacción del Producto")
    st.write(
        "¿Cómo te sentirías si ya no pudieras utilizar este producto a partir de mañana?"
    )

    with st.form(key="pmf_user_form", clear_on_submit=True):
        voto_usuario = st.radio(
            "Seleccioná una opción:", todas_opciones, index=0, label_visibility="collapsed"
        )
        enviar_voto = st.form_submit_button(label="Enviar mi Respuesta")

        if enviar_voto:
            # Sumar el voto al estado de la aplicación
            st.session_state.votos_formulario[voto_usuario] += 1
            st.toast(f"¡Voto registrado: '{voto_usuario}'!", icon="🚀")

    # Botón para reiniciar el contador del formulario
    if st.sidebar.button("🗑️ Reiniciar votos del formulario"):
        st.session_state.votos_formulario = {opc: 0 for opc in todas_opciones}
        st.rerun()

    # Convertir el diccionario de sesión a un DataFrame para el análisis
    respuestas_lista = []
    for opcion, cantidad in st.session_state.votos_formulario.items():
        respuestas_lista.extend([opcion] * cantidad)
    df_origen = pd.DataFrame(respuestas_lista, columns=["Respuesta"])

# OPCIÓN 2: SIMULADOR MANUAL (SLIDERS)
elif origen_datos == "Simulador manual":
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

# OPCIÓN 3: SUBIR ARCHIVOS EXTERNOS
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
    else:
        st.info("💡 Subí un archivo en la barra lateral para procesar tus métricas reales.")

# --- PROCESAMIENTO GENERAL Y MÉTRICAS ---
if not df_origen.empty and "Respuesta" in df_origen.columns:
    conteo = df_origen["Respuesta"].value_counts()
    conteo_completo = conteo.reindex(todas_opciones, fill_value=0)
    total_respuestas = len(df_origen)

    if total_respuestas > 0:
        porcentajes = (conteo_completo / total_respuestas) * 100
        pmf_score = porcentajes.get("Muy decepcionado", 0.0)

        # UI de Resultados
        st.write("---")
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

        # Botón de descarga Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_reporte.to_excel(writer, sheet_name="Reporte PMF")
        buffer.seek(0)

        st.download_button(
            label="📥 Descargar Reporte en Excel",
            data=buffer,
            file_name="reporte_product_market_fit.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

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
        st.warning("No hay respuestas registradas actualmente.")
