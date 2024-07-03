import warnings
warnings.filterwarnings("ignore")
import joblib as joblib
import os
import streamlit as st
import pandas as pd
import numpy as np


# Carregando o modelo pré-treinado
model_path = os.path.abspath(os.path.join(os.getcwd(), 'previsao_precos_veiculos_20240702.joblib'))
# model = joblib.load('previsao_precos_veiculos_20240702.joblib')
# model = model['model']
model_path = 'previsao_precos_veiculos_20240702.joblib'
model = joblib.load(model_path)
model = model['model']

# Carregando dados adicionais
data_path = os.path.abspath(os.path.join(os.getcwd(), 'data_tratados.parquet'))
df_dados_adicionais = pd.read_parquet(data_path)

# Extraindo as opções únicas para o estado (UF)
ufs = df_dados_adicionais['uf'].unique().tolist()

# Definindo a interface do usuário
st.title("Previsão de Preço de Carros")
st.markdown("Insira as características do carro:")

# Entradas do usuário na ordem especificada
ano = st.number_input('Ano', min_value=1994, max_value=2025, step=1, format="%d")
motor = df_dados_adicionais['motor'].unique().tolist()
# Filtrando dados com base no ano selecionado
df_filtro_por_ano = df_dados_adicionais[df_dados_adicionais['ano'] == ano]
marcas = df_filtro_por_ano['marca'].unique().tolist()

# Selecionando a marca
if marcas:
    marca_selecionada = st.selectbox('Marca', marcas)
    # Filtrando dados com base na marca selecionada
    df_filtro_por_marca = df_filtro_por_ano[df_filtro_por_ano['marca'] == marca_selecionada]
    modelos = df_filtro_por_marca['modelo'].unique().tolist()
else:
    marca_selecionada = st.selectbox('Marca', [])
    modelos = []

# Selecionando o modelo
modelo = st.selectbox('Modelo', modelos)
# Selecionando UF 
UF = st.selectbox('Estado (UF)', ufs)
# Selecionando o motor
motor = st.selectbox('motor', motor)

KM = st.number_input('Quilometragem (KM)', min_value=0.0, format="%f")
vidros_eletricos = st.selectbox('Vidros Elétricos', [0, 1], format_func=lambda x: 'Sim' if x == 1 else 'Não')
ar_condicionado = st.selectbox('Ar Condicionado', [0, 1], format_func=lambda x: 'Sim' if x == 1 else 'Não')
combustivel = st.selectbox('Combustível', ['alcool', 'diesel', 'eletrico', 'flex', 'gasolina', 'hibrido', 'outros'])
direcao = st.selectbox('Tipo de Direção', ['Assistida', 'Elétrica', 'Hidráulica', 'Mecânica'])
transmissao = st.selectbox('Tipo de Transmissão', ['Automatica', 'Manual', 'Semiautomatica'])



# criando um dataframe com as entradas do usuário
input_data = pd.DataFrame({
    'vidros_eletricos': [vidros_eletricos],
    'ar_condicionado': [ar_condicionado],
    'KM_LOG': [np.log(KM + 1)],
    'ano': [ano],
    'alcool': [1 if combustivel == 'alcool' else 0],
    'diesel': [1 if combustivel == 'diesel' else 0],
    'eletrico': [1 if combustivel == 'eletrico' else 0],
    'flex': [1 if combustivel == 'flex' else 0],
    'gasolina': [1 if combustivel == 'gasolina' else 0],
    'hibrido': [1 if combustivel == 'hibrido' else 0],
    'outros': [1 if combustivel == 'outros' else 0],
    'Assistida': [1 if direcao == 'Assistida' else 0],
    'Elétrica': [1 if direcao == 'Elétrica' else 0],
    'Hidráulica': [1 if direcao == 'Hidráulica' else 0],
    'Mecânica': [1 if direcao == 'Mecânica' else 0],
    'Automatica': [1 if transmissao == 'Automatica' else 0],
    'Manual': [1 if transmissao == 'Manual' else 0],
    'Semiautomatica': [1 if transmissao == 'Semiautomatica' else 0]
})



def formatar_moeda_brl(valor):
    valor_formatado = f"R$ {valor:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
    return valor_formatado
# tratamentos da previsão
if st.button('Prever Preço'):
    try:
        prediction = model.predict(input_data)
        predicted_price = np.exp(prediction[0])  # Transformação inversa para obter o preço previsto
        formatted_price = formatted_price = formatar_moeda_brl(predicted_price)
        st.success(f"O preço previsto de venda é:   {formatted_price}")
    except Exception as e:
        st.error(f"Erro ao fazer a previsão: {e}")

