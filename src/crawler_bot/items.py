import scrapy


class NewsItem(scrapy.Item):
    # Định nghĩa các trường theo Schema
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    content = scrapy.Field()
    pub_date = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    tags = scrapy.Field()


class DemoCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()


class NewsArticleItem(scrapy.Item):
    # Metadata Group
    metadata = scrapy.Field()
    # Sẽ chứa: doc_id, source_name, source_url, publish_date, author

    # Content Group
    content = scrapy.Field()
    # Sẽ chứa: title, sapo, body_raw, body_cleaned, word_count

    # Labeling Group
    labeling = scrapy.Field()
    # Sẽ chứa: original_category, target_label, tags, is_multilabel
