import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pandas as pd
from api_handler import get_todays_matches

# Configuración de la página
st.set_page_config(
    page_title="Partidos de Fútbol Argentino",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título profesional
st.title("⚽ Dashboard de Partidos - Fútbol Argentino")
st.markdown("---")

# Auto-refresh cada 60 segundos
st_autorefresh(interval=60*1000, key="data_refresh")

# Función cacheada para obtener datos
@st.cache_data(ttl=60)
def get_cached_matches():
    """Obtiene los partidos de hoy con cache de 60 segundos"""
    try:
        return get_todays_matches()
    except Exception as e:
        st.error(f"Error al obtener los partidos: {e}")
        return pd.DataFrame()

# Obtener datos
df = get_cached_matches()

# Indicador de última actualización
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"**Última actualización:** {datetime.now().strftime('%H:%M:%S')}")
st.markdown("---")

# Mostrar resultados si hay datos
if not df.empty:
    # Obtener ligas únicas
    leagues = df['Liga'].unique()
    
    # Mostrar cada liga en su propia sección
    for league in leagues:
        league_df = df[df['Liga'] == league]
        
        # Subtítulo de la liga
        st.subheader(f"🏆 {league}")
        
        # Configurar el DataFrame para mostrar
        display_df = league_df[['Hora', 'Local', 'Visitante', 'Resultado']].copy()
        
        # Mostrar la tabla
        st.table(display_df)
        
        st.markdown("---")
else:
    st.warning("No hay partidos programados para hoy.")
    st.info("Verifica que tu API Key esté configurada correctamente en el archivo .env")

# Información adicional en sidebar
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    Este dashboard muestra los partidos de hoy de las siguientes ligas argentinas:
    
    - **Liga Profesional**
    - **Primera Nacional**
    - **Federal A**
    
    Los datos se actualizan automáticamente cada 60 segundos.
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuración")
    st.markdown("La aplicación se recarga automáticamente para mantener los datos actualizados en tiempo real.")
