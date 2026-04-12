import scrapy
from ..items import DemoCrawlerItem
from scrapy.http import Response


class BasicSpider(scrapy.Spider):
    name = "vnexpress_soccer"  # Đổi tên để tránh trùng với file vnexpress.py cũ
    start_urls = ["https://vnexpress.net/bong-da"]

    def parse(self, response: Response):
        # Lấy tất cả các khối bài viết
        articles = response.css("article.item-news")

        for art in articles:
            item = DemoCrawlerItem()
            # Lấy tiêu đề và link
            item["title"] = art.css("h2.title-news a::text").get()
            item["url"] = art.css("h2.title-news a::attr(href)").get()

            # Để đơn giản, bước này ta lấy thông tin ở trang danh sách trước
            if item["title"]:
                yield item

        # Tự động tìm nút "Trang sau" và cào tiếp (nếu muốn)
        # next_page = response.css("a.next-page::attr(href)").get()
        # if next_page:
        #     yield response.follow(next_page, self.parse)
