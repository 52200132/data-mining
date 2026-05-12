"""
run_all_10topics.py
Chạy crawl 10 chủ đề song song — mỗi chủ đề ~200 trang ≈ 3000 bài
Chạy bằng: poetry run python run_all_10topics.py
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.crawler_bot.spiders.vnexpress import VnExpressSpider

# ============================================================
# CẤU HÌNH 10 CHỦ ĐỀ
# category  : slug trên URL vnexpress.net/[category]
# label     : nhãn chuẩn hóa cho mô hình
# dir       : thư mục lưu file .jsonl
# ============================================================
TOPICS = [
    {
        "category": "the-thao",
        "label": "Thể thao",
        "dir": "data/raw/the-thao",
    },
    {
        "category": "kinh-doanh",
        "label": "Kinh doanh",
        "dir": "data/raw/kinh-doanh",
    },
    {
        "category": "phap-luat",
        "label": "Pháp luật",
        "dir": "data/raw/phap-luat",
    },
    {
        "category": "Khoa-hoc-cong-nghe",        # VnExpress gọi mục Công nghệ là "so-hoa"
        "label": "Khoa học công nghệ",
        "dir": "data/raw/cong-nghe",
    },
    {
        "category": "giai-tri",
        "label": "Giải trí",
        "dir": "data/raw/giai-tri",
    },
    {
        "category": "thoi-su",
        "label": "Thời sự",
        "dir": "data/raw/thoi-su",
    },
    {
        "category": "suc-khoe",
        "label": "Sức khỏe",
        "dir": "data/raw/suc-khoe",
    },
    {
        "category": "du-lich",
        "label": "Du lịch",
        "dir": "data/raw/du-lich",
    },
    {
        "category": "giao-duc",
        "label": "Giáo dục",
        "dir": "data/raw/giao-duc",
    },
    {
        "category": "doi-song",
        "label": "Đời sống",
        "dir": "data/raw/doi-song",
    },
]

MAX_PAGES = 200

settings = get_project_settings()
process = CrawlerProcess(settings)

for i, topic in enumerate(TOPICS):
    process.crawl(
        VnExpressSpider,
        category=topic["category"],
        label=topic["label"],
        output_dir=topic["dir"],
        process_id=str(i + 1),
        max_pages=MAX_PAGES,
    )

print(f"Bắt đầu crawl {len(TOPICS)} chủ đề × ~{MAX_PAGES} trang...")
print("Dự kiến thu thập: ~30,000 bài báo")
process.start()
print("\n Hoàn thành crawl!")
