import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/veiculos"]
    page_count = 1
    max_pages = 100

    def parse(self, response):
        self.log(f'Parsing page {self.page_count}')
        anuncios = response.css('div.ui-search-result__content')

        for anuncio in anuncios:
            link = anuncio.css('a.ui-search-link::attr(href)').get()
            local = anuncio.css('span.ui-search-item__group__element.ui-search-item__location::text').get()
            if link:
                yield response.follow(link, self.parse_anuncio, meta={'link': link, 'local': local})

        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_anuncio(self, response):
        link = response.meta['link']
        local = response.meta['local']
        modelo = response.css('h1.ui-pdp-title::text').get()
        valor = response.css('span.andes-money-amount__fraction::text').get()

        detalhes = response.css('table.andes-table')

        ano = detalhes.xpath('.//th[div[contains(text(), "Ano")]]/following-sibling::td/span/text()').get() 
        km = detalhes.xpath('.//th[div[contains(text(), "Quilômetros")]]/following-sibling::td/span/text()').get()[:-4] 
        tipo_combustivel = detalhes.xpath('.//th[div[contains(text(), "Tipo de combustível")]]/following-sibling::td/span/text()').get() 
        transmissao = detalhes.xpath('.//th[div[contains(text(), "Transmissão")]]/following-sibling::td/span/text()').get() 
        motor = detalhes.xpath('.//th[div[contains(text(), "Motor")]]/following-sibling::td/span/text()').get() 
        ar_condicionado = detalhes.xpath('.//th[div[contains(text(), "Ar-condicionado")]]/following-sibling::td/span/text()').get() 
        cor = detalhes.xpath('.//th[div[contains(text(), "Cor")]]/following-sibling::td/span/text()').get() 
        Portas = detalhes.xpath('.//th[div[contains(text(), "Portas")]]/following-sibling::td/span/text()').get() 
        direcao = detalhes.xpath('.//th[div[contains(text(), "Direção")]]/following-sibling::td/span/text()').get() 
        vidros_eletricos  = detalhes.xpath('.//th[div[contains(text(), "Vidros elétricos")]]/following-sibling::td/span/text()').get() 

        yield {
            'modelo': modelo,
            'valor': valor,
            'ano': ano,
            'KM': km,
            'tipo_combustivel': tipo_combustivel,
            'transmissao': transmissao,
            'motor': motor,
            'ar_condicionado': ar_condicionado,
            'cor': cor,
            'Portas': Portas,
            'direcao': direcao,
            'vidros_eletricos': vidros_eletricos,
            'local': local,
            'link': link
        }
