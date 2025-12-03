from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/api/dados')
def pegar_dados():
    try:
        # Recebe o ticker, period, ma_period e interval do Frontend
        # Se não vier nada na URL, usa valores padrão
        ticker = request.args.get('ticker', 'BTC-USD')
        period = request.args.get('period', '1mo')
        interval = request.args.get('interval', '1h')
        ma_period = int(request.args.get('ma_period', 14))
        
        print(f"Buscando dados para: {ticker}, Periodo: {period}, Intervalo: {interval}, MA: {ma_period}") 

        # Baixa os dados
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        
        # Tratamento para tabela vazia ou ticker inválido
        if df.empty:
            return jsonify({"erro": "Ticker não encontrado ou sem dados"}), 404

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Calcula a Média Móvel Dinâmica
        ma_col_name = f'MA{ma_period}'
        df[ma_col_name] = df['Close'].rolling(window=ma_period).mean()
        
        # Remove NaNs resultantes do cálculo da MA
        df.dropna(inplace=True)

        # Monta o JSON
        dados_json = {
            "symbol": ticker, 
            "datas": df.index.strftime('%Y-%m-%d %H:%M').tolist(),
            "open": df['Open'].tolist(),
            "high": df['High'].tolist(),
            "low": df['Low'].tolist(),
            "close": df['Close'].tolist(),
            "ma": df[ma_col_name].tolist(),
            "ma_label": f"MA {ma_period}",
            "preco_atual": f"{df['Close'].iloc[-1]:.2f}"
        }
        
        return jsonify(dados_json)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"erro": str(e)}), 500

@app.route('/api/heatmap')
def heatmap_data():
    try:
        # Pega o tipo de ativo da URL (default: cripto)
        tipo = request.args.get('type', 'cripto')
        
        tickers = []
        
        if tipo == 'cripto':
            tickers = [
                "BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", 
                "TRX-USD", "DOT-USD", "LINK-USD", "MATIC-USD", "LTC-USD", "BCH-USD", "UNI-USD", "ATOM-USD",
                "XLM-USD", "ETC-USD", "FIL-USD", "HBAR-USD", "APT-USD", "NEAR-USD", "VET-USD", "QNT-USD",
                "MKR-USD", "AAVE-USD", "ALGO-USD", "GRT-USD", "FTM-USD", "SAND-USD", "EOS-USD", "MANA-USD"
            ]
        elif tipo == 'br':
            tickers = [
                "VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBDC4.SA", "BBAS3.SA", "PETR3.SA", "ABEV3.SA", "WEGE3.SA",
                "RENT3.SA", "BPAC11.SA", "SUZB3.SA", "ITSA4.SA", "HAPV3.SA", "RDOR3.SA", "JBSS3.SA", "B3SA3.SA",
                "GGBR4.SA", "RADL3.SA", "PRIO3.SA", "RAIL3.SA", "VBBR3.SA", "ELET3.SA", "UGPA3.SA", "CSAN3.SA",
                "BBSE3.SA", "LREN3.SA", "VIVT3.SA", "EQTL3.SA", "SBSP3.SA", "CMIG4.SA", "CPLE6.SA", "EMBR3.SA",
                "TIMS3.SA", "CCRO3.SA", "ASAI3.SA", "HYPE3.SA", "TOTS3.SA", "CSNA3.SA", "MGLU3.SA", "VIIA3.SA"
            ]
        elif tipo == 'us':
            tickers = [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK-B", "LLY", "V",
                "UNH", "XOM", "JNJ", "JPM", "PG", "MA", "AVGO", "HD", "CVX", "MRK",
                "ABBV", "PEP", "KO", "COST", "ADBE", "WMT", "MCD", "CSCO", "CRM", "PFE",
                "TMO", "BAC", "NFLX", "ABT", "DHR", "CMCSA", "AMD", "NKE", "DIS", "INTC"
            ]
        elif tipo == 'indices':
            tickers = [
                "^BVSP", "^GSPC", "^IXIC", "^DJI", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI", 
                "GC=F", "CL=F", "SI=F", "HG=F", "EURUSD=X", "GBPUSD=X", "JPY=X", "BRL=X"
            ]
        
        dados_heatmap = []
        
        # Otimização: Baixar tudo de uma vez
        if tickers:
            string_tickers = " ".join(tickers)
            # period='5d' para garantir que pegamos dias úteis anteriores (feriados/fds)
            data = yf.download(string_tickers, period="5d", group_by='ticker', progress=False)
            
            for ticker in tickers:
                try:
                    if ticker not in data:
                         continue
                    
                    df_ticker = data[ticker]
                    # Remove NaNs
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
                        "label": f"{ticker}<br>{change_percent:.2f}%"
                    })
                except Exception as e:
                    # print(f"Erro ao processar {ticker}: {e}")
                    continue
                
        return jsonify(dados_heatmap)

    except Exception as e:
        print(f"Erro no heatmap: {e}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)