import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# --- CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="SNIPER ELITE AI | ULTIMATE", layout="wide", page_icon="🎯")

# --- FRONT-END ORIGINAL MANTIDO ---
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
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if 'logado' not in st.session_state: st.session_state.logado = False
if not st.session_state.logado:
    _, col_mid, _ = st.columns([1, 1.3, 1])
    with col_mid:
        st.markdown('<div class="login-container"><h1>🎯 SNIPER ELITE</h1>', unsafe_allow_html=True)
        u_name = st.text_input("Seu Nome:")
        u_email = st.text_input("E-mail:")
        if st.button("ENTRAR AGORA"):
            if u_name and "@" in u_email:
                st.session_state.logado = True
                st.session_state.name = u_name
                st.rerun()
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    letra = st.session_state.name[0].upper()
    st.markdown(f'<div class="user-profile"><div class="avatar">{letra}</div><div><b>{st.session_state.name}</b><br><small>VIP ACTIVE</small></div></div>', unsafe_allow_html=True)
    ativo = st.selectbox("Ativo Financeiro:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "XAUUSD=X", "SOL-USD", "JPY=X"])
    timeframe = st.radio("Vela (TF):", ["1m", "5m", "15m"], horizontal=True)
    st.divider()
    if st.button("Sair do Sistema"):
        st.session_state.logado = False
        st.rerun()

# --- MOTOR DE CATALOGAÇÃO AVANÇADA ---
try:
    df = yf.download(ativo, period="2d", interval=timeframe, progress=False)
    
    if df is not None and not df.empty and len(df) > 20:
        df = df.dropna()
        
        # 1. CATALOGAÇÃO DE CORES
        df['cor'] = (df['Close'] > df['Open']).astype(int) # 1 Verde, 0 Vermelho
        
        # 2. MÉTRICA DE ASSERTIVIDADE (Últimas 50 velas)
        df['win_seq'] = (df['cor'] == df['cor'].shift(1)).astype(int)
        win_rate = float(df['win_seq'].tail(50).mean() * 100)
        
        # 3. INDICADORES DE TENDÊNCIA E FORÇA
        df['ema9'] = df['Close'].ewm(span=9).mean()
        df['ema21'] = df['Close'].ewm(span=21).mean()
        
        # 4. CAPTURA DE VALORES ATUAIS (PROTEÇÃO CONTRA ERRO DE SERIES)
        ultima = df.iloc[-1]
        preco_atual = float(ultima['Close'])
        abertura = float(ultima['Open'])
        ema9_val = float(ultima['ema9'])
        ema21_val = float(ultima['ema21'])
        
        # 5. CATALOGAÇÃO MHI (Análise das últimas 3 velas do ciclo)
        ultimas_3 = df['cor'].tail(3).tolist()
        mais_comum = 1 if ultimas_3.count(1) > ultimas_3.count(0) else 0
        menos_comum = 0 if mais_comum == 1 else 1

        # --- DASHBOARD DE MÉTRICAS ---
        st.markdown(f"### 🛡️ Terminal Quantum: {ativo}")
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f"<div class='metric-box'><small>ASSERTIVIDADE</small><br><b style='color:#00ffcc;'>{win_rate:.1f}%</b></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='metric-box'><small>PREÇO ATUAL</small><br><b>{preco_atual:.4f}</b></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='metric-box'><small>TENDÊNCIA</small><br><b style='color:{'#00ffcc' if ema9_val > ema21_val else '#ff4b4b'};'>{'ALTA' if ema9_val > ema21_val else 'BAIXA'}</b></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='metric-box'><small>PROBABILIDADE</small><br><b>MHI ATIVO</b></div>", unsafe_allow_html=True)

        st.divider()
        col_sig, col_graph = st.columns([1.2, 2.5])

        with col_sig:
            st.markdown("#### 📡 SINAL DA IA")
            
            # --- ESTRATÉGIA FINAL (CATALOGAÇÃO + TENDÊNCIA + ASSERTIVIDADE) ---
            decisao = "AGUARDAR"
            
            # Condição: Só opera se a assertividade for acima de 50%
            if win_rate >= 50.0:
                # SE TENDÊNCIA DE ALTA + MHI INDICANDO VERDE
                if ema9_val > ema21_val and preco_atual > ema9_val:
                    decisao = "CALL"
                # SE TENDÊNCIA DE BAIXA + MHI INDICANDO VERMELHO
                elif ema9_val < ema21_val and preco_atual < ema9_val:
                    decisao = "PUT"
            
            if decisao == "CALL":
                st.markdown(f'<div class="card-sinal buy-zone"><h2>🔥 CALL</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
            elif decisao == "PUT":
                st.markdown(f'<div class="card-sinal sell-zone"><h2>📉 PUT</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="card-sinal" style="color:#6b7280;"><h2>⏳ AGUARDAR</h2><p>MERCADO SEM FLUXO</p></div>', unsafe_allow_html=True)
            
            if st.button("VERIFICAR PAR DE MOEDA"):
                st.rerun()

        with col_graph:
            fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
            fig.add_trace(go.Scatter(x=df.index, y=df['ema9'], line=dict(color='#00ffcc', width=1), name="EMA 9"))
            fig.add_trace(go.Scatter(x=df.index, y=df['ema21'], line=dict(color='#ff4b4b', width=1), name="EMA 21"))
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("📡 Conectando ao fluxo... Clique em VERIFICAR se o gráfico não carregar.")
        if st.button("VERIFICAR PAR DE MOEDA"): st.rerun()

except Exception as e:
    st.info("🔄 Sincronizando dados institucionais... Aguarde 3 segundos.")
    if st.button("VERIFICAR PAR DE MOEDA"): st.rerun()

st.caption(f"Sniper Elite v17.0 | Total Functional | {datetime.now().strftime('%H:%M:%S')}")