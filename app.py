from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
import logging
from bcb import sgs

# --- CONFIGURATION ---
app = Flask(__name__)
CORS(app)  # Enable CORS for development/cross-origin if needed
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache for Heatmap
CACHE_HEATMAP = {}
CACHE_DURATION = 60  # seconds

# --- ASSETS AND TICKERS (Merged from Backend 3) ---
ASSETS = {
    'cripto': [
        "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "TRX-USD", "DOT-USD",
        "LTC-USD", "SHIB-USD", "BCH-USD", "LINK-USD", "ATOM-USD", "XLM-USD", "UNI7083-USD", "HBAR-USD", "OKB-USD",
        "FIL-USD", "LDO-USD", "APT21794-USD", "ARB11841-USD", "NEAR-USD", "VET-USD", "QNT-USD", "MKR-USD", "AAVE-USD", "ALGO-USD",
        "GRT6719-USD", "STX4847-USD", "SAND-USD", "EOS-USD", "MANA-USD", "THETA-USD", "EGLD-USD",
        "FLOW-USD", "XTZ-USD", "IMX10603-USD", "AXS-USD", "RPL-USD", "KCS-USD", "CRV-USD", "NEO-USD", "KLAY-USD"
    ],
    'br': [
        "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "BBDC3.SA", "ITSA4.SA", "BPAC11.SA", "SANB11.SA", "BBSE3.SA", "CXSE3.SA", "PSSA3.SA",
        "IRBR3.SA", "B3SA3.SA", "BRSR6.SA", "ABCB4.SA", "BPAN4.SA",
        "PETR4.SA", "PETR3.SA", "PRIO3.SA", "VBBR3.SA", "UGPA3.SA", "CSAN3.SA", "RECV3.SA", "BRKM5.SA",
        "VALE3.SA", "GGBR4.SA", "GOAU4.SA", "CSNA3.SA", "USIM5.SA", "CMIN3.SA", "FESA4.SA", "SEER3.SA",
        "MGLU3.SA", "LREN3.SA", "ALPA4.SA", "AMER3.SA", "BHIA3.SA", "PETZ3.SA",
        "ASAI3.SA", "PCAR3.SA", "GMAT3.SA", "SMTO3.SA", "ABEV3.SA", "MDIA3.SA", "CAML3.SA", "BEEF3.SA",
        "SLCE3.SA", "AGRO3.SA",
        "ELET3.SA", "ELET6.SA", "EQTL3.SA", "CPLE3.SA", "CPFE3.SA", "CMIG4.SA", "EGIE3.SA", "ENEV3.SA", "TAEE11.SA",
        "TAEE3.SA", "TAEE4.SA", "NEOE3.SA", "ALUP11.SA", "SBSP3.SA", "SAPR11.SA", "SAPR4.SA", "SAPR3.SA",
        "CSMG3.SA", "AMBP3.SA",
        "HAPV3.SA", "RDOR3.SA", "RADL3.SA", "FLRY3.SA", "HYPE3.SA", "PNVL3.SA", "QUAL3.SA", "MATD3.SA",
        "CYRE3.SA", "EZTC3.SA", "MRVE3.SA", "TEND3.SA", "JHSF3.SA", "IGTI11.SA", "LOGG3.SA", "ALOS3.SA",
        "WEGE3.SA", "TOTS3.SA", "LWSA3.SA", "CASH3.SA", "POSI3.SA", "INTB3.SA", "VIVT3.SA", "TIMS3.SA", "OIBR3.SA",
        "EMBR3.SA", "AZUL4.SA", "CVCB3.SA", "ECOR3.SA", "RAIL3.SA", "RENT3.SA", "MOVI3.SA", "VAMO3.SA",
        "SIMH3.SA", "KEPL3.SA", "WEGE3.SA", "TASA4.SA", "POMO4.SA", "RAPT4.SA", "MYPK3.SA", "LEVE3.SA",
        "COGN3.SA", "YDUQ3.SA", "ANIM3.SA", "AURE3.SA"
    ],
    'us': [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "LLY", "V", "UNH", "XOM", "JNJ", "JPM", "PG", "MA",
        "AVGO", "HD", "CVX", "MRK", "ABBV", "PEP", "KO", "COST", "ADBE", "WMT", "MCD", "CSCO", "CRM", "PFE", "TMO", "BAC",
        "NFLX", "ABT", "DHR", "CMCSA", "AMD", "NKE", "DIS", "INTC", "VZ", "WFC", "TXN", "PM", "NEE", "LIN", "RTX", "BMY",
        "HON", "QCOM", "UPS", "UNP", "AMGN", "LOW", "SPGI", "CAT", "BA", "IBM", "INTU", "GE", "ISRG", "AMAT", "NOW", "SBUX",
        "GS", "DE", "EL", "PLD", "MS", "BLK", "BKNG", "MDLZ", "TJX", "ADP", "T", "GILD", "ADI", "MMC", "C", "CVS", "LMT",
        "MDXG", "UBER", "PYPL", "MO", "REGN", "ZTS", "VRTX", "FI", "SO", "EOG", "PGR", "CI", "BDX", "SLB", "SNOW", "PLTR",
        "COIN", "RBLX", "U"
    ],
    'indices': [
        "^BVSP", "^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI", "^RUT", "^VIX", "^STOXX50E",
        "GC=F", "CL=F", "SI=F", "HG=F", "NG=F", "KC=F", "CC=F", "SB=F", "CT=F", "ZW=F", "ZC=F", "ZS=F",
        "EURUSD=X", "GBPUSD=X", "JPY=X", "BRL=X", "AUDUSD=X", "USDCAD=X", "USDCHF=X", "EURGBP=X"
    ]
}

