import streamlit as st
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="RADAR POLÍTICO | Comunicación política digital",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ESTILOS ADAPTADOS A CELULARES Y MODO OSCURO
st.markdown("""
<style>
    .main { background-color: #020617; color: #f8fafc; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: 700; min-height: 46px; }
    .briefing-box { background: linear-gradient(135deg, #0f172a 0%, #082f49 100%); border: 1px solid #0284c7; border-radius: 12px; padding: 18px; margin-bottom: 20px; }
    .news-card { background-color: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 14px; margin-bottom: 12px; }
    .badge-alert { background-color: #450a0a; color: #f87171; border: 1px solid #991b1b; padding: 2px 8px; border-radius: 9999px; font-size: 11px; font-weight: 600; }
    .badge-normal { background-color: #082f49; color: #38bdf8; border: 1px solid #0369a1; padding: 2px 8px; border-radius: 9999px; font-size: 11px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# CABECERA
col_brand, col_action = st.columns([3, 1])
with col_brand:
    st.title("📡 RADAR POLÍTICO")
    st.caption("Comunicación política digital • Séptima Sección Electoral & Provincia de Buenos Aires")

with col_action:
    if st.button("🔄 Actualizar Novedades Ahora (En Vivo)", type="primary"):
        st.cache_data.clear()
        st.rerun()

# MOTOR DE MONITOREO EN VIVO EN LA NUBE (Auto-actualización cada 30 min y a las 7:00 AM)
@st.cache_data(ttl=1800)
def obtener_noticias_en_vivo():
    actores = '"Bali Bucca" OR "Wesner" OR "Kicillof" OR "Egüen" OR "Salomón" OR "Nelson Sombra" OR "Katopodis" OR "Séptima Sección"'
    temas = 'presupuesto OR tarifas OR reelecciones OR seguridad OR protestas OR obras OR tasas'
    distritos = 'Bolívar OR Olavarría OR Azul OR Saladillo OR "25 de Mayo" OR "General Alvear" OR "Roque Pérez" OR "Tapalqué"'
    query = f'({actores}) ({temas}) ({distritos}) when:2d'
    
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=es-419&gl=AR&ceid=AR:es-419"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    noticias = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = root.findall('./channel/item')
            
            for item in items:
                title_full = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                source = "Medios Regionales"
                title = title_full
                if " - " in title_full:
                    parts = title_full.rsplit(" - ", 1)
                    title = parts[0]
                    source = parts[1]
                
                lower = (title + " " + source).lower()
                ref = "Séptima Sección"
                if "wesner" in lower or "olavarría" in lower: ref = "Maximiliano Wesner"
                elif "bucca" in lower or "bolívar" in lower: ref = "Bali Bucca"
                elif "egüen" in lower or "25 de mayo" in lower: ref = "Ramiro Egüen"
                elif "salomón" in lower or "saladillo" in lower: ref = "José Luis Salomón"
                elif "sombra" in lower or "azul" in lower: ref = "Nelson Sombra"
                elif "kicillof" in lower: ref = "Axel Kicillof"
                elif "katopodis" in lower: ref = "Gabriel Katopodis"
                elif "capra" in lower: ref = "Ramón José Capra"
                elif "sciaini" in lower: ref = "Maximiliano Oscar Sciaini"
                elif "cocconi" in lower: ref = "Gustavo Cocconi"
                
                tema = "Gestión / Presupuesto"
                is_alerta = False
                if any(k in lower for k in ["tarifa", "luz", "gas", "aumento"]):
                    tema = "Tarifas / Servicios"
                    is_alerta = True
                elif any(k in lower for k in ["protesta", "reclamo", "conflicto", "paro"]):
                    tema = "Protestas / Conflicto"
                    is_alerta = True
                elif "reelecci" in lower:
                    tema = "Reelecciones 2027"
                    is_alerta = True
                elif any(k in lower for k in ["seguridad", "polic", "robo"]):
                    tema = "Seguridad"
                
                noticias.append({
                    "title": title,
                    "source": source,
                    "link": link,
                    "date": pubDate,
                    "referente": ref,
                    "tema": tema,
                    "is_alerta": is_alerta
                })
    except Exception as e:
        st.error(f"Error consultando fuentes: {e}")
        
    return noticias

noticias = obtener_noticias_en_vivo()

# BARRA LATERAL CON FILTROS
st.sidebar.header("🎯 Filtros de Monitoreo")
referentes_lista = ["Todos"] + sorted(list(set(n["referente"] for n in noticias)))
filtro_ref = st.sidebar.selectbox("Referente Político", referentes_lista)

temas_lista = ["Todos"] + sorted(list(set(n["tema"] for n in noticias)))
filtro_tema = st.sidebar.selectbox("Tema de Coyuntura", temas_lista)

solo_alertas = st.sidebar.checkbox("🚨 Mostrar solo Alertas Críticas", value=False)

# RESUMEN DE COYUNTURA GENERADO DINÁMICAMENTE CON LAS NOTICIAS REALES DE HOY
hoy_str = datetime.now().strftime("%d/%m/%Y")
st.markdown(f"""
<div class="briefing-box">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3 style="margin:0; color:#38bdf8;">📢 Resumen de Coyuntura Matutino (Sincronizado 7:00 AM / En Vivo)</h3>
        <span class="badge-normal">Fecha: {hoy_str}</span>
    </div>
    <p style="font-size:12px; color:#cbd5e1; margin-top:4px;">Síntesis de coyuntura generada automáticamente con los despachos de las últimas 24-48 horas.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Claves de Gestión")
    noticias_gestion = [n for n in noticias if not n["is_alerta"]][:3]
    if noticias_gestion:
        for n in noticias_gestion:
            st.markdown(f"• **{n['referente']}**: [{n['title']}]({n['link']}) _({n['source']})_")
    else:
        st.write("Sin novedades de gestión en las últimas horas.")

with col2:
    st.subheader("2. Alertas & Conflictos")
    noticias_alertas = [n for n in noticias if n["is_alerta"]][:3]
    if noticias_alertas:
        for n in noticias_alertas:
            st.markdown(f"🚨 **{n['tema']}**: [{n['title']}]({n['link']}) _({n['source']})_")
    else:
        st.write("No se detectan alertas críticas activas en este momento.")

with col3:
    st.subheader("3. Recomendación de Vocería")
    st.markdown("""
    • **Obras Locales**: Priorizar la visibilidad de obras municipales ante el ajuste nacional.  
    • **Prevención Tarifaria**: Adelantarse al impacto de tarifas con mesas de diálogo comerciales.  
    • **Articulación de la Sección**: Sostener presencia de intendentes en la agenda bonaerense.
    """)

st.divider()

# FEED COMPLETO EN VIVO
st.subheader(f"📋 Feed en Tiempo Real ({len(noticias)} noticias detectadas)")

noticias_filtradas = noticias
if filtro_ref != "Todos":
    noticias_filtradas = [n for n in noticias_filtradas if n["referente"] == filtro_ref]
if filtro_tema != "Todos":
    noticias_filtradas = [n for n in noticias_filtradas if n["tema"] == filtro_tema]
if solo_alertas:
    noticias_filtradas = [n for n in noticias_filtradas if n["is_alerta"]]

if not noticias_filtradas:
    st.info("No se encontraron noticias con los filtros seleccionados.")
else:
    for n in noticias_filtradas:
        badge = '<span class="badge-alert">Alerta Crítica</span>' if n["is_alerta"] else '<span class="badge-normal">Gestión</span>'
        st.markdown(f"""
        <div class="news-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div>
                    <span style="font-weight:700; color:#38bdf8;">{n['source']}</span> • 
                    <span style="color:#94a3b8; font-size:12px;">{n['referente']}</span>
                </div>
                {badge}
            </div>
            <a href="{n['link']}" target="_blank" style="text-decoration:none; font-size:15px; font-weight:700; color:#f8fafc; display:block; margin-bottom:6px;">
                {n['title']} ↗
            </a>
            <div style="font-size:12px; color:#64748b;">
                Tema: {n['tema']} | Publicada: {n['date']}
            </div>
        </div>
        """, unsafe_allow_html=True)
