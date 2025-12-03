from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app) # Permite que seu HTML acesse esse Python sem bloqueios de segurança

@app.route('/api/dados')
def pegar_dados():
    try:
        ticker = "BTC-USD"
        # Baixa os dados
        df = yf.download(ticker, period="10d", interval="1h", progress=False)
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Calcula a Média Móvel (Backend fazendo o trabalho pesado)
        df['MA14'] = df['Close'].rolling(window=14).mean()

        # Limpa dados vazios (NaN) gerados pela média móvel
        df.dropna(inplace=True)

        # Prepara o JSON para o Frontend
        # O Plotly.js gosta de listas separadas (Array de datas, Array de fechametno, etc)
        dados_json = {
            "datas": df.index.strftime('%Y-%m-%d %H:%M').tolist(),
            "open": df['Open'].tolist(),
            "high": df['High'].tolist(),
            "low": df['Low'].tolist(),
            "close": df['Close'].tolist(),
            "ma14": df['MA14'].tolist(),
            "preco_atual": f"{df['Close'].iloc[-1]:.2f}"
        }
        
        return jsonify(dados_json)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(debug=True, port=5000)