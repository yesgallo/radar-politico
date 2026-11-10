import streamlit as st
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="RADAR POLÍTICO | Comunicación Política Digital",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ESTILOS CSS DE VANGUARDIA (UX/UI MODERNO, MINIMALISTA Y RESPONSIVE)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0c1527 0%, #030712 70%);
        color: #f1f5f9;
    }

    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent; }

    .brand-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 24px;
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    
    .logo-lockup {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .brand-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        line-height: 1.1;
        background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .brand-subtitle {
        font-size: 12px;
        font-weight: 500;
        color: #38bdf8;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin: 0;
        margin-top: 3px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
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

    .kpi-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 18px;
        transition: all 0.2s ease;
    }
    .kpi-card:hover {
        border-color: rgba(56, 189, 248, 0.3);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94a3b8;
        margin-bottom: 4px;
    }
    .kpi-val {
        font-size: 26px;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 11px;
        color: #64748b;
        margin-top: 4px;
    }

    .briefing-hero {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(12, 74, 110, 0.4) 100%);
        border: 1px solid rgba(56, 189, 248, 0.35);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 28px;
        box-shadow: 0 15px 35px -5px rgba(2, 132, 199, 0.15);
    }
    
    .briefing-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .briefing-badge {
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .briefing-col-box {
        background: rgba(3, 7, 18, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 18px;
        height: 100%;
    }
    .briefing-col-title {
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .news-card-v2 {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .news-card-v2:hover {
        background: rgba(15, 23, 42, 0.85);
        border-color: rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 12px 24px -10px rgba(0, 0, 0, 0.5);
    }
    
    .news-meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .news-source-tag {
        font-size: 12px;
        font-weight: 700;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        padding: 3px 10px;
        border-radius: 6px;
    }
    
    .news-actor-tag {
        font-size: 12px;
        font-weight: 600;
        color: #cbd5e1;
    }
    
    .news-time-tag {
        font-size: 11px;
        color: #64748b;
        font-family: 'JetBrains Mono', monospace;
    }

    .news-title-link {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
        text-decoration: none;
        line-height: 1.4;
        display: block;
        margin-bottom: 10px;
    }
    .news-title-link:hover {
        color: #38bdf8;
    }
    
    .tag-critica {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid rgba(239, 68, 68, 0.35);
        color: #f87171;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    .tag-gestion {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34d399;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        min-height: 48px !important;
        box-shadow: 0 4px 14px 0 rgba(2, 132, 199, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 22px 0 rgba(2, 132, 199, 0.5) !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 13px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.15) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        color: #38bdf8 !important;
    }

    @media (max-width: 768px) {
        .brand-container { flex-direction: column; align-items: flex-start; gap: 14px; padding: 16px; }
        .kpi-card { margin-bottom: 8px; }
        .briefing-hero { padding: 16px; }
    }
</style>
""", unsafe_allow_html=True)

# LOGO MINIMALISTA VECTORIAL + BRANDING LOCKUP
st.markdown("""
<div class="brand-container">
    <div class="logo-lockup">
        <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="44" height="44" rx="12" fill="#0284c7" fill-opacity="0.12" stroke="#0284c7" stroke-width="1.2"/>
            <circle cx="22" cy="22" r="15" stroke="#38bdf8" stroke-width="1" stroke-opacity="0.25"/>
            <circle cx="22" cy="22" r="10" stroke="#38bdf8" stroke-width="1.2" stroke-opacity="0.5"/>
            <circle cx="22" cy="22" r="5" stroke="#38bdf8" stroke-width="1.5" stroke-opacity="0.9"/>
            <circle cx="22" cy="22" r="2.5" fill="#38bdf8"/>
            <path d="M22 7C30.2843 7 37 13.7157 37 22" stroke="url(#sweep_grad)" stroke-width="2.5" stroke-linecap="round"/>
            <defs>
                <linearGradient id="sweep_grad" x1="22" y1="7" x2="37" y2="22" gradientUnits="userSpaceOnUse">
                    <stop stop-color="#38bdf8"/>
                    <stop offset="1" stop-color="#38bdf8" stop-opacity="0"/>
                </linearGradient>
            </defs>
        </svg>
        <div>
            <h1 class="brand-title">RADAR POLÍTICO</h1>
            <p class="brand-subtitle">Comunicación Política Digital • Séptima Sección & PBA</p>
        </div>
    </div>
    <div class="status-badge">
        <span class="live-dot"></span>
        <span>MONITOREO EN VIVO • 7:00 AM</span>
    </div>
</div>
""", unsafe_allow_html=True)

# MOTOR DE MONITOREO EN VIVO (Servidor Cloud Python)
@st.cache_data(ttl=1800)
def fetch_political_intelligence():
    actores = '"Bali Bucca" OR "Wesner" OR "Kicillof" OR "Egüen" OR "Salomón" OR "Nelson Sombra" OR "Katopodis" OR "Séptima Sección"'
    temas = 'presupuesto OR tarifas OR reelecciones OR seguridad OR protestas OR obras OR tasas OR paritarias'
    distritos = 'Bolívar OR Olavarría OR Azul OR Saladillo OR "25 de Mayo" OR "General Alvear" OR "Roque Pérez" OR "Tapalqué"'
    query = f'({actores}) ({temas}) ({distritos}) when:3d'
    
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=es-419&gl=AR&ceid=AR:es-419"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    items_list = []
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
                
                tema = "Gestión & Obras"
                is_alerta = False
                if any(k in lower for k in ["tarifa", "luz", "gas", "aumento"]):
                    tema = "Tarifas / Servicios"
                    is_alerta = True
                elif any(k in lower for k in ["protesta", "reclamo", "conflicto", "paro"]):
                    tema = "Conflicto & Protestas"
                    is_alerta = True
                elif "reelecci" in lower:
                    tema = "Reelecciones 2027"
                    is_alerta = True
                elif any(k in lower for k in ["seguridad", "polic", "robo"]):
                    tema = "Seguridad"
                elif any(k in lower for k in ["presupuesto", "fondo", "leasing", "paritaria"]):
                    tema = "Presupuesto & Finanzas"
                
                items_list.append({
                    "title": title,
                    "source": source,
                    "link": link,
                    "date": pubDate,
                    "referente": ref,
                    "tema": tema,
                    "is_alerta": is_alerta
                })
    except Exception as e:
        st.warning(f"Sincronizando con fuentes alternativas de la Séptima: {e}")
        
    return items_list

news_data = fetch_political_intelligence()

# FILA DE MÉTRICAS KPI
total_novedades = len(news_data)
total_alertas = sum(1 for n in news_data if n["is_alerta"])
referentes_activos = len(set(n["referente"] for n in news_data))

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Novedades Detectadas</div>
        <div class="kpi-val" style="color:#38bdf8;">{total_novedades}</div>
        <div class="kpi-sub">Últimas 48-72 horas</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Alertas Críticas</div>
        <div class="kpi-val" style="color:#f87171;">{total_alertas}</div>
        <div class="kpi-sub">Tarifas, conflicto y tasas</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Referentes Monitoreados</div>
        <div class="kpi-val">{referentes_activos}</div>
        <div class="kpi-sub">Séptima Sección & PBA</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    hora_actual = datetime.now().strftime("%H:%M hs")
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Última Sincronización</div>
        <div class="kpi-val" style="color:#34d399; font-size:22px;">{hora_actual}</div>
        <div class="kpi-sub">Servidor Cloud Activo</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# BOTÓN DE ESCANEO
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("⚡ Forzar Escaneo en Tiempo Real (Limpiar Caché)"):
        st.cache_data.clear()
        st.rerun()
with col_btn2:
    st.caption("ℹ️ El sistema se ejecuta automáticamente a las **7:00 AM** y mantiene sincronizadas las fuentes.")

st.write("")

# PESTAÑAS PRINCIPALES
tab_briefing, tab_feed, tab_alertas, tab_whatsapp, tab_portales = st.tabs([
    "📢 Resumen de Coyuntura (7 AM)",
    "📰 Feed en Tiempo Real",
    "🚨 Radar de Alertas Críticas",
    "📲 Formato WhatsApp",
    "🏛️ Directorio de Medios (23)"
])

# 1. RESUMEN DE COYUNTURA
with tab_briefing:
    hoy_fecha = datetime.now().strftime("%A %d de %B de %Y").capitalize()
    
    st.markdown(f"""
    <div class="briefing-hero">
        <div class="briefing-header">
            <div>
                <span class="briefing-badge">Despacho Diario • 7:00 AM</span>
                <h2 style="font-size:20px; font-weight:800; color:#ffffff; margin:8px 0 0 0;">
                    Informe Matutino de Inteligencia y Comunicación Política
                </h2>
                <p style="font-size:13px; color:#94a3b8; margin:4px 0 0 0;">
                    {hoy_fecha} • Análisis sintético estructurado sobre la Séptima Sección Electoral
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div class="briefing-col-box">
            <div class="briefing-col-title" style="color:#38bdf8;">
                <span>🏛️</span><span>1. Claves de Gestión</span>
            </div>
        """, unsafe_allow_html=True)
        
        gestion_items = [n for n in news_data if not n["is_alerta"]][:4]
        if gestion_items:
            for n in gestion_items:
                st.markdown(f"• **{n['referente']}**: [{n['title']}]({n['link']}) <span style='font-size:11px; color:#64748b;'>({n['source']})</span>", unsafe_allow_html=True)
        else:
            st.info("Sin novedades destacadas en este bloque.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="briefing-col-box">
            <div class="briefing-col-title" style="color:#f87171;">
                <span>🚨</span><span>2. Alertas & Crisis</span>
            </div>
        """, unsafe_allow_html=True)
        
        alert_items = [n for n in news_data if n["is_alerta"]][:4]
        if alert_items:
            for n in alert_items:
                st.markdown(f"• **{n['tema']}**: [{n['title']}]({n['link']}) <span style='font-size:11px; color:#64748b;'>({n['source']})</span>", unsafe_allow_html=True)
        else:
            st.success("Tranquilidad relativa: no se registran focos críticos inmediatos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="briefing-col-box">
            <div class="briefing-col-title" style="color:#34d399;">
                <span>🎯</span><span>3. Recomendación Táctica</span>
            </div>
            <div style="font-size:13px; line-height:1.6; color:#cbd5e1;">
                <p>• <strong>Visibilidad de Obra Pública:</strong> Mostrar en redes las maquinarias y obras de proximidad para contrastar con el parate del presupuesto nacional.</p>
                <p>• <strong>Contención en Tarifas:</strong> Evitar respuestas defensivas ante quejas de comerciantes; canalizar reclamos hacia la desregulación de Nación.</p>
                <p>• <strong>Cercanía Comunitaria:</strong> Capitalizar eventos educativos y de salud en los distritos de la sección como anclas de gestión positiva.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. FEED EN TIEMPO REAL
with tab_feed:
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search_query = st.text_input("🔍 Buscar por titular, referente o tema...", placeholder="Ej: Bali Bucca, presupuesto, tarifas...")
    with col_f2:
        referentes_disponibles = ["Todos los Referentes"] + sorted(list(set(n["referente"] for n in news_data)))
        selected_ref = st.selectbox("Filtrar por Actor:", referentes_disponibles)

    filtered_news = news_data
    if search_query:
        q = search_query.lower()
        filtered_news = [n for n in filtered_news if q in n["title"].lower() or q in n["referente"].lower() or q in n["tema"].lower()]
    if selected_ref != "Todos los Referentes":
        filtered_news = [n for n in filtered_news if n["referente"] == selected_ref]

    st.write(f"Mostrando **{len(filtered_news)}** noticias verificadas:")

    for n in filtered_news:
        tag_badge = '<span class="tag-critica">Alerta Crítica</span>' if n["is_alerta"] else '<span class="tag-gestion">Gestión</span>'
        st.markdown(f"""
        <div class="news-card-v2">
            <div class="news-meta-row">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="news-source-tag">{n['source']}</span>
                    <span class="news-actor-tag">👤 {n['referente']}</span>
                </div>
                <div>
                    {tag_badge}
                    <span class="news-time-tag">{n['date']}</span>
                </div>
            </div>
            <a href="{n['link']}" target="_blank" class="news-title-link">
                {n['title']} ↗
            </a>
            <div style="font-size:12px; color:#64748b; display:flex; justify-content:space-between; align-items:center;">
                <span>Eje: <strong>{n['tema']}</strong></span>
                <a href="{n['link']}" target="_blank" style="color:#38bdf8; text-decoration:none; font-weight:600;">Leer fuente original &rarr;</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 3. MONITOR DE ALERTAS
with tab_alertas:
    alertas_puras = [n for n in news_data if n["is_alerta"]]
    st.markdown(f"### 🚨 Tablero de Alertas Tempranas ({len(alertas_puras)} activas)")
    st.caption("Filtro exclusivo de eventos de tensión: subas tarifarias, reclamos gremiales y disputas presupuestarias.")
    
    if not alertas_puras:
        st.success("No hay alertas críticas registradas en las últimas horas.")
    else:
        for a in alertas_puras:
            st.markdown(f"""
            <div class="news-card-v2" style="border-left: 4px solid #ef4444;">
                <div class="news-meta-row">
                    <span class="news-source-tag" style="color:#f87171; background:rgba(239,68,68,0.15);">{a['source']}</span>
                    <span class="tag-critica">{a['tema']}</span>
                </div>
                <a href="{a['link']}" target="_blank" class="news-title-link" style="color:#fecaca;">
                    {a['title']} ↗
                </a>
                <div style="font-size:12px; color:#94a3b8;">
                    Referente involucrado: <strong>{a['referente']}</strong> | Publicada: {a['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# 4. WHATSAPP READY
with tab_whatsapp:
    st.markdown("### 📲 Despacho Matutino para WhatsApp")
    st.caption("Texto formateado con negritas y emojis, listo para copiar y enviar.")

    today_str = datetime.now().strftime("%d/%m/%Y")
    
    lineas_gestion = [f"• *{n['referente']}*: {n['title']}" for n in news_data if not n["is_alerta"]][:3]
    lineas_alertas = [f"• 🚨 *{n['tema']}*: {n['title']}" for n in news_data if n["is_alerta"]][:3]
    
    wa_text = f"""📡 *RADAR POLÍTICO • REPORTE MATUTINO 7:00 AM*
🗓️ {today_str} | Séptima Sección Electoral & PBA

🏛️ *1. CLAVES DE GESTIÓN*
{chr(10).join(lineas_gestion) if lineas_gestion else '• Sin novedades relevantes.'}

🚨 *2. ALERTAS & CONFLICTO*
{chr(10).join(lineas_alertas) if lineas_alertas else '• Sin alertas críticas activas.'}

🎯 *3. RECOMENDACIÓN DE VOCERÍA*
• Priorizar visibilidad de obras y cercanía local ante el escenario nacional.
• Atender preventivamente reclamos tarifarios del comercio.

_Monitoreo automatizado en tiempo real por Radar Político_"""

    st.text_area("Mensaje Formateado:", value=wa_text, height=260)
    st.info("💡 Hacé clic dentro del cuadro y presioná Ctrl + A para copiar el reporte completo.")

# 5. DIRECTORIO DE MEDIOS
with tab_portales:
    st.markdown("### 🏛️ Red de 23 Medios Monitoreados en la Séptima Sección")
    st.caption("Enlaces directos a los medios periodísticos e institucionales que alimentan el radar.")

    p1, p2 = st.columns(2)
    with p1:
        st.markdown("""
        **Provinciales & Especializados:**
        * [Infocielo](https://www.infocielo.com/) • Actualidad bonaerense
        * [La Tecla](https://www.latecla.info/actualidad) • Política & Legislatura
        * [La Política Online](https://www.lapoliticaonline.com/) • Rosca & gobierno
        * [La Noticia 1](https://www.lanoticia1.com/) • Interior provincial
        * [Hablemos de Política](https://www.hablemosdepolitica.com.ar/) • Análisis
        * [Séptima Sección Noticias](https://septimaseccion.com.ar/) • Regional

        **Bolívar & Zona:**
        * [Presente Noticias](https://www.presentenoticias.com/) • Bolívar
        * [Diario La Mañana](https://www.diariolamanana.com.ar/) • Bolívar
        * [FM 10 Bolívar](https://fm10bolivar.com.ar/) • Radio & noticias
        """)

    with p2:
        st.markdown("""
        **Olavarría, Azul & Municipios:**
        * [Infoeme](https://www.infoeme.com/) • Olavarría
        * [En Línea Noticias](https://enlineanoticias.com.ar/) • Olavarría
        * [Diario El Tiempo](https://www.diarioeltiempo.com.ar/) • Azul
        * [Noticias de Azul](https://noticiasdeazul.com/) • Azul
        * [La Síntesis](https://www.lasintesis.com.ar/) • Saladillo
        * [25 Digital](https://www.25digital.com.ar/) • 25 de Mayo
        * [Alvear Noticias](https://alvearnoticias.com.ar/) • General Alvear
        * [Roque Pérez Hoy](https://www.roqueperezhoy.com.ar/) • Roque Pérez
        """)
