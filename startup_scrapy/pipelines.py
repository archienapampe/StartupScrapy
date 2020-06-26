from scrapy.exporters import CsvItemExporter


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