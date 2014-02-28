# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ScrapperItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class Rank(Item):
  cur = Field()
  cnt = Field()
  pnt = Field()
  people = Field()
  date = Field()

class CurMovie(Item):
  code = Field()
  title = Field()
  rank = Field()

class CntMovie(Item):
  code = Field()
  title = Field()
  rank = Field()

class PntMovie(Item):
  code = Field()
  title = Field()
  rank = Field()

class People(Item):
  code = Field()
  title = Field()
  birth = Field()
  rank = Field()
