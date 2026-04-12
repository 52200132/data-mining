Dưới đây là file **JSON Schema** được thiết kế dựa trên các tiêu chuẩn khai thác dữ liệu báo chí chuyên sâu:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NewsArticleClassificationSchema",
  "description": "Schema dành cho việc thu thập dữ liệu bài báo phục vụ huấn luyện Text Classification",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "doc_id": {
          "type": "string",
          "description": "ID duy nhất của bài viết (ví dụ: VNEX-12345)"
        },
        "source_name": {
          "type": "string",
          "description": "Tên nguồn tin (VnExpress, Tuổi Trẻ, v.v.)"
        },
        "source_url": {
          "type": "string",
          "format": "uri",
          "description": "Đường dẫn gốc của bài báo"
        },
        "publish_date": {
          "type": "string",
          "format": "date-time",
          "description": "Thời gian xuất bản định dạng ISO 8601"
        },
        "author": {
          "type": "string",
          "description": "Tên tác giả hoặc nhóm phóng viên"
        }
      },
      "required": ["doc_id", "source_name", "source_url"]
    },
    "content": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "Tiêu đề bài báo"
        },
        "sapo": {
          "type": "string",
          "description": "Đoạn tóm tắt đầu bài"
        },
        "body_raw": {
          "type": "string",
          "description": "Văn bản thô sau khi loại bỏ HTML"
        },
        "body_cleaned": {
          "type": "string",
          "description": "Văn bản đã qua xử lý (loại bỏ quảng cáo, text thừa)"
        },
        "word_count": {
          "type": "integer",
          "minimum": 0
        }
      },
      "required": ["title", "body_cleaned"]
    },
    "labeling": {
      "type": "object",
      "properties": {
        "original_category": {
          "type": "string",
          "description": "Chuyên mục gốc từ website"
        },
        "target_label": {
          "type": "string",
          "enum": [
            "Chính trị",
            "Kinh doanh",
            "Công nghệ",
            "Thể thao",
            "Sức khỏe",
            "Giải trí",
            "Giáo dục",
            "Pháp luật",
            "Đời sống",
            "Thế giới"
          ],
          "description": "Nhãn đã chuẩn hóa để huấn luyện mô hình"
        },
        "tags": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Danh sách các từ khóa đi kèm"
        },
        "is_multilabel": {
          "type": "boolean",
          "default": false
        }
      },
      "required": ["target_label"]
    }
  },
  "required": ["metadata", "content", "labeling"]
}
```

---

### Giải thích nhanh về các thành phần chính:

- **`metadata`**: Giúp bạn truy vết nguồn gốc. Nếu sau này bạn thấy mô hình dự đoán sai hàng loạt bài từ một nguồn nhất định, bạn có thể kiểm tra lại crawler của nguồn đó.
- **`body_cleaned`**: Đây là "thức ăn" chính cho AI. Việc tách biệt `body_raw` và `body_cleaned` giúp bạn có thể thử nghiệm nhiều phương pháp tiền xử lý (Preprocessing) khác nhau mà không phải cào lại dữ liệu từ đầu.
- **`target_label` với `enum`**: Tôi đã giới hạn danh sách 10 chủ đề phổ biến. Việc dùng `enum` trong schema giúp validate dữ liệu ngay lập tức; nếu crawler lấy về một nhãn không nằm trong danh sách này, nó sẽ báo lỗi, tránh làm "nhiễu" tập train.
- **`is_multilabel`**: Một "mẹo" nhỏ. Nếu bài báo vừa là _Công nghệ_ vừa là _Kinh doanh_ (ví dụ: Vụ kiện của Apple), bạn đánh dấu `true` để sau này cân nhắc có đưa vào tập huấn luyện đơn nhãn (Single-label) hay không.

Bạn có thể lưu nội dung trên vào file `schema.json`. Nếu bạn dùng Python để cào dữ liệu, bạn có thể dùng thư viện `jsonschema` để kiểm tra dữ liệu trước khi lưu vào database nhé!
