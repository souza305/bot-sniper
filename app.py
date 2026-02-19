import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI | VIP", layout="wide", page_icon="🎯")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email_usuario):
    if email_usuario.lower().strip() == "wpmail222@gmail.com":
        return True
    SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv"
    try:
        df_acesso = pd.read_csv(SHEET_URL)
        lista_autorizada = df_acesso['email'].str.lower().str.strip().tolist()
        return email_usuario.lower().strip() in lista_autorizada
    except:
        return False

# --- BARRA LATERAL (LOGIN E FILTROS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2534/2534312.png", width=80)
    st.title("SNIPER ELITE AI")
    st.subheader("🚀 Área do Trader")
    
    user_email = st.text_input("E-mail de Acesso:", placeholder="seu@email.com")
    
    if not user_email:
        st.info("💡 Digite seu e-mail para desbloquear os sinais.")
        st.stop()
    
    if not check_access(user_email):
        st.error("❌ Acesso Negado. Verifique sua assinatura.")
        st.stop()
    
    st.success("✅ Acesso VIP Ativo")
    st.markdown("---")
    
    # FUNCIONALIDADES FACILITADAS
    st.subheader("⚙️ Configurações")
    ativo = st.selectbox("Escolha o Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "SOL-USD"])
    timeframe = st.radio("Tempo Gráfico:", ["1m", "5m", "15m", "1h"], horizontal=True)
    
    if st.button("Sair / Deslogar"):
        st.rerun()

# --- CONTEÚDO PRINCIPAL ---
st.title("🎯 Painel de Análise Sniper")
st.write(f"Monitorando **{ativo}** em tempo real no período de **{timeframe}**.")

# Layout de Colunas para Métricas
col1, col2, col3, col4 = st.columns(4)

try:
    # Ajuste de período baseado no timeframe selecionado
    periodo = "1d" if timeframe in ["1m", "5m", "15m"] else "5d"
    dados = yf.download(ativo, period=periodo, interval=timeframe, progress=False)

    if not dados.empty and len(dados) > 1:
        preco_atual = dados['Close'].iloc[-1]
        preco_anterior = dados['Close'].iloc[-2]
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
        
        # Métricas de Topo
        col1.metric("Preço Atual", f"${preco_atual:.4f}")
        col2.metric("Variação (Candle)", f"{variacao:.2f}%", delta=f"{variacao:.2f}%")
        
        # Lógica de Sinal "Sniper"
        if preco_atual > preco_anterior:
            col3.markdown(f'<div style="background-color:#09332e; padding:10px; border-radius:10px; text-align:center; border:1px solid #2ecc71"><h3 style="color:#2ecc71; margin:0">⚡ SINAL: COMPRA</h3></div>', unsafe_allow_html=True)
            tendencia = "ALTA"
        else:
            col3.markdown(f'<div style="background-color:#331010; padding:10px; border-radius:10px; text-align:center; border:1px solid #e74c3c"><h3 style="color:#e74c3c; margin:0">📉 SINAL: VENDA</h3></div>', unsafe_allow_html=True)
            tendencia = "BAIXA"
            
        col4.metric("Tendência", tendencia)

        st.markdown("---")

        # Gráfico Candlestick Profissional
        fig = go.Figure(data=[go.Candlestick(
            x=dados.index,
            open=dados['Open'], high=dados['High'],
            low=dados['Low'], close=dados['Close'],
            increasing_line_color='#2ecc71', decreasing_line_color='#e74c3c'
        )])

        fig.update_layout(
            title=f"Movimentação de Preço - {ativo} ({timeframe})",
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            height=500,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Rodapé com Funcionalidades Extra
        expander = st.expander("📝 Como operar este sinal?")
        expander.write("""
            1. Verifique se o sinal de **COMPRA** ou **VENDA** coincide com a cor do gráfico.
            2. Recomendamos operar com gerenciamento de 1% a 3% da banca.
            3. Em períodos de **1m**, as operações são de curta duração (scalping).
        """)

    else:
        st.warning(f"Aguardando dados de {ativo}. Se for fim de semana, ativos Forex ficam pausados.")

except Exception as e:
    st.error(f"Erro na conexão com o mercado: {e}")

st.markdown("---")
st.caption(f"Sniper Elite AI v2.0 - Atualizado em: {datetime.now().strftime('%H:%M:%S')}")