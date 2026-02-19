import streamlit as st
import pandas as pd

# --- SISTEMA DE ACESSO POR RECORRÊNCIA ---
# Podes usar um ficheiro CSV online ou uma lista que atualizas no Admin
def verificar_acesso(email_usuario):
    # Lista de emails de clientes que pagaram a Kiwify
    # No futuro, podemos automatizar para ler isto direto da Kiwify
    lista_autorizada = ["contato@cliente1.com", "admin@sniper.com", "teste@gmail.com"]
    return email_usuario in lista_autorizada

st.sidebar.markdown("## 🔐 ÁREA DO ASSINANTE")
email_login = st.sidebar.text_input("Introduz o teu e-mail de compra da Kiwify:")

if not email_login:
    st.warning("⚠️ Por favor, faz login para aceder ao terminal.")
    st.stop()

if not verificar_acesso(email_login):
    st.error("❌ Acesso Bloqueado ou Assinatura Expirada.")
    st.info("Caso tenhas pago agora, aguarda 5 min ou contacta o suporte.")
    st.stop()

# --- SE PASSAR DAQUI, O RESTO DO CÓDIGO DO ROBÔ APARECE ---
st.success(f"🔓 Bem-vindo, {email_login}! Acesso VIP Libertado.")

# --- SISTEMA DE LICENÇA SIMPLES ---
usuarios_ativos = ["cliente1@email.com", "vip_trader_01", "admin"] # Você atualiza essa lista

st.sidebar.subheader("🔑 Autenticação")
user_token = st.sidebar.text_input("Digite seu E-mail ou Token de Acesso:")

if user_token not in usuarios_ativos:
    st.error("❌ Acesso não autorizado ou assinatura expirada.")
    st.stop() # Interrompe o código aqui

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA E NOME DA MARCA
BRAN_NAME = "SNIPER ELITE AI" # <-- COLOQUE O NOME DA SUA MARCA AQUI

st.set_page_config(page_title=BRAN_NAME, layout="wide", initial_sidebar_state="expanded")

# --- DESIGN CUSTOMIZADO (CSS) ---
st.markdown(f"""
    <style>
    /* Fundo e Fonte Geral */
    .main {{ background-color: #0e1117; }}
    .stMetric {{ background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #262730; }}
    
    /* Cabeçalho da Marca */
    .brand-header {{
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 45px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
        letter-spacing: -1px;
    }}
    .brand-sub {{
        color: #808495;
        text-align: center;
        font-size: 14px;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    
    /* Box de Sinais */
    .sinal-box {{
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 20px 0;
    }}
    
    /* Botão Customizado */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        padding: 15px;
        font-weight: bold;
        border-radius: 10px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.02); }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER COM A SUA MARCA ---
st.markdown(f'<p class="brand-header">{BRAN_NAME}</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-sub">Algoritmo de Alta Precisão & Catalogação MHI</p>', unsafe_allow_html=True)

# --- SIDEBAR DESIGN ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2533/2533203.png", width=80) # Ícone de mira
st.sidebar.markdown(f"### Painel de Controle")
par = st.sidebar.selectbox("💰 Ativo:", ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD", "SOL-USD"])
tempo_vela = st.sidebar.radio("⏱️ Timeframe:", ["1m", "5m"], horizontal=True)

# Relógio estilizado na sidebar
agora = datetime.now()
st.sidebar.info(f"🕒 Hora: {agora.strftime('%H:%M:%S')}")

if st.button('🚀 ESCANEAR MERCADO'):
    with st.spinner('O Algoritmo está processando velas...'):
        df = yf.download(tickers=par, period="2d", interval=tempo_vela)
        
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            df = df.astype(float)
            
            # --- LÓGICA DE CATALOGAÇÃO MHI + GALE 1 ---
            win_direto, win_gale, loss = 0, 0, 0
            for i in range(0, len(df) - 7, 5):
                bloco = df.iloc[i:i+5]
                if len(bloco) < 5: continue
                cores = [1 if bloco['Close'].iloc[j] > bloco['Open'].iloc[j] else 0 for j in range(2, 5)]
                minoria = 1 if cores.count(0) > cores.count(1) else 0
                res1 = 1 if df['Close'].iloc[i+5] > df['Open'].iloc[i+5] else 0
                
                if res1 == minoria: win_direto += 1
                else:
                    res2 = 1 if df['Close'].iloc[i+6] > df['Open'].iloc[i+6] else 0
                    if res2 == minoria: win_gale += 1
                    else: loss += 1

            total = win_direto + win_gale + loss
            assertividade = ( (win_direto + win_gale) / total * 100) if total > 0 else 0

            # --- LAYOUT DE MÉTRICAS ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎯 Assertividade", f"{assertividade:.1f}%")
            col2.metric("✅ Direto", win_direto)
            col3.metric("🛡️ Gale 1", win_gale)
            col4.metric("❌ Loss", loss)

            st.markdown("---")

            # --- FILTRO E EXIBIÇÃO DO SINAL ---
            if assertividade >= 50.0:
                ultimas_3 = df.tail(3)
                cores_atuais = [1 if ultimas_3['Close'].iloc[j] > ultimas_3['Open'].iloc[j] else 0 for j in range(3)]
                
                if cores_atuais.count(0) > cores_atuais.count(1):
                    direcao, cor_box, cor_glow = "COMPRA (CALL)", "#00ff88", "rgba(0, 255, 136, 0.2)"
                else:
                    direcao, cor_box, cor_glow = "VENDA (PUT)", "#ff4b4b", "rgba(255, 75, 75, 0.2)"

                st.markdown(f"""
                <div class="sinal-box" style="background-color: {cor_glow}; border: 2px solid {cor_box};">
                    <h2 style="color: {cor_box}; margin:0;">🚨 SINAL IDENTIFICADO 🚨</h2>
                    <h1 style="color: white; font-size: 50px; margin: 10px 0;">{direcao}</h1>
                    <p style="color: white; font-size: 18px;"><b>EXPIRAÇÃO:</b> {tempo_vela} | <b>PROTEÇÃO:</b> GALE 1</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Algoritmo em espera: Aguardando Assertividade > 50%")

            # --- GRÁFICO PROFISSIONAL ---
            fig = go.Figure(data=[go.Candlestick(x=df.index[-40:], open=df['Open'][-40:], high=df['High'][-40:], low=df['Low'][-40:], close=df['Close'][-40:])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)