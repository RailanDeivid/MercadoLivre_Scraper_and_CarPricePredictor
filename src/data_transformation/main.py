import pandas as pd
import sqlite3
from datetime import datetime
import os

# Setando caminhos dos dados
json_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'data', 'data.json'))
db_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'data', 'ML_db.db'))
# Carregando dados
df = pd.read_json(json_path, lines=True)
# Criando conexão com o banco de dados SQLite
conn = sqlite3.connect(db_path)
# Salvando dados no banco
df.to_sql('mercadolivre_veiculos', conn, if_exists='replace', index=False)
conn.close()

