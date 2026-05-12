# Tên bot dự án
BOT_NAME = "crawler_bot"

SPIDER_MODULES = ["src.crawler_bot.spiders"]
NEWSPIDER_MODULE = "src.crawler_bot.spiders"

# Cấu hình User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Cấu hình Delay để tránh bị chặn
DOWNLOAD_DELAY = 2  # giây
CONCURRENT_REQUESTS = 13  # số request cùng lúc

# Nếu muốn bot tự động điều chỉnh tốc độ dựa trên phản hồi của server
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0

# Kích hoạt pipeline lưu file
ITEM_PIPELINES = {
    # "src.crawler_bot.pipelines.DuplicatesPipeline": 100,
    "src.crawler_bot.pipelines.IsValidItemPipeline": 200,
    "src.crawler_bot.pipelines.JsonlRotationPipeline": 300,
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Đường dẫn đến file log bạn muốn lưu
LOG_FILE = "logs/crawl_errors.log"

# Chỉ lưu những lỗi từ mức WARNING trở lên để file không bị quá nặng
LOG_LEVEL = "WARNING"

import logging
from scrapy.utils.log import configure_logging

# Vô hiệu hóa cấu hình log mặc định của Scrapy để tự thiết lập
configure_logging(install_root_handler=False)

# 1. Định dạng log (giống log mặc định của Scrapy cho quen mắt)
log_format = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
log_datefmt = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,  # Hoặc DEBUG nếu muốn soi kỹ
    format=log_format,
    datefmt=log_datefmt,
    handlers=[
        # logging.FileHandler("logs/crawl.log", encoding="utf-8"),  # Ghi vào file
        logging.StreamHandler(),  # Đẩy ra console (màn hình)
    ],
)
