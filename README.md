# StartupScrapy


### Description
This is a scraper page of the site https://e27.co/startups by Scrapy framework.  
The first spider runs throughout the site and collects links to startups.  
The second spider goes through the list of links to startups and parses information from there.  

The page has dynamic content in the form of infinite scrolling, therefore the data is parsed on the basis of the hidden api.  
Spider parses the extracted data into Items where was added pre/post processing to each Item field (via ItemLoader).   
Then the Items go through Item Pipelines for further processing and is saved to csv file.  

### HOW TO
Use python version 3.8.0 or later.
1. clone this project
2. activate your virtual environment
3. pip install -r requirements.txt
4. run spiders by 'scrapy crawl startup_url && scrapy crawl startup_info' command
