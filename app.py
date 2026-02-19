import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# --- CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="SNIPER ELITE AI | PRO", layout="wide", page_icon="🎯")

# --- BANCO DE DATOS CONECTADO (LINK FORNECIDO) ---
URL_DB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZU5Y6Fmmp-Mjl_vlyZkCNtuybCzldoQ78AKS9hWo7lwmUrvBQCUMyZbDUguAW2uOQmOhijo01rjsq/pub?output=csv"

def verificar_acesso(email_user, senha_user):
    try:
        # Lê a planilha publicada em CSV
        df_db = pd.read_csv(URL_DB)
        # Limpa espaços em branco para evitar erros
        df_db.columns = df_db.columns.str.strip().str.lower()
        df_db['email'] = df_db['email'].astype(str).str.strip()
        df_db['senha'] = df_db['senha'].astype(str).str.strip()
        
        # Procura o usuário
        permitido = df_db[(df_db['email'] == email_user.strip()) & (df_db['senha'] == senha_user.strip())]
        return not permitido.empty
    except Exception as e:
        # Em caso de erro na leitura da planilha (ex: link offline)
        return False

# --- FRONT-END ORIGINAL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #05070a; color: #e5e7eb; }
    .login-container {
        background: rgba(17, 23, 30, 0.9); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.7);
    }
    .user-profile {
        display: flex; align-items: center; gap: 15px;
        background: rgba(255, 255, 255, 0.05); padding: 15px;
        border-radius: 15px; margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .avatar {
        width: 50px; height: 50px; border-radius: 50%;
        background: linear-gradient(45deg, #00ffcc, #d4af37);
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; color: #000; font-size: 20px;
    }
    .card-sinal { padding: 35px; border-radius: 20px; text-align: center; border: 2px solid #1f2937; margin-bottom: 15px; }
    .buy-zone { background: rgba(0, 255, 204, 0.12); color: #00ffcc; border-color: #00ffcc; }
    .sell-zone { background: rgba(255, 75, 75, 0.12); color: #ff4b4b; border-color: #ff4b4b; }
    .stButton>button {
        background: linear-gradient(90deg, #00ffcc, #00ccaa) !important;
        color: #06090c !important; font-weight: 800 !important;
        border-radius: 12px !important; height: 50px !important; border: none !important;
    }
    .metric-box { background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #1f2937; text-align: center; }
    .timer-text { color: #d4af37; font-weight: 900; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if 'logado' not in st.session_state: st.session_state.logado = False

if not st.session_state.logado:
    _, col_mid, _ = st.columns([1, 1.3, 1])
    with col_mid:
        st.markdown('<div class="login-container"><h1>🎯 SNIPER ELITE</h1>', unsafe_allow_html=True)
        u_email = st.text_input("E-mail Cadastrado:")
        u_senha = st.text_input("Senha de Acesso:", type="password")
        if st.button("ENTRAR AGORA"):
            if verificar_acesso(u_email, u_senha):
                st.session_state.logado = True
                st.session_state.name = u_email.split('@')[0].upper()
                st.rerun()
            else:
                st.error("Acesso Negado: E-mail ou Senha incorretos.")
    st.stop()

# --- CONFIGURAÇÕES DO ROBÔ (ORIGINAIS) ---
with st.sidebar:
    letra = st.session_state.name[0].upper()
    st.markdown(f'<div class="user-profile"><div class="avatar">{letra}</div><div><b>{st.session_state.name}</b><br><small>VIP ACTIVE</small></div></div>', unsafe_allow_html=True)
    ativo = st.selectbox("Selecione o Par:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "XAUUSD=X", "SOL-USD"])
    timeframe = st.radio("Timeframe:", ["1m", "5m", "15m"], horizontal=True)
    st.divider()
    if st.button("Deslogar"):
        st.session_state.logado = False
        st.rerun()

def calcular_fechamento(tf):
    agora = datetime.now()
    minutos_tf = int(tf.replace("m", ""))
    segundos_passados = (agora.minute % minutos_tf) * 60 + agora.second
    total_segundos = minutos_tf * 60
    restante = total_segundos - segundos_passados
    mins, segs = divmod(restante, 60)
    return f"{mins:02d}:{segs:02d}"

try:
    df = yf.download(ativo, period="2d", interval=timeframe, progress=False)
    if df is not None and not df.empty and len(df) > 15:
        df = df.dropna()
        df['cor'] = (df['Close'] > df['Open']).astype(int)
        df['win_seq'] = (df['cor'] == df['cor'].shift(1)).astype(int)
        win_rate = float(df['win_seq'].tail(40).mean() * 100)
        
        ultima = df.iloc[-1]
        preco_atual = float(ultima['Close'])
        ema9 = float(df['Close'].ewm(span=9).mean().iloc[-1])
        tempo_restante = calcular_fechamento(timeframe)

        st.markdown(f"### 🛡️ Sniper Intelligence: {ativo}")
        m1, m2, m3 = st.columns(3)
        with m1: st.markdown(f"<div class='metric-box'><small>ASSERTIVIDADE</small><br><b style='color:#00ffcc;'>{win_rate:.1f}%</b></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-box'><small>PRÓXIMA VELA EM</small><br><b class='timer-text'>{tempo_restante}</b></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-box'><small>GESTÃO</small><br><b>1 GALE MAX</b></div>", unsafe_allow_html=True)

        st.divider()
        col_sig, col_graph = st.columns([1.2, 2.5])

        with col_sig:
            st.markdown("#### 📡 SINAL DA IA")
            decisao = "AGUARDAR"
            if win_rate >= 50.0:
                if preco_atual > ema9: decisao = "CALL"
                else: decisao = "PUT"
            
            if decisao == "CALL":
                st.markdown(f'<div class="card-sinal buy-zone"><h2>🔥 CALL</h2><p>ENTRADA CONFIRMADA</p></div>', unsafe_allow_html=True)
            elif decisao == "PUT":
                st.markdown(f'<div class="card-sinal sell-zone"><h2>📉 PUT</h2><p>ENTRADA CONFIRMADA</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card-sinal" style="color:#6b7280;"><h2>⏳ AGUARDAR</h2><p>BUSCANDO PADRÃO</p></div>', unsafe_allow_html=True)
            
            if st.button("VERIFICAR PAR DE MOEDA"):
                st.rerun()

        with col_graph:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)
except:
    st.info("🔄 Sincronizando conexão...")

st.caption(f"Sniper Elite v18.5 | Banco de Dados Ativo | {datetime.now().strftime('%H:%M:%S')}")