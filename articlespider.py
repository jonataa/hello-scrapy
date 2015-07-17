from scrapy import Spider, Request
from items import Article, Image

class ArticleSpider(Spider):
  name = 'articlespider'
  start_urls = ['http://sportv.globo.com/site']

  def parse(self, response):
    for url in response.css('a.gui-feed-title::attr("href")').extract():      
      yield Request(url, self.parse_article)

  def parse_article(self, response):
    for article_html in response.css('#glb-materia'):
      article = Article()
      article['url'] = response.url
      article['title'] = article_html.css('[itemprop=headline]::text').extract_first()
      article['description'] = article_html.css('[itemprop=description]::text').extract_first()
      article['author'] = article_html.css('[itemprop=author]::text').extract_first()
      article['body'] = article_html.css('[itemprop=articleBody] p::text').extract()
      article['imgs'] = self.get_images(article_html)
      yield article

  def get_images(self, article_html):    
    images = []    
    for img in article_html.css('.foto img'):
      image = Image()
      image['src'] = img.xpath('@src').extract_first(), 
      image['title'] =img.xpath('@title').extract_first()      
      images.append(image)
    return images