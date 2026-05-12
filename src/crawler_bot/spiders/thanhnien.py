import os
from urllib import response

import scrapy
from scrapy.exceptions import DropItem
from scrapy.http import Response
from ..items import NewsArticleItem
import re


class ThanhNienSpider(scrapy.Spider):
    name = "thanhnien"
    allowed_domains = ["thanhnien.vn"]

    def __init__(
        self,
        start_url=None,
        label=None,
        vietnamese_label=None,
        process_id=None,
        output_dir=None,
        *args,
        **kwargs,
    ):
        # Đừng quên gọi super(), nó rất quan trọng để Scrapy hoạt động đúng
        super(ThanhNienSpider, self).__init__(*args, **kwargs)

        if label is None:
            raise ValueError("Label is required")
        if vietnamese_label is None:
            raise ValueError("Vietnamese label is required")
        if process_id is None:
            raise ValueError("Process ID is required")
        if output_dir is None:
            raise ValueError("Target directory is required")
        if start_url is None:
            raise ValueError("Start URL is required")

        self.label = label
        self.vietnamese_label = vietnamese_label
        self.process_id = process_id
        self.output_dir = output_dir

        # Tạo link xuất phát dựa trên biến truyền vào
        self.start_urls = [start_url]

    def parse(self, response: Response):
        self.save_last_url(response.url)

        articles_urls = response.css("div.box-category-item a::attr(href)").getall()

        yield from response.follow_all(articles_urls, self.parse_article)

        has_next_page = len(articles_urls) > 0
        if has_next_page:
            m = re.search(r"/(\d+)\.htm(?:$|\?)", response.url)
            if m:
                try:
                    current = int(m.group(1))
                    next_page = current + 1
                    # rebuild next page url by replacing the number
                    next_url = re.sub(r"/\d+\.htm", f"/{next_page}.htm", response.url)
                    yield response.follow(next_url, callback=self.parse)
                except ValueError:
                    self.logger.warning(
                        f"Cannot parse page number from URL: {response.url}"
                    )
                    pass

    def parse_article(self, response: Response):
        item = NewsArticleItem()

        # Kiểm tra xem category có chứa nhãn tiếng Việt hay không, nếu không thì bỏ qua bài viết này
        category = [
            cat.strip().lower()
            for cat in response.css("a.category-page__name::text").getall()
        ]
        if self.vietnamese_label not in category:
            self.save_url_not_in_category(response.url)
            raise DropItem(
                f"Category '{self.vietnamese_label}' not found in article categories: {category}"
            )

        doc_id = response.url.split("-")[-1].split(".")[
            0
        ]  # id bài viết của trang thanhnien.vn
        publish_date = response.css(
            "meta[property='article:published_time']::attr(content)"
        ).get()
        author = response.css("meta[name='article:author']::attr(content)").get()
        if not author:
            author = response.css(".detail-author .name::text").get()

        metadata = {
            "doc_id": doc_id,
            "source_name": "ThanhNien",
            "source_url": response.url,
            "publish_date": publish_date,
            "author": author,
        }

        title = response.css("h1.detail-title span[data-role='title']::text").get()
        sapo = response.css("h2.detail-sapo::text").get()
        body_parts = response.css(
            "div.detail-content[data-role='content'] p ::text"
        ).getall()
        body_parts = [part.strip() for part in body_parts if part.strip()]
        body_cleaned = " ".join(body_parts)

        content = {
            "title": title,
            "sapo": sapo,
            "body_cleaned": body_cleaned,
            "word_count": len(body_cleaned.split()),
        }

        tags_value = response.css("meta[name='keywords']::attr(content)").get()
        tags = []
        if tags_value:
            tags = [tag.strip() for tag in tags_value.split(",") if tag.strip()]

        labeling = {
            "original_category": category if category else [],
            "target_label": self.label,
            "tags": tags,
            "is_multilabel": False,
        }

        item["metadata"] = metadata
        item["content"] = content
        item["labeling"] = labeling

        yield item

    def save_last_url(self, url):
        last_url_file = os.path.join(self.output_dir, "last_url.txt")
        with open(last_url_file, "w") as f:
            f.write(url)

    def save_url_not_in_category(self, url):
        not_in_category_file = os.path.join(self.output_dir, "not_in_category.txt")
        with open(not_in_category_file, "a") as f:
            f.write(url + "\n")


class ThanhNienSingleParseSpider(scrapy.Spider):
    """Spider này dùng để parse một bài báo cụ thể, phục vụ cho việc test và debug."""

    name = "thanhnien_single_parse"
    allowed_domains = ["thanhnien.vn"]

    def __init__(
        self,
        url=None,
        label=None,
        *args,
        **kwargs,
    ):
        super(ThanhNienSingleParseSpider, self).__init__(*args, **kwargs)

        if url is None:
            raise ValueError("URL is required")
        if label is None:
            raise ValueError("Label is required")

        self.url = url
        self.label = label

        self.start_urls = [self.url]

    def parse(self, response: Response):
        item = NewsArticleItem()

        doc_id = response.url.split("-")[-1].split(".")[
            0
        ]  # id bài viết của trang thanhnien.vn
        publish_date = response.css(
            "meta[property='article:published_time']::attr(content)"
        ).get()
        author = response.css("meta[name='article:author']::attr(content)").get()
        if not author:
            author = response.css(".detail-author .name::text").get()

        metadata = {
            "doc_id": doc_id,
            "source_name": "ThanhNien",
            "source_url": response.url,
            "publish_date": publish_date,
            "author": author,
        }

        title = response.css("h1.detail-title span[data-role='title']::text").get()
        sapo = response.css("h2.detail-sapo::text").get()
        body_parts = response.css(
            "div.detail-content[data-role='content'] p ::text"
        ).getall()
        body_parts = [part.strip() for part in body_parts if part.strip()]
        body_cleaned = " ".join(body_parts)

        content = {
            "title": title,
            "sapo": sapo,
            "body_cleaned": body_cleaned,
            "word_count": len(body_cleaned.split()),
        }

        category = response.css("a.category-page__name::text").getall()
        tags_value = response.css("meta[name='keywords']::attr(content)").get()
        tags = []
        if tags_value:
            tags = [tag.strip() for tag in tags_value.split(",") if tag.strip()]

        labeling = {
            "original_category": category if category else [],
            "target_label": self.label,
            "tags": tags,
            "is_multilabel": False,
        }

        item["metadata"] = metadata
        item["content"] = content
        item["labeling"] = labeling

        # save to file .json
        with open(f"{doc_id}.json", "w") as f:
            f.write(str(dict(item)))

        # yield item
