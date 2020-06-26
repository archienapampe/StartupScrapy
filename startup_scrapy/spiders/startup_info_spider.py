import csv
import random
import json

import scrapy
from scrapy.loader import ItemLoader

from startup_scrapy.items import StartupInfoItem


class StartupInfoSpider(scrapy.Spider):
    name = 'startup_info'
    api_url_startup = 'https://e27.co/api/startups/get/?slug={}&data_type=general&get_badge=true'
    api_url_team = 'https://e27.co/api/site_user_startups/site_users/?startup_id={}'
    startups_url = 'https://e27.co/startups/{}'
    custom_settings = {
        'ITEM_PIPELINES': {
            'startup_scrapy.pipelines.CsvInfoPipeline': 200,
        }
    }
    
    def __init__(self):
        with open('urls.csv', 'r') as list_urls:
            list_urls = csv.reader(list_urls)
            next(list_urls)
            self.slugs_from_urls_to_parse = random.sample([row[0][24:] for row in list_urls], 250)
        
    def start_requests(self):
        for slug in self.slugs_from_urls_to_parse:
            yield scrapy.Request(url=self.api_url_startup.format(slug), callback=self.parse)
      
    def parse(self, response):
        self.logger.info('start scraping startup info')
        data_json = json.loads(response.text)
        data = data_json['data']
        loader = ItemLoader(item=StartupInfoItem(), selector=data)
        loader.add_value('company_name', value=data['name'])
        loader.add_value('profile_url', value=self.startups_url.format(data['slug']))
        loader.add_value('company_website_url', value=data['metas'].get('website', ''))
        loader.add_value('location', value=data.get('location', '')[0]['text'])
        loader.add_value('tags', value=data['metas'].get('market', ''))
        loader.add_value('founding_date', value=f'{data["metas"].get("found_month", "")} {data["metas"].get("found_year", "")}')
        loader.add_value('urls', value=f'{data["metas"]["linkedin"]},{data["metas"]["twitter"]},{data["metas"]["facebook"]}')
        loader.add_value('emails', value=data['metas'].get('email', ''))
        loader.add_value('phones', value='')
        loader.add_value('description_short', value=data['metas'].get('short_description', ''))
        loader.add_value('description', value=data['metas'].get('description', ''))
        startup_item = loader.load_item()
        
        yield scrapy.Request(url=self.api_url_team.format(data['id']),
                                  callback=self.parse_team, meta={'startup_item': startup_item})
            
    def parse_team(self, response):
        self.logger.info('start scraping team info')
        startup_item = response.meta['startup_item']
        data_json = json.loads(response.text)
        data = data_json['data']
        loader = ItemLoader(item=startup_item, selector=data)
        loader.add_value('employee_range', value=data['count'])
        for info_user in data['site_users']:   
            loader.add_value('founders', value=info_user['name'])
            yield loader.load_item()
            
            
            
            