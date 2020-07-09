import scrapy
from scrapy_splash import SplashRequest

class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net/en']
    
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))
  
            usd_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
            usd_tab[3]:mouse_click()
            assert(splash:wait(2))
            splash:set_viewport_full()
            return {
                html = splash:html(),
                --png = splash:png(),
                --har = splash:har(),
            }   
        end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en",callback=self.parse,endpoint="execute",args={
            'lua_source':self.script
        })

    def parse(self, response):
        currencies = response.xpath(r'//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS")]')
        for currency in currencies:
            yield{
                'current_pair': currency.xpath(r'.//div[1]/div/text()').get(),
                'volume(24h)' : currency.xpath(r'.//div[2]/span/text()').get(),
            }