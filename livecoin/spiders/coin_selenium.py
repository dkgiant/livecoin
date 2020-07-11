# # -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import which


class CoinSpiderSelenium(scrapy.Spider):
    name = 'coin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['https://www.livecoin.net/en']

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
        driver.set_window_size(1920, 6080)
        driver.get("https://www.livecoin.net/en")
        usd_tab = driver.find_elements_by_class_name("filterPanelItem___2z5Gb")

        usd_tab[2].click()
        show_btn = driver.find_element_by_xpath(r'//div[@class="showMoreContainer___2HlS0"]/button')
        # show_btn.click()
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        currencies = resp.xpath(r'//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS")]')
        for currency in currencies:
            yield {
                'current_pair': currency.xpath(r'.//div[1]/div/text()').get(),
                'volume(24h)': currency.xpath(r'.//div[2]/span/text()').get(),
            }
