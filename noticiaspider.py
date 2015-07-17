import scrapy

class NoticiaSpider(scrapy.Spider):
  name = 'noticiaspider'
  start_urls = ['http://sportv.globo.com/site']

  def parse(self, response):
    for url in response.css('a.gui-feed-title::attr("href")').extract():      
      yield scrapy.Request(url, self.parse_noticia)

  def parse_noticia(self, response):
    for article_html in response.css('#glb-materia'):       
      article = {
        'url': response.url,
        'title': article_html.css('[itemprop=headline]::text').extract_first(),
        'description': article_html.css('[itemprop=description]::text').extract_first(),
        'author': article_html.css('[itemprop=author]::text').extract_first(),
        'body': article_html.css('[itemprop=articleBody] p::text').extract(),
        'imgs': self.get_images(article_html)
      }
      yield article

  def get_images(self, article_html):    
    images = []    
    for img in article_html.css('img'):
      images.append({
        'src': img.xpath('@src').extract_first(), 
        'title': img.xpath('@title').extract_first()
        })
    return images
