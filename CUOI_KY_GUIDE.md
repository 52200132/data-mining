# 📋 Hướng dẫn Cuối Kỳ — Phân loại bài báo tiếng Việt

> **Nhóm:** Võ Văn Sáng & Đỗ Xuân Thắng | Tôn Đức Thắng | 2026

---

### Cách chạy

```bash
# Chạy 10 chủ đề song song (3-6 tiếng)
poetry run python run_all_10topics.py

# Hoặc chạy từng chủ đề riêng (nếu muốn kiểm tra trước)
poetry run scrapy crawl vnexpress \
    -a category=the-thao \
    -a label="Thể thao" \
    -a output_dir=data/raw/the-thao \
    -a process_id=1 \
    -a max_pages=200
```

### Kiểm tra dữ liệu sau khi crawl

```bash
# Đếm số bài mỗi chủ đề
for dir in data/raw/*/; do
    count=$(cat "$dir"/*.jsonl | wc -l)
    echo "$dir: $count bài"
done
```

##  PHẦN 3 — TIỀN XỬ LÝ (preprocess.py)

### Pipeline 5 bước

```
Input text
    │
    ▼
1. normalize_unicode()  → "chữ" tổ hợp → "chữ" dựng sẵn (NFC)
    │
    ▼
2. clean_text()         → bỏ HTML, URL, email, ký tự lạ
    │
    ▼
3. lowercase()          → "Việt Nam" → "việt nam"
    │
    ▼
4. word_tokenize()      → "học sinh" → "học_sinh"  (underthesea)
    │
    ▼
5. remove_stopwords()   → bỏ "thì, là, mà, của..."
    │
    ▼
Output: "học_sinh thi_cử đại_học tuyển_sinh bộ_giáo_dục..."
```

### Chạy preprocessing

```bash
# gộp data trươc
poetry run python merge_datasets.py

# chuan hoa nhe cac label cho dong nhat
poetry run python normalize_labels.py
poetry run python fix_labels.py 

# tien xu ly
poetry run python preprocess.py
# Output: data/processed/dataset_final.jsonl
```

---

## PHẦN 4 — TRAIN MODEL MÔ HÌNH (classify/train_model.py)

### Bước 1 — Rule-based (Baseline)

**Cách hoạt động:**
- Định nghĩa danh sách từ khóa đặc trưng cho mỗi chủ đề
- Đếm số từ khóa xuất hiện trong văn bản → chủ đề nào có điểm cao nhất là kết quả
- Đơn giản, không cần training, không cần dữ liệu

**Ưu điểm:** Nhanh, dễ hiểu, dễ debug
**Nhược điểm:** Accuracy thấp (~50-65%), không bắt được ngữ cảnh

```python
# Ví dụ hoạt động:
text = "cầu_thủ ghi bàn_thắng trong trận_đấu vô_địch"

scores = {
    "Thể thao":  count("bóng_đá") + count("cầu_thủ") + count("bàn_thắng") + ...
    "Kinh doanh": count("doanh_nghiệp") + ...
    ...
}
# → {"Thể thao": 3, "Kinh doanh": 0, ...} → dự đoán: "Thể thao"
```

### Bước 2 — TF-IDF + Logistic Regression

**TF-IDF là gì?**

```
TF-IDF(từ, bài) = TF × IDF

TF  = số lần từ xuất hiện / tổng số từ trong bài  (term frequency)
IDF = log(tổng số bài / số bài chứa từ này)       (inverse document frequency)

Ý nghĩa: Từ xuất hiện nhiều trong bài nhưng ít trong corpus → quan trọng hơn
```

**Cấu hình quan trọng:**
```python
TfidfVectorizer(
    max_features=50000,    # Giữ 50k từ phổ biến nhất
    ngram_range=(1, 2),    # Dùng cả đơn từ và cụm 2 từ
    min_df=2,              # Bỏ từ chỉ xuất hiện trong 1 bài
    max_df=0.95,           # Bỏ từ quá phổ biến (>95% bài)
    sublinear_tf=True,     # Dùng log(tf) → ổn định hơn
)
```

**Logistic Regression:**
```python
LogisticRegression(
    C=5.0,                     # Regularization strength
    class_weight="balanced",   
    solver="lbfgs",
    max_iter=1000,
)
```

**Kết quả kỳ vọng:**

| Phương pháp          | Accuracy kỳ vọng |
|----------------------|-----------------|
| Rule-based           | 50–65%          |
| TF-IDF + LR          | 85–93%          |
| TF-IDF + Random Forest | 82–90%        |

### Chạy training

```bash
poetry run python classify/train_model.py
# Output:
#   models/vectorizer.pkl
#   models/lr_model.pkl
#   models/confusion_matrix.png
#   models/top_keywords.png
```

### Phân tích Confusion Matrix

Sau khi train, mở `models/confusion_matrix.png`:
- **Đường chéo sáng** → model phân loại đúng nhiều
- **Ô ngoài đường chéo sáng** → nhầm lẫn giữa 2 chủ đề
- Thường gặp: **Sức khỏe ↔ Khoa học**, **Kinh doanh ↔ Chính trị - Xã hội**

Nếu nhầm nhiều → thêm dữ liệu hoặc bổ sung từ khóa cho rule-based.

---

## 🌐 PHẦN 5 — WEB APP (app/app.py)

### Cài thêm Streamlit

```bash
poetry add streamlit
# hoặc
pip install streamlit
```

### Chạy web app

```bash
poetry run streamlit run app.py
```
Mở trình duyệt: **http://localhost:8501**

### Tính năng web app

- Nhập tiêu đề + nội dung bài báo
- Chọn phương pháp: Rule-based / TF-IDF+LR / So sánh cả hai
- Hiển thị kết quả + độ tin cậy (confidence %)
- Biểu đồ xác suất từng chủ đề
- Bài mẫu để test nhanh

---

## 📁 PHẦN 6 — CẤU TRÚC DỰ ÁN CUỐI KỲ

```

```

---

## 🚀 PHẦN 7 — THỨ TỰ THỰC HIỆN

```bash
# BƯỚC 1: Crawl dữ liệu 
poetry run python run_all_10topics.py

# BƯỚC 2: Tiền xử lý 
poetry run python preprocess.py

# BƯỚC 3: Train mô hình 
poetry run python classify/train_model.py

# BƯỚC 4: Chạy web app
streamlit run app/app.py
```

---

## 💡 PHẦN 8 — DÀN Ý BÁO CÁO CUỐI KỲ + ĐIỂM CỘNG

1. **So sánh 3 phương pháp rõ ràng**: Rule-based → TF-IDF+LR → (bonus) Random Forest
2. **Phân tích Confusion Matrix**: Chỉ ra cặp chủ đề nào hay bị nhầm và tại sao
3. **Top keywords chart**: Giải thích tại sao model chọn những từ này
4. **Thêm pyproject.toml**: `streamlit`, `scikit-learn`, `matplotlib`, `seaborn`
5. **Slide**: Dùng biểu đồ từ `models/` trong slide thuyết trình

```toml
# Thêm vào pyproject.toml
dependencies = [
  ...
  "scikit-learn>=1.3.0",
  "streamlit>=1.32.0",
  "matplotlib>=3.8.0",
  "seaborn>=0.13.0",
]
```
