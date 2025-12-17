from flask import Flask, jsonify, request, send_from_directory, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import yfinance as yf
import pandas as pd
import numpy as np
import time
import os
import logging
from bcb import sgs

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Set template_folder to base dir to render root HTMLs
app = Flask(__name__, template_folder=BASE_DIR, static_folder='static')
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security & DB Config
app.secret_key = 'super_secret_key_change_this_in_production' # Needed for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect here if not logged in

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

# --- USER MODEL ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False) # YYYY-MM-DD
    qty = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---

@app.route('/')
def home():
    # Pass current_user to template
    return render_template('index2.html', user=current_user)

@app.route('/portfolio')
@login_required
def portfolio():
    return render_template('portfolio.html', user=current_user)

@app.route('/analise')
@login_required
def analise():
    return render_template('analise_carteiras.html', user=current_user)

# --- AUTH ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        action = request.form.get('action') # 'login' or 'register'

        if action == 'register':
            if User.query.filter_by(username=username).first():
                flash('Usuário já existe!', 'error')
            else:
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('home'))

        else: # Login
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Credenciais inválidas.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({"message": "Logged out"})
    return redirect(url_for('login'))

@app.route('/api/me')
def api_me():
    if current_user.is_authenticated:
        return jsonify({"authenticated": True, "username": current_user.username})
    return jsonify({"authenticated": False}), 401

@app.route('/api/transactions', methods=['GET', 'POST', 'DELETE'])
@login_required
def manage_transactions():
    if request.method == 'GET':
        txs = Transaction.query.filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': t.id,
            'ticker': t.ticker,
            'date': t.date,
            'qty': t.qty,
            'price': t.price,
            'total': t.qty * t.price
        } for t in txs])

    if request.method == 'POST':
        data = request.json
        try:
            new_tx = Transaction(
                user_id=current_user.id,
                ticker=data['ticker'],
                date=data['date'],
                qty=float(data['qty']),
                price=float(data['price'])
            )
            db.session.add(new_tx)
            db.session.commit()
            return jsonify({'message': 'Transaction added', 'id': new_tx.id})
        except Exception as e:
             return jsonify({'error': str(e)}), 400
             
@app.route('/api/transactions/<int:id>', methods=['DELETE'])
@login_required
def delete_transaction(id):
    tx = Transaction.query.filter_by(id=id, user_id=current_user.id).first()
    if tx:
        db.session.delete(tx)
        db.session.commit()
        return jsonify({'message': 'Deleted'})
    return jsonify({'error': 'Not found'}), 404

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
            "macd": df['MACD_Line'].tolist(),
            "signal": df['Signal_Line'].tolist(),
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

