import streamlit as st
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import time
import uuid 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide", page_title="Monitor Cripto")

# Título
st.title("BTC-USD Tempo Real + Média Móvel 14")

# Placeholder para o gráfico (espaço reservado)
grafico_placeholder = st.empty()

# --- LOOP DE ATUALIZAÇÃO ---
ticker = "BTC-USD"

while True:
    try:
        # 1. Baixar dados
        df = yf.download(ticker, period="15d", interval="1h", progress=False)
        
        # Tratamento MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Se o download falhar ou vier vazio, pula para a próxima tentativa
        if df.empty:
            time.sleep(5)
            continue

        # --- CÁLCULO DA MÉDIA MÓVEL (14 Períodos) ---
        df['MA14'] = df['Close'].rolling(window=14).mean()
        
        # 2. Criar a estrutura do gráfico
        fig = go.Figure()

        # Adicionar os Candles (Branco e Vermelho)
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Preço",
            increasing_line_color='white', 
            decreasing_line_color='red'
        ))

        # --- Adicionar a Linha da Média Móvel ---
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['MA14'], 
            mode='lines', 
            name='Média 14',
            line=dict(color='yellow', width=2)
        ))

        # Customizar o layout
        fig.update_layout(
            template="plotly_dark",
            title=f"{ticker} - Último Preço: {df['Close'].iloc[-1]:.2f}",
            xaxis_rangeslider_visible=False,
            height=600,
            legend=dict(x=0, y=1)
        )

        # 3. Exibir no Streamlit
        with grafico_placeholder.container():
    
            st.plotly_chart(fig, use_container_width=True, key=str(uuid.uuid4()))

        # Esperar 60 segundos antes de atualizar de novo
        time.sleep(60)
        
    except Exception as e:
        st.error(f"Erro momentâneo: {e}")
        time.sleep(10)