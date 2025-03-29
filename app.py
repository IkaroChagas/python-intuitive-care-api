from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app) 
CSV_FILE = 'Relatorio_cadop.csv'

df = pd.read_csv(CSV_FILE, sep=';', encoding='utf-8', dtype=str)


df.columns = df.columns.str.strip()  

df.rename(columns={
    "Registro ANS": "Registro_ANS",
    "Razao Social": "Razao_Social",
    "Nome Fantasia": "Nome_Fantasia",
    "Cargo Representante": "Cargo_Representante",
    "Regiao de Comercializacao": "Regiao_de_Comercializacao",
    "Data Registro ANS": "Data_Registro_ANS"
}, inplace=True)


df.fillna('', inplace=True)

CAMPOS_PESQUISA = ["Registro_ANS", "Nome_Fantasia", "Modalidade"]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()

    if not query:
        return jsonify({'error': 'Parâmetro "q" é obrigatório.'}), 400

    mask = df[CAMPOS_PESQUISA].apply(lambda row: row.astype(str).str.lower().str.contains(query, na=False)).any(axis=1)

    resultados = df[mask].to_dict(orient='records')

    return jsonify(resultados[:50])  
    
app.run(debug=True)