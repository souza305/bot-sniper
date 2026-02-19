import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI", layout="wide")

# --- SISTEMA DE ACESSO (O MELHOR JEITO) ---
def check_access(email_usuario):
    # DICA: Substitua o link abaixo pelo seu link de "Publicar na Web" (CSV) do Google Sheets
    SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlJrLgRWQ6i_aAzDqL-szsUAsmuiL9tB3HSjthArpzpFJydRHz0fnFFDHuMWghzZThr_2FjPD6MLgm/pub?output=csv"
    
    try:
        df_acesso = pd.read_csv(SHEET_URL)
        # Deixa tudo em minúsculo para não dar erro se o cliente digitar maiúsculo
        lista_autorizada = df_acesso['email'].str.lower().tolist()
        return email_usuario.lower() in lista_autorizada
    except:
        # Se a planilha der erro ou estiver vazia, seu email mestre entra:
        return email_usuario.lower() == "seuemail@teste.com"

# --- INTERFACE DE LOGIN NA BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2534/2534312.png", width=100)
st.sidebar.title("🎯 Sniper Elite AI")
st.sidebar.markdown("---")

user_email = st.sidebar.text_input("Digite seu e-mail da Kiwify:")

if not user_email:
    st.warning("⚠️ Por favor, insira seu e-mail para acessar o robô.")
    st.info("O acesso é liberado automaticamente após a compra na Kiwify.")
    st.stop()

if check_access(user_email):
    st.sidebar.success(f"Bem-vindo, {user_email.split('@')[0]}!")
else:
    st.sidebar.error("❌ E-mail não autorizado ou assinatura expirada.")
    st.sidebar.info("Dúvidas? Entre em contato com o suporte.")
    st.stop()

# --- DAQUI PARA BAIXO É O ROBÔ EM SI ---

st.title("📊 Painel de Sinais - Sniper Elite AI")
st.markdown(f"**Status do Mercado:** 🟢 Operacional | **Data:** {datetime.now().strftime('%d/%m/%Y')}")

# Seleção do Ativo
simbolo = st.selectbox("Selecione o Par de Moedas ou Ativo:", ["EURUSD=X", "GBPUSD=X", "BTC-USD", "ETH-USD"])

# Lógica Simples de Sinal (Exemplo)
dados = yf.download(simbolo, period="1d", interval="15m")
if not dados.empty:
    preco_atual = dados['Close'].iloc[-1]
    fechamento_anterior = dados['Close'].iloc[-2]
    
    col1, col2 = st.columns(2)
    col1.metric("Preço Atual", f"{preco_atual:.4f}")
    
    if preco_atual > fechamento_anterior:
        col2.success("🔥 SINAL DE COMPRA (CALL)")
    else:
        col2.error("📉 SINAL DE VENDA (PUT)")

    # Gráfico
    fig = go.Figure(data=[go.Candlestick(x=dados.index,
                open=dados['Open'], high=dados['High'],
                low=dados['Low'], close=dados['Close'])])
    fig.update_layout(title=f"Gráfico em Tempo Real - {simbolo}", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("Aviso: Operações financeiras envolvem risco. Use o robô como ferramenta de auxílio.")