TICKER_NAMES_BASE = {
    # Cripto
    "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum", "BNB-USD": "Binance Coin", "SOL-USD": "Solana", "XRP-USD": "XRP",
    "ADA-USD": "Cardano", "DOGE-USD": "Dogecoin", "AVAX-USD": "Avalanche", "TRX-USD": "Tron", "DOT-USD": "Polkadot",
    "MATIC-USD": "Polygon", "LTC-USD": "Litecoin", "SHIB-USD": "Shiba Inu", "BCH-USD": "Bitcoin Cash", "LINK-USD": "Chainlink",
    "ATOM-USD": "Cosmos", "XLM-USD": "Stellar", "UNI7083-USD": "Uniswap", "HBAR-USD": "Hedera", "OKB-USD": "OKB",
    "FIL-USD": "Filecoin", "LDO-USD": "Lido DAO", "APT21794-USD": "Aptos", "ARB11841-USD": "Arbitrum", "NEAR-USD": "Near Protocol",
    "VET-USD": "VeChain", "QNT-USD": "Quant", "MKR-USD": "Maker", "AAVE-USD": "Aave", "ALGO-USD": "Algorand",
    "GRT6719-USD": "The Graph", "STX4847-USD": "Stacks", "SAND-USD": "The Sandbox", "EOS-USD": "EOS", "MANA-USD": "Decentraland",
    "THETA-USD": "Theta Network", "FTM-USD": "Fantom", "BIT-USD": "BitDAO", "EGLD-USD": "MultiversX", "FLOW-USD": "Flow",
    "XTZ-USD": "Tezos", "APE3-USD": "ApeCoin", "IMX10603-USD": "Immutable", "AXS-USD": "Axie Infinity", "RPL-USD": "Rocket Pool",
    "KCS-USD": "KuCoin Token", "CRV-USD": "Curve DAO", "NEO-USD": "Neo", "KLAY-USD": "Klaytn",

    # Brasil
    "ITUB4.SA": "Itaú Unibanco", "BBDC4.SA": "Bradesco", "BBAS3.SA": "Banco do Brasil", "BBDC3.SA": "Bradesco ON", "ITSA4.SA": "Itaúsa",
    "BPAC11.SA": "BTG Pactual", "SANB11.SA": "Santander", "BBSE3.SA": "BB Seguridade", "CXSE3.SA": "Caixa Seguridade", "PSSA3.SA": "Porto Seguro",
    "IRBR3.SA": "IRB Brasil", "SULA11.SA": "SulAmérica", "B3SA3.SA": "B3", "CIEL3.SA": "Cielo", "BRSR6.SA": "Banrisul",
    "PETR4.SA": "Petrobras PN", "PETR3.SA": "Petrobras ON", "PRIO3.SA": "Prio", "VBBR3.SA": "Vibra", "UGPA3.SA": "Ultrapar",
    "CSAN3.SA": "Cosan", "RRRP3.SA": "3R Petroleum", "RECV3.SA": "PetroRecôncavo", "ENAT3.SA": "Enauta", "BRKM5.SA": "Braskem",
    "VALE3.SA": "Vale", "GGBR4.SA": "Gerdau", "GOAU4.SA": "Met. Gerdau", "CSNA3.SA": "CSN", "USIM5.SA": "Usiminas",
    "CMIN3.SA": "CSN Mineração", "FESA4.SA": "Ferbasa", "SEER3.SA": "Ser Educacional",
    "MGLU3.SA": "Magalu", "LREN3.SA": "Renner", "ARZZ3.SA": "Arezzo", "SOMA3.SA": "Grupo Soma", "ALPA4.SA": "Alpargatas",
    "AMER3.SA": "Americanas", "BHIA3.SA": "Casas Bahia", "PETZ3.SA": "Petz", "NTCO3.SA": "Natura", "CRFB3.SA": "Carrefour",
    "ASAI3.SA": "Assaí", "PCAR3.SA": "Pão de Açúcar", "GMAT3.SA": "Grupo Mateus", "SMTO3.SA": "São Martinho", "ABEV3.SA": "Ambev",
    "MDIA3.SA": "M. Dias Branco", "CAML3.SA": "Camil", "BEEF3.SA": "Minerva", "MRFG3.SA": "Marfrig", "JBSS3.SA": "JBS",
    "BRFS3.SA": "BRF", "SLCE3.SA": "SLC Agrícola", "AGRO3.SA": "BrasilAgro",
    "ELET3.SA": "Eletrobras", "ELET6.SA": "Eletrobras PNB", "EQTL3.SA": "Equatorial", "CPLE6.SA": "Copel", "CPFE3.SA": "CPFL",
    "CMIG4.SA": "Cemig", "EGIE3.SA": "Engie", "ENEV3.SA": "Eneva", "TRPL4.SA": "ISA CTO", "TAEE11.SA": "Taesa",
    "NEOE3.SA": "Neoenergia", "ENBR3.SA": "EDP Brasil", "ALUP11.SA": "Alupar", "AESB3.SA": "AES Brasil", "SBSP3.SA": "Sabesp",
    "SAPR11.SA": "Sanepar", "CSMG3.SA": "Copasa", "AMBP3.SA": "Ambipar",
    "HAPV3.SA": "Hapvida", "RDOR3.SA": "Rede D'Or", "RADL3.SA": "RaiaDrogasil", "FLRY3.SA": "Fleury", "HYPE3.SA": "Hypera",
    "CYRE3.SA": "Cyrela", "EZTC3.SA": "EZTEC", "MRVE3.SA": "MRV", "TEND3.SA": "Tenda", "JHSF3.SA": "JHSF",
    "MULTI3.SA": "Multiplan", "IGTI11.SA": "Iguatemi", "LOGG3.SA": "Log CP", "ALOS3.SA": "Allos",
    "WEGE3.SA": "WEG", "TOTS3.SA": "Totvs", "LWSA3.SA": "Locaweb", "CASH3.SA": "Méliuz", "POSI3.SA": "Positivo",
    "VIVT3.SA": "Vivo", "TIMS3.SA": "TIM", "OIBR3.SA": "Oi", "EMBR3.SA": "Embraer", "AZUL4.SA": "Azul", "GOLL4.SA": "Gol",
    "CVCB3.SA": "CVC", "CCRO3.SA": "CCR", "ECOR3.SA": "EcoRodovias", "RAIL3.SA": "Rumo", "RENT3.SA": "Localiza",
    "MOVI3.SA": "Movida", "VAMO3.SA": "Vamos", "SIMH3.SA": "Simpar", "KEPL3.SA": "Kepler Weber",
    "COGN3.SA": "Cogna", "YDUQ3.SA": "Yduqs", "ANIM3.SA": "Ânima", "AURE3.SA": "Auren", "STBP3.SA": "Santos Brasil",

    # USA
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Alphabet", "AMZN": "Amazon", "NVDA": "Nvidia", "TSLA": "Tesla", "META": "Meta",
    "BRK-B": "Berkshire", "LLY": "Eli Lilly", "V": "Visa", "UNH": "UnitedHealth", "XOM": "Exxon Mobil", "JNJ": "Johnson & Johnson",
    "JPM": "JPMorgan", "PG": "Procter & Gamble", "MA": "Mastercard", "AVGO": "Broadcom", "HD": "Home Depot", "CVX": "Chevron",
    "MRK": "Merck", "ABBV": "AbbVie", "PEP": "PepsiCo", "KO": "Coca-Cola", "COST": "Costco", "ADBE": "Adobe", "WMT": "Walmart",
    "MCD": "McDonald's", "CSCO": "Cisco", "CRM": "Salesforce", "PFE": "Pfizer", "TMO": "Thermo Fisher", "BAC": "Bank of America",
    "NFLX": "Netflix", "ABT": "Abbott", "DHR": "Danaher", "CMCSA": "Comcast", "AMD": "AMD", "NKE": "Nike", "DIS": "Disney",
    "INTC": "Intel", "VZ": "Verizon", "WFC": "Wells Fargo", "TXN": "Texas Instr", "PM": "Philip Morris", "NEE": "NextEra",
    "LIN": "Linde", "RTX": "Raytheon", "BMY": "Bristol-Myers", "HON": "Honeywell", "QCOM": "Qualcomm", "UPS": "UPS",
    "UNP": "Union Pacific", "AMGN": "Amgen", "LOW": "Lowe's", "SPGI": "S&P Global", "CAT": "Caterpillar", "BA": "Boeing",
    "IBM": "IBM", "INTU": "Intuit", "GE": "GE Aerospace", "ISRG": "Intuitive Surg", "AMAT": "Applied Mat", "NOW": "ServiceNow",
    "SBUX": "Starbucks", "GS": "Goldman Sachs", "DE": "Deere & Co", "EL": "Estée Lauder", "PLD": "Prologis", "MS": "Morgan Stanley",
    "BLK": "BlackRock", "BKNG": "Booking.com", "MDLZ": "Mondelez", "TJX": "TJX Cos", "ADP": "ADP", "T": "AT&T", "GILD": "Gilead",
    "ADI": "Analog Devices", "MMC": "Marsh & McL", "C": "Citigroup", "CVS": "CVS Health", "LMT": "Lockheed Martin",
    "MDXG": "Mimedx", "UBER": "Uber", "PYPL": "PayPal", "MO": "Altria", "REGN": "Regeneron", "ZTS": "Zoetis", "VRTX": "Vertex",
    "FI": "Fiserv", "SO": "Southern Co", "EOG": "EOG Res", "PGR": "Progressive", "CI": "Cigna", "BDX": "Becton Dick",
    "SLB": "Schlumberger", "SNOW": "Snowflake", "PLTR": "Palantir", "COIN": "Coinbase", "RBLX": "Roblox", "U": "Unity",

    # Índices e Commodities
    "^BVSP": "Ibovespa", "^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^DJI": "Dow Jones", "^FTSE": "FTSE 100",
    "^GDAXI": "DAX", "^FCHI": "CAC 40", "^N225": "Nikkei 225", "^HSI": "Hang Seng", "^RUT": "Russell 2000",
    "^VIX": "VIX", "^STOXX50E": "Euro Stoxx 50",
    "GC=F": "Ouro", "CL=F": "Petróleo WTI", "SI=F": "Prata", "HG=F": "Cobre", "NG=F": "Gás Natural",
    "KC=F": "Café", "CC=F": "Cacau", "SB=F": "Açúcar", "CT=F": "Algodão", "ZW=F": "Trigo", "ZC=F": "Milho", "ZS=F": "Soja",
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "JPY=X": "USD/JPY", "BRL=X": "USD/BRL", "AUDUSD=X": "AUD/USD",
    "USDCAD=X": "USD/CAD", "USDCHF=X": "USD/CHF", "EURGBP=X": "EUR/GBP"
}
# (The full dictionary from backend3 is assumed for brevity, will implement lookup logic gracefully)

