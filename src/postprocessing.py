# src/postprocessing.py
import pandas as pd
import json
from pathlib import Path
from dateparser import parse as date_parse
import re

IN = Path('data/final_triage.csv')
OUT = Path('data/final_triage_enriched.csv')

HIGH_VALUE_THRESHOLD = 1000.0
CANCEL_WORDS = ['cancelar', 'cancelamento', 'rescisão', 'cancelei', 'quero cancelar']
PROCON_WORDS = ['procon', 'advogado', 'ação judicial', 'processo', 'vou procurar os meus direitos']

def determine_priority(row):
    sentiment = str(row.get('sentiment') or 'neutro').lower()
    text = str(row.get('text') or '').lower()
    try:
        entities = json.loads(row.get('entities', '[]'))
    except:
        entities = []
    value = None
    date = None
    for e in entities:
        lbl = e.get('label', '').upper()
        if lbl in ('MONEY', 'VALOR'):
            txt = str(e.get('text', ''))
            txt = txt.replace('R$', '').replace('.', '').replace(',', '.')
            try:
                value = float(re.sub(r'[^\d\.]', '', txt))
            except:
                pass
        if lbl in ('DATE', 'TIME'):
            val = e.get('text')
            if val:
                d = date_parse(str(val))
                if d:
                    date = d.isoformat()
    if any(w in text for w in CANCEL_WORDS):
        return 'alta', 'possivel_cancelamento'
    if any(w in text for w in PROCON_WORDS):
        return 'alta', 'legal_risk'
    if sentiment == 'negativo':
        if value and value >= HIGH_VALUE_THRESHOLD:
            return 'alta', 'cliente_risco_valor'
        if date:
            return 'alta', 'prazo_proximo'
        return 'media', 'insatisfeito'
    if sentiment == 'neutro':
        return 'baixa', ''
    return 'baixa', ''

def main(in_path=IN, out_path=OUT):
    if not Path(in_path).exists():
        print(f"[WARNING] Arquivo de entrada {in_path} não encontrado.")
        return

    df = pd.read_csv(in_path)
    
    if df.empty:
        print(f"[INFO] O dataframe de entrada {in_path} está vazio. Nenhuma pós-processamento necessário.")
        df.to_csv(out_path, index=False)
        return

    # Garante que as colunas necessárias existam
    if 'text' not in df.columns:
        df['text'] = ''
    if 'sentiment' not in df.columns:
        df['sentiment'] = 'neutro'
    
    df['text'] = df['text'].fillna('')
    df['sentiment'] = df['sentiment'].fillna('neutro')
    if 'entities' not in df.columns:
        df['entities'] = '[]'
    else:
        df['entities'] = df['entities'].fillna('[]')
    priorities = []
    alerts = []
    explain = []
    for _, row in df.iterrows():
        p, alert = determine_priority(row)
        priorities.append(p)
        alerts.append(alert)
        txt = str(row.get('text') or '')
        explain.append(txt.split('.')[0][:120])
    df['priority'] = priorities
    df['alert'] = alerts
    df['explain_snippet'] = explain
    df.to_csv(out_path, index=False)
    print('enriched saved to', out_path)

if __name__ == '__main__':
    main()






    