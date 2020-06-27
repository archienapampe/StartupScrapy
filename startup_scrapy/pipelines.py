import csv

from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem


class CsvPipeline():
    def __init__(self, file_name):
        self.file = open(file_name, 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    
    
class CsvUrlPipeline(CsvPipeline):
    def __init__(self, file_name='urls.csv'):
        super().__init__(file_name)
        
    
class CsvInfoPipeline(CsvPipeline):
    def __init__(self, file_name='info.csv'):
        super().__init__(file_name)


class DuplicatesUrlPipeline:
    def __init__(self):
        try:
            with open('urls.csv', 'r') as list_urls:
                list_urls = csv.reader(list_urls)
                try:
                    next(list_urls)
                except StopIteration:
                    self.scraped_urls = []
                else:
                    self.scraped_urls = [row[0] for row in list_urls]
        except FileNotFoundError:
            self.scraped_urls = []  
             
    def process_item(self, item, spider):
        if item['url'] in self.scraped_urls:
            raise DropItem('Duplicate item found: {}'.format(item['url']))
        else:
            return item