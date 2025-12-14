from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import logging
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- DATA DEFINITIONS (Copied from backend3.py for consistency) ---
ASSETS = {
    'cripto': [
        "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "TRX-USD", "DOT-USD",
        "MATIC-USD", "LTC-USD", "SHIB-USD", "BCH-USD", "LINK-USD", "ATOM-USD", "XLM-USD", "UNI7083-USD", "HBAR-USD", "OKB-USD",
        "FIL-USD", "LDO-USD", "APT21794-USD", "ARB11841-USD", "NEAR-USD", "VET-USD", "QNT-USD", "MKR-USD", "AAVE-USD", "ALGO-USD",
        "GRT6719-USD", "STX4847-USD", "SAND-USD", "EOS-USD", "MANA-USD", "THETA-USD", "FTM-USD", "BIT-USD", "EGLD-USD",
        "FLOW-USD", "XTZ-USD", "APE3-USD", "IMX10603-USD", "AXS-USD", "RPL-USD", "KCS-USD", "CRV-USD", "NEO-USD", "KLAY-USD"
    ],
    'br': [
        "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "BBDC3.SA", "ITSA4.SA", "BPAC11.SA", "SANB11.SA", "BBSE3.SA", "CXSE3.SA", "PSSA3.SA",
        "IRBR3.SA", "SULA11.SA", "B3SA3.SA", "CIEL3.SA", "BRSR6.SA", "ABCB4.SA", "BPAN4.SA",
        "PETR4.SA", "PETR3.SA", "PRIO3.SA", "VBBR3.SA", "UGPA3.SA", "CSAN3.SA", "RRRP3.SA", "RECV3.SA", "ENAT3.SA", "BRKM5.SA",
        "VALE3.SA", "GGBR4.SA", "GOAU4.SA", "CSNA3.SA", "USIM5.SA", "CMIN3.SA", "FESA4.SA", "SEER3.SA",
        "MGLU3.SA", "LREN3.SA", "ARZZ3.SA", "SOMA3.SA", "ALPA4.SA", "AMER3.SA", "BHIA3.SA", "PETZ3.SA", "NTCO3.SA", "CRFB3.SA",
        "ASAI3.SA", "PCAR3.SA", "GMAT3.SA", "SMTO3.SA", "ABEV3.SA", "MDIA3.SA", "CAML3.SA", "BEEF3.SA", "MRFG3.SA", "JBSS3.SA",
        "BRFS3.SA", "SLCE3.SA", "AGRO3.SA",
        "ELET3.SA", "ELET6.SA", "EQTL3.SA", "CPLE6.SA", "CPFE3.SA", "CMIG4.SA", "EGIE3.SA", "ENEV3.SA", "TRPL4.SA", "TAEE11.SA",
        "TAEE3.SA", "TAEE4.SA", "NEOE3.SA", "ENBR3.SA", "ALUP11.SA", "AESB3.SA", "SBSP3.SA", "SAPR11.SA", "SAPR4.SA", "SAPR3.SA",
        "CSMG3.SA", "AMBP3.SA",
        "HAPV3.SA", "RDOR3.SA", "RADL3.SA", "FLRY3.SA", "HYPE3.SA", "PNVL3.SA", "QUAL3.SA", "MATD3.SA",
        "CYRE3.SA", "EZTC3.SA", "MRVE3.SA", "TEND3.SA", "JHSF3.SA", "MULTI3.SA", "IGTI11.SA", "LOGG3.SA", "ALOS3.SA",
        "WEGE3.SA", "TOTS3.SA", "LWSA3.SA", "CASH3.SA", "POSI3.SA", "INTB3.SA", "VIVT3.SA", "TIMS3.SA", "OIBR3.SA",
        "EMBR3.SA", "AZUL4.SA", "GOLL4.SA", "CVCB3.SA", "CCRO3.SA", "ECOR3.SA", "RAIL3.SA", "RENT3.SA", "MOVI3.SA", "VAMO3.SA",
        "SIMH3.SA", "KEPL3.SA", "WEGE3.SA", "TASA4.SA", "POMO4.SA", "RAPT4.SA", "MYPK3.SA", "LEVE3.SA",
        "COGN3.SA", "YDUQ3.SA", "ANIM3.SA", "AURE3.SA", "STBP3.SA"
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

TICKER_NAMES_UPDATE_BR = {
    "SAPR11.SA": "Sanepar Unit", "SAPR4.SA": "Sanepar PN", "SAPR3.SA": "Sanepar ON",
    "TAEE11.SA": "Taesa Unit", "TAEE3.SA": "Taesa ON", "TAEE4.SA": "Taesa PN",
    "TASA4.SA": "Taurus Armas", "TRPL4.SA": "ISA CTEEP", "ALUP11.SA": "Alupar",
    "CXSE3.SA": "Caixa Seguridade", "PSSA3.SA": "Porto Seguro", "IRBR3.SA": "IRB Brasil",
    "SULA11.SA": "SulAmérica", "CIEL3.SA": "Cielo", "BRSR6.SA": "Banrisul",
    "ABCB4.SA": "Banco ABC", "BPAN4.SA": "Banco Pan", "RECV3.SA": "PetroReconcavo",
    "ENAT3.SA": "Enauta", "BRKM5.SA": "Braskem", "FESA4.SA": "Ferbasa",
    "SEER3.SA": "Ser Educacional", "ARZZ3.SA": "Arezzo", "AMER3.SA": "Americanas",
    "GMAT3.SA": "Grupo Mateus", "SMTO3.SA": "São Martinho", "MDIA3.SA": "M. Dias Branco",
    "CAML3.SA": "Camil", "BEEF3.SA": "Minerva", "MRFG3.SA": "Marfrig",
    "SLCE3.SA": "SLC Agrícola", "AGRO3.SA": "BrasilAgro", "ELET6.SA": "Eletrobras PNB",
    "NEOE3.SA": "Neoenergia", "ENBR3.SA": "EDP Brasil", "AESB3.SA": "AES Brasil",
    "CSMG3.SA": "Copasa", "AMBP3.SA": "Ambipar", "PNVL3.SA": "Dimed",
    "QUAL3.SA": "Qualicorp", "MATD3.SA": "Mater Dei", "TEND3.SA": "Tenda",
    "JHSF3.SA": "JHSF", "MULTI3.SA": "Multiplan", "ALOS3.SA": "Allos",
    "INTB3.SA": "Intelbras", "OIBR3.SA": "Oi", "ECOR3.SA": "EcoRodovias",
    "MOVI3.SA": "Movida", "VAMO3.SA": "Vamos", "SIMH3.SA": "Simpar",
    "KEPL3.SA": "Kepler Weber", "POMO4.SA": "Marcopolo", "RAPT4.SA": "Randon",
    "MYPK3.SA": "Iochpe-Maxion", "LEVE3.SA": "Mahle Metal Leve",
    "COGN3.SA": "Cogna", "YDUQ3.SA": "Yduqs", "ANIM3.SA": "Anima",
    "AURE3.SA": "Auren Energia", "STBP3.SA": "Santos Brasil"
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
    "XTZ-USD": "Tezos", "APE3-USD": "ApeCoin", "IMX10603-USD": "Immutable X", "AXS-USD": "Axie Infinity", "RPL-USD": "Rocket Pool",
    "KCS-USD": "KuCoin Token", "CRV-USD": "Curve DAO", "NEO-USD": "NEO", "KLAY-USD": "Klaytn",

    # US (Shortened)
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", "AMZN": "Amazon", "NVDA": "Nvidia",
    "TSLA": "Tesla", "META": "Meta",
    # ... assuming standard set from before ...
    "VALE3.SA": "Vale", "PETR4.SA": "Petrobras PN", "ITUB4.SA": "Itaú Unibanco"
}

# Simplified merge but you can keep full map if needed.
TICKER_NAMES = {**TICKER_NAMES_BASE, **TICKER_NAMES_UPDATE_BR}

# --- ROUTES ---

@app.route('/')
def home():
    # Serve portfolio page by default for this backend
    return send_file(os.path.join(os.getcwd(), 'portfolio.html'))

@app.route('/portfolio')
def portfolio_page():
    return send_file(os.path.join(os.getcwd(), 'portfolio.html'))

@app.route('/api/assets', methods=['GET'])
def list_assets():
    flat_list = []
    seen = set()
    for category in ['cripto', 'br', 'us', 'indices']:
        if category in ASSETS:
            for symbol in ASSETS[category]:
                if symbol not in seen:
                    name = TICKER_NAMES.get(symbol, symbol)
                    flat_list.append({
                        "symbol": symbol,
                        "name": name,
                        "category": category
                    })
                    seen.add(symbol)
    return jsonify(flat_list)

@app.route('/api/calculate_portfolio', methods=['POST'])
def calculate_portfolio():
    try:
        transactions = request.get_json()
        if not transactions:
            return jsonify({"error": "No transactions provided"}), 400

        # 1. Fetch current prices
        tickers = list(set([t['ticker'] for t in transactions]))
        
        # Download 1d data just to get latest price
        # Using period='1d' is faster than date range for current price
        # But yfinance might return empty if market is closed?
        # Better to fetch a few days to be safe
        data = yf.download(tickers, period="5d", progress=False, threads=True)
        
        # Extract latest close prices
        latest_prices = {}
        if len(tickers) == 1:
            ticker = tickers[0]
            # yfinance returns DataFrame directly for single
            # Check structure
            # data could be Series or DataFrame depending on yfinance version/call
            try:
                # Get last valid index
                last_price = data['Close'].iloc[-1]
                # If MultiIndex (unlikely for 1 ticker but possible)
                if isinstance(last_price, pd.Series):
                    last_price = last_price.values[0]
                latest_prices[ticker] = float(last_price)
            except Exception as e:
                logger.error(f"Error extracting price for {ticker}: {e}")
        else:
            # multiple tickers
            # data['Close'] has columns as tickers
            closes = data['Close'] if 'Close' in data else data
            for ticker in tickers:
                try:
                    if ticker in closes.columns:
                        latest_prices[ticker] = float(closes[ticker].dropna().iloc[-1])
                    else:
                        latest_prices[ticker] = 0.0 # Failed to fetch
                except Exception as e:
                     logger.error(f"Error extracting price for {ticker}: {e}")
                     latest_prices[ticker] = 0.0

        # 2. Calculate Portfolio
        total_invested = 0.0
        current_value = 0.0
        holdings = []

        # Group by ticker to handle multiple transactions of same asset
        holdings_map = {}

        for t in transactions:
            ticker = t['ticker']
            qty = float(t['qty'])
            buy_price = float(t['price'])
            
            invested = qty * buy_price
            
            # Current price
            curr_price = latest_prices.get(ticker, buy_price) 
            if curr_price == 0.0: curr_price = buy_price
            
            curr_val = qty * curr_price
            
            total_invested += invested
            current_value += curr_val
            
            if ticker not in holdings_map:
                holdings_map[ticker] = {'ticker': ticker, 'current_value': 0.0, 'invested': 0.0}
            
            holdings_map[ticker]['current_value'] += curr_val
            holdings_map[ticker]['invested'] += invested

        holdings = list(holdings_map.values())

        profit_loss = current_value - total_invested
        profit_loss_pct = (profit_loss / total_invested * 100) if total_invested > 0 else 0.0

        return jsonify({
            "total_invested": total_invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_pct": profit_loss_pct,
            "holdings": holdings,
            "prices": latest_prices
        })

    except Exception as e:
        logger.error(f"Error calculating portfolio: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/benchmark', methods=['POST'])
def calculate_benchmark():
    try:
        data = request.get_json()
        transactions = data.get('tickers', []) 
        if not transactions and 'weights' not in data: # Support old format or new format
            # If came from portfolio.html logic, it sends full transactions list
            transactions = data
        
        # If we receive the full transaction list from portfolio.html
        if isinstance(transactions, list) and len(transactions) > 0 and 'date' in transactions[0]:
            return calculate_portfolio_history(transactions, data.get('benchmark', '^BVSP'))
            
        return jsonify({"error": "Invalid data format"}), 400

    except Exception as e:
        logger.error(f"Error in benchmark: {e}")
        return jsonify({"error": str(e)}), 500

def calculate_portfolio_history(transactions, benchmark_ticker='^BVSP'):
    # 1. Prepare Data
    df_tx = pd.DataFrame(transactions)
    df_tx['date'] = pd.to_datetime(df_tx['date'])
    df_tx['qty'] = df_tx['qty'].astype(float)
    df_tx['price'] = df_tx['price'].astype(float)
    
    start_date = df_tx['date'].min()
    end_date = pd.Timestamp.now()
    
    # 2. Download Data (Portfolio Tickers + Benchmark)
    unique_tickers = df_tx['ticker'].unique().tolist()
    all_tickers = unique_tickers + [benchmark_ticker]
    
    # Download history
    has_crypto = any(t.endswith('-USD') for t in unique_tickers)
    # Crypto trades 24/7, Stocks Mon-Fri. yfinance handles this but alignment is needed.
    # We'll use '1d' interval.
    
    market_data = yf.download(all_tickers, start=start_date, end=end_date, progress=False, threads=True)['Close']
    
    # Handle single ticker case in yfinance (returns Series instead of DataFrame)
    if len(all_tickers) == 1:
        market_data = pd.DataFrame({all_tickers[0]: market_data})
    
    # Fill NAs (forward fill first, then backward fill for very start)
    market_data = market_data.fillna(method='ffill').fillna(method='bfill')
    
    # 3. Calculate Daily Portfolio Value
    # Create an index of all days
    all_days = market_data.index
    portfolio_history = []
    benchmark_history = []
    dates = []
    
    # Initial Benchmark Value (normalized)
    bench_start_val = 100.0 # Base 100
    
    # We need to simulate "What if I bought Benchmark?" or just "Compare Returns"?
    # Kinvo compares % yield.
    # Let's calculate Daily Portfolio Value and Total Invested.
    
    daily_values = []
    invested_values = []
    
    # Pre-calculate holdings for each day is slow in loop.
    # Better: for each transaction, add its value contribution to all subsequent days.
    
    # Initialize series with 0
    portfolio_series = pd.Series(0.0, index=all_days)
    invested_series = pd.Series(0.0, index=all_days)
    
    for _, tx in df_tx.iterrows():
        # Mask for days after transaction
        mask = all_days >= tx['date']
        
        # Contribution to invested amount (Cash Flow)
        invested_amount = tx['qty'] * tx['price']
        invested_series.loc[mask] += invested_amount
        
        # Contribution to current value (qty * price_of_day)
        # If ticker not in market_data (e.g. IPO later), handle gracefully
        if tx['ticker'] in market_data.columns:
            prices = market_data.loc[mask, tx['ticker']]
            value_contribution = prices * tx['qty']
            portfolio_series.loc[mask] += value_contribution
    
    # 4. Calculate Benchmark Scale
    # We want to compare "Growth of Portfolio" vs "Growth of Benchmark"
    # Or "Profitability %".
    # Portfolio Return % = (PortValue / Invested - 1) * 100
    # Benchmark Return % = (BenchPrice / BenchStartPrice - 1) * 100 -> This is wrong if cashflows happened later.
    # Correct Bench comparison: "If I invested the SAME AMOUNT at the SAME TIME in Benchmark".
    
    bench_series = pd.Series(0.0, index=all_days)
    
    # To calculate "Benchmark Equivalent Portfolio":
    # Identify each cashflow. Buy 'InvestedAmount' worth of Benchmark at that day's price.
    # Track "Qty of Benchmark held".
    
    bench_qty_held = pd.Series(0.0, index=all_days)
    
    if benchmark_ticker in market_data.columns:
        bench_prices = market_data[benchmark_ticker]
        
        for _, tx in df_tx.iterrows():
            mask = all_days >= tx['date']
            
            # Price of benchmark at transaction date
            # Find closest date if exact match missing
            try:
                # get price at tx date or nearest before
                idx = market_data.index.get_indexer([tx['date']], method='pad')[0]
                if idx == -1: idx = 0 # fallback
                price_at_buy = bench_prices.iloc[idx]
                
                investment = tx['qty'] * tx['price']
                bench_units_bought = investment / price_at_buy
                
                # Add this qty to all subsequent days
                bench_qty_held.loc[mask] += bench_units_bought
            except:
                pass # skip if date issues
        
        # Now Calculate Value of Bench Portfolio
        bench_series = bench_qty_held * bench_prices
    
    # 5. Format for JSON
    # Resample to reduce data size if huge? No, daily is fine for 1 year.
    
    result = {
        "dates": all_days.strftime('%Y-%m-%d').tolist(),
        "portfolio": portfolio_series.fillna(0).tolist(),
        "invested": invested_series.fillna(0).tolist(),
        "benchmark": bench_series.fillna(0).tolist(),
        "benchmark_symbol": benchmark_ticker
    }
    
    return jsonify(result)

if __name__ == '__main__':
    print("Starting Portfolio Backend (backend4.py) on port 5002...")
    app.run(debug=True, port=5002)
