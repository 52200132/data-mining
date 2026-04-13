import scrapy
from scrapy.http import Response
from ..items import NewsArticleItem


class VnExpressSpider(scrapy.Spider):
    name = "vnexpress"
    allowed_domains = ["vnexpress.net"]
    allow_labels = [
        "Thể thao",
        "Chính trị - Xã hội",
        "Kinh doanh",
        "Công nghệ",
        "Giải trí",
        "Pháp luật",
    ]
    # start_urls = [
    #     "https://vnexpress.net/inter-miami-van-chua-thang-tren-san-moi-nu-5061354.html"
    # ]

    max_articles_for_test = 25
    article_count = 0

    def __init__(
        self,
        category=None,
        label=None,
        process_id=None,
        output_dir=None,
        *args,
        **kwargs,
    ):
        # Đừng quên gọi super(), nó rất quan trọng để Scrapy hoạt động đúng
        super(VnExpressSpider, self).__init__(*args, **kwargs)

        # Gán biến truyền vào
        if category is None:
            raise ValueError("Category is required")
        if label is None:
            raise ValueError("Label is required")
        if process_id is None:
            raise ValueError("Process ID is required")
        if output_dir is None:
            raise ValueError("Target directory is required")
        if label not in self.allow_labels:
            raise ValueError(f"Label must be one of {self.allow_labels}")
        self.category = category
        self.label = label
        self.process_id = process_id
        self.output_dir = output_dir

        # Tạo link xuất phát dựa trên biến truyền vào
        self.start_urls = [f"https://vnexpress.net/{self.category}"]

    def parse(self, response: Response):
        # Lấy tất cả các khối bài viết
        articles = response.css("article.item-news")

        for art in articles:

            # lấy link bài báo
            url = art.css("h2.title-news a[data-medium]::attr(href)").get()
            if url is None:
                self.logger.warning("No url found h2 title link")
                url = art.css("h3.title-news a[data-medium]::attr(href)").get()
            if url is None:
                self.logger.warning("No url found h3 title link")
                url = art.css("h4.title-news a[data-medium]::attr(href)").get()

            if url:
                yield response.follow(url, self.parse_article)
            else:
                self.logger.warning("No url found h4 title link")

        # Test chạy thử 25 bài
        # self.article_count += articles.count()
        # if self.article_count >= self.max_articles_for_test:
        #     return

        # Tự động tìm nút "Trang sau" và cào tiếp (nếu muốn)
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response: Response):
        """
        Lấy các dữ liệu cần thiết của bài báo
        """
        item = NewsArticleItem()
        metadata = {
            "doc_id": response.url.split("-")[-1].replace(
                ".html", ""
            ),  # Ví dụ cách lấy ID từ URL
            "source_name": "VnExpress",
            "source_url": response.url,
            "publish_date": response.css(
                "div.header-content.width_common > span.date::text"
            ).get(),  # Cần format lại ISO 8601
            "author": "VnExpress",
        }

        paragraphs = response.css("article.fck_detail p.Normal::text").getall()
        content = " ".join(paragraphs).strip()

        content = {
            "title": response.css("h1.title-detail::text").get(),
            "sapo": response.css("p.description::text").get(),
            "content": content,
            "word_count": len(content.split()),
        }

        labeling = {
            "original_category": response.css("ul.breadcrumb li a::text").getall(),
            "target_label": self.label,  # Logic phân loại của bạn
            "tags": response.css('meta[name="keywords"]::attr(content)').getall(),
            "is_multilabel": False,
        }

        item["metadata"] = metadata
        item["content"] = content
        item["labeling"] = labeling

        yield item
        pass
