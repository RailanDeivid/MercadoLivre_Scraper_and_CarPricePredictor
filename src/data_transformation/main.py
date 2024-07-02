import pandas as pd
import sqlite3
from datetime import datetime
import os
import numpy as np

# Setando caminhos dos dados
json_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'data', 'data.jsonl'))
db_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'data', 'ML_db.db'))
# Carregando dados
df = pd.read_json(json_path, lines=True)

# ------------ Tratamento dos dados ----------------------------------------- #

# ----- Tratando os dados nulos
# Dismenbrando o modelo da marca na coluna 'modelo', pois já tenho uma coluna com a marca
df['modelo'] = df['modelo'].str.split(n=1).str[1]
# Preencher os valores ausentes na coluna 'ano', 'direcao', 'portas', 'ar_condicionado', 'motor', 'transmissao', 'tipo_combustivel'  com base no mapeamento dos modelos
df['ano'] = df.groupby('modelo')['ano'].transform(lambda x: x.ffill().bfill())
df['direcao'] = df.groupby('modelo')['direcao'].transform(lambda x: x.ffill().bfill())
df['portas'] = df.groupby('modelo')['portas'].transform(lambda x: x.ffill().bfill())
df['ar_condicionado'] = df.groupby('modelo')['ar_condicionado'].transform(lambda x: x.ffill().bfill())
df['vidros_eletricos'] = df.groupby('modelo')['ar_condicionado'].transform(lambda x: x.ffill().bfill())
df['transmissao'] = df.groupby('modelo')['transmissao'].transform(lambda x: x.ffill().bfill())
df['tipo_combustivel'] = df.groupby('modelo')['tipo_combustivel'].transform(lambda x: x.ffill().bfill())
df['motor'] = df.groupby('modelo')['motor'].transform(lambda x: x.ffill().bfill())

# DADOS NULOS POR COLUNAS
""" marca                  0
    modelo                 2 # REMOVER
    valor                  0
    ano                    3 # REMOVER
    KM                   498 # USAR A MÉDIA DO MSM modelo 
    tipo_combustivel       3 # REMOVER
    transmissao          106 # REMOVER
    motor                735 # REMOVER
    ar_condicionado     1814 # SETAR COMO "SIM"
    cor                 1971 # REMOVER
    portas                 3 # REMOVER
    direcao              318 # REMOVER
    vidros_eletricos    5072 # SETAR COMO "NÃO" 
    local                  0
    uf                    47 # USAR DADOS DA COLUNA LOCAL 
    link                   0
    data_coleta            0
"""
# ---------- Removendo dados nulos das colunas: modelo, ano, tipo_combustivel, transmissao, motor, portas, direcao e cor

# Selecionando as colunas que precisam ter dados nulos removidos
colunas_remover_nulos = ['modelo', 'ano', 'tipo_combustivel', 'transmissao', 'motor', 'portas', 'direcao', 'cor']
# Removendo linhas com valores nulos apenas nas colunas especificadas
df = df.dropna(subset=colunas_remover_nulos)

# ----------------------------------------------------------------- coluna: KM
# Converter a coluna KM para numérica
df['KM'] = pd.to_numeric(df['KM'], errors='coerce')
# Calcular a média dos valores de KM para cada modelo
modelo_km_media = df.groupby('modelo')['KM'].mean()
# Preenche os valores ausentes na coluna KM com a média correspondente ao modelo
df['KM'] = df.apply(lambda row: modelo_km_media[row['modelo']] if pd.isnull(row['KM']) else row['KM'], axis=1)
df = df.dropna(subset=['KM'])

# modelo_ano = df.dropna(subset=['ano']).drop_duplicates('modelo').set_index('modelo')['ano'].to_dict()
# # preenchendo os valores ausentes na coluna 'ano' com base no mapeamento dos modelos e seus anos
# modelos = df['modelo'].unique()
# for modelo in modelos:
#     if modelo not in modelo_ano:
#         modelo_ano[modelo] = np.nan

# ----------------------------------------------------------------- coluna: UF
# Função para extrair a UF do campo 'local'
def extrair_uf(local):
    if '-' in local:
        uf_part = local.split('-')[-1].strip()
        if uf_part:
            return uf_part
    return local  # Retorna o valor completo de 'local' se não houver dados após '-'

