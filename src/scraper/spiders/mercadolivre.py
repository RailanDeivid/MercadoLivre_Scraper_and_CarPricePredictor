import scrapy
from datetime import datetime


# start_urls = ["https://lista.mercadolivre.com.br/veiculos"]

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

    def parse_anuncio(self, response):
        link = response.meta['link']
        local = response.meta['local']
        data_coleta = response.meta['data_coleta']
        marca = response.meta['marca']
        uf = response.meta['uf']

        modelo = response.css('h1.ui-pdp-title::text').get()
        valor = response.css('span.andes-money-amount__fraction::text').get()

        detalhes = response.css('table.andes-table')

        ano = detalhes.xpath('.//th[div[contains(text(), "Ano")]]/following-sibling::td/span/text()').get() 
        km = detalhes.xpath('.//th[div[contains(text(), "Quilômetros")]]/following-sibling::td/span/text()').get()[:-4] if detalhes.xpath('.//th[div[contains(text(), "Quilômetros")]]/following-sibling::td/span/text()').get() else None
        tipo_combustivel = detalhes.xpath('.//th[div[contains(text(), "Tipo de combustível")]]/following-sibling::td/span/text()').get() 
        transmissao = detalhes.xpath('.//th[div[contains(text(), "Transmissão")]]/following-sibling::td/span/text()').get() 
        motor = detalhes.xpath('.//th[div[contains(text(), "Motor")]]/following-sibling::td/span/text()').get() 
        ar_condicionado = detalhes.xpath('.//th[div[contains(text(), "Ar-condicionado")]]/following-sibling::td/span/text()').get() 
        cor = detalhes.xpath('.//th[div[contains(text(), "Cor")]]/following-sibling::td/span/text()').get() 
        portas = detalhes.xpath('.//th[div[contains(text(), "Portas")]]/following-sibling::td/span/text()').get() 
        direcao = detalhes.xpath('.//th[div[contains(text(), "Direção")]]/following-sibling::td/span/text()').get() 
        vidros_eletricos = detalhes.xpath('.//th[div[contains(text(), "Vidros elétricos")]]/following-sibling::td/span/text()').get() 

        yield {
            'marca': marca,
            'modelo': modelo,
            'valor': valor,
            'ano': ano,
            'KM': km,
            'tipo_combustivel': tipo_combustivel,
            'transmissao': transmissao,
            'motor': motor,
            'ar_condicionado': ar_condicionado,
            'cor': cor,
            'portas': portas,
            'direcao': direcao,
            'vidros_eletricos': vidros_eletricos,
            'local': local,
            'uf': uf,
            'link': link,
            'data_coleta': data_coleta
        }
