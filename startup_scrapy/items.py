from datetime import datetime, date

from scrapy import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst


def convert_date(text):
    if text:
        try:
            parse_to_date = datetime.strptime(text, '%m %Y')
        except ValueError:
            return ''
        iso_format = parse_to_date.date().isoformat()
        return iso_format
    return ''


def parse_urls(data_urls):
    list_data_urls = data_urls.split(',')
    no_empty_urls = [url for url in list_data_urls if url]
    return no_empty_urls

    
class StartupUrlItem(Item):
    url = Field()
    

class StartupInfoItem(Item):
    company_name = Field(
        output_processor=TakeFirst()
    )
    profile_url = Field(
        output_processor=TakeFirst()
    )
    company_website_url = Field(
        output_processor=TakeFirst()
    )
    location = Field(
        output_processor=TakeFirst()
    )
    tags = Field()
    founding_date = Field(
        input_processor=MapCompose(str.strip, convert_date),
        output_processor=TakeFirst()
    )
    founders = Field()
    employee_range= Field(
        output_processor=TakeFirst()
    )
    urls = Field(
        input_processor=MapCompose(parse_urls)
    )
    emails = Field(
        output_processor=TakeFirst()
    )
    phones = Field(
        output_processor=TakeFirst()
    )
    description_short = Field(
        output_processor=TakeFirst()
    )
    description = Field(
        output_processor=TakeFirst()
    )