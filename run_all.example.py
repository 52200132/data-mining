from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.crawler_bot.spiders.vnexpress import VnExpressSpider

settings = get_project_settings()
process = CrawlerProcess(settings)

# Chạy cùng lúc với các tham số khác nhau
process.crawl(
    VnExpressSpider,
    category="bong-da",
    label="Thể thao",
    output_dir="data/the-thao",
    process_id="bot1",
)

process.crawl(
    VnExpressSpider,
    category="the-thao/tennis",
    label="Thể thao",
    output_dir="data/the-thao",
    process_id="bot2",
)

process.start()  # Bắt đầu chạy tất cả
