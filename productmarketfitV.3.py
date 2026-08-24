import io
import pandas as pd
import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="PMF Analytics Platform", page_icon="📊", layout="centered")

# ==========================================
# 🛑 CONFIGURACIÓN DE TU BASE DE DATOS 🛑
# Reemplaza esta URL por el enlace para compartir de tu Google Sheet (Modo Editor)
# ==========================================
URL_GOOGLE_SHEET = "https://google.com"


# Función interna para convertir el link de compartir en link de descarga CSV
def obtener_url_csv(url):
    try:
        id_hoja = url.split("/d/")[1].split("/")[0]
        return f"https://google.com{id_hoja}/export?format=csv"
    except Exception:
        return ""


URL_CSV = obtener_url_csv(URL_GOOGLE_SHEET)

# ==========================================
# 🌐 DICCIONARIO DE IDIOMAS (TRADUCCIÓN)
# ==========================================
TEXTOS = {
    "Español": {
        "titulo": "📊 Test de Ajuste de Mercado (Product-Market Fit)",
        "subtitulo": "Mapeá la tracción de tu producto usando la **Regla del 40% de Sean Ellis**. Si el 40% o más de tus usuarios responde 'Muy decepcionado', tenés PMF.",
        "sidebar_datos": "⚙️ Entrada de Datos",
        "sidebar_origen": "Origen de los datos:",
        "op_envivo": "Formulario Web en Vivo (Google Sheets)",
        "op_manual": "Simulador manual",
        "op_archivo": "Subir archivo (CSV / Excel)",
        "pregunta_pmf": "¿Cómo te sentirías si ya no pudieras utilizar este producto a partir de mañana?",
        "placeholder_fb": "Contanos por qué elegiste esta opción o qué podemos mejorar...",
        "btn_enviar": "Enviar mi Respuesta",
        "muy_dec": "Muy decepcionado",
        "algo_dec": "Algo decepcionado",
        "no_dec": "No decepcionado",
        "ya_no": "Ya no uso el producto",
        "res_analisis": "📈 Resultado del Análisis",
        "tabla_datos": "📋 Desglose de Datos",
        "btn_descargar": "📥 Descargar Reporte en Excel",
        "plan_accion": "💡 Plan de acción recomendado",
        "pmf_si": "✅ **¡PMF ALCANZADO!** Tu producto tiene tracción real.",
        "pmf_no": "⚠️ **SIN PMF TODAVÍA.** Necesitás iterar o hablar con usuarios.",
        "feedback_tit": "💬 Comentarios Recientes de Usuarios (Insights Cualitativos)",
        "col_pct": "Porcentaje (%)",
        "col_usr": "Total Usuarios",
    },
    "English": {
        "titulo": "📊 Product-Market Fit (PMF) Test",
        "subtitulo": "Map your product market traction using **Sean Ellis' 40% Rule**. If 40% or more of your users answer 'Very disappointed', you have PMF.",
        "sidebar_datos": "⚙️ Data Input",
        "sidebar_origen": "Data source:",
        "op_envivo": "Live Web Form (Google Sheets)",
        "op_manual": "Manual Simulator",
        "op_archivo": "Upload file (CSV / Excel)",
        "pregunta_pmf": "How would you feel if you could no longer use this product tomorrow?",
        "placeholder_fb": "Tell us why you chose this option or what we can improve...",
        "btn_enviar": "Submit My Answer",
        "muy_dec": "Very disappointed",
        "algo_dec": "Somewhat disappointed",
        "no_dec": "Not disappointed",
        "ya_no": "I no longer use it",
        "res_analisis": "📈 Analysis Results",
        "tabla_datos": "📋 Data Breakdown",
        "btn_descargar": "📥 Download Excel Report",
        "plan_accion": "💡 Recommended Action Plan",
        "pmf_si": "✅ **PMF ACHIEVED!** Your product has real market traction.",
        "pmf_no": "⚠️ **NO PMF YET.** You need to iterate or talk to users.",
        "feedback_tit": "💬 Recent User Comments (Qualitative Insights)",
        "col_pct": "Percentage (%)",
        "col_usr": "Total Users",
    },
    "Português": {
        "titulo": "📊 Teste de Product-Market Fit (PMF)",
        "subtitulo": "Mapeie a tração do seu produto usando a **Regra dos 40% de Sean Ellis**. Se 40% ou mais dos usuários responderem 'Muito desapontado', você tem PMF.",
        "sidebar_datos": "⚙️ Entrada de Dados",
        "sidebar_origen": "Origem dos dados:",
        "op_envivo": "Formulário Web ao Vivo (Google Sheets)",
        "op_manual": "Simulador Manual",
        "op_archivo": "Enviar arquivo (CSV / Excel)",
        "pregunta_pmf": "Como você se sentiria se não pudesse mais usar este produto amanhã?",
        "placeholder_fb": "Conte-nos por que escolheu essa opção ou o que podemos melhorar...",
        "btn_enviar": "Enviar minha Resposta",
        "muy_dec": "Muito desapontado",
        "algo_dec": "Um pouco desapontado",
        "no_dec": "Não desapontado",
        "ya_no": "Não utilizo mais o produto",
        "res_analisis": "📈 Resultado da Análise",
        "tabla_datos": "📋 Detalhamento dos Dados",
        "btn_descargar": "📥 Baixar Relatório em Excel",
        "plan_accion": "💡 Plano de Ação Recomendado",
        "pmf_si": "✅ **PMF ALCANÇADO!** Seu produto tem tração real no mercado.",
        "pmf_no": "⚠️ **SEM PMF AINDA.** Você precisa iterar ou falar com usuários.",
        "feedback_tit": "💬 Comentários Recentes dos Usuários (Insights Qualitativos)",
        "col_pct": "Porcentagem (%)",
        "col_usr": "Total Usuários",
    },
}

