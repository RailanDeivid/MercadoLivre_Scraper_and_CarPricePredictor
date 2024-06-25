# MercadoLivre Scraper and Car Price Predictor

## Descrição

Este projeto realiza web scraping de anúncios de veículos no Mercado Livre e prevê valores de vendas usando um modelo de machine learning. O projeto é dividido em várias partes, incluindo coleta de dados, transformação de dados, análise exploratória e predição de preços.

## Estrutura do Projeto



## Instalação

1. Clone o repositório:
    ```sh
    git clone https://github.com/seu-usuario/MercadoLivre_Scraper_and_CarPricePredictor.git
    cd MercadoLivre_Scraper_and_CarPricePredictor
    ```

2. Crie e ative o ambiente virtual:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

### Scraping de Dados

1. Navegue até a pasta `src/scraper`:
    ```sh
    cd src/scraper
    ```

2. Execute o scraper:
    ```sh
    scrapy crawl mercadolivre
    ```

### Transformação de Dados

1. Navegue até a pasta `src/data_transformation`:
    ```sh
    cd src/data_transformation
    ```

2. Execute o script de transformação de dados:
    ```sh
    python main.py
    ```

### Análise Exploratória

1. Abra o notebook `EDA.ipynb` em um ambiente Jupyter para explorar os dados.

### Predição de Preços

1. Navegue até a pasta `src/models` e adicione seu código de modelagem.

### Aplicação Streamlit

1. Navegue até a pasta `streamlit_app` e execute a aplicação:
    ```sh
    streamlit run app.py
