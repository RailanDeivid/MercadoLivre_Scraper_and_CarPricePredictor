<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge"/>
</p>

# Scrape dos Dados Anuncios de Veiculos do MercadoLivre e Predição dos valores de Vendas.

## Descrição

Este projeto realiza web scraping de anúncios de veículos no Mercado Livre e prevê valores de vendas usando um modelo de machine learning. O projeto é dividido em várias partes, incluindo coleta de dados, transformação de dados, análise exploratória e predição de preços.

<h4 align="center"> 
    :construction:  Projeto em construção  :construction:
</h4>

O projeto ainda está em desenvolvimento e as próximas atualizações serão voltadas nas seguintes tarefas:

- [x] Scrape dos dados
- [x] Tratamento e armazenamento em um banco de dados
- [x] EDA
- [ ] Modelagem
- [ ] Deploy Streamlit

## Principais Tecnologias Utilizadas

- ``Python 3.12.1``
- ``SQLite3``
- ``Streamlit``
- ``Pandas``
- ``Numpy``
- ``Matplotlib``
- ``Seaborn``
- ``Regex``
- ``Scrapy``
- ``scikit-learn``

## 📁 Acesso aos do  arquivos projeto
Você pode acessar os arquivos do projeto:

Scrape dos dados: [Mercadolivre.py](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/scraper/spiders/mercadolivre.py)

Transformações dos dados: [main.py](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/data_transformation/main.py)

Analises dos dados: [EDA.ipynb](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/analysis/EDA.ipynb)

Dados: [data](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/tree/main/data)

## Scraper dos dados
Foi utilizada a biblioteca ``Scrapy`` para obter os dados dos anuncios de veiculos do Mercado Livre. Os registros são obtidos pelo script [Mercadolivre.py](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/scraper/spiders/mercadolivre.py) Onde é feito a raspagem, entrando e cada um dos 49 anuncios por pagina e pegando as informações de cado anuncio, anuncios por marca e estado.
Um trecho do código utilizado:
```
class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    
    lista_marcas = ['volkswagen', 'chevrolet', 'ford', 'hyundai', 'fiat', 'renault', 'honda', 'jeep', 'nissan', 'audi', 'bmh', 
                    'chery', 'citroen', 'dodge', 'jac', 'jaguar', 'kia', 'lexus', 'mini', 'mercedes-benz', 'land-rover', 'lifan',
                    'peugeot', 'subaru', 'suzuki', 'toyota', 'volvo']
    
    listas_UF = ['ceara', 'distrito-federal', 'goias', 'mato-grosso', 'minas-gerais', 'parana', 'para', 'pernambuco', 
                 'rio-de-janeiro', 'sao-paulo', 'santa-catarina', 'rio-grande-do-sul', 'tocantins', 'alagoa', 'amazonas', 'goias', 
                 'bahia','maranhao', 'mato-grosso-do-sul', 'piaui', 'paraiba', 'rio-grande-do-norte', 'sergipe', 'espirito-santo']

    start_urls = []

    def __init__(self):
        for marca in self.lista_marcas:
            for uf in self.listas_UF:
                url = f"https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/{marca}-em-{uf}/"
                self.start_urls.append(url)
    
    page_count = 1
    max_pages = 42

    def parse(self, response):
        anuncios = response.css('div.ui-search-result__content')
        url_parts = response.url.split('/')
        marca = url_parts[-2].split('-')[0]
        uf = '-'.join(url_parts[-2].split('-')[2:])
        # marca = response.url.split('/')[-2].split('-')[0]
        # uf = response.url.split('/')[-2].split('-')[2]

        for anuncio in anuncios:
            data_coleta = datetime.now().date()
            link = anuncio.css('a.ui-search-link::attr(href)').get()
            local = anuncio.css('span.ui-search-item__group__element.ui-search-item__location::text').get()
            if link:
                yield response.follow(link, self.parse_anuncio, meta={'link': link, 'local': local, 'data_coleta': data_coleta, 'marca': marca, 'uf': uf})

        if self.page_count <= self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
```

