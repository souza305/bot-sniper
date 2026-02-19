import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="SNIPER ELITE AI | PRO", layout="wide", page_icon="🎯")

# --- BANCO DE DATOS CONECTADO ---
URL_DB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTZU5Y6Fmmp-Mjl_vlyZkCNtuybCzldoQ78AKS9hWo7lwmUrvBQCUMyZbDUguAW2uOQmOhijo01rjsq/pub?output=csv"

@st.cache_data(ttl=30)
def fetch_data(ativo, tf):
    return yf.download(ativo, period="2d", interval=tf, progress=False)

def verificar_acesso(email_user, senha_user):
    try:
        df_db = pd.read_csv(URL_DB)
        df_db.columns = df_db.columns.str.strip().str.lower()
        permitido = df_db[(df_db['email'] == email_user.strip()) & (df_db['senha'].astype(str) == senha_user.strip())]
        return not permitido.empty
    except: return False

# --- FRONT-END ORIGINAL (CONGELADO) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #05070a; color: #e5e7eb; }
    .login-container { background: rgba(17, 23, 30, 0.9); padding: 50px; border-radius: 25px; text-align: center; }
    .user-profile { display: flex; align-items: center; gap: 15px; background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; margin-bottom: 20px; }
    .avatar { width: 50px; height: 50px; border-radius: 50%; background: linear-gradient(45deg, #00ffcc, #d4af37); display: flex; align-items: center; justify-content: center; font-weight: bold; color: #000; }
    .card-sinal { padding: 35px; border-radius: 20px; text-align: center; border: 2px solid #1f2937; margin-bottom: 15px; }
    .buy-zone { background: rgba(0, 255, 204, 0.12); color: #00ffcc; border-color: #00ffcc; }
    .sell-zone { background: rgba(255, 75, 75, 0.12); color: #ff4b4b; border-color: #ff4b4b; }
    .metric-box { background: rgba(255,255,255,0.03); padding: 15px; border-radius: 10px; border: 1px solid #1f2937; text-align: center; }
    .timer-text { color: #d4af37; font-weight: 900; font-size: 1.4rem; }
    .gestion-card { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-top: 5px; border-left: 3px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if 'logado' not in st.session_state: st.session_state.logado = False
if not st.session_state.logado:
    _, col_mid, _ = st.columns([1, 1.3, 1])
    with col_mid:
        st.markdown('<div class="login-container"><h1>🎯 SNIPER ELITE</h1>', unsafe_allow_html=True)
        u_email = st.text_input("E-mail:")
        u_senha = st.text_input("Senha:", type="password")
        if st.button("ENTRAR"):
            if verificar_acesso(u_email, u_senha):
                st.session_state.logado = True
                st.session_state.name = u_email.split('@')[0].upper()
                st.rerun()
    st.stop()

# --- SIDEBAR (GESTÃO INTELIGENTE) ---
with st.sidebar:
    st.markdown(f'<div class="user-profile"><div class="avatar">{st.session_state.name[0]}</div><div><b>{st.session_state.name}</b><br><small>VIP ACTIVE</small></div></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Gestão Inteligente")
    banca_atual = st.number_input("Banca Atual ($)", min_value=0.0, value=100.0, step=10.0)
    
    # Recomendação Automática (5% a 10%)
    meta_sugerida = banca_atual * 0.10 # Sugere 10% por padrão
    
    st.markdown("#### Meta do Dia")
    tipo_meta = st.radio("Definir meta por:", ["Porcentagem (%)", "Valor Fixo ($)"], horizontal=True)
    
    if tipo_meta == "Porcentagem (%)":
        porcentagem = st.slider("Escolha % da Banca", 1, 20, 10)
        valor_meta = banca_atual * (porcentagem / 100)
    else:
        valor_meta = st.number_input("Valor desejado ($)", min_value=0.0, value=meta_sugerida)

    # Exibição da recomendação operacional
    st.markdown(f"""
    <div class="gestion-card">
        <small>RECOMENDAÇÃO SNIPER:</small><br>
        <b>Meta (Take): <span style="color:#00ffcc;">${valor_meta:.2f}</span></b><br>
        <b>Stop Loss: <span style="color:#ff4b4b;">${valor_meta * 0.8:.2f}</span></b>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    payout = st.slider("Payout %", 70, 100, 87)
    entrada_base = st.number_input("Valor da Entrada ($)", value=banca_atual * 0.02)
    
    st.divider()
    ativo = st.selectbox("Par:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "XAUUSD=X", "SOL-USD"])
    timeframe = st.radio("TF:", ["1m", "5m", "15m"], horizontal=True)

# --- LÓGICA DE TEMPO ---
def get_timer(tf):
    now = datetime.now()
    minutes_tf = int(tf.replace("m", ""))
    total_sec = minutes_tf * 60
    passed_sec = (now.minute % minutes_tf) * 60 + now.second
    rem = total_sec - passed_sec
    return f"{rem // 60:02d}:{rem % 60:02d}"

tempo_restante = get_timer(timeframe)

# --- MOTOR DE ESTRATÉGIA ---
try:
    df = fetch_data(ativo, timeframe)
    df = df.dropna()
    df['cor'] = (df['Close'] > df['Open']).astype(int)
    df['win_seq'] = (df['cor'] == df['cor'].shift(1)).astype(int)
    win_rate = float(df['win_seq'].tail(40).mean() * 100)
    preco_atual = float(df.iloc[-1]['Close'])
    ema9 = float(df['Close'].ewm(span=9).mean().iloc[-1])

    st.markdown(f"### 🛡️ Sniper Intelligence: {ativo}")
    m1, m2, m3 = st.columns(3)
    m1.markdown(f"<div class='metric-box'><small>PROBABILIDADE</small><br><b style='color:#00ffcc;'>{win_rate:.1f}%</b></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='metric-box'><small>PRÓXIMA VELA</small><br><b class='timer-text'>{tempo_restante}</b></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='metric-box'><small>VALOR GALE</small><br><b>${entrada_base*2.1:.2f}</b></div>", unsafe_allow_html=True)

    st.divider()
    col_sig, col_graph = st.columns([1, 2])

    with col_sig:
        if win_rate >= 50.0:
            decisao = "CALL" if preco_atual > ema9 else "PUT"
            color_class = "buy-zone" if decisao == "CALL" else "sell-zone"
            st.markdown(f'<div class="card-sinal {color_class}"><h2>🔥 {decisao}</h2><p>ALTA PROBABILIDADE</p></div>', unsafe_allow_html=True)
            st.success(f"Estratégia Confirmada ({win_rate:.1f}%)")
        else:
            st.markdown(f'<div class="card-sinal" style="color:#6b7280; border-color:#374151;"><h2>⏳ AGUARDAR</h2><p>MERCADO INSTÁVEL</p></div>', unsafe_allow_html=True)
        
        lucro_op = entrada_base * (payout/100)
        st.info(f"Progresso p/ Meta: {((lucro_op/valor_meta)*100):.1f}% por Win")
        
    with col_graph:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

except:
    st.info("🔄 Sincronizando...")

time.sleep(1)
st.rerun()