from checker.scraper import Scraper
import time
with Scraper() as bot:
    
    bot.land_first_page()
    bot.choose_section()
    bot.scrap()