Os dados são salvos em um arquivos  [jsonl](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/tree/main/data)

## Tratamento dos dados
Os tratamentos dos dados foram feitos no arquivo [main.py](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/data_transformation/main.py) onde é feito todos os tratamentos possiveis e o armazenamento em um banco de dados [SQLite](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/tree/main/data). 

## Análise Exploratória de Dados (EDA)

<h3 align="center"> 
    ⚠️ Apenas um trecho das analises feitas  ⚠️
</h3>

As seguintes bibliotecas foram importadas para a análise:

- ``warnings`` para ignorar avisos
- ``pandas`` e ``numpy`` para manipulação de dados
- ``matplotlib`` e ``seaborn`` para visualização de dados
- ``sqlite3`` para conexão com o banco de dados
- ``os`` para manipulação de caminhos de arquivos

### Analise Descritivas
Criação de histogramas para as variáveis numéricas: valor, ano e KM, para observar a distribuição dos dados.

![image](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/assets/78448568/6909b6dc-166a-467b-9018-da7d8b6b6f65)
Os gráficos representam a distribuição de frequência de três variáveis numéricas: valor, ano e KM.

1. Distribuição de valor:

O histograma mostra que a distribuição do valor é assimétrica à direita, com uma maior concentração de dados nos valores mais baixos.

2. Distribuição de ano:

O histograma do ano mostra uma distribuição aproximadamente normal, com uma maior concentração de dados em torno do ano 2000.
A curva KDE confirma a normalidade, com uma curva simétrica em torno do ano 2000.
O ano mínimo é de aproximadamente 1970, enquanto o ano máximo é de aproximadamente 2020.

3. Distribuição de KM:

O histograma do KM mostra uma distribuição assimétrica à direita, com uma maior concentração de dados nos valores mais baixos.
Também podemos confirmar com a curva KDE a assimetria.
O KM mínimo é de aproximadamente 0, enquanto o KM máximo é de aproximadamente 1200.

* Analisando distribuição dos dados usando um BOXPLOT
  
![image](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/assets/78448568/c0dbabf9-4228-4e9a-9475-18f11aef7376)
Os gráficos representam Análise de Distribuição dos Dados com Boxplots: valor, ano e KM.

1. valor:

    O boxplot mostra uma mediana próxima a 0, com outliers que se estendem de aproximadamente 1 a pouco mais de 3. 
    Os valores nesse boxplot estão na faixa dos milhões. Portanto, a mediana próxima de 0 na verdade representa um valor de 500.000, e os outliers que vão até 4 representam valores na casa dos 4 milhões. 


2. ano

    O boxplot mostra uma distribuição com a mediana em torno do ano 2000. A ausência de outliers sugere que não há anos atípicos ou extremos no conjunto de dados com pouca variação entre eles.

3. KM:

    O boxplot tem uma mediana ligeiramente abaixo de 0,5. Os outliers são visíveis em ambos os lados, indicando a presença de valores de quilometragem muito baixos e muito altos em comparação com a maioria dos dados.

* Analisando a distribuição e relação de todas as variáveis.
  
![image](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/assets/78448568/a10a1082-52b9-4b6c-b346-d9868e5021c3)

O que os gráficos de distribuição de todas as variáveis nos mostram?

* Valor vs. Ano: Este gráfico ilustra a relação entre o preço dos carros e o ano de fabricação. Em geral, observa-se que carros mais novos tendem a ter preços mais altos.

* Ano vs. Quilometragem (KM): Este gráfico mostra a relação entre o ano de fabricação e a quilometragem dos carros. Carros mais novos normalmente apresentam menor quilometragem, pois foram utilizados por menos tempo.

* Valor vs. Quilometragem (KM): Este gráfico apresenta como o preço dos carros se relaciona com a quilometragem. Carros com menos quilômetros rodados tendem a ser mais caros, indicando que a menor utilização aumenta o valor de mercado.

Todo o processo de análise dos dados estão no notebook [EDA.ipynb](https://github.com/RailanDeivid/MercadoLivre_Scraper_and_CarPricePredictor/blob/main/src/analysis/EDA.ipynb)
