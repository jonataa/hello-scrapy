from scrapy.item import Item, Field

class Article(Item):
  url = Field()
  title = Field()
  description = Field()
  author = Field()
  body = Field()
  imgs = Field()

class Image(Item):
  src = Field()
  title = Field()