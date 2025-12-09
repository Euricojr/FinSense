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

# Mapeamento de Nomes Amigáveis
TICKER_NAMES = {
    # Cripto
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "SOL-USD": "Solana", "BNB-USD": "Binance Coin",
    "XRP-USD": "XRP", "ADA-USD": "Cardano", "DOGE-USD": "Dogecoin", "AVAX-USD": "Avalanche",
    "TRX-USD": "Tron", "DOT-USD": "Polkadot", "LINK-USD": "Chainlink", "LTC-USD": "Litecoin",
    "BCH-USD": "Bitcoin Cash", "ATOM-USD": "Cosmos", "XLM-USD": "Stellar", "ETC-USD": "Ethereum Classic",
    "FIL-USD": "Filecoin", "HBAR-USD": "Hedera", "NEAR-USD": "Near Protocol", "VET-USD": "VeChain",
    "QNT-USD": "Quant", "MKR-USD": "Maker", "AAVE-USD": "Aave", "ALGO-USD": "Algorand",
    "SAND-USD": "The Sandbox", "EOS-USD": "EOS", "MANA-USD": "Decentraland",
    
    # BR Actions
    "VALE3.SA": "Vale", "PETR4.SA": "Petrobras PN", "ITUB4.SA": "Itaú Unibanco", "BBDC4.SA": "Bradesco PN",
    "BBAS3.SA": "Banco do Brasil", "PETR3.SA": "Petrobras ON", "ABEV3.SA": "Ambev", "WEGE3.SA": "WEG",
    "RENT3.SA": "Localiza", "BPAC11.SA": "BTG Pactual", "SUZB3.SA": "Suzano", "ITSA4.SA": "Itaúsa",
    "HAPV3.SA": "Hapvida", "RDOR3.SA": "Rede D'Or", "JBSS3.SA": "JBS", "B3SA3.SA": "B3",
    "GGBR4.SA": "Gerdau", "RADL3.SA": "Raia Drogasil", "PRIO3.SA": "Prio", "RAIL3.SA": "Rumo",
    "VBBR3.SA": "Vibra", "ELET3.SA": "Eletrobras", "UGPA3.SA": "Ultrapar", "CSAN3.SA": "Cosan",
    "BBSE3.SA": "BB Seguridade", "LREN3.SA": "Lojas Renner", "VIVT3.SA": "Vivo", "EQTL3.SA": "Equatorial",
    "SBSP3.SA": "Sabesp", "CMIG4.SA": "Cemig", "CPLE6.SA": "Copel", "EMBR3.SA": "Embraer",
    "TIMS3.SA": "TIM", "CCRO3.SA": "CCR", "ASAI3.SA": "Assaí", "HYPE3.SA": "Hypera",
    "TOTS3.SA": "Totvs", "CSNA3.SA": "CSN", "MGLU3.SA": "Magalu", "BHIA3.SA": "Casas Bahia",

    # US Actions
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", "AMZN": "Amazon",
    "NVDA": "Nvidia", "TSLA": "Tesla", "META": "Meta", "BRK-B": "Berkshire",
    "LLY": "Eli Lilly", "V": "Visa", "UNH": "UnitedHealth", "XOM": "Exxon Mobil",
    "JNJ": "Johnson & Johnson", "JPM": "JPMorgan", "PG": "P&G", "MA": "Mastercard",
    "AVGO": "Broadcom", "HD": "Home Depot", "CVX": "Chevron", "MRK": "Merck",
    "ABBV": "AbbVie", "PEP": "PepsiCo", "KO": "Coca-Cola", "COST": "Costco",
    "ADBE": "Adobe", "WMT": "Walmart", "MCD": "McDonald's", "CSCO": "Cisco",
    "CRM": "Salesforce", "PFE": "Pfizer", "TMO": "Thermo Fisher", "BAC": "Bank of America",
    "NFLX": "Netflix", "ABT": "Abbott", "DHR": "Danaher", "CMCSA": "Comcast",
    "AMD": "AMD", "NKE": "Nike", "DIS": "Disney", "INTC": "Intel",

    # Indices
    "^BVSP": "Ibovespa", "^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^DJI": "Dow Jones",
    "^FTSE": "FTSE 100", "^GDAXI": "DAX", "^FCHI": "CAC 40", "^N225": "Nikkei 225",
    "^HSI": "Hang Seng", "GC=F": "Ouro", "CL=F": "Petróleo WTI", "SI=F": "Prata",
    "HG=F": "Cobre", "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "JPY=X": "USD/JPY",
    "BRL=X": "USD/BRL"
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
        period = request.args.get('period', '3mo')
        interval = request.args.get('interval', '1d')
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

################################ ATR, Volume, ADX , Estocastico
        
        # Calcula a Média Móvel Dinâmica
        ma_col_name = f'MA{ma_period}'
        df[ma_col_name] = df['Close'].rolling(window=ma_period).mean()
        
        # Calcula RSI (14 periodos padrao)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # Calcula MACD
        # EMA 12 e 26
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD_Line'] = ema12 - ema26
        df['Signal_Line'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD_Line'] - df['Signal_Line']
        
        # Calcula Estocastico Lento (14, 3, 3)
        # Fast %K = 100 * ((Close - Lowest Low) / (Highest High - Lowest Low))
        # Slow %K = SMA(Fast %K, 3)
        # Slow %D = SMA(Slow %K, 3)
        
        low_min = df['Low'].rolling(window=14).min()
        high_max = df['High'].rolling(window=14).max()
        
        # Evitar divisao por zero
        denom = high_max - low_min
        denom = denom.replace(0, 0.000001)
        
        df['Fast_K'] = 100 * ((df['Close'] - low_min) / denom)
        df['Slow_K'] = df['Fast_K'].rolling(window=3).mean()
        df['Slow_D'] = df['Slow_K'].rolling(window=3).mean()

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
            "macd_line": df['MACD_Line'].tolist(),
            "signal_line": df['Signal_Line'].tolist(),
            "macd_hist": df['MACD_Hist'].tolist(),
            "stoch_k": df['Slow_K'].tolist(),
            "stoch_d": df['Slow_D'].tolist(),
            "volume": df['Volume'].fillna(0).tolist(),
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
                        "name": TICKER_NAMES.get(ticker, ticker),
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

@app.route('/api/market-movers')
def market_movers():
    try:
        tipo = request.args.get('type', 'all')
        
        # 1. Select Asset List
        todos_tickers = []
        if tipo in ASSETS:
            todos_tickers = ASSETS[tipo]
        else:
            # Flatten all
            for cat, lista in ASSETS.items():
                todos_tickers.extend(lista)
            
        # 2. Batch download (last 5 days)
        data = yf.download(todos_tickers, period='5d', progress=False, threads=True, auto_adjust=False)
        
        # Determine if we have MultiIndex columns (Ticker as level)
        # If multiple tickers, columns are (PriceType, Ticker) or similar.
        # We need 'Close'.
        if isinstance(data.columns, pd.MultiIndex):
            closes = data['Close']
        else:
            # If single ticker or flat, might just be 'Close'
            # But with list download it's usually MultiIndex or flat if just 1.
            # Use 'Close' if available, else assume it IS close (unlikely).
            if 'Close' in data:
                closes = data['Close']
            else:
                closes = data

        variacoes = []
        
        # Iterate over all tickers we think we have
        # Columns of 'closes' should be tickers if MultiIndex was handled correctly by yf
        # or we might need to check.
        
        for ticker in todos_tickers:
            try:
                # Get series
                if ticker in closes.columns:
                    series = closes[ticker].dropna()
                else:
                    continue

                if len(series) >= 2:
                    current = series.iloc[-1]
                    prev = series.iloc[-2]
                    # Avoid zero division
                    if prev == 0: continue
                    
                    change_pct = ((current - prev) / prev) * 100
                    
                    variacoes.append({
                        "symbol": ticker,
                        "name": TICKER_NAMES.get(ticker, ticker),
                        "price": float(current),
                        "change": float(change_pct)
                    })
            except Exception:
                continue

        # 3. Sort
        # Gainers: Descending
        variacoes.sort(key=lambda x: x['change'], reverse=True)
        gainers = variacoes[:5]
        
        # Losers: Ascending
        variacoes.sort(key=lambda x: x['change'])
        losers = variacoes[:5]
        
        return jsonify({
            "gainers": gainers,
            "losers": losers
        })

    except Exception as e:
        print(f"Erro movers: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)