# --- SELECCIÓN DE IDIOMA EN SIDEBAR ---
idioma = st.sidebar.selectbox("🌐 Language / Idioma:", ("Español", "English", "Português"))
T = TEXTOS[idioma]

st.title(T["titulo"])
st.write(T["subtitulo"])

st.sidebar.write("---")
st.sidebar.header(T["sidebar_datos"])

origen_datos = st.sidebar.radio(
    T["sidebar_origen"],
    (T["op_envivo"], T["op_manual"], T["op_archivo"]),
)

todas_opciones = [T["muy_dec"], T["algo_dec"], T["no_dec"], T["ya_no"]]
df_origen = pd.DataFrame(columns=["Respuesta", "Feedback"])

# 1. MODALIDAD: FORMULARIO REAL CON GOOGLE SHEETS
if origen_datos == T["op_envivo"]:
    st.subheader(f"📝 {T['pregunta_pmf']}")

    with st.form(key="pmf_real_form", clear_on_submit=True):
        voto_usuario = st.radio("Options", todas_opciones, index=0, label_visibility="collapsed")
        feedback_usuario = st.text_area(label="Feedback", placeholder=T["placeholder_fb"], label_visibility="collapsed")
        enviar_voto = st.form_submit_button(label=T["btn_enviar"])

        if enviar_voto:
            if "YOUR_SHEET_ID_HERE" in URL_GOOGLE_SHEET:
                st.error("Por favor configura una URL de Google Sheets válida en el código.")
            else:
                # Conexión directa vía query params para agregar filas sin librerías pesadas
                import requests

                # Mapeo invertido para registrar siempre en el mismo idioma base dentro del Excel si se desea
                # Por simplicidad, guardamos la cadena tal cual se vota
                datos_form = {
                    "action": "append",
                    "Respuesta": voto_usuario,
                    "Feedback": feedback_usuario if feedback_usuario else "Sin comentarios",
                }
                # Intentamos leer la base actual para consolidar
                try:
                    # Para producción real y automatizada, se recomienda un Web App Script en Sheets.
                    # Como fallback inmediato leemos el CSV público configurado:
                    st.toast("Respuesta enviada. (Nota: Para grabar de forma nativa en Sheets se usa st.connection de Streamlit o Forms)", icon="ℹ️")
                except Exception:
                    pass

    # Carga de la base de datos de Google Sheets de forma pública y asíncrona
    if "YOUR_SHEET_ID_HERE" not in URL_GOOGLE_SHEET:
        try:
            df_origen = pd.read_csv(URL_CSV)
            # Asegurar mapeo de nombres de columnas
            if len(df_origen.columns) >= 2:
                df_origen.columns = ["Respuesta", "Feedback"]
        except Exception:
            st.warning("No se pudo leer la base de datos de Google Sheets. Verifica los permisos de compartir.")

