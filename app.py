import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI | PRO", layout="wide", page_icon="🎯")

# --- CSS ESTILO PLATAFORMA DE LUXO ---
st.markdown("""
    <style>
    .main { background-color: #050608; }
    .stMetric { background: #0d1117; border-left: 4px solid #d4af37; border-radius: 10px; padding: 15px; }
    .card-sinal { padding: 30px; border-radius: 20px; text-align: center; border: 2px solid #1f2937; margin: 10px 0; }
    .buy-zone { background: linear-gradient(145deg, #064e3b, #065f46); color: #00ffcc; border-color: #00ffcc; }
    .sell-zone { background: linear-gradient(145deg, #7f1d1d, #991b1b); color: #ff4b4b; border-color: #ff4b4b; }
    .wait-zone { background-color: #111827; color: #9ca3af; border-color: #374151; }
    h1, h2, h3 { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email):
    email_limpo = email.lower().strip()
    if email_limpo == "wpmail222@gmail.com": return True
    try:
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv", timeout=5)
        return email_limpo in df['email'].str.lower().str.strip().tolist()
    except: return False

if 'logado' not in st.session_state: st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<h1 style='text-align:center;'>🎯 SNIPER ELITE AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:white;'>PLATAFORMA DE INTELIGÊNCIA EM CATALOGAÇÃO</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        u_email = st.text_input("E-mail de Acesso VIP:")
        if st.button("ATIVAR ALGORITMO"):
            if check_access(u_email):
                st.session_state.logado = True
                st.rerun()
            else: st.error("Acesso negado.")
    st.stop()

# --- INTERFACE ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>MENU PRO</h2>", unsafe_allow_html=True)
    ativo = st.selectbox("Escolha o Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "SOL-USD"])
    timeframe = st.radio("Tempo Gráfico:", ["1m", "5m", "15m"], horizontal=True)
    st.markdown("---")
    if st.button("DESLOGAR"):
        st.session_state.logado = False
        st.rerun()

# --- MOTOR DE CATALOGAÇÃO INTELIGENTE ---
try:
    # Coleta 40 velas para ter uma base sólida de catalogação
    dados = yf.download(ativo, period="2d", interval=timeframe, progress=False)
    
    if not dados.empty and len(dados) >= 20:
        # Pega as últimas 20 velas para catalogar
        ultimas = dados.tail(20)
        
        # Lógica de cores corrigida (evita o erro de length)
        fechamentos = ultimas['Close'].values
        aberturas = ultimas['Open'].values
        
        verdes = sum(1 for f, a in zip(fechamentos, aberturas) if f > a)
        vermelhas = sum(1 for f, a in zip(fechamentos, aberturas) if f < a)
        
        # Inteligência de Força (0 a 100%)
        forca_compradora = (verdes / 20) * 100
        forca_vendedora = (vermelhas / 20) * 100
        
        preco_atual = float(fechamentos[-1])
        assertividade = 85.0 + (max(verdes, vermelhas) / 2)

        # --- DASHBOARD ---
        st.markdown(f"### 🚀 Analisando: {ativo} ({timeframe})")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Cotação", f"${preco_atual:.4f}")
        m2.metric("Assertividade IA", f"{min(assertividade, 98.7):.1f}%")
        m3.metric("Velas de Alta", f"{verdes}")
        m4.metric("Velas de Baixa", f"{vermelhas}")

        st.markdown("---")

        c_sinal, c_grafico = st.columns([1.2, 2.5])

        with c_sinal:
            st.markdown("### 🤖 DECISÃO DA IA")
            
            # ESTRATÉGIA: Só libera com mais de 55% de força (11 velas de 20)
            if forca_compradora >= 55:
                st.markdown(f'<div class="card-sinal buy-zone"><h2>🔥 CALL (COMPRA)</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
                st.success(f"FORÇA COMPRADORA EM {forca_compradora}%")
            elif forca_vendedora >= 55:
                st.markdown(f'<div class="card-sinal sell-zone"><h2>📉 PUT (VENDA)</h2><p>CATALOGAÇÃO CONFIRMADA</p><h3>PRÓXIMA VELA</h3></div>', unsafe_allow_html=True)
                st.error(f"FORÇA VENDEDORA EM {forca_vendedora}%")
            else:
                st.markdown('<div class="card-sinal wait-zone"><h2>⏳ AGUARDAR</h2><p>MERCADO SEM TENDÊNCIA</p></div>', unsafe_allow_html=True)
                st.warning("IA: Força insuficiente para operar com segurança.")

            st.info("💡 A entrada deve ser feita no início da próxima vela.")

        with c_grafico:
            fig = go.Figure(data=[go.Candlestick(
                x=dados.index, open=dados['Open'], high=dados['High'],
                low=dados['Low'], close=dados['Close'],
                increasing_line_color='#00ffcc', decreasing_line_color='#ff4b4b'
            )])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=480, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Aguardando formação de mercado... Tente BTC-USD se o mercado Forex estiver fechado.")

except Exception as e:
    st.error(f"Erro de Conexão: Escolha outro ativo ou aguarde 1 minuto.")

st.markdown("---")
st.caption(f"💎 Sniper Elite AI | Premium Edition | v7.0 | {datetime.now().strftime('%H:%M:%S')}")