# Preenche os valores vazios da coluna 'uf' com base na coluna 'local'
df['uf'] = df.apply(lambda row: extrair_uf(row['local']) if row['uf'] == '' else row['uf'], axis=1)
# Ajustando nomes 
lista_map_uf = {
    'ceara': 'CE',
    'distrito-federal': 'DF',
    'goias': 'GO',
    'mato-grosso': 'MT',
    'minas-gerais': 'MG',
    'parana': 'PR',
    'para': 'PA',
    'pernambuco': 'PE',
    'rio-de-janeiro': 'RJ',
    'sao-paulo': 'SP',
    'São Paulo': 'SP',
    'santa-catarina': 'SC',
    'rio-grande-do-sul': 'RS',
    'tocantins': 'TO',
    'alagoas': 'AL',
    'amazonas': 'AM',
    'bahia': 'BA',
    'Bahia': 'BA',
    'maranhao': 'MA',
    'mato-grosso-do-sul': 'MS',
    'piaui': 'PI',
    'paraiba': 'PB',
    'rio-grande-do-norte': 'RN',
    'sergipe': 'SE',
    'espirito-santo': 'ES',
    'em-ceara': 'CE',
    'em-distrito-federal': 'DF',
    'em-goias': 'GO',
    'em-minas-gerais': 'MG',
    'em-parana': 'PR',
    'em-para': 'PA',
    'em-pernambuco': 'PE',
    'em-rio-de-janeiro': 'RJ',
    'em-sao-paulo': 'SP',
    'em-santa-catarina': 'SC',
    'em-rio-grande-do-sul': 'RS',
    'em-bahia': 'BA',
    'em-mato-grosso-do-sul': 'MS',
    'em-sergipe': 'SE',
    'em-espirito-santo': 'ES',
    'em-mato-grosso': 'MT',
    'em-tocantins': 'TO',
    'em-paraiba': 'PB',
    'em-rio-grande-do-norte': 'RN'
}

df['uf'] = df['uf'].map(lista_map_uf)

# ----------------------------------------------------------------- coluna: tipo_combustivel
# Ajustando nomes 
lista_map_combustivel = {
    'Gasolina e álcool': 'flex',
    'Gasolina': 'gasolina',
    'Gasolina-Álcool e gás natural': 'flex',
    'Diesel': 'diesel',
    'Flex': 'flex',
    'Álcool e gás natural': 'flex',
    'Híbrido': 'hibrido',
    'Tetra-combustible': 'outros',
    'Elétrico': 'eletrico',
    'Gasolina e gás natural': 'flex',
    'Álcool': 'alcool',
    'Gasolina e elétrico': 'hibrido',
    'Híbrido/Gasolina': 'hibrido',
    'FLEX': 'flex',
}
df['tipo_combustivel'] = df['tipo_combustivel'].map(lista_map_combustivel)

# ----------------------------------------------------------------- coluna: motor
# Usando expressão regular para extrair apenas os números
df['motor'] = df['motor'].str.extract(r'(\d+\.\d+|\d+)')[0]
df = df.loc[df['motor'] != '0.0']
df = df.dropna(subset=['motor'])
# ----------------------------------------------------------------- coluna: ar_condicionado
# Substituindo dados null pra 'Sim'
df['ar_condicionado'] = df['ar_condicionado'].fillna('Sim')

# ----------------------------------------------------------------- coluna: vidros_eletricos
# Substituindo dados null pra 'Sim'
df['vidros_eletricos'] = df['vidros_eletricos'].fillna('Não')

# ----------------------------------------------------------------- coluna: transmissao
# Ajustando nomes 
lista_map_transmissao = {
    'Manual': 'Manual',
    'Automática': 'Automatica',
    'Automática sequencial': 'Automatica',
    'Semiautomática': 'Semiautomatica',
    'AUTOMÁTICO': 'Automatica',
    'Automatizado': 'Automatica',
    'Automático': 'Automatica',

}
df['transmissao'] = df['transmissao'].map(lista_map_transmissao)


# --------------------------------------------------------------- Tratamento de tipos de colunas
df['data_coleta'] = pd.to_datetime(df['data_coleta'])
df['valor'] = df['valor'].str.replace('.', '').astype('float64')
df['ano'] = df['ano'].astype('float64')
df['KM'] = df['KM'].replace('', np.nan).astype('float64')
df['motor'] = df['motor'].astype('float64')
df['portas'] = df['portas'].astype('float64')

# ----------------------------------------------------------------- SALVANDO DADOS EM UM BANCO SQLITE
#  Criando conexão com o banco de dados SQLite
conn = sqlite3.connect(db_path)
# Salvando dados
df.to_sql('mercadolivre_veiculos', conn, if_exists='replace', index=False)
conn.close()

