import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI", layout="wide")

# --- SISTEMA DE ACESSO ---
def check_access(email_usuario):
    # Seu e-mail mestre para sempre ter acesso
    if email_usuario.lower().strip() == "wpmail222@gmail.com":
        return True
    
    # Link da sua planilha (CSV)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv"
    
    try:
        df_acesso = pd.read_csv(SHEET_URL)
        lista_autorizada = df_acesso['email'].str.lower().str.strip().tolist()
        return email_usuario.lower().strip() in lista_autorizada
    except:
        return False

# --- SIDEBAR ---
st.sidebar.title("🎯 Sniper Elite AI")
user_email = st.sidebar.text_input("Digite seu e-mail da Kiwify:")

if not user_email:
    st.info("Aguardando login...")
    st.stop()

if not check_access(user_email):
    st.error("❌ E-mail não autorizado.")
    st.stop()

st.sidebar.success("Acesso Liberado!")

# --- CORPO DO APP ---
st.title("📊 Painel de Sinais - Sniper Elite AI")

# Seleção do Ativo
simbolo = st.selectbox("Selecione o Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X"])

# Tentativa de baixar dados
try:
    dados = yf.download(simbolo, period="1d", interval="15m", progress=False)

    # VERIFICAÇÃO DE SEGURANÇA: Só continua se houver dados
    if dados is not None and not dados.empty and len(dados) > 1:
        preco_atual = float(dados['Close'].iloc[-1])
        fechamento_anterior = float(dados['Close'].iloc[-2])
        
        col1, col2 = st.columns(2)
        
        # Mostra o preço com segurança
        col1.metric("Preço Atual", f"{preco_atual:.4f}")
        
        if preco_atual > fechamento_anterior:
            col2.success("🔥 SINAL DE COMPRA (CALL)")
        else:
            col2.error("📉 SINAL DE VENDA (PUT)")

        # Gráfico
        fig = go.Figure(data=[go.Candlestick(x=dados.index,
                    open=dados['Open'], high=dados['High'],
                    low=dados['Low'], close=dados['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Se cair aqui, é porque o mercado está fechado ou o YFinance falhou
        st.warning(f"🟡 O mercado para {simbolo} está sem dados no momento (pode estar fechado por ser fim de semana).")
        st.info("Tente selecionar **BTC-USD** (Bitcoin) para testar, pois ele funciona 24h.")

except Exception as e:
    st.error(f"Erro técnico: Selecione outro ativo ou tente mais tarde.")

st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")