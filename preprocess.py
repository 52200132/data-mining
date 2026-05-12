import json
import re
import glob
import unicodedata
from pathlib import Path

# underthesea dung de tach tu
try:
    from underthesea import word_tokenize
    HAS_UNDERTHESEA = True
except ImportError:
    print("⚠️  underthesea chưa cài. Chạy: pip install underthesea")
    HAS_UNDERTHESEA = False
# STOPWORDS tieng viet

STOPWORDS = {
    "thì", "là", "mà", "của", "và", "các", "những", "được", "trong",
    "có", "cho", "với", "về", "từ", "này", "đó", "theo", "tại", "khi",
    "để", "đã", "sẽ", "đang", "bị", "do", "vì", "nên", "nhưng", "còn",
    "hay", "hoặc", "như", "cũng", "vẫn", "đều", "chỉ", "rất", "một",
    "hai", "ba", "tôi", "bạn", "họ", "chúng", "ta", "ông", "bà", "anh",
    "chị", "em", "người", "năm", "ngày", "tháng", "hôm", "nay", "đây",
    "kia", "ai", "gì", "nào", "đâu", "sao", "thế", "không", "chưa",
    "hơn", "nhất", "nhiều", "ít", "lại", "lên", "xuống", "ra", "vào",
    "tuy", "dù", "mặc", "dù", "vậy", "thật", "thực", "sự", "việc",
    "điều", "cái", "con", "cây", "chiếc", "cuộc", "khoảng", "bởi",
    "qua", "trên", "dưới", "sau", "trước", "giữa", "ngoài", "bên",
    "phải", "thể", "muốn", "cần", "biết", "thấy", "nói", "làm",
}

# ham chuan hoa Unicode
def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFC", text)

# lam sach du lieu
def clean_text(text: str) -> str:
    """Loại bỏ HTML, URL, email, ký tự đặc biệt, khoảng trắng thừa"""
    # Xóa HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    # Xóa URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Xóa email
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    # Xóa emoji và ký tự đặc biệt
    text = re.sub(r"[^\w\s\u00C0-\u024F\u1E00-\u1EFF]", " ", text)
    # Xóa số đứng một mình
    text = re.sub(r"\b\d+\b", " ", text)
    # Xóa khoảng trắng thừa
    text = re.sub(r"\s+", " ", text).strip()
    return text

# tach tu
def segment_words(text: str) -> str:
    if not HAS_UNDERTHESEA:
        return text
    return word_tokenize(text, format="text")


def remove_stopwords(text: str) -> str:
    words = text.split()
    filtered = [
        w for w in words
        if w.lower() not in STOPWORDS and len(w) > 1
    ]
    return " ".join(filtered)

"""Pipeline đầy đủ: normalize → clean → lowercase → segment → remove stopwords"""
def full_pipeline(text: str) -> str:
    text = normalize_unicode(text)
    text = clean_text(text)
    text = text.lower()
    text = segment_words(text)
    text = remove_stopwords(text)
    return text

# ĐỌC & XỬ LÝ FILE DATA (.jsonl)

def process_jsonl_file(file_path: str) -> list[dict]:
    """Đọc 1 file .jsonl, tiền xử lý và trả về list các bài đã clean"""
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)

                title   = (item.get("content", {}) or {}).get("title",   "") or ""
                sapo    = (item.get("content", {}) or {}).get("sapo",    "") or ""
                body    = (item.get("content", {}) or {}).get("content", "") or ""
                label   = (item.get("labeling", {}) or {}).get("target_label", "")
                url     = (item.get("metadata", {}) or {}).get("source_url", "")
                word_ct = (item.get("content", {}) or {}).get("word_count", 0) or 0

                # Bỏ bài quá ngắn (< 50 từ) — thường là video/ảnh không có text
                if word_ct < 50:
                    continue

                # Ghép title + sapo + body để tạo văn bản đầy đủ
                raw_text = f"{title} {sapo} {body}"
                cleaned = full_pipeline(raw_text)

                if cleaned and label:
                    results.append({
                        "text_cleaned": cleaned,
                        "label": label,
                        "url": url,
                        "word_count": word_ct,
                    })
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"  ⚠️  Lỗi dòng {line_num} trong {file_path}: {e}")
    return results

# MAIN
if __name__ == "__main__":
    all_data = []
    label_counts = {}

    # doc file da merge tu du lieu 2 bao thanh nien va Vnexpress
    merged_file = Path("data/processed/dataset_fixedlabel.jsonl")
    
    if not merged_file.exists():
        print(f"Không tìm thấy file!!: {merged_file}")
        print("Hãy chạy merge_datasets.py trước!")
    else:
        print(f"Đang xử lý file merged: {merged_file}")
        data = process_jsonl_file(str(merged_file))   
        all_data.extend(data)

        print(f"Đã xử lý {len(data):,} bài từ file merged")

    print("-" * 60)
    print(f"Tổng cộng: {len(all_data):,} bài")

    # lưu dataset đã clean
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "dataset_final.jsonl"

    with open(out_path, "w", encoding="utf-8") as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\nDataset đã lưu tại: {out_path}")

    # thong ke de kiem tra co sot du lieu khong
    from collections import Counter
    label_counts = Counter(item["label"] for item in all_data)
    print("\nPhân phối nhãn:")
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1]):
        print(f"  {label:25s}: {count:,} bài")