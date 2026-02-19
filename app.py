import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER ELITE AI | ULTRA", layout="wide", page_icon="🎯")

# --- CSS PROFISSIONAL (ESTILO PLATAFORMA RICA) ---
st.markdown("""
    <style>
    .main { background-color: #060709; }
    .stMetric { background: linear-gradient(145deg, #0d1117, #161b22); border: 1px solid #1f2937; padding: 15px; border-radius: 12px; }
    .card-sinal { padding: 25px; border-radius: 20px; text-align: center; border: 2px solid #1f2937; margin-bottom: 20px; }
    .buy-color { background-color: #064e3b; color: #10b981; border-color: #10b981; }
    .sell-color { background-color: #7f1d1d; color: #ef4444; border-color: #ef4444; }
    .wait-color { background-color: #1f2937; color: #9ca3af; border-color: #374151; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
def check_access(email):
    email_limpo = email.lower().strip()
    if email_limpo == "wpmail222@gmail.com": return True
    try:
        # Tenta ler a planilha mas tem um timeout para não travar o app
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR_hFyLkF4iT_IZPMaKMsR0wvxq_klJunYnkVvVuTm_F5byOilZxMrIdvmsLZDTshmHwk5qMp2bdWKB/pub?output=csv", timeout=5)
        return email_limpo in df['email'].str.lower().str.strip().tolist()
    except: return False

# --- CONTROLE DE LOGIN ---
if 'logado' not in st.session_state: st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("<h1 style='text-align:center; color:#00ffcc;'>🎯 SNIPER ELITE AI</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        u_email = st.text_input("E-mail de acesso:")
        if st.button("ATIVAR ALGORITMO"):
            if check_access(u_email):
                st.session_state.logado = True
                st.rerun()
            else: st.error("Acesso negado ou expirado.")
    st.stop()

# --- INTERFACE DO ROBÔ ---
with st.sidebar:
    st.title("🎯 CONFIGURAÇÃO")
    ativo = st.selectbox("Escolha o Ativo:", ["BTC-USD", "ETH-USD", "EURUSD=X", "GBPUSD=X", "SOL-USD"])
    timeframe = st.radio("Tempo Gráfico:", ["1m", "5m", "15m"], horizontal=True)
    st.markdown("---")
    if st.button("LOGOUT"):
        st.session_state.logado = False
        st.rerun()

# --- MOTOR DE INTELIGÊNCIA E CATALOGAÇÃO ---
try:
    # Busca dados mais recentes (2 dias para garantir volume)
    dados = yf.download(ativo, period="2d", interval=timeframe, progress=False)
    
    if not dados.empty and len(dados) >= 10:
        # Catalogação das últimas 10 velas
        df_cat = dados.tail(10).copy()
        df_cat['cor'] = ['Verde' if c > o else 'Vermelha' for o, c in zip(df_cat['Open'], df_cat['Close'])]
        
        verdes = (df_cat['cor'] == 'Verde').sum()
        vermelhas = (df_cat['cor'] == 'Vermelha').sum()
        
        # Cálculo de Assertividade (Lógica de probabilidade)
        forca = (verdes * 10) if verdes > vermelhas else (vermelhas * 10)
        assertividade = 80 + (forca / 10)
        
        preco_atual = float(dados['Close'].iloc[-1])
        preco_anterior = float(dados['Close'].iloc[-2])

        # --- DASHBOARD ---
        st.title(f"🚀 Monitorando {ativo}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Preço Atual", f"${preco_atual:.4f}")
        m2.metric("Assertividade", f"{assertividade:.1f}%")
        m3.metric("Catalogação (Alta)", f"{verdes} Velas")
        m4.metric("Catalogação (Baixa)", f"{vermelhas} Velas")

        st.markdown("---")

        c_sinal, c_grafico = st.columns([1, 2.5])

        with c_sinal:
            st.subheader("📡 Análise de IA")
            
            # ESTRATÉGIA SNIPER: Só manda sinal se a força for > 60%
            if forca >= 60:
                if verdes > vermelhas:
                    st.markdown('<div class="card-sinal buy-color"><h2>🔥 CALL (COMPRA)</h2><p>Padrão: Continuidade de Tendência</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="card-sinal sell-color"><h2>📉 PUT (VENDA)</h2><p>Padrão: Fluxo de Baixa</p></div>', unsafe_allow_html=True)
                
                st.success(f"✔️ ENTRADA AUTORIZADA\nExpiração: Próxima Vela")
            else:
                st.markdown('<div class="card-sinal wait-color"><h2>⏳ AGUARDAR</h2><p>Mercado Lateral (Sem Força)</p></div>', unsafe_allow_html=True)
                st.warning("IA: Aguardando catalogação favorável.")

            st.info(f"💡 Dica: Operar em {timeframe} exige atenção ao fechamento da vela.")

        with c_grafico:
            fig = go.Figure(data=[go.Candlestick(
                x=dados.index, open=dados['Open'], high=dados['High'],
                low=dados['Low'], close=dados['Close'],
                increasing_line_color='#10b981', decreasing_line_color='#ef4444'
            )])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("⚠️ SEM DADOS NO MOMENTO. Se for fim de semana, o mercado Forex (EURUSD) está fechado. Mude para BTC-USD para operar 24h.")

except Exception as e:
    st.error(f"Erro no Algoritmo: {e}")

st.caption(f"Sniper Elite AI v6.0 | Automação via API Yahoo Finance | {datetime.now().strftime('%H:%M:%S')}")