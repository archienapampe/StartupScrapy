import csv
import random

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
        try:
            with open('urls.csv', 'r') as list_urls:
                list_urls = csv.reader(list_urls)
                try:
                    next(list_urls)
                except StopIteration:
                    self.slugs_from_urls_to_parse = []
                else:
                    try:
                        self.slugs_from_urls_to_parse = random.sample([row[0][24:] for row in list_urls], 5)
                    except ValueError as e:
                        print(e)
                        self.slugs_from_urls_to_parse = []
        except FileNotFoundError:
            self.slugs_from_urls_to_parse = []
                
    def start_requests(self):
        if self.slugs_from_urls_to_parse:
            for slug in self.slugs_from_urls_to_parse:
               yield scrapy.Request(url=self.api_url_startup.format(slug), callback=self.parse)
        else:
            return None
    
    def parse(self, response):
        self.logger.info('start scraping startup info')
        data_json = response.json()
        data = data_json['data']
        loader = ItemLoader(item=StartupInfoItem(), selector=data)
        loader.add_value('company_name', data['name'])
        loader.add_value('profile_url', self.startups_url.format(data['slug']))
        loader.add_value('company_website_url', data['metas'].get('website', ''))
        loader.add_value('location', data.get('location', '')[0]['text'])
        loader.add_value('tags', data['metas'].get('market', ''))
        loader.add_value('founding_date', f'{data["metas"].get("found_month", "")} {data["metas"].get("found_year", "")}')
        loader.add_value('urls', f'{data["metas"]["linkedin"]},{data["metas"]["twitter"]},{data["metas"]["facebook"]}')
        loader.add_value('emails', data['metas'].get('email', ''))
        loader.add_value('phones', '')
        loader.add_value('description_short', data['metas'].get('short_description', ''))
        loader.add_value('description', data['metas'].get('description', ''))
        startup_item = loader.load_item()
        
        yield scrapy.Request(url=self.api_url_team.format(data['id']),
                                callback=self.parse_team, meta={'startup_item': startup_item})
            
    def parse_team(self, response):
        self.logger.info('start scraping team info')
        startup_item = response.meta['startup_item']
        
        data_json = response.json()
        data = data_json['data']
        loader = ItemLoader(item=startup_item, selector=data)
        loader.add_value('employee_range', data['count'])
        for info_user in data['site_users']:   
            loader.add_value('founders', info_user['name'])
            yield loader.load_item()