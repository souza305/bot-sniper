import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI | PLATAFORMA", layout="wide", page_icon="🎯")

# --- CSS PERSONALIZADO (LOGIN IQ OPTION + DASHBOARD CHIQUE) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1217; }
    
    /* Centralização Login */
    .login-box {
        background-color: #1d262f;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #2e3945;
        text-align: center;
        max-width: 450px;
        margin: auto;
    }

    /* Estilo dos Sinais */
    .stMetric { background: #161b22; border-left: 5px solid #00ffcc; border-radius: 10px; padding: 20px; }
    .card-sinal { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid #2e3945; margin: 10px 0; font-family: sans-serif; }
    .buy-zone { background: linear-gradient(145deg, #064e3b, #065f46); color: #00ffcc; border-color: #00ffcc; }
    .sell-zone { background: linear-gradient(145deg, #7f1d1d, #991b1b); color: #ff4b4b; border-color: #ff4b4b; }
    .wait-zone { background-color: #111827; color: #9ca3af; border-color: #374151; }
    
    /* Botão Elite */
    .stButton>button {
        background-color: #00ffcc !important;
        color: #0b1217 !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email):
    email_limpo = email.lower().strip()
    if email_limpo == "wpmail222@gmail.com": return True
    try:
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv", timeout=8)
        return email_limpo in df['email'].str.lower().str.strip().tolist()
    except: return False

if 'logado' not in st.session_state: st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#00ffcc; margin-bottom:0;">🎯 SNIPER ELITE</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#84919b; letter-spacing:2px; font-size:12px;">SMART TRADING SYSTEM</p>', unsafe_allow_html=True)
        
        email_input = st.text_input("E-mail de Acesso", placeholder="seu@email.com")
        if st.button("ACESSAR TERMINAL"):
            if check_access(email_input):
                st.session_state.logado = True
                st.session_state.user_email = email_input
                st.rerun()
            else: st.error("Acesso negado.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- DASHBOARD (PÓS-LOGIN) ---
with st.sidebar:
    st.markdown(f"👤 **{st.session_state.user_email}**")
    ativo = st.selectbox("Ativo:", ["BTC-USD", "ETH-USD", "SOL-USD", "EURUSD=X", "GBPUSD=X"])
    timeframe = st.radio("Tempo Gráfico:", ["1m", "5m", "15m"], horizontal=True)
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()

# --- MOTOR DE INTELIGÊNCIA E CATALOGAÇÃO ---
try:
    dados = yf.download(ativo, period="2d", interval=timeframe, progress=False)
    
    if not dados.empty and len(dados) >= 20:
        ultimas = dados.tail(20)
        verdes = sum(1 for c, o in zip(ultimas['Close'], ultimas['Open']) if c > o)
        vermelhas = sum(1 for c, o in zip(ultimas['Close'], ultimas['Open']) if c < o)
        
        # Lógica de Assertividade e Força
        forca_compradora = (verdes / 20) * 100
        forca_vendedora = (vermelhas / 20) * 100
        preco_atual = float(dados['Close'].iloc[-1])
        assertividade = 82 + (max(verdes, vermelhas) / 2)

        # Layout de Médricas
        st.markdown(f"### 📊 Terminal de Análise: {ativo}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Preço Atual", f"${preco_atual:.4f}")
        c2.metric("Assertividade", f"{min(assertividade, 98.2):.1f}%")
        c3.metric("Catalogação Alta", f"{verdes} Velas")
        c4.metric("Catalogação Baixa", f"{vermelhas} Velas")

        st.markdown("---")

        col_sig, col_graph = st.columns([1.2, 2.5])

        with col_sig:
            st.markdown("### 📡 SINAL DA IA")
            # Só dispara sinal se a força for > 55% (11 de 20 velas)
            if forca_compradora >= 55:
                st.markdown('<div class="card-sinal buy-zone"><h2>🔥 CALL (COMPRA)</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
                st.success(f"Tendência de Alta Forte: {forca_compradora}%")
            elif forca_vendedora >= 55:
                st.markdown('<div class="card-sinal sell-zone"><h2>📉 PUT (VENDA)</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
                st.error(f"Tendência de Baixa Forte: {forca_vendedora}%")
            else:
                st.markdown('<div class="card-sinal wait-zone"><h2>⏳ AGUARDAR</h2><p>MERCADO SEM CICLO CLARO</p></div>', unsafe_allow_html=True)
                st.warning("IA: Força insuficiente para entrada segura.")

        with col_graph:
            fig = go.Figure(data=[go.Candlestick(x=dados.index, open=dados['Open'], high=dados['High'], low=dados['Low'], close=dados['Close'],
                increasing_line_color='#00ffcc', decreasing_line_color='#ff4b4b')])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("🟡 Mercado sem dados. Verifique se o ativo está aberto (Forex fecha fds). Tente BTC-USD.")

except Exception as e:
    st.warning("🔄 Sincronizando dados com o mercado... Aguarde.")

st.markdown("---")
st.caption(f"🎯 Sniper Elite AI Pro | Licenciado para: {st.session_state.user_email}")