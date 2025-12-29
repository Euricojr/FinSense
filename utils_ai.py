import re
import datetime

def parse_natural_language(text):
    text = text.lower()
    today = datetime.date.today().isoformat()
    
    # Defaults
    t_type = 'expense'
    category = 'Outros'
    amount = 0.0
    description = text.strip()

    # 1. Determine Type
    if any(w in text for w in ['recebi', 'ganhei', 'salario', 'deposito', 'venda', 'lucro']):
        t_type = 'income'
        category = 'Receitas' # Default income category

    # 2. Extract Amount (simple regex for currency)
    # Matches 100, 100.50, 100,00, R$100
    amount_match = re.search(r'[\d]+[.,]?\d*', text)
    if amount_match:
        val_str = amount_match.group(0).replace(',', '.')
        try:
            amount = float(val_str)
        except:
            pass
    
    # 3. Guess Category (for expenses)
    if t_type == 'expense':
        keywords = {
            'Alimentação': ['comida', 'lanche', 'pizza', 'restaurante', 'mercado', 'açougue', 'ifood', 'burguer'],
            'Transporte': ['uber', 'taxi', 'gasolina', 'posto', 'onibus', 'metro', 'passagem'],
            'Lazer': ['cinema', 'filme', 'jogo', 'steam', 'netflix', 'spotify', 'bar', 'show'],
            'Moradia': ['aluguel', 'luz', 'agua', 'internet', 'condominio', 'casa', 'energia'],
            'Saúde': ['farmacia', 'remedio', 'medico', 'dentista', 'convenio']
        }
        for cat, keys in keywords.items():
            if any(k in text for k in keys):
                category = cat
                break
    else:
        # Income categories
        if 'salario' in text: category = 'Salário'
        elif 'investimento' in text: category = 'Investimentos'

    return {
        'description': description.capitalize(),
        'amount': amount,
        'date': today,
        'category': category,
        'type': t_type
    }
