# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from lxml import etree
import requests,time,json
import re
from w3lib.html import remove_tags
from jinritoutiao.items import toutiaoItem


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['www.toutiao.com/']
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS" : {
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en',
          'cookie':'WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=163b8c66679a90-0782f2397a1db7-b7a103e-144000-163b8c6667aaaa; csrftoken=9fedb00b6fd33e3af55720814ba89295; uuid="w:63616cf1cc1f43b485b7dd3d49bb519d"; tt_webid=75446291913; tt_webid=75446291913; _ga=GA1.2.625102943.1536644856; _gid=GA1.2.683756205.1536644856; __tasessionId=hu7vdiyha1536651215201; CNZZDATA1259612802=1789237699-1527811105-https%253A%252F%252Fwww.baidu.com%252F%7C1536653885',
          'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
    }
    def start_requests(self):
        option_chrome = webdriver.ChromeOptions()
        option_chrome.add_argument('--headless')
        chrome_options = option_chrome
        url = "https://www.toutiao.com/ch/news_finance/"
        driver = webdriver.Chrome(chrome_options=option_chrome)
        driver.get(url)
        try:
            j = 5000
            for i in range(0, 100000, 5000):
                j = int(i + j)
                js = "window.scrollBy({},{})".format(i, j)
                print(js)
                driver.execute_script(js)
                if i == 0:
                    time.sleep(15)
                else:
                    time.sleep(2)
                print("****" * 60)
        except Exception as e:
            print(e)
        time.sleep(10)
        response = driver.page_source.encode('utf8')
        response = etree.HTML(response)
        url = response.xpath("//a[@class = 'img-wrap']/@href")
        for delist in url:
            if "group" in delist:
                delist_url = "https://www.toutiao.com" + str(delist)
                yield scrapy.Request(delist_url, callback=self.parse)
    def parse(self, response):
        response = response.text
        try:
            path = r"content: (.*?)groupId:"
            title_path = r"title: '(.*?)\',content"
            title_name = re.search(title_path,response,re.S)
            info = re.search(path,response,re.S)
            info_message = info.group(1)
            title = title_name.group(1)
            info_message = remove_tags(info_message)
            item =toutiaoItem()
            item["title"] = title
            item["info_message"] = info_message
            yield item
        except Exception as e:
            print(e)
