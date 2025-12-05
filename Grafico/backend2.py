from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import time

app = Flask(__name__)
CORS(app)

# Cache simples em memória: { 'tipo': {'timestamp': 0, 'data': []} }
CACHE_HEATMAP = {}
CACHE_DURATION = 60  # segundos

# Lista de ativos limpa e robusta
ASSETS = {
    'cripto': [
        "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", 
        "TRX-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "ATOM-USD",
        "XLM-USD", "ETC-USD", "FIL-USD", "HBAR-USD", "NEAR-USD", "VET-USD", "QNT-USD",
        "MKR-USD", "AAVE-USD", "ALGO-USD", "SAND-USD", "EOS-USD", "MANA-USD"
    ],
    'br': [
        "VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "PETR3.SA", "ABEV3.SA", "WEGE3.SA",
        "RENT3.SA", "BPAC11.SA", "SUZB3.SA", "ITSA4.SA", "HAPV3.SA", "RDOR3.SA", "JBSS3.SA", "B3SA3.SA",
        "GGBR4.SA", "RADL3.SA", "PRIO3.SA", "RAIL3.SA", "VBBR3.SA", "ELET3.SA", "UGPA3.SA", "CSAN3.SA",
        "BBSE3.SA", "LREN3.SA", "VIVT3.SA", "EQTL3.SA", "SBSP3.SA", "CMIG4.SA", "CPLE6.SA", "EMBR3.SA",
        "TIMS3.SA", "CCRO3.SA", "ASAI3.SA", "HYPE3.SA", "TOTS3.SA", "CSNA3.SA", "MGLU3.SA", "BHIA3.SA"
    ],
    'us': [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "LLY", "V",
        "UNH", "XOM", "JNJ", "JPM", "PG", "MA", "AVGO", "HD", "CVX", "MRK",
        "ABBV", "PEP", "KO", "COST", "ADBE", "WMT", "MCD", "CSCO", "CRM", "PFE",
        "TMO", "BAC", "NFLX", "ABT", "DHR", "CMCSA", "AMD", "NKE", "DIS", "INTC"
    ],
    'indices': [
        "^BVSP", "^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI", 
        "GC=F", "CL=F", "SI=F", "HG=F", "EURUSD=X", "GBPUSD=X", "JPY=X", "BRL=X"
    ]
}

@app.route('/api/assets')
def listar_ativos():
    """Retorna a lista completa de ativos para o autocomplete"""
    todos_ativos = []
    for categoria, lista in ASSETS.items():
        for ticker in lista:
            todos_ativos.append({"symbol": ticker, "category": categoria})
    return jsonify(todos_ativos)

@app.route('/api/dados')
def pegar_dados():
    try:
        ticker = request.args.get('ticker', 'BTC-USD')
        period = request.args.get('period', '1mo')
        interval = request.args.get('interval', '1h')
        ma_period = int(request.args.get('ma_period', 14))
        
        print(f"Buscando dados para: {ticker}, Periodo: {period}, Intervalo: {interval}, MA: {ma_period}") 

        # Baixa os dados
        df = yf.download(ticker, period=period, interval=interval, progress=False, threads=False, auto_adjust=False)
        
        if df.empty:
            return jsonify({"erro": "Ticker não encontrado ou sem dados"}), 404

        # Tratamento MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            try:
                if ticker in df.columns.get_level_values(1):
                     df = df.xs(ticker, axis=1, level=1)
                else:
                     df.columns = df.columns.get_level_values(0)
            except:
                df.columns = df.columns.get_level_values(0)

        df.columns = [c.capitalize() for c in df.columns]

        # Conversão de Fuso Horário para Brasil (Brasília)
        if df.index.tz is None:
            # Se não tiver timezone, assume UTC e converte
            df.index = df.index.tz_localize('UTC').tz_convert('America/Sao_Paulo')
        else:
            # Se já tiver, apenas converte
            df.index = df.index.tz_convert('America/Sao_Paulo')
        
        # Calcula a Média Móvel Dinâmica
        ma_col_name = f'MA{ma_period}'
        df[ma_col_name] = df['Close'].rolling(window=ma_period).mean()
        
        # Calcula RSI (14 periodos padrao)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        df.dropna(inplace=True)

        if df.empty:
            return jsonify({"erro": "Dados insuficientes"}), 404

        dados_json = {
            "symbol": ticker, 
            "datas": df.index.strftime('%Y-%m-%d %H:%M').tolist(),
            "open": df['Open'].tolist(),
            "high": df['High'].tolist(),
            "low": df['Low'].tolist(),
            "close": df['Close'].tolist(),
            "ma": df[ma_col_name].tolist(),
            "ma_label": f"MA {ma_period}",
            "rsi": df['RSI'].tolist(),
            "preco_atual": f"{df['Close'].iloc[-1]:.2f}"
        }
        
        return jsonify(dados_json)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/api/heatmap')
def heatmap_data():
    try:
        tipo = request.args.get('type', 'cripto')
        
        # Verifica Cache
        now = time.time()
        if tipo in CACHE_HEATMAP:
            last_update = CACHE_HEATMAP[tipo]['timestamp']
            if now - last_update < CACHE_DURATION:
                print(f"Retornando cache para {tipo}")
                return jsonify(CACHE_HEATMAP[tipo]['data'])

        tickers = ASSETS.get(tipo, ASSETS['cripto'])
        
        dados_heatmap = []
        
        if tickers:
            string_tickers = " ".join(tickers)
            # Enable threads for speed, cache handles s
            print(f"Baixando dados para heatmap: {tipo}")
            data = yf.download(string_tickers, period="5d", group_by='ticker', progress=False, threads=True, auto_adjust=False)
            
            if data.empty:
                return jsonify([])

            for ticker in tickers:
                try:
                    # Handle different data structures
                    if ticker in data:
                        df_ticker = data[ticker]
                    elif isinstance(data.columns, pd.MultiIndex) and ticker in data.columns.get_level_values(0):
                        df_ticker = data[ticker]
                    else:
                        # Fallback for single ticker result or flat structure
                        if len(tickers) == 1 and not isinstance(data.columns, pd.MultiIndex):
                             df_ticker = data
                        else:
                             continue
                    
                    # Clean up columns if needed
                    if isinstance(df_ticker.columns, pd.MultiIndex):
                        df_ticker.columns = df_ticker.columns.get_level_values(0)
                    
                    df_ticker = df_ticker.dropna(subset=['Close'])

                    if df_ticker.empty or len(df_ticker) < 2:
                        continue
                        
                    last_close = df_ticker['Close'].iloc[-1]
                    prev_close = df_ticker['Close'].iloc[-2]
                    
                    change_percent = ((last_close - prev_close) / prev_close) * 100
                    
                    dados_heatmap.append({
                        "symbol": ticker,
                        "price": last_close,
                        "change": change_percent,
                        "label": f"{ticker}"
                    })
                except Exception as e:
                    continue
        
        # Atualiza Cache
        CACHE_HEATMAP[tipo] = {
            'timestamp': now,
            'data': dados_heatmap
        }
                
        return jsonify(dados_heatmap)

    except Exception as e:
        print(f"Erro no heatmap: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)