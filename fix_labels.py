import json
from pathlib import Path
from collections import Counter

label_map = {
    # Underscore versions
    "the_thao": "Thể thao",
    "kinh_te": "Kinh doanh",
    "kinh_doanh": "Kinh doanh",
    "chinh_tri": "Chính trị - Xã hội",
    "thoi_su": "Chính trị - Xã hội",
    "doi_song": "Chính trị - Xã hội",
    "giai_tri": "Giải trí",
    "cong_nghe": "Công nghệ",
    "khoa_hoc": "Công nghệ",
    "suc_khoe": "Sức khỏe",
    "du_lich": "Du lịch",
    "giao_duc": "Giáo dục",
    "phap_luat": "Pháp luật",
    "chính trị - Xã hội": "Chính trị - Xã hội",
    "chinh_tri": "Chính trị - Xã hội",
    "thoi_su": "Chính trị - Xã hội",
    "xa_hoi": "Chính trị - Xã hội",
    "doi_song": "Chính trị - Xã hội",

    # Vietnamese full name versions
    "Thể thao": "Thể thao",
    "Kinh doanh": "Kinh doanh",
    "Giải trí": "Giải trí",
    "Du lịch": "Du lịch",
    "Sức khỏe": "Sức khỏe",
    "Giáo dục": "Giáo dục",
    "Pháp luật": "Pháp luật",
    "Công nghệ": "Công nghệ",
}

input_file = Path("data/processed/dataset_normalizedlabel.jsonl")
output_file = Path("data/processed/dataset_fixedlabel.jsonl")

fixed_count = Counter()
total = 0
unknown_labels = Counter()

print(" Đang chuẩn hóa...")

with open(input_file, "r", encoding="utf-8") as f_in, \
    open(output_file, "w", encoding="utf-8") as f_out:
    
    for line in f_in:
        if not line.strip():
            continue
        item = json.loads(line)
        old_label = item.get("label", "").strip()
        
        # Chuẩn hóa
        new_label = label_map.get(old_label)
        if new_label is None:
            # Thử lowercase + replace
            normalized = old_label.lower().replace(" ", "_").replace("-", "_")
            new_label = label_map.get(normalized)
        
        if new_label is None:
            new_label = old_label  
            unknown_labels[old_label] += 1
        else:
            fixed_count[new_label] += 1
        
        item["label"] = new_label
        total += 1
        f_out.write(json.dumps(item, ensure_ascii=False) + "\n")

#THỐNG KÊ 
print(f" Done! Đã xử lý {total:,} bài báo.")
print("\nPhân phối label sau khi fix:")
for label, count in sorted(fixed_count.items(), key=lambda x: -x[1]):
    print(f"  {label:20s}: {count:,} bài")

if unknown_labels:
    print("\n  Một số label chưa được map:")
    for lbl, cnt in unknown_labels.items():
        print(f"  {lbl}: {cnt} bài")
else:
    print("\n Tất cả label đã được chuẩn hóa thành công!")

print(f"\nFile mới đã lưu tại: {output_file}")