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

if __name__ == '__main__':
    app.run(debug=True, port=5000)