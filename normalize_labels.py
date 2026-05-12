import json
from pathlib import Path

label_map = {
    "the_thao": "Thể thao",
    "kinh_te": "Kinh doanh",
    "chinh_tri": "Chính trị - Xã hội",
    "giai_tri": "Giải trí",
    "suc_khoe": "Sức khỏe",
    "du_lich": "Du lịch",
    "giao_duc": "Giáo dục",
    "khoa_hoc": "Khoa học",
    "phap_luat": "Pháp luật",
    "cong_nghe": "Công nghệ",
}

input_file = Path("data/processed/dataset_merged.jsonl")
output_file = Path("data/processed/dataset_normalizedlabel.jsonl")

with open(input_file, "r", encoding="utf-8") as f_in, \
    open(output_file, "w", encoding="utf-8") as f_out:
    
    count = 0
    for line in f_in:
        if line.strip():
            item = json.loads(line)
            old_label = item.get("label", "").strip().lower().replace(" ", "_")
            item["label"] = label_map.get(old_label, item["label"])
            f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
            count += 1

print(f"Đã chuẩn hóa: {output_file}")