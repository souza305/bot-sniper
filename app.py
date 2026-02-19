import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI | VIP", layout="wide", page_icon="🎯")

# --- ESTILO CSS PARA LOGO E INTERFACE ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .brand-title {
        color: #00ffcc;
        font-family: 'Courier New', Courier, monospace;
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
        text-shadow: 2px 2px #000000;
    }
    .brand-subtitle {
        color: #ffffff;
        text-align: center;
        font-size: 14px;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00ffcc; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email_usuario):
    email_limpo = email_usuario.lower().strip()
    if email_limpo == "wpmail222@gmail.com":
        return True
    SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv"
    try:
        df_acesso = pd.read_csv(SHEET_URL)
        lista_autorizada = df_acesso['email'].str.lower().str.strip().tolist()
        return email_limpo in lista_autorizada
    except:
        return False

# --- TELA DE LOGIN COM LOGO ---
def login_screen():
    st.markdown('<p class="brand-title">🎯 SNIPER ELITE AI</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-subtitle">PRECISION TRADING SYSTEM</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("### 🔐 Área do Assinante")
        email = st.text_input("Digite seu e-mail da Kiwify para liberar os sinais:", placeholder="exemplo@email.com")
        if email:
            if check_access(email):
                st.success("Acesso Liberado! Carregando painel...")
                return email
            else:
                st.error("E-mail não encontrado ou assinatura expirada.")
                st.stop()
        else:
            st.info("Aguardando seu e-mail de compra...")
            st.stop()
    return None

# Executa tela de login
user_email = login_screen()

# --- SE CHEGOU AQUI, O ACESSO FOI LIBERADO ---

# Sidebar para configurações após login
with st.sidebar:
    st.markdown(f"👤 **Usuário:** {user_email}")
    st.markdown("---")
    ativo = st.selectbox("Selecione o Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X"])
    timeframe = st.radio("Timeframe:", ["1m", "5m", "15m", "1h"], horizontal=True)
    st.markdown("---")
    if st.button("Sair"):
        st.rerun()

# --- PAINEL DE SINAIS ---
st.title(f"📊 Monitoramento: {ativo}")

try:
    periodo = "1d" if timeframe in ["1m", "5m", "15m"] else "5d"
    dados = yf.download(ativo, period=periodo, interval=timeframe, progress=False)

    if not dados.empty and len(dados) >= 2:
        preco_atual = float(dados['Close'].iloc[-1])
        preco_anterior = float(dados['Close'].iloc[-2])
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Cotação Atual", f"{preco_atual:.4f}")
        c2.metric("Variação", f"{variacao:.2f}%")
        
        if preco_atual > preco_anterior:
            c3.success("🔥 SINAL: COMPRA")
        else:
            c3.error("📉 SINAL: VENDA")

        fig = go.Figure(data=[go.Candlestick(
            x=dados.index, open=dados['Open'], high=dados['High'],
            low=dados['Low'], close=dados['Close'],
            increasing_line_color='#00ffcc', decreasing_line_color='#ff4b4b'
        )])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("Mercado fechado ou sem dados. O Forex pausa nos finais de semana. Teste com BTC-USD.")

except Exception as e:
    st.error("Conectando ao servidor de sinais... Aguarde.")

st.markdown("---")
st.caption(f"Sniper Elite AI | v2.0 | {datetime.now().strftime('%H:%M:%S')}")