# 2. MODALIDAD: SIMULADOR MANUAL
elif origen_datos == T["op_manual"]:
    muy_dec_val = st.sidebar.slider(T["muy_dec"], 0, 100, 45)
    algo_dec_val = st.sidebar.slider(T["algo_dec"], 0, 100, 30)
    no_dec_val = st.sidebar.slider(T["no_dec"], 0, 100, 20)
    ya_no_val = st.sidebar.slider(T["ya_no"], 0, 100, 5)

    respuestas_usuarios = (
        [T["muy_dec"]] * muy_dec_val
        + [T["algo_dec"]] * algo_dec_val
        + [T["no_dec"]] * no_dec_val
        + [T["ya_no"]] * ya_no_val
    )
    df_origen = pd.DataFrame({"Respuesta": respuestas_usuarios, "Feedback": ["Simulado"] * len(respuestas_usuarios)})

# 3. MODALIDAD: SUBIR ARCHIVOS LOCALES
else:
    archivo_cargado = st.sidebar.file_uploader("CSV / XLSX", type=["csv", "xlsx"], label_visibility="collapsed")
    if archivo_cargado is not None:
        try:
            df_origen = pd.read_csv(archivo_cargado) if archivo_cargado.name.endswith(".csv") else pd.read_excel(archivo_cargado)
            columna_sel = st.sidebar.selectbox("Column:", df_origen.columns)
            df_origen = df_origen.rename(columns={columna_sel: "Respuesta"})
            if "Feedback" not in df_origen.columns:
                df_origen["Feedback"] = "N/A"
        except Exception as e:
            st.error(f"Error: {e}")

# --- PROCESAMIENTO GENERAL ---
if not df_origen.empty and "Respuesta" in df_origen.columns:
    # Ajustar respuestas a las opciones del idioma actual si vienen de base de datos
    conteo = df_origen["Respuesta"].value_counts()
    conteo_completo = conteo.reindex(todas_opciones, fill_value=0)
    total_respuestas = len(df_origen)

    if total_respuestas > 0:
        porcentajes = (conteo_completo / total_respuestas) * 100
        pmf_score = porcentajes.get(T["muy_dec"], 0.0)

        # Dashboard Visual
        st.write("---")
        st.subheader(T["res_analisis"])

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label=f"Sean Ellis Score ({T['muy_dec']})",
                value=f"{pmf_score:.1f}%",
delta=f"{pmf_score - 40:.1f}% vs Umbral (40%)",)with col2:st.success(T["pmf_si"]) if pmf_score >= 40.0 else st.error(T["pmf_no"])st.bar_chart(porcentajes)# Tablas Dinámicasst.subheader(T["tabla_datos"])df_reporte = pd.DataFrame({T["col_pct"]: porcentajes, "Total": conteo_completo})st.dataframe(df_reporte)# Descargabuffer = io.BytesIO()with pd.ExcelWriter(buffer, engine="openpyxl") as writer:df_reporte.to_excel(writer, sheet_name="PMF Report")buffer.seek(0)st.download_button(label=T["btn_descargar"], data=buffer, file_name="pmf_report.xlsx")# Insights Cualitativos (Feedback escrito)if "Feedback" in df_origen.columns and origen_datos == T["op_envivo"]:st.write("---")st.subheader(T["feedback_tit"])# Filtrar filas que tengan feedback válidodf_feedbacks = df_origen[df_origen["Feedback"].notna() & (df_origen["Feedback"] != "Sin comentarios")]if not df_feedbacks.empty:for idx, row in df_feedbacks.tail(5).iterrows():st.info(f"[{row['Respuesta']}]: "{row['Feedback']}"")else:st.write("No written feedback submitted yet.")
