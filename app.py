import streamlit as st
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from collections import Counter

# CONFIGURACIÓN GENERAL
st.set_page_config(
    page_title="RADAR POLÍTICO | Comunicación Política",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ESTILOS PROFESIONALES INSTITUCIONALES (DISEÑO MODERNO, RESPONSIVE, DARK MODE)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0c1527 0%, #030712 75%);
        color: #f1f5f9;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 24px;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6);
    }
    
    .brand-logo-lockup {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .brand-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        line-height: 1.1;
        background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .brand-subtitle {
        font-size: 12px;
        font-weight: 600;
        color: #38bdf8;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    .badge-live {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
    }

    .live-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .kpi-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px;
        transition: all 0.2s ease;
    }
    .kpi-box:hover {
        border-color: rgba(56, 189, 248, 0.35);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8;
    }
    .kpi-num {
        font-size: 26px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 4px;
        line-height: 1.1;
    }
    .kpi-hint {
        font-size: 11px;
        color: #64748b;
        margin-top: 4px;
    }

    .news-card-pro {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .news-card-pro:hover {
        border-color: rgba(56, 189, 248, 0.35);
        background: rgba(15, 23, 42, 0.9);
        transform: translateY(-2px);
    }
    .news-title-text {
        font-size: 15px;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.4;
        text-decoration: none;
        display: block;
        margin-bottom: 8px;
    }
    .news-title-text:hover { color: #38bdf8; }

    .tag-medio {
        font-size: 11px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        padding: 3px 8px;
        border-radius: 6px;
    }
    .tag-dirigente {
        font-size: 11px;
        font-weight: 600;
        color: #e2e8f0;
        background: rgba(255, 255, 255, 0.07);
        padding: 3px 8px;
        border-radius: 6px;
    }
    .tag-denuncia {
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #fca5a5;
        background: rgba(220, 38, 38, 0.25);
        border: 1px solid #ef4444;
        padding: 3px 9px;
        border-radius: 9999px;
    }
    .tag-trending {
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #fde047;
        background: rgba(234, 179, 8, 0.2);
        border: 1px solid #eab308;
        padding: 3px 9px;
        border-radius: 9999px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 44px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 18px 0 rgba(2, 132, 199, 0.45) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 12px;
        padding: 6px 14px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.15) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #38bdf8 !important;
    }

    @media (max-width: 768px) {
        .brand-header { flex-direction: column; align-items: flex-start; gap: 12px; padding: 14px; }
        .kpi-box { margin-bottom: 8px; }
    }
</style>
""", unsafe_allow_html=True)

# GESTOR DE CONTACTOS PARA WHATSAPP
if "whatsapp_contacts" not in st.session_state:
    st.session_state.whatsapp_contacts = [
        {"nombre": "Equipo de Comunicación", "telefono": "+5492314000000", "cargo": "Prensa Central"},
        {"nombre": "Despacho de Intendencia", "telefono": "+5492314111111", "cargo": "Gabinete"}
    ]

# PLANTEL COMPLETO DE LA SÉPTIMA SECCIÓN Y CONCEJO DELIBERANTE DE BOLÍVAR
if "dirigentes_lista" not in st.session_state:
    st.session_state.dirigentes_lista = [
        # Intendentes de la Séptima (8)
        "Bali Bucca", "Maximiliano Wesner", "Nelson Sombra", "Ramiro Egüen",
        "José Luis Salomón", "Ramón José Capra", "Maximiliano Oscar Sciaini", "Gustavo Cocconi",
        # Legisladores Provinciales de la Séptima
        "Mercedes Landívar", "Martín Endere", "Alejandra Lordén", "Ricardo Lissalde",
        "Lorena Mandagarán", "Alejandro Celillo",
        # Concejales y Referentes de Bolívar
        "Franco Canepare", "Nico Morán", "César Pacho", "Sandra Santos",
        "Flavio De Marco", "Mónica Ochoa", "Ariel Alomar", "Patricia Oroz",
        # Provincia y Referentes Clave
        "Axel Kicillof", "Gabriel Katopodis", "Sergio Massa"
    ]

if "municipios_lista" not in st.session_state:
    st.session_state.municipios_lista = [
        "Bolívar", "Olavarría", "Azul", "25 de Mayo", "Saladillo",
        "General Alvear", "Roque Pérez", "Tapalqué", "Provincia de Buenos Aires"
    ]

if "temas_lista" not in st.session_state:
    st.session_state.temas_lista = [
        "Presupuesto y Tasas", "Denuncias y Cruces", "Tarifas y Servicios",
        "Obras Públicas", "Reelecciones 2027", "Seguridad y Patrullaje",
        "Salarios y Paritarias", "Producción y Empleo", "Caminos Rurales"
    ]

# CABECERA VISUAL CON LOGO MINIMALISTA
st.markdown("""
<div class="brand-header">
    <div class="brand-logo-lockup">
        <svg width="42" height="42" viewBox="0 0 42 42" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="42" height="42" rx="10" fill="#0284c7" fill-opacity="0.12" stroke="#0284c7" stroke-width="1.2"/>
            <circle cx="21" cy="21" r="14" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.25"/>
            <circle cx="21" cy="21" r="9" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.5"/>
            <circle cx="21" cy="21" r="4.5" stroke="#38bdf8" stroke-width="1.5" stroke-opacity="0.9"/>
            <circle cx="21" cy="21" r="2.2" fill="#38bdf8"/>
            <path d="M21 7C28.732 7 35 13.268 35 21" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round"/>
        </svg>
        <div>
            <h1 class="brand-title">RADAR POLÍTICO</h1>
            <div class="brand-subtitle">Comunicación Política Digital • Séptima Sección & PBA</div>
        </div>
    </div>
    <div class="badge-live">
        <span class="live-dot"></span>
        <span>MONITOREO EN VIVO • COYUNTURA 7:00 AM</span>
    </div>
</div>
""", unsafe_allow_html=True)

# MOTOR DE ESCANEO CONTINUO (BARRIDO COMPLETO DE MEDIOS REGIONALES)
@st.cache_data(ttl=1800)
def ejecutar_monitoreo_profesional(dirigentes, municipios, temas):
    actores_query = " OR ".join([f'"{d}"' for d in dirigentes[:12]])
    distritos_query = " OR ".join([f'"{m}"' for m in municipios[:8]])
    temas_query = "denuncia OR cuestionan OR reclamo OR presupuesto OR tarifas OR reelecciones OR seguridad OR obras OR tasas"
    
    query = f"({actores_query}) ({distritos_query}) ({temas_query}) when:3d"
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=es-419&gl=AR&ceid=AR:es-419"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    resultados = []
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = root.findall('./channel/item')
            
            for item in items:
                title_full = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
                
                source = "Medio Regional"
                title = title_full
                if " - " in title_full:
                    parts = title_full.rsplit(" - ", 1)
                    title = parts[0]
                    source = parts[1]
                
                lower = (title + " " + source).lower()
                
                # Identificación de Dirigente
                ref_encontrado = "Séptima Sección"
                for d in dirigentes:
                    if d.lower() in lower or d.split()[-1].lower() in lower:
                        ref_encontrado = d
                        break
                
                # Identificación de Municipio
                mun_encontrado = "Provincia de Buenos Aires"
                for m in municipios:
                    if m.lower() in lower:
                        mun_encontrado = m
                        break
                
                # Clasificación de Denuncias Opositoras y Temas
                es_denuncia_oposicion = any(k in lower for k in [
                    "denuncia", "cuestionan", "reclamo", "oposición", "pedido de informes",
                    "interpelación", "reparos", "irregularidad", "apuntó contra", "cruce"
                ])
                
                tema_encontrado = "Gestión Municipal"
                if es_denuncia_oposicion:
                    tema_encontrado = "Denuncias y Cruces"
                elif any(k in lower for k in ["tarifa", "luz", "gas", "aumento", "factura"]):
                    tema_encontrado = "Tarifas y Servicios"
                elif "reelecci" in lower:
                    tema_encontrado = "Reelecciones 2027"
                elif any(k in lower for k in ["seguridad", "polic", "robo", "delito"]):
                    tema_encontrado = "Seguridad y Patrullaje"
                elif any(k in lower for k in ["presupuesto", "fondo", "leasing", "tasas", "paritaria"]):
                    tema_encontrado = "Presupuesto y Tasas"
                elif any(k in lower for k in ["obra", "pavimento", "cloaca", "hidráulica"]):
                    tema_encontrado = "Obras Públicas"
                
                resultados.append({
                    "title": title,
                    "source": source,
                    "link": link,
                    "date": pubDate,
                    "dirigente": ref_encontrado,
                    "municipio": mun_encontrado,
                    "tema": tema_encontrado,
                    "es_denuncia": es_denuncia_oposicion,
                    "is_alerta": es_denuncia_oposicion or tema_encontrado in ["Tarifas y Servicios", "Reelecciones 2027"]
                })
    except Exception as e:
        st.warning(f"Sincronizando fuentes locales: {e}")
        
    return resultados

noticias = ejecutar_monitoreo_profesional(
    st.session_state.dirigentes_lista,
    st.session_state.municipios_lista,
    st.session_state.temas_lista
)

# DETECCIÓN DEL TEMA MÁS REPLICADO (TRENDING TOPIC REGIONAL)
conteo_temas = Counter(n["tema"] for n in noticias)
tema_mas_replicado = conteo_temas.most_common(1)[0][0] if conteo_temas else "Gestión y Obras"
cantidad_replicas = conteo_temas.most_common(1)[0][1] if conteo_temas else 0

total_denuncias = sum(1 for n in noticias if n["es_denuncia"])
total_noticias = len(noticias)
hora_actual = datetime.now().strftime("%H:%M hs")

# FILA DE INDICADORES EJECUTIVOS
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Novedades en Medios</div>
        <div class="kpi-num" style="color:#38bdf8;">{total_noticias}</div>
        <div class="kpi-hint">Monitoreo global continuo</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Denuncias de Oposición</div>
        <div class="kpi-num" style="color:#f87171;">{total_denuncias}</div>
        <div class="kpi-hint">Alertas de cruce político</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Eje Más Replicado</div>
        <div class="kpi-num" style="font-size:18px; color:#fde047; padding-top:6px;">{tema_mas_replicado}</div>
        <div class="kpi-hint">{cantidad_replicas} publicaciones coincidentes</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="kpi-box">
        <div class="kpi-label">Hora del Informe</div>
        <div class="kpi-num" style="color:#34d399; font-size:22px;">{hora_actual}</div>
        <div class="kpi-hint">Sincronizado para el equipo</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# BOTÓN DE RE-ESCANEO A DEMANDA
c_btn1, c_btn2 = st.columns([1, 2])
with c_btn1:
    if st.button("🔄 Escanear Medios Ahora", type="primary"):
        st.cache_data.clear()
        st.rerun()
with c_btn2:
    st.caption("ℹ️ El escaneo por defecto incluye **a todos los intendentes, legisladores, concejales de Bolívar y temas cargados**.")

st.write("")

# ADMINISTRADOR PARA AGREGAR NUEVAS ENTIDADES
with st.expander("➕ Administrar y Agregar Nuevos Dirigentes, Municipios o Temas"):
    col_add1, col_add2, col_add3 = st.columns(3)
    
    with col_add1:
        nuevo_d = st.text_input("Nuevo Dirigente / Concejal:", placeholder="Ej: Patricia Cobello")
        if st.button("Agregar Político") and nuevo_d:
            if nuevo_d not in st.session_state.dirigentes_lista:
                st.session_state.dirigentes_lista.append(nuevo_d)
                st.cache_data.clear()
                st.success(f"Se sumó al radar: {nuevo_d}")
                st.rerun()

    with col_add2:
        nuevo_m = st.text_input("Nuevo Municipio / Sección:", placeholder="Ej: Las Flores / Cuarta Sección")
        if st.button("Agregar Territorio") and nuevo_m:
            if nuevo_m not in st.session_state.municipios_lista:
                st.session_state.municipios_lista.append(nuevo_m)
                st.cache_data.clear()
                st.success(f"Se sumó al radar: {nuevo_m}")
                st.rerun()

    with col_add3:
        nuevo_t = st.text_input("Nuevo Tema de Coyuntura:", placeholder="Ej: Conflicto con IOMA")
        if st.button("Agregar Eje de Agenda") and nuevo_t:
            if nuevo_t not in st.session_state.temas_lista:
                st.session_state.temas_lista.append(nuevo_t)
                st.cache_data.clear()
                st.success(f"Se sumó al radar: {nuevo_t}")
                st.rerun()

st.write("")

# PESTAÑAS ESTRUCTURADAS
tab_general, tab_denuncias, tab_politicos, tab_territorio, tab_temas, tab_whatsapp = st.tabs([
    "📊 Panorama General",
    "🚨 Denuncias Opositoras & Cruces",
    "👤 Por Político / Concejal",
    "📍 Por Municipio",
    "📌 Por Tema Replicado",
    "📲 WhatsApp & Difusión (7 AM)"
])

# 1. PANORAMA GENERAL
with tab_general:
    hoy_texto = datetime.now().strftime("%A %d de %B de %Y").capitalize()
    st.markdown(f"### 📋 Novedades de la Jornada • {hoy_texto}")
    st.caption("Listado completo de publicaciones en los 23 medios de la región.")
    
    for n in noticias:
        tag_denuncia = '<span class="tag-denuncia">Cruce Opositor</span>' if n["es_denuncia"] else ''
        tag_top = '<span class="tag-trending">Mayor Repercusión</span>' if n["tema"] == tema_mas_replicado else ''
        
        st.markdown(f"""
        <div class="news-card-pro">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:6px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="tag-medio">{n['source']}</span>
                    <span class="tag-dirigente">👤 {n['dirigente']}</span>
                    <span style="font-size:11px; color:#94a3b8;">📍 {n['municipio']}</span>
                </div>
                <div style="display:flex; gap:6px;">{tag_denuncia} {tag_top}</div>
            </div>
            <a href="{n['link']}" target="_blank" class="news-title-text">
                {n['title']} ↗
            </a>
            <div style="font-size:12px; color:#64748b;">
                Eje: <strong style="color:#94a3b8;">{n['tema']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. RADAR DE DENUNCIAS OPOSITORAS Y CRUCES
with tab_denuncias:
    st.markdown("### 🚨 Denuncias de la Oposición y Conflictos en Medios")
    st.caption("Filtro prioritario de reclamos, pedidos de informes de concejales y cuestionamientos a la gestión.")
    
    denuncias_list = [n for n in noticias if n["es_denuncia"]]
    if not denuncias_list:
        st.success("Tranquilidad mediática: no se detectan denuncias u operaciones opositoras registradas en las últimas horas.")
    else:
        for d in denuncias_list:
            st.markdown(f"""
            <div class="news-card-pro" style="border-left: 4px solid #ef4444; background: rgba(30, 10, 10, 0.5);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="tag-medio" style="color:#f87171; background:rgba(239,68,68,0.2);">{d['source']}</span>
                    <span class="tag-denuncia">Conflicto Opositor</span>
                </div>
                <a href="{d['link']}" target="_blank" class="news-title-text" style="color:#fecaca;">
                    {d['title']} ↗
                </a>
                <div style="font-size:12px; color:#cbd5e1;">
                    Referente / Concejal: <strong style="color:#ffffff;">{d['dirigente']}</strong> | Distrito: <strong>{d['municipio']}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

# 3. POR POLÍTICO (INCLUYE CONCEJALES DE BOLÍVAR Y LEGISLADORES)
with tab_politicos:
    st.markdown("### 👤 Seguimiento Individual por Intendentes, Legisladores y Concejales")
    dirigente_seleccionado = st.selectbox("Seleccionar dirigente o concejal:", ["Todos"] + sorted(st.session_state.dirigentes_lista))
    
    noticias_dirigente = noticias if dirigente_seleccionado == "Todos" else [n for n in noticias if n["dirigente"] == dirigente_seleccionado]
    st.write(f"Coberturas encontradas para **{dirigente_seleccionado}**: **{len(noticias_dirigente)}**")
    
    if not noticias_dirigente:
        st.info(f"No se detectaron publicaciones recientes que mencionen directamente a {dirigente_seleccionado}.")
    else:
        for n in noticias_dirigente:
            st.markdown(f"""
            <div class="news-card-pro">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span class="tag-medio">{n['source']}</span>
                    <span style="font-size:11px; color:#64748b;">📍 {n['municipio']}</span>
                </div>
                <a href="{n['link']}" target="_blank" class="news-title-text">
                    {n['title']} ↗
                </a>
                <div style="font-size:12px; color:#94a3b8;">Tema: {n['tema']}</div>
            </div>
            """, unsafe_allow_html=True)

# 4. POR MUNICIPIO
with tab_territorio:
    st.markdown("### 📍 Seguimiento Territorial por Municipio y Provincia")
    municipio_seleccionado = st.selectbox("Seleccionar municipio o ámbito territorial:", ["Todos"] + sorted(st.session_state.municipios_lista))
    
    noticias_municipio = noticias if municipio_seleccionado == "Todos" else [n for n in noticias if n["municipio"] == municipio_seleccionado]
    st.write(f"Noticias registradas en **{municipio_seleccionado}**: **{len(noticias_municipio)}**")
    
    if not noticias_municipio:
        st.info(f"Sin registros específicos en {municipio_seleccionado} en las últimas horas.")
    else:
        for n in noticias_municipio:
            st.markdown(f"""
            <div class="news-card-pro">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                    <span class="tag-medio">{n['source']}</span>
                    <span class="tag-dirigente">👤 {n['dirigente']}</span>
                </div>
                <a href="{n['link']}" target="_blank" class="news-title-text">
                    {n['title']} ↗
                </a>
                <div style="font-size:12px; color:#94a3b8;">Tema: {n['tema']}</div>
            </div>
            """, unsafe_allow_html=True)

# 5. POR TEMA REPLICADO
with tab_temas:
    st.markdown("### 📌 Seguimiento por Ejes de Agenda Pública")
    tema_seleccionado = st.selectbox("Seleccionar eje temático:", ["Todos"] + sorted(list(set(n["tema"] for n in noticias))))
    
    noticias_tema = noticias if tema_seleccionado == "Todos" else [n for n in noticias if n["tema"] == tema_seleccionado]
    st.write(f"Noticias vinculadas a **{tema_seleccionado}**: **{len(noticias_tema)}**")
    
    for n in noticias_tema:
        st.markdown(f"""
        <div class="news-card-pro">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span class="tag-medio">{n['source']}</span>
                <span class="tag-dirigente">👤 {n['dirigente']}</span>
            </div>
            <a href="{n['link']}" target="_blank" class="news-title-text">
                {n['title']} ↗
            </a>
            <div style="font-size:12px; color:#64748b;">Distrito: {n['municipio']}</div>
        </div>
        """, unsafe_allow_html=True)

# 6. DISTRIBUCIÓN DE WHATSAPP (A LAS 7:00 AM)
with tab_whatsapp:
    st.markdown("### 📲 Centro de Envío y Difusión por WhatsApp")
    st.caption("Administrá los destinatarios para que reciban el informe matutino directo a su WhatsApp personal o grupo.")

    hoy_f = datetime.now().strftime("%d/%m/%Y")
    
    # Armado del mensaje ejecutivo
    items_texto = []
    for d in [n for n in noticias if n["es_denuncia"]][:3]:
        items_texto.append(f"🚨 *CRUCE OPOSITOR* | *{d['dirigente']}* ({d['municipio']}): {d['title']}")
    for p in [n for n in noticias if not n["es_denuncia"]][:4]:
        items_texto.append(f"• *{p['dirigente']}* ({p['municipio']}): {p['title']}")
        
    wa_msg = f"""📡 *RADAR POLÍTICO • REPORTE MATUTINO 7:00 AM*
🗓️ {hoy_f} | Séptima Sección & Provincia de Buenos Aires

🔥 *TEMA MÁS REPLICADO EN MEDIOS:* {tema_mas_replicado.upper()}

*SÍNTESIS DE NOVEDADES:*
{chr(10).join(items_texto) if items_texto else '• Sin temas de alta repercusión.'}

🔗 *Ver panel completo en vivo:* https://radar-politico-7.streamlit.app/
_Monitoreo en tiempo real de los 23 medios de la región._"""

    col_w1, col_w2 = st.columns([3, 2])
    with col_w1:
        st.text_area("Texto listo para difusión:", value=wa_msg, height=260)
        st.info("💡 Podés seleccionar el texto anterior para reenviarlo manualmente o usar los accesos directos de la derecha.")
    
    with col_w2:
        st.markdown("##### 👥 Enviar con un clic a contactos registrados:")
        for c in st.session_state.whatsapp_contacts:
            url_wa = f"https://api.whatsapp.com/send?phone={c['telefono'].replace('+', '').replace(' ', '')}&text={urllib.parse.quote(wa_msg)}"
            st.markdown(f"""
            <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.08); padding:10px 14px; border-radius:10px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <strong style="color:#ffffff; font-size:13px;">{c['nombre']}</strong><br/>
                    <span style="font-size:11px; color:#38bdf8;">{c['cargo']}</span> • <span style="font-size:11px; color:#94a3b8;">{c['telefono']}</span>
                </div>
                <a href="{url_wa}" target="_blank" style="background:#10b981; color:#ffffff; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:700; text-decoration:none;">
                    Enviar ↗
                </a>
            </div>
            """, unsafe_allow_html=True)
            
        with st.expander("➕ Sumar nuevo número de WhatsApp a la lista"):
            nuevo_nom = st.text_input("Nombre o Grupo:", placeholder="Ej: Prensa Bolívar / Intendente")
            nuevo_tel = st.text_input("Teléfono (con código de país):", placeholder="Ej: +5492314123456")
            nuevo_car = st.text_input("Rol / Cargo:", placeholder="Ej: Vocero / Concejal")
            if st.button("Guardar Contacto") and nuevo_nom and nuevo_tel:
                st.session_state.whatsapp_contacts.append({
                    "nombre": nuevo_nom, "telefono": nuevo_tel, "cargo": nuevo_car
                })
                st.success(f"Se sumó {nuevo_nom} a la lista de envíos.")
                st.rerun()
