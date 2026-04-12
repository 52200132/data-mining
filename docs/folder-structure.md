Dưới đây là cấu trúc thư mục chuẩn chuyên nghiệp cho dự án **News Data Mining** của bạn:

---

## 1. Cấu trúc thư mục dự án

```text
news-data-mining/
├── pyproject.toml              # File cấu hình bạn vừa tạo
├── .env                        # Lưu các tham số nhạy cảm (nếu có)
├── data/
│   ├── raw/                    # Dữ liệu thô vừa cào về (JSON)
│   │   ├── phap-luat/          # Chia theo chủ đề để dễ quản lý
│   │   ├── kinh-doanh/
│   │   └── ...
│   ├── processed/              # Dữ liệu sau khi Preprocessing (đã tách từ, làm sạch)
│   └── final/                  # File cuối cùng để đưa vào huấn luyện (ví dụ: train.csv, test.csv)
├── src/
|   |── crawler_bot/            # Folder chứa logic Scrapy chính
│   |   ├── __init__.py
│   |   ├── items.py            # Định nghĩa các trường theo Schema
│   |   ├── pipelines.py        # Lưu file vào data/raw/
│   |   ├── settings.py         # Cấu hình Delay, User-Agent, v.v.
│   |   └── spiders/            # Nơi chứa các "con nhện"
│   |       └── vnexpress.py    # Spider cho VnExpress
│   ├── preprocessing/          # Chứa code làm sạch, tách từ (underthesea)
│   └── utils/                  # Các hàm bổ trợ (lưu file, logger, validator)
├── configs/
│   └── schema.json             # File JSON Schema để kiểm tra dữ liệu
├── notebook/                   # Chứa các file .ipynb để thử nghiệm nhanh
└── tests/                      # Code kiểm tra lỗi (Unit test)
```

---

## 2. Tại sao nên chia thư mục như thế này?

- **`data/raw` vs `data/processed`:** Đây là quy tắc vàng. Bạn không bao giờ được ghi đè lên dữ liệu gốc. Nếu sau này bạn đổi thuật ngữ tách từ (Word Segmentation), bạn chỉ cần chạy lại code trên `raw` thay vì phải đi cào lại từ đầu trên web (rất tốn thời gian và dễ bị ban IP).
- **Chia nhỏ theo chủ đề:** Khi mỗi chủ đề có 3.000 - 5.000 bài, việc chia folder giúp bạn kiểm tra số lượng (Data Balance) cực nhanh chỉ bằng cách nhìn vào dung lượng thư mục.
- **Tách biệt logic:** Script lấy link (`browser_bot.py`) và script lấy nội dung (`content_extractor.py`) nên tách riêng. Lấy link có thể chạy chậm trên trình duyệt, nhưng lấy nội dung có thể chạy đa luồng (multi-threading) để tăng tốc.

---

## 3. Một mẹo nhỏ cho việc lưu file

Thay vì lưu tên file là `1.json`, `2.json`, bạn nên lưu theo định dạng:
`source_date_hash.json` (Ví dụ: `vne_20240510_a7b2.json`).

Việc này giúp tránh trùng lặp nếu bạn cào từ nhiều nguồn khác nhau.

---

### Bạn đã sẵn sàng để bắt đầu chưa?

Nếu bạn đồng ý với cấu trúc này, tôi sẽ viết cho bạn đoạn code đầu tiên: **`src/utils/validator.py`** để đảm bảo mọi dữ liệu bạn cào về đều "khớp" hoàn toàn với cái **JSON Schema** chúng ta đã tạo.

Bạn muốn bắt đầu viết code cho phần nào trước: **Phần lấy link tự động** hay **Phần kiểm tra dữ liệu**?
