from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import numpy as np
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- EXPANDED ASSET LIST (More Comprehensive B3) ---
ASSETS = {
    'cripto': [
        "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "TRX-USD", "DOT-USD",
        "MATIC-USD", "LTC-USD", "SHIB-USD", "BCH-USD", "LINK-USD", "ATOM-USD", "XLM-USD", "UNI7083-USD", "HBAR-USD", "OKB-USD",
        "FIL-USD", "LDO-USD", "APT21794-USD", "ARB11841-USD", "NEAR-USD", "VET-USD", "QNT-USD", "MKR-USD", "AAVE-USD", "ALGO-USD",
        "GRT6719-USD", "STX4847-USD", "SAND-USD", "EOS-USD", "MANA-USD", "THETA-USD", "FTM-USD", "BIT-USD", "EGLD-USD",
        "FLOW-USD", "XTZ-USD", "APE3-USD", "IMX10603-USD", "AXS-USD", "RPL-USD", "KCS-USD", "CRV-USD", "NEO-USD", "KLAY-USD"
    ],
    'br': [
        # Setor Financeiro / Bancos / Seguros
        "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "BBDC3.SA", "ITSA4.SA", "BPAC11.SA", "SANB11.SA", "BBSE3.SA", "CXSE3.SA", "PSSA3.SA",
        "IRBR3.SA", "SULA11.SA", "B3SA3.SA", "CIEL3.SA", "BRSR6.SA", "ABCB4.SA", "BPAN4.SA",
        # Petróleo, Gás e Petroquímica
        "PETR4.SA", "PETR3.SA", "PRIO3.SA", "VBBR3.SA", "UGPA3.SA", "CSAN3.SA", "RRRP3.SA", "RECV3.SA", "ENAT3.SA", "BRKM5.SA",
        # Mineração e Siderurgia
        "VALE3.SA", "GGBR4.SA", "GOAU4.SA", "CSNA3.SA", "USIM5.SA", "CMIN3.SA", "FESA4.SA", "SEER3.SA",
        # Varejo e Consumo
        "MGLU3.SA", "LREN3.SA", "ARZZ3.SA", "SOMA3.SA", "ALPA4.SA", "AMER3.SA", "BHIA3.SA", "PETZ3.SA", "NTCO3.SA", "CRFB3.SA",
        "ASAI3.SA", "PCAR3.SA", "GMAT3.SA", "SMTO3.SA", "ABEV3.SA", "MDIA3.SA", "CAML3.SA", "BEEF3.SA", "MRFG3.SA", "JBSS3.SA",
        "BRFS3.SA", "SLCE3.SA", "AGRO3.SA",
        # Elétricas e Saneamento
        "ELET3.SA", "ELET6.SA", "EQTL3.SA", "CPLE6.SA", "CPFE3.SA", "CMIG4.SA", "EGIE3.SA", "ENEV3.SA", "TRPL4.SA", "TAEE11.SA",
        "TAEE3.SA", "TAEE4.SA", "NEOE3.SA", "ENBR3.SA", "ALUP11.SA", "AESB3.SA", "SBSP3.SA", "SAPR11.SA", "SAPR4.SA", "SAPR3.SA",
        "CSMG3.SA", "AMBP3.SA",
        # Saúde
        "HAPV3.SA", "RDOR3.SA", "RADL3.SA", "FLRY3.SA", "HYPE3.SA", "PNVL3.SA", "QUAL3.SA", "MATD3.SA",
        # Construção e Imobiliário
        "CYRE3.SA", "EZTC3.SA", "MRVE3.SA", "TEND3.SA", "JHSF3.SA", "MULTI3.SA", "IGTI11.SA", "LOGG3.SA", "ALOS3.SA",
        # Tecnologia e Telecom
        "WEGE3.SA", "TOTS3.SA", "LWSA3.SA", "CASH3.SA", "POSI3.SA", "INTB3.SA", "VIVT3.SA", "TIMS3.SA", "OIBR3.SA",
        # Transportes e Bens de Capital
        "EMBR3.SA", "AZUL4.SA", "GOLL4.SA", "CVCB3.SA", "CCRO3.SA", "ECOR3.SA", "RAIL3.SA", "RENT3.SA", "MOVI3.SA", "VAMO3.SA",
        "SIMH3.SA", "KEPL3.SA", "WEGE3.SA", "TASA4.SA", "POMO4.SA", "RAPT4.SA", "MYPK3.SA", "LEVE3.SA",
        # Outros
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

# Mapping names for new additions + existing
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

# Base names (same as before, collapsed for brevity in this tool call, but full in file)
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

    # US
    "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", "AMZN": "Amazon", "NVDA": "Nvidia",
    "TSLA": "Tesla", "META": "Meta", "BRK-B": "Berkshire", "LLY": "Eli Lilly", "V": "Visa",
    "UNH": "UnitedHealth", "XOM": "Exxon Mobil", "JNJ": "Johnson & Johnson", "JPM": "JPMorgan", "PG": "P&G",
    "MA": "Mastercard", "AVGO": "Broadcom", "HD": "Home Depot", "CVX": "Chevron", "MRK": "Merck",
    "ABBV": "AbbVie", "PEP": "PepsiCo", "KO": "Coca-Cola", "COST": "Costco", "ADBE": "Adobe",
    "WMT": "Walmart", "MCD": "McDonald's", "CSCO": "Cisco", "CRM": "Salesforce", "PFE": "Pfizer",
    "TMO": "Thermo Fisher", "BAC": "Bank of America", "NFLX": "Netflix", "ABT": "Abbott", "DHR": "Danaher",
    "CMCSA": "Comcast", "AMD": "AMD", "NKE": "Nike", "DIS": "Disney", "INTC": "Intel", "VZ": "Verizon",
    "WFC": "Wells Fargo", "TXN": "Texas Instruments", "PM": "Philip Morris", "NEE": "NextEra Energy", "LIN": "Linde",
    "RTX": "Raytheon", "BMY": "Bristol-Myers Squibb", "HON": "Honeywell", "QCOM": "Qualcomm", "UPS": "UPS",
    "UNP": "Union Pacific", "AMGN": "Amgen", "LOW": "Lowe's", "SPGI": "S&P Global", "CAT": "Caterpillar",
    "BA": "Boeing", "IBM": "IBM", "INTU": "Intuit", "GE": "General Electric", "ISRG": "Intuitive Surgical",
    "AMAT": "Applied Materials", "NOW": "ServiceNow", "SBUX": "Starbucks", "GS": "Goldman Sachs", "DE": "Deere & Co",
    "EL": "Estée Lauder", "PLD": "Prologis", "MS": "Morgan Stanley", "BLK": "BlackRock", "BKNG": "Booking Holdings",
    "MDLZ": "Mondelez", "TJX": "TJX Companies", "ADP": "ADP", "T": "AT&T", "GILD": "Gilead", "ADI": "Analog Devices",
    "MMC": "Marsh & McLennan", "C": "Citigroup", "CVS": "CVS Health", "LMT": "Lockheed Martin", "MDXG": "MiMedx",
    "UBER": "Uber", "PYPL": "PayPal", "MO": "Altria", "REGN": "Regeneron", "ZTS": "Zoetis", "VRTX": "Vertex",
    "FI": "Fiserv", "SO": "Southern Co", "EOG": "EOG Resources", "PGR": "Progressive", "CI": "Cigna",
    "BDX": "Becton Dickinson", "SLB": "Schlumberger", "SNOW": "Snowflake", "PLTR": "Palantir", "COIN": "Coinbase",
    "RBLX": "Roblox", "U": "Unity",

    # Indices
    "^BVSP": "Ibovespa", "^GSPC": "S&P 500", "^IXIC": "Nasdaq", "^DJI": "Dow Jones",
    "^FTSE": "FTSE 100", "^GDAXI": "DAX", "^FCHI": "CAC 40", "^N225": "Nikkei 225",
    "^HSI": "Hang Seng", "^RUT": "Russell 2000", "^VIX": "VIX", "^STOXX50E": "Euro Stoxx 50",
    "GC=F": "Ouro", "CL=F": "Petróleo WTI", "SI=F": "Prata", "HG=F": "Cobre",
    "NG=F": "Gás Natural", "KC=F": "Café", "CC=F": "Cacau", "SB=F": "Açúcar",
    "CT=F": "Algodão", "ZW=F": "Trigo", "ZC=F": "Milho", "ZS=F": "Soja",
    "EURUSD=X": "EUR/USD", "GBPUSD=X": "GBP/USD", "JPY=X": "USD/JPY", "BRL=X": "USD/BRL",
    "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD", "USDCHF=X": "USD/CHF", "EURGBP=X": "EUR/GBP",
    
    # BR Previously known
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
    "ENEV3.SA": "Eneva", "EGIE3.SA": "Engie Brasil", "CPFE3.SA": "CPFL Energia", "BBDC3.SA": "Bradesco ON",
    "KLBN11.SA": "Klabin", "BRFS3.SA": "BRF", "CRFB3.SA": "Carrefour Brasil", "SANB11.SA": "Santander Brasil",
    "GOAU4.SA": "Metalúrgica Gerdau", "MULT3.SA": "Multiplan", "FLRY3.SA": "Fleury", "PCAR3.SA": "Pão de Açúcar",
    "AZUL4.SA": "Azul", "CMIN3.SA": "CSN Mineração", "NTCO3.SA": "Natura", "USIM5.SA": "Usiminas",
    "MRVE3.SA": "MRV", "GOLL4.SA": "Gol", "IGTI11.SA": "Iguatemi", "CYRE3.SA": "Cyrela",
    "SOMA3.SA": "Grupo Soma", "RRRP3.SA": "3R Petroleum", "ALPA4.SA": "Alpargatas", "CVCB3.SA": "CVC",
    "DXCO3.SA": "Dexco", "EZTC3.SA": "EZTEC", "CASH3.SA": "Méliuz", "PETZ3.SA": "Petz",
    "LWSA3.SA": "Locaweb", "POSI3.SA": "Positivo"
}

# Merge Dictionaries
TICKER_NAMES = {**TICKER_NAMES_BASE, **TICKER_NAMES_UPDATE_BR}

@app.route('/api/assets', methods=['GET'])
def list_assets():
    """Returns a flat list of potential assets for autocomplete"""
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

@app.route('/api/portfolio/correlation', methods=['POST'])
def analyze_portfolio_correlation():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        tickers = data.get('tickers', [])
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not tickers or not start_date or not end_date:
            return jsonify({"error": "Missing required fields: tickers, start_date, end_date"}), 400

        # Clean tickers
        tickers = [t.strip().upper() for t in tickers if t.strip()]

        if len(tickers) < 2:
            return jsonify({"error": "At least 2 tickers are required for correlation analysis"}), 400

        logger.info(f"Analyzing tickers: {tickers} from {start_date} to {end_date}")

        # Download data
        df = yf.download(tickers, start=start_date, end=end_date, progress=False, auto_adjust=True, threads=True)
        
        close_data = pd.DataFrame()
        
        # Handling yfinance structure variations
        if isinstance(df.columns, pd.MultiIndex):
            try:
                if 'Close' in df.columns.get_level_values(0):
                     close_data = df['Close']
                else:
                    close_data = df.xs('Close', level=1, axis=1)
            except:
                 try:
                    close_data = df.xs('Close', level=1, axis=1)
                 except:
                     pass
        else:
            pass

        if close_data.empty and 'Close' in df:
             close_data = df['Close']
        
        if close_data.empty:
             close_data = df
             if close_data.empty:
                return jsonify({"error": "Could not download data for the provided tickers"}), 404

        # Clean
        close_data.dropna(axis=1, how='all', inplace=True)
        close_data.dropna(inplace=True)

        if close_data.shape[1] < 2:
             return jsonify({"error": "Insufficient valid data for at least 2 assets after cleaning."}), 400
        
        # Calculate Returns for Correlation
        returns = close_data.pct_change().dropna()

        if returns.empty:
             return jsonify({"error": "Insufficient returns data."}), 400

        # Correlation Matrix
        correlation_matrix = returns.corr()

        # Calculate Cumulative Performance (Normalized to 0%)
        # (Price / Initial Price) - 1
        normalized_performance = (close_data / close_data.iloc[0]) - 1
        normalized_performance = normalized_performance * 100
        
        # Prepare Performance Data for Frontend
        performance_dates = normalized_performance.index.strftime('%Y-%m-%d').tolist()
        performance_traces = {}
        for col in normalized_performance.columns:
            # Replace NaN with None for JSON compliance
            performance_traces[col] = normalized_performance[col].where(pd.notnull(normalized_performance[col]), None).tolist()

        # Summary Analysis
        mask = np.ones(correlation_matrix.shape, dtype=bool)
        np.fill_diagonal(mask, 0)
        off_diagonal = correlation_matrix.values[mask]
        
        avg_correlation = np.mean(np.abs(off_diagonal)) if len(off_diagonal) > 0 else 0

        # Elaborate Summary Analysis (Pearson/Wooldridge Style)
        avg_corr_val = avg_correlation
        summary_text = ""

        if avg_corr_val >= 0.6:
            strength = "POSITIVA DE FORÇA ALTA"
            explanation = "os retornos dos seus ativos tendem a responder de forma muito semelhante aos choques de mercado."
            risk_context = "isso sinaliza uma BAIXA diversificação. Segundo a Teoria Moderna de Portfólios, sua carteira está exposta a um alto risco sistêmico, pois os ativos não oferecem proteção mútua eficiente contra volatilidade."
        elif avg_corr_val >= 0.3:
            strength = "POSITIVA DE FORÇA MODERADA"
            explanation = "os retornos tendem a se mover na mesma direção, mas a relação não é rígida."
            risk_context = "segundo princípios estatísticos, isso sugere que há alguma diversificação de risco (pois não é próximo de 1), mas não é a diversificação ideal. O risco total da carteira é menor que a soma dos riscos individuais, mas ainda é afetado por fatores macroeconômicos comuns."
        else:
            strength = "BAIXA OU DESCORRELACIONADA"
            explanation = "os ativos comportam-se de maneira independente ou até inversa."
            risk_context = "esta é uma configuração favorável para mitigar o risco não-sistêmico (idiossincrático). Seus ativos oferecem proteção real uns aos outros, estabilizando a curva de capital da carteira no longo prazo."

        summary_text = (
            f"O Coeficiente de Correlação de Pearson Médio de {avg_corr_val:.2f} desta carteira indica uma correlação {strength}. "
            f"Isso significa que {explanation} Na gestão de carteiras, {risk_context}"
        )

        z_values = correlation_matrix.values.tolist()
        z_values = [[round(val, 4) for val in row] for row in z_values]
        valid_tickers = correlation_matrix.columns.tolist()

        result = {
            "tickers": valid_tickers,
            "z": z_values,
            "avg_correlation": round(avg_correlation, 4),
            "summary": summary_text,
            "performance": {
                "dates": performance_dates,
                "traces": performance_traces
            }
        }

        result = {
            "tickers": valid_tickers,
            "z": z_values,
            "avg_correlation": round(avg_correlation, 4),
            "summary": summary_text,
            "performance": {
                "dates": performance_dates,
                "traces": performance_traces
            }
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in correlation analysis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/benchmark', methods=['POST'])
def analyze_benchmark_comparison():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        tickers = data.get('tickers', [])
        weights = data.get('weights', []) # List of floats, e.g. [0.5, 0.5]
        benchmark_ticker = data.get('benchmark', '^BVSP')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not tickers or not start_date or not end_date:
            return jsonify({"error": "Missing required fields: tickers, start_date, end_date"}), 400

        # Clean tickers
        tickers = [t.strip().upper() for t in tickers if t.strip()]
        
        # Validate Weights
        if not weights:
            # Default to equal weights if not provided
            w = 1.0 / len(tickers)
            weights = [w] * len(tickers)
        
        if len(tickers) != len(weights):
             return jsonify({"error": f"Number of weights ({len(weights)}) must match number of assets ({len(tickers)})"}), 400

        # Create a dictionary for easy weight lookup
        asset_weights = dict(zip(tickers, weights))

        # 2. Download Data (Portfolio + Benchmark)
        unique_tickers = list(set(tickers + [benchmark_ticker]))
        
        logger.info(f"Downloading for Benchmark Analysis: {unique_tickers}")
        
        df = yf.download(unique_tickers, start=start_date, end=end_date, progress=False, auto_adjust=True, threads=True)
        
        # Extract Close/Adj Close
        price_data = pd.DataFrame()
        
        # Handle MultiIndex if multiple tickers
        if len(unique_tickers) > 1:
            if isinstance(df.columns, pd.MultiIndex):
                # Try to get Close or Adj Close
                try:
                    price_data = df['Close']
                except KeyError:
                    try:
                        price_data = df['Adj Close']
                    except KeyError:
                        price_data = df # Fallback
            else:
                 # Should not happen with yfinance usually if multiple tickers, but fallback
                 price_data = df
        else:
            # Single ticker case handling
             if isinstance(df.columns, pd.MultiIndex):
                  price_data = df.xs('Close', level=1, axis=1) # Simplified
             else:
                  price_data = df['Close'] if 'Close' in df else df

        # Ensure we have data
        if price_data.empty:
             return jsonify({"error": "Could not download data."}), 404

        # Filter for our specific assets
        available_assets = [t for t in tickers if t in price_data.columns]
        
        if not available_assets:
             return jsonify({"error": "No valid data found for portfolio assets."}), 400
             
        # Recalculate weights for available assets if some are missing?
        # Creating a safe weight list
        safe_weights = []
        final_assets = []
        for asset in available_assets:
            if asset in asset_weights:
                final_assets.append(asset)
                safe_weights.append(asset_weights[asset])
        
        # Normalize weights to sum to 1 if some assets were dropped
        total_weight = sum(safe_weights)
        if total_weight > 0:
            safe_weights = [w / total_weight for w in safe_weights]
        
        # Check Benchmark
        if benchmark_ticker not in price_data.columns:
            # Try single download if it failed in bulk? (Unlikely but possible)
            return jsonify({"error": f"Benchmark {benchmark_ticker} not found in data."}), 400

        # 3. Clean NaN
        cleaned_data = price_data[final_assets + [benchmark_ticker]].dropna()

        if cleaned_data.empty:
             return jsonify({"error": "Insufficient overlapping data for assets and benchmark."}), 400

        # 4. Calculate Cumulative Returns
        # Start at 0%
        daily_returns = cleaned_data.pct_change().dropna()
        cumulative_returns = (1 + daily_returns).cumprod() - 1
        
        # 5. Create "My Portfolio" Curve
        # Multiply returns by weights
        # We need to apply weights to the DAILY returns first for accuracy in rebalancing simulation?
        # Quote from prompt: "Multiplica o retorno de cada ativo pelo seu peso e soma para criar a linha 'Minha Carteira'"
        # Prompt uses: weighted_returns = (carteira_retornos * pesos).sum(axis=1) on CUMULATIVE returns.
        # Note: Summing cumulative returns weighted is an approximation (fixed mix assumption vs buy-and-hold),
        # but requested by user prompt pattern. Let's follow the prompt's math logic for consistency.
        
        # Prompt logic:
        # retornos_acumulados = (1 + retornos_diarios).cumprod() - 1
        # carteira_retornos = retornos_acumulados[ativos_carteira_presentes]
        # weighted_returns = (carteira_retornos * pesos).sum(axis=1)
        
        # Applying prompt logic:
        portfolio_cumulative_component = cumulative_returns[final_assets]
        # Align weights for matrix multiplication
        weights_array = np.array(safe_weights)
        
        # weighted sum
        my_portfolio_curve = (portfolio_cumulative_component * weights_array).sum(axis=1)
        
        # Benchmark curve
        benchmark_curve = cumulative_returns[benchmark_ticker]
        
        # Prepare for JSON
        dates = my_portfolio_curve.index.strftime('%Y-%m-%d').tolist()
        
        # Multiply by 100 for percentage
        portfolio_values = (my_portfolio_curve * 100).tolist()
        benchmark_values = (benchmark_curve * 100).tolist()
        
        # Also return individual assets for detail if needed? User chart only showed Portfolio vs Benchmark.
        # Let's stick to the requested plot requirements.

        result = {
            "dates": dates,
            "portfolio": portfolio_values,
            "benchmark": benchmark_values,
            "benchmark_symbol": benchmark_ticker
        }

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in benchmark analysis: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Portfolio Analysis Backend on port 5001...")
    # debug=True allows auto reload
    app.run(debug=True, port=5001)