@app.route('/api/calculate_portfolio', methods=['POST'])
def calculate_portfolio_endpoint():
    try:
        transactions = request.get_json().get('transactions', [])
        if not transactions:
            return jsonify({"error": "No transactions provided"}), 400

        # 1. Fetch current prices
        tickers = list(set([t['ticker'] for t in transactions]))
        
        # Download 1d data just to get latest price
        # Using period='5d' to be safe against holidays/weekends
        data = yf.download(tickers, period="5d", progress=False, threads=True)
        
        # Extract latest close prices
        latest_prices = {}
        if len(tickers) == 1:
            ticker = tickers[0]
            try:
                # Handle MultiIndex (Price, Ticker) or Single Index
                if isinstance(data, pd.DataFrame):
                    # Check for 'Close'
                    if 'Close' in data.columns:
                        close_data = data['Close']
                        # If MultiIndex (Time, Ticker) -> accessing 'Close' returns DataFrame if many tickers, 
                        # or Series if one. But if just one ticker request, it might be just Series.
                        
                        last_val = close_data.iloc[-1]
                        
                        # If Series (value per ticker? or just value?)
                        if isinstance(last_val, pd.Series):
                            # It has ticker index
                            # Try to find the ticker in the series
                            if ticker in last_val.index:
                                latest_prices[ticker] = float(last_val[ticker])
                            else:
                                # Just take the first value if it's the only one
                                latest_prices[ticker] = float(last_val.iloc[0])
                        else:
                            # Scalar
                            latest_prices[ticker] = float(last_val)
                    else:
                         # Fallback to column name directly
                        if ticker in data.columns:
                            latest_prices[ticker] = float(data[ticker].dropna().iloc[-1])
                        else:
                            latest_prices[ticker] = 0.0
                else:
                    latest_prices[ticker] = 0.0
                
                
            except Exception as e:
                logger.error(f"Error extracting price for {ticker}: {e}")
                latest_prices[ticker] = 0.0
        else:
            # multiple tickers
            closes = data['Close'] if 'Close' in data else data
            for ticker in tickers:
                try:
                    price = 0.0
                    if isinstance(closes, pd.DataFrame) and ticker in closes.columns:
                         price = float(closes[ticker].dropna().iloc[-1])
                    elif isinstance(closes, pd.Series):
                         # Should not happen for multiple tickers unless yf quirk
                         price = float(closes.iloc[-1])
                    
                    latest_prices[ticker] = price
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
        
        # Calculate Allocation by Category
        category_totals = {}
        total_val_check = 0.0
        
        # Define ASSETS map locally or use existing global if present (assuming ASSETS global exists in app.py)
        # If not, use simple heuristics or empty map. 
        # Using the one from app.py line 21-62 viewed earlier.
        
        for h in holdings:
            sym = h['ticker']
            cat = 'Outros'
            # Find category in global ASSETS
            for c, lst in ASSETS.items():
                if sym in lst:
                    cat = c
                    break
            
            friendly_cat = {
                'br': 'Ações Brasil',
                'us': 'Ações EUA',
                'cripto': 'Cripto',
                'indices': 'Índices'
            }.get(cat, 'Outros')
            
            h['category'] = friendly_cat 
            
            if friendly_cat not in category_totals:
                category_totals[friendly_cat] = 0.0
            category_totals[friendly_cat] += h['current_value']
            total_val_check += h['current_value']
            
        allocation_by_category = []
        if total_val_check > 0:
            for cat, val in category_totals.items():
                allocation_by_category.append({
                    "category": cat,
                    "value": val,
                    "percentage": (val / total_val_check) * 100
                })
        
        allocation_by_category.sort(key=lambda x: x['percentage'], reverse=True)

        profit_loss = current_value - total_invested
        profit_loss_pct = (profit_loss / total_invested * 100) if total_invested > 0 else 0.0

        return jsonify({
            "total_invested": total_invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_pct": profit_loss_pct,
            "holdings": holdings,
            "allocation_by_category": allocation_by_category,
            "prices": latest_prices
        })

    except Exception as e:
        logger.error(f"Error calculating portfolio: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/portfolio/evolution', methods=['POST'])
def portfolio_evolution():
    try:
        data = request.get_json()
        transactions = data.get('tickers', []) 
        benchmark = data.get('benchmark', '^BVSP')
        filter_type = data.get('filter', 'all') # 'all', 'br', 'us', 'cripto'

        if not transactions:
            return jsonify({"error": "No transactions"}), 400
            
        # Filter Logic
        filtered_tx = []
        if filter_type == 'all':
            filtered_tx = transactions
        else:
            target_list = ASSETS.get(filter_type, [])
            filtered_tx = [t for t in transactions if t['ticker'] in target_list]
        
        # If filter results in empty list (e.g. asking for 'cripto' but user has none)
        if not filtered_tx and transactions: 
            return jsonify({
                "dates": [], 
                "portfolio": [], 
                "invested": [],
                "benchmark": [], 
                "benchmark_symbol": benchmark
            })

        return calculate_portfolio_history(filtered_tx, benchmark)
    except Exception as e:
        logger.error(f"Error in evolution: {e}")
        return jsonify({"error": str(e)}), 500

def calculate_portfolio_history(transactions, benchmark_ticker='^BVSP'):
    df_tx = pd.DataFrame(transactions)
    df_tx['date'] = pd.to_datetime(df_tx['date'])
    df_tx['qty'] = df_tx['qty'].astype(float)
    df_tx['price'] = df_tx['price'].astype(float)
    df_tx['flow'] = df_tx['qty'] * df_tx['price'] # Positive = Buy (Inflow of Asset Value, Outflow of Cash)
    
    start_date = df_tx['date'].min()
    end_date = pd.Timestamp.now()
    
    unique_tickers = df_tx['ticker'].unique().tolist()
    is_cdi = (benchmark_ticker == 'CDI')
    download_tickers = unique_tickers + ([benchmark_ticker] if not is_cdi else [])
    
    try:
        data = yf.download(download_tickers, start=start_date, end=end_date, progress=False, threads=True)
        market_data = data['Close'] if 'Close' in data else data
    except Exception as e:
        return jsonify({"error": "Failed to download market data"}), 500
    
    # Handle single ticker
    if len(download_tickers) == 1:
        if isinstance(market_data, pd.Series):
             market_data = pd.DataFrame({download_tickers[0]: market_data})
        if isinstance(market_data, pd.DataFrame) and download_tickers[0] not in market_data.columns:
             market_data.columns = [download_tickers[0]]
             
    market_data = market_data.fillna(method='ffill').fillna(method='bfill')
    all_days = market_data.index
    
    # 1. Calculate Daily Total Value (Assets owned at end of day * Price)
    # We need to reconstruct the portfolio composition for every day
    daily_value = pd.Series(0.0, index=all_days)
    daily_flows = pd.Series(0.0, index=all_days)

    # Pre-calculate flows per day
    grouped_flows = df_tx.groupby(df_tx['date'].dt.normalize())['flow'].sum()
    daily_flows = daily_flows.add(grouped_flows, fill_value=0)
    
    # Calculate holdings over time
    # This is expensive in a loop, optimize by iterating over ordered transactions
    # Create a DataFrame of holdings changes: columns=ticker, index=date
    holdings_change = pd.DataFrame(0.0, index=all_days, columns=unique_tickers)
    
    for _, tx in df_tx.iterrows():
        d = tx['date'].normalize()
        if d in holdings_change.index:
            holdings_change.loc[d, tx['ticker']] += tx['qty']
    
    # Cumulative sum to get current units held on each day
    daily_units = holdings_change.cumsum()
    
    # Compute Daily Portfolio Value
    for t in unique_tickers:
        if t in market_data.columns:
            # Units held * Price on that day
            daily_val_asset = daily_units[t] * market_data[t]
            daily_value += daily_val_asset.fillna(0)

    # 2. Calculate Daily Returns (Quota System)
    # Formula: Ret_t = (EndVal_t - Flow_t) / EndVal_{t-1} - 1
    
    quota_series = [1.0] # Start at 1.0 (100%)
    dates = [all_days[0]]
    
    # We need to iterate carefully.
    # On Day 0: Value is just Flow. Return is 0.
    
    stats_df = pd.DataFrame({
        'end_value': daily_value,
        'flow': daily_flows
    })
    
    # Shift end_value to get prev_value
    # But strictly: Ret = (V_t - Flow_t) / V_{t-1}
    
    daily_pct_change = pd.Series(0.0, index=all_days)
    
    prev_val = 0.0
    
    # Efficient Iteration
    # First day with value:
    first_idx = np.argmax(stats_df['end_value'] > 0)
    
    # Initialize calculated series
    quota = pd.Series(0.0, index=all_days)
    
    # This loop calculates the quota based on daily variations, effectively stripping out inflows
    # Logic: If I have 100, deposit 100, I have 200. Return is 0%.
    # If I have 100, it grows to 110, deposit 90, I have 200. Return is 10%.
    
    current_quota = 100.0
    quota.iloc[:first_idx] = 100.0
    
    prev_total = 0.0
    
    for i in range(len(stats_df)):
        if i < first_idx: 
            prev_total = stats_df['end_value'].iloc[i]
            continue
            
        today_total = stats_df['end_value'].iloc[i]
        today_flow = stats_df['flow'].iloc[i]
        
        if prev_total > 0:
            # Adjust today's total by removing the cash that entered today
            adjusted_today = today_total - today_flow
            daily_ret = (adjusted_today / prev_total) - 1
        else:
            daily_ret = 0.0
            
        current_quota = current_quota * (1 + daily_ret)
        quota.iloc[i] = current_quota
        prev_total = today_total

    # 3. Benchmark Normalization (to % starting at 0)
    bench_series = pd.Series(0.0, index=all_days)
    
    if is_cdi:
        try:
             start_str = start_date.strftime('%Y-%m-%d')
             cdi_daily = sgs.get({'CDI': 12}, start=start_str)
             if cdi_daily is not None:
                 cdi_daily['factor'] = 1 + (cdi_daily['CDI'] / 100)
                 cdi_aligned = cdi_daily['factor'].reindex(all_days, fill_value=1.0)
                 # Cumulative Product
                 bench_cum = cdi_aligned.cumprod()
                 # Normalize to start at 100
                 bench_series = (bench_cum / bench_cum.iloc[0]) * 100
        except: pass
    elif benchmark_ticker in market_data.columns:
        b_prices = market_data[benchmark_ticker]
        valid_start = b_prices.first_valid_index()
        if valid_start:
             base_price = b_prices.loc[valid_start]
             bench_series = (b_prices / base_price) * 100
        else:
             bench_series = b_prices # Fallback

    # Shift to Percentage Change (0 basis) for Chart
    # i.e., 100 -> 0%, 110 -> 10%
    quota_final = quota - 100
    bench_final = bench_series - 100
    
    return jsonify({
        "dates": all_days.strftime('%Y-%m-%d').tolist(),
        "portfolio": quota_final.fillna(0).tolist(),
        "invested": [], # No longer plotted
        "benchmark": bench_final.fillna(0).tolist(),
        "benchmark_symbol": benchmark_ticker
    })



@app.route('/api/portfolio/correlation', methods=['POST'])
def portfolio_correlation():
    try:
        data = request.get_json()
        tickers = data.get('tickers', [])
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not tickers or len(tickers) < 2:
            return jsonify({"error": "Need at least 2 tickers"}), 400
            
        logger.info(f"Correlation Request: {tickers} from {start_date} to {end_date}")
        
        # Download Data
        prices = yf.download(tickers, start=start_date, end=end_date, progress=False, threads=True)['Close']
        prices = prices.fillna(method='ffill').fillna(method='bfill')
        
        # Calculate Correlation (Based on Price as requested)
        corr_matrix = prices.corr()
        
        # Calculate Average Absolute Correlation (upper triangle)
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        # Using ABSOLUTE correlation as requested ("Média de Correlação Absoluta")
        avg_corr = np.abs(corr_matrix.where(mask).stack()).mean()
        
        if pd.isna(avg_corr): avg_corr = 0.0
        
        # Determine Class and Text based on the screenshot provided
        classification = ""
        meaning = ""
        
        if avg_corr > 0.7:
            classification = "ALTA"
            meaning = "Isso indica que seus ativos tendem a se mover na mesma direção, o que reduz os benefícios da diversificação. Em momentos de crise, é provável que a maioria sofra quedas simultâneas, aumentando o risco sistêmico da carteira."
        elif avg_corr > 0.4:
            classification = "MODERADA"
            meaning = "Isso indica que existe algum nível de diversificação, mas os ativos ainda podem sofrer influências de mercado similares. É um ponto de equilíbrio, mas vale considerar adicionar ativos descorrelacionados para maior proteção."
        else:
            classification = "BAIXA OU DESCORRELACIONADA"
            meaning = "Isso significa que os ativos comportam-se de maneira independente ou até inversa. Na gestão de carteiras, esta é uma configuração favorável para mitigar o risco não-sistêmico (idiossincrático). Seus ativos oferecem proteção real uns aos outros, estabilizando a curva de capital da carteira no longo prazo."

        summary = (
            f"O Coeficiente de Correlação de Pearson Médio de {avg_corr:.2f} desta carteira indica uma correlação {classification}. "
            f"{meaning}"
        )

        return jsonify({
            "correlation_matrix": corr_matrix.reset_index().to_dict(orient='records'),
            "avg_correlation": float(avg_corr),
            "summary": summary
        })

    except Exception as e:
        logger.error(f"Error in correlation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Create tables if not exists
    print("Starting Unified FinSense App with Auth on Port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
