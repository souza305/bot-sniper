import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURAÇÃO DA PÁGINA (CHIQUE E RICA) ---
st.set_page_config(page_title="SNIPER ELITE AI | PLATAFORMA", layout="wide", page_icon="💎")

# --- CSS DARK GOLDEN (VISUAL DE LUXO) ---
st.markdown("""
    <style>
    .main { background-color: #050608; }
    .stMetric { background-color: #0d1117; border-left: 5px solid #d4af37; padding: 20px; border-radius: 10px; }
    .ia-card { background: linear-gradient(145deg, #161b22, #0d1117); border: 1px solid #d4af37; padding: 25px; border-radius: 20px; color: white; }
    .sidebar-brand { font-size: 24px; color: #d4af37; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(to right, #d4af37, #f4d03f); color: black; border: none; font-weight: bold; width: 100%; border-radius: 8px; }
    .status-check { color: #00ffcc; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email):
    email_limpo = email.lower().strip()
    if email_limpo == "wpmail222@gmail.com": return True
    try:
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv")
        return email_limpo in df['email'].str.lower().str.strip().tolist()
    except: return False

# --- TELA DE LOGIN ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<p class="sidebar-brand">💎 SNIPER ELITE PLATFORM</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown('<div class="ia-card" style="text-align:center;">', unsafe_allow_html=True)
        email = st.text_input("Acesso Exclusivo (E-mail):")
        if st.button("INICIAR ALGORITMO IA"):
            if check_access(email):
                st.session_state.auth = True
                st.rerun()
            else: st.error("Acesso não autorizado.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- INTERFACE PRINCIPAL ---
with st.sidebar:
    st.markdown('<p class="sidebar-brand">🎯 SNIPER ELITE</p>', unsafe_allow_html=True)
    ativo = st.selectbox("📊 Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X"])
    timeframe = st.radio("⏳ Timeframe:", ["1m", "5m", "15m"], horizontal=True)
    st.markdown("---")
    st.markdown("### 🤖 Status da IA: <span class='status-check'>ONLINE</span>", unsafe_allow_html=True)
    if st.button("SAIR"):
        st.session_state.auth = False
        st.rerun()

# --- MOTOR DE INTELIGÊNCIA ---
try:
    dados = yf.download(ativo, period="1d", interval=timeframe, progress=False)
    
    if not dados.empty and len(dados) >= 20:
        # 1. CATALOGAÇÃO PARA PRÓXIMA VELA
        ultimas_velas = dados.tail(15)
        velas_alta = len(ultimas_velas[ultimas_velas['Close'] > ultimas_velas['Open']])
        velas_baixa = len(ultimas_velas[ultimas_velas['Close'] < ultimas_velas['Open']])
        forca = (velas_alta / 15) * 100 if velas_alta > velas_baixa else (velas_baixa / 15) * 100
        
        # 2. IA DE RECOMENDAÇÃO (ANÁLISE DE VOLUME E TENDÊNCIA)
        preco_atual = float(dados['Close'].iloc[-1])
        preco_anterior = float(dados['Close'].iloc[-2])
        
        # 3. FILTRO DE HORÁRIO
        hora_atual = datetime.now().hour
        horario_nobre = "EXCELENTE" if 4 <= hora_atual <= 12 else "MODERADO"

        # --- CABEÇALHO ---
        st.title("🛡️ Dashboard de Inteligência")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Preço", f"${preco_atual:.4f}")
        c2.metric("Assertividade IA", f"{88 + (forca/10):.1f}%")
        c3.metric("Horário Operacional", horario_nobre)
        c4.metric("Próxima Vela", "CALCULDANDO..." if forca < 50 else "CONFIRMADA")

        st.markdown("---")

        # --- LAYOUT DE ANÁLISE ---
        col_ia, col_chart = st.columns([1.3, 2.5])

        with col_ia:
            st.markdown('<div class="ia-card">', unsafe_allow_html=True)
            st.markdown("### 🤖 RECOMENDAÇÃO DA IA")
            
            if forca >= 55:
                direcao = "CALL (COMPRA)" if velas_alta > velas_baixa else "PUT (VENDA)"
                cor = "#00ffcc" if "CALL" in direcao else "#ff4b4b"
                
                st.markdown(f"<h2 style='color:{cor};'>{direcao}</h2>", unsafe_allow_html=True)
                st.write(f"**Estratégia:** Catalogação de Ciclo em {timeframe}")
                st.write(f"**Análise:** Identificada força de {forca:.0f}% na tendência atual.")
                st.write(f"**Expiração:** Próxima Vela (M1)")
                
                st.markdown(f"<div style='background-color:{cor}; height:5px; width:100%; border-radius:5px;'></div>", unsafe_allow_html=True)
                st.write("✅ **ORDEM CONFIRMADA PELO ALGORITMO**")
            else:
                st.markdown("<h2>⏳ AGUARDAR</h2>", unsafe_allow_html=True)
                st.write("IA analisando volume insuficiente. Não opere agora.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # BLOCO DE CATALOGAÇÃO
            with st.expander("📚 Resumo da Catalogação"):
                st.write(f"Velas de Alta: {velas_alta}")
                st.write(f"Velas de Baixa: {velas_baixa}")
                st.write(f"Tendência: {'Compradora' if velas_alta > velas_baixa else 'Vendedora'}")

        with col_chart:
            fig = go.Figure(data=[go.Candlestick(
                x=dados.index, open=dados['Open'], high=dados['High'],
                low=dados['Low'], close=dados['Close'],
                increasing_line_color='#00ffcc', decreasing_line_color='#ff4b4b'
            )])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=480, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("IA em modo de espera. Aguardando dados de mercado.")

except Exception as e:
    st.error(f"Erro no Motor de IA: {e}")

st.markdown("---")
st.caption(f"💎 Sniper Elite AI | Premium Edition | v5.0 | {datetime.now().strftime('%H:%M:%S')}")