# --- STATIC FILES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return send_from_directory(BASE_DIR, 'index2.html')

@app.route('/portfolio')
def portfolio():
    return send_from_directory(BASE_DIR, 'portfolio.html')

@app.route('/analise')
def analise():
    return send_from_directory(BASE_DIR, 'analise_carteiras.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(BASE_DIR, filename)

# --- MARKET DATA API (from Backend 2) ---

@app.route('/api/dados')
def pegar_dados():
    try:
        ticker = request.args.get('ticker', 'BTC-USD')
        period = request.args.get('period', '1y')
        interval = request.args.get('interval', '1d')
        ma_period = int(request.args.get('ma_period', 14))

        df = yf.download(ticker, period=period, interval=interval, progress=False, threads=False, auto_adjust=False)
        
        if df.empty:
            return jsonify({"erro": "Ticker não encontrado"}), 404

        # Clean MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            try:
                if ticker in df.columns.get_level_values(1):
                    df = df.xs(ticker, axis=1, level=1)
                else:
                    df.columns = df.columns.get_level_values(0)
            except:
                df.columns = df.columns.get_level_values(0)

        df.columns = [c.capitalize() for c in df.columns]

        # Indicators
        ma_col = f'MA{ma_period}'
        df[ma_col] = df['Close'].rolling(window=ma_period).mean()

        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # MACD
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD_Line'] = ema12 - ema26
        df['Signal_Line'] = df['MACD_Line'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD_Line'] - df['Signal_Line']

        # Stochastic
        low_min = df['Low'].rolling(window=14).min()
        high_max = df['High'].rolling(window=14).max()
        denom = (high_max - low_min).replace(0, 0.000001)
        df['Fast_K'] = 100 * ((df['Close'] - low_min) / denom)
        df['Slow_K'] = df['Fast_K'].rolling(window=3).mean()
        df['Slow_D'] = df['Slow_K'].rolling(window=3).mean()

        df.dropna(inplace=True)
        
        return jsonify({
            "symbol": ticker,
            "datas": df.index.strftime('%Y-%m-%d %H:%M').tolist(),
            "open": df['Open'].tolist(),
            "high": df['High'].tolist(),
            "low": df['Low'].tolist(),
            "close": df['Close'].tolist(),
            "ma": df[ma_col].tolist(),
            "rsi": df['RSI'].tolist(),
            "macd_hist": df['MACD_Hist'].tolist(),
            "stoch_k": df['Slow_K'].tolist(),
            "stoch_d": df['Slow_D'].tolist(),
            "volume": df['Volume'].fillna(0).tolist(),
            "preco_atual": f"{df['Close'].iloc[-1]:.2f}"
        })

    except Exception as e:
        logger.error(f"Error in /api/dados: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/api/heatmap')
def heatmap_data():
    try:
        tipo = request.args.get('type', 'cripto')
        now = time.time()
        
        # Cache Check
        if tipo in CACHE_HEATMAP:
            if now - CACHE_HEATMAP[tipo]['timestamp'] < CACHE_DURATION:
                return jsonify(CACHE_HEATMAP[tipo]['data'])

        tickers = ASSETS.get(tipo, ASSETS['cripto'])
        if not tickers: return jsonify([])

        data = yf.download(tickers, period="5d", progress=False, threads=True, auto_adjust=False)
        result = []

        # Process each ticker
        for t in tickers:
            try:
                # Extract Close series safely
                if isinstance(data.columns, pd.MultiIndex):
                    if t in data.columns.get_level_values(1):
                        series = data.xs(t, axis=1, level=1)['Close']
                    elif 'Close' in data.columns.get_level_values(0):
                         # If level 0 is 'Close' and level 1 is ticker
                         series = data['Close'][t]
                    else: continue
                else:
                    # Single level columns?
                    if t in data: series = data[t] # Might be 'Close' check needed
                    elif 'Close' in data and t in data['Close']: series = data['Close'][t]
                    else: continue
                
                series = series.dropna()
                if len(series) < 2: continue

                last = series.iloc[-1]
                prev = series.iloc[-2]
                change = ((last - prev) / prev) * 100
                
                name = TICKER_NAMES_BASE.get(t, t) # Simplified lookup
                
                result.append({
                    "symbol": t,
                    "name": name,
                    "price": float(last),
                    "change": float(change),
                    "label": t
                })
            except Exception as e:
                continue
        
        CACHE_HEATMAP[tipo] = {'timestamp': now, 'data': result}
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in heatmap: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/api/market-movers')
def market_movers():
    try:
        tipo = request.args.get('type', 'all')
        target_assets = []
        if tipo == 'all':
            for k in ASSETS: target_assets.extend(ASSETS[k])
        else:
            target_assets = ASSETS.get(tipo, [])

        # Limit for performance if 'all' (could be hundreds) -> batching or limiting?
        # Let's take first 50 of each or just all. 'all' is heavy.
        if len(target_assets) > 100: target_assets = target_assets[:100]

        data = yf.download(target_assets, period="5d", progress=False, threads=True)['Close']
        changes = []

        for t in target_assets:
            try:
                if isinstance(data, pd.DataFrame):
                    if t in data.columns:
                        vals = data[t].dropna()
                        if len(vals) >= 2:
                            c = ((vals.iloc[-1] - vals.iloc[-2]) / vals.iloc[-2]) * 100
                            changes.append({
                                "symbol": t,
                                "name": TICKER_NAMES_BASE.get(t, t),
                                "price": float(vals.iloc[-1]),
                                "change": float(c)
                            })
                elif isinstance(data, pd.Series): # Single asset case
                    vals = data.dropna()
                    if len(vals) >= 2:
                        c = ((vals.iloc[-1] - vals.iloc[-2])/vals.iloc[-2])*100
                        changes.append({"symbol": t, "name": t, "price": float(vals.iloc[-1]), "change": float(c)})
            except: pass
        
        changes.sort(key=lambda x: x['change'], reverse=True)
        return jsonify({"gainers": changes[:5], "losers": changes[-5:]})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# --- PORTFOLIO & ANALYSIS API (from Backend 3) ---

@app.route('/api/assets', methods=['GET'])
def list_assets():
    flat = []
    seen = set()
    for cat, items in ASSETS.items():
        for t in items:
            if t not in seen:
                flat.append({"symbol": t, "name": TICKER_NAMES_BASE.get(t, t), "category": cat})
                seen.add(t)
    return jsonify(flat)

@app.route('/api/calculate_portfolio', methods=['POST'])
def calculate_portfolio():
    try:
        data = request.get_json()
        transactions = data.get('transactions', [])
        if not transactions: return jsonify({"error": "No transactions"}), 400

        tickers = list(set([t['ticker'] for t in transactions]))
        live_data = yf.download(tickers, period="2d", progress=False)['Close']
        
        current_prices = {}
        for t in tickers:
            try:
                if isinstance(live_data, pd.DataFrame) and t in live_data.columns:
                    current_prices[t] = float(live_data[t].dropna().iloc[-1])
                elif isinstance(live_data, pd.Series): # One ticker
                    current_prices[t] = float(live_data.dropna().iloc[-1])
                else: current_prices[t] = 0.0
            except: current_prices[t] = 0.0

        total_invested = 0.0
        current_val = 0.0
        holdings_map = {}

        for tx in transactions:
            t = tx['ticker']
            qty = float(tx['qty'])
            price = float(tx['price'])
            
            total_invested += qty * price
            
            if t not in holdings_map: holdings_map[t] = {'ticker': t, 'qty': 0, 'invested': 0.0, 'current_value': 0.0}
            holdings_map[t]['qty'] += qty
            holdings_map[t]['invested'] += qty * price

        holdings = []
        for t, h in holdings_map.items():
            cur_p = current_prices.get(t, 0.0)
            h['current_price'] = cur_p
            h['current_value'] = h['qty'] * cur_p
            h['profit'] = h['current_value'] - h['invested']
            h['profit_pct'] = (h['profit']/h['invested']*100) if h['invested'] else 0
            
            # Category calc
            cat = 'Outros'
            for c, l in ASSETS.items():
                if t in l: 
                    cat = c; break
            h['category'] = cat
            
            current_val += h['current_value']
            holdings.append(h)

        return jsonify({
            "total_invested": total_invested,
            "current_value": current_val,
            "profit_loss": current_val - total_invested,
            "profit_loss_pct": ((current_val - total_invested)/total_invested*100) if total_invested else 0,
            "holdings": holdings
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/correlation', methods=['POST'])
def portfolio_correlation():
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        start = data.get('start_date')
        end = data.get('end_date')

        if len(tickers) < 2: return jsonify({"error": "Need 2+ tickers"}), 400

        df = yf.download(tickers, start=start, end=end, progress=False)['Close']
        df = df.dropna()
        returns = df.pct_change().dropna()
        corr_matrix = returns.corr()

        # Summary
        mask = np.ones(corr_matrix.shape, dtype=bool)
        np.fill_diagonal(mask, 0)
        avg_corr = np.nanmean(np.abs(corr_matrix.values[mask])) if len(tickers) > 1 else 0

        return jsonify({
            "tickers": corr_matrix.columns.tolist(),
            "z": corr_matrix.values.tolist(),
            "avg_correlation": avg_corr,
            "summary": f"Correlação Média de {avg_corr:.2f}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/benchmark', methods=['POST'])
def portfolio_benchmark():
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        weights = data.get('weights', [1.0/len(data.get('tickers'))]*len(data.get('tickers')))
        bench = data.get('benchmark', '^BVSP')
        start = data.get('start_date')
        end = data.get('end_date')

        all_sym = tickers + [bench]
        df = yf.download(all_sym, start=start, end=end, progress=False)['Close']
        
        # Portfolio Curve
        # This is a simplification vs backend3 but functionally sufficient for display
        # assuming daily rebalance or simple index tracking
        
        port_returns = df[tickers].pct_change().fillna(0)
        weighted_returns = (port_returns * weights).sum(axis=1)
        port_cum = (1 + weighted_returns).cumprod() - 1

        bench_data = df[bench].pct_change().fillna(0)
        bench_cum = (1 + bench_data).cumprod() - 1

        dates = port_cum.index.strftime('%Y-%m-%d').tolist()

        return jsonify({
            "dates": dates,
            "portfolio": (port_cum * 100).fillna(0).tolist(),
            "benchmark": (bench_cum * 100).fillna(0).tolist(),
            "benchmark_symbol": bench
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Unified FinSense App on Port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
