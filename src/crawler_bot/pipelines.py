import json
import os
from datetime import datetime
from scrapy.exceptions import DropItem


class JsonWriterPipeline:
    def open_spider(self, spider):
        # Lưu file vào data/raw/
        os.makedirs("../../data/raw", exist_ok=True)
        self.file = open(
            f"../../data/raw/{spider.name}_data.jsonl", "w", encoding="utf-8"
        )

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item


class DuplicatesPipeline:
    def __init__(self):
        self.urls_seen = set()

    def process_item(self, item, spider):
        url = item["metadata"]["source_url"]
        if url in self.urls_seen:
            raise DropItem(f"Trùng lặp link: {url}")

        self.urls_seen.add(url)
        return item


class JsonlRotationPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        # Lấy giá trị 'SAVE_PATH' từ settings.py, nếu không có thì mặc định là 'output_data'
        return cls(
            output_path=crawler.settings.get("SAVE_PATH", "data/raw/not-checked")
        )

    def __init__(self, output_path):
        self.items_per_file = 500
        self.item_count = 0
        self.file_index = 1
        self.current_file = None
        self.start_time = int(datetime.now().timestamp())
        self.output_dir = output_path  # Đường dẫn động đã được truyền vào

        # Tạo thư mục nếu chưa tồn tại
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _open_new_file(self, spider_name, spider_process_id):
        if self.current_file:
            self.current_file.close()

        filename = f"{self.start_time}_part{self.file_index}_spider_{spider_name}_{spider_process_id}.jsonl"
        filepath = os.path.join(self.output_dir, filename)

        self.current_file = open(filepath, "w", encoding="utf-8")
        self.file_index += 1
        self.item_count = 0

    def open_spider(self, spider):
        self._handel_target_dir(getattr(spider, "output_dir", ""))
        process_id = getattr(spider, "process_id", "unknown")
        self._open_new_file(spider.name, process_id)

    def close_spider(self, spider):
        if self.current_file:
            self.current_file.close()

    def process_item(self, item, spider):
        if self.item_count >= self.items_per_file:
            process_id = getattr(spider, "process_id", "unknown")
            self._open_new_file(spider.name, process_id)

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.current_file.write(line)
        self.item_count += 1
        return item

    def _handel_target_dir(self, output_dir):
        """
        Kiểm tra và tạo thư mục đích
        """
        if output_dir == "":
            return
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


class IsValidItemPipeline:
    def process_item(self, item, spider):
        # Kiểm tra các trường bắt buộc trong metadata
        metadata = item.get("metadata", {})
        required_metadata_fields = [
            "doc_id",
            "source_name",
            "source_url",
            "publish_date",
        ]
        for field in required_metadata_fields:
            if not metadata.get(field):
                self.save_news_url_of_invalid_item(
                    metadata.get("source_url", "unknown"), spider
                )
                raise DropItem(f"Thiếu trường metadata bắt buộc: {field}")

        # Kiểm tra các trường bắt buộc trong content
        content = item.get("content", {})
        required_content_fields = ["title", "sapo", "body_cleaned"]
        for field in required_content_fields:
            if not content.get(field):
                self.save_news_url_of_invalid_item(
                    metadata.get("source_url", "unknown"), spider
                )
                raise DropItem(f"Thiếu trường content bắt buộc: {field}")

        return item

    def save_news_url_of_invalid_item(self, url, spider):
        """
        Lưu URL của các item không hợp lệ vào một file riêng để sau này có thể kiểm tra lại
        """
        target_label = getattr(spider, "label", "unknown_label")
        # Save into data/failed-urls/thanhnien.csv with a timestamp column
        out_dir = os.path.join("data", "failed-urls")
        os.makedirs(out_dir, exist_ok=True)
        csv_path = os.path.join(out_dir, "thanhnien.csv")

        # Prepare CSV line: url, first_datetime_failed
        ts = datetime.now().isoformat()
        line = f"{url},{ts},False,none,none,{target_label}\n"

        # If file doesn't exist or is empty, write header first
        write_header = False
        if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
            write_header = True

        with open(csv_path, "a", encoding="utf-8") as f:
            if write_header:
                f.write(
                    "url,first_datetime_failed,refetched,successfully_fetched,refetched_datetime,label\n"
                )
            f.write(line)
