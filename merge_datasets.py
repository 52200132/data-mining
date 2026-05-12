import json
from pathlib import Path

def merge_all_sources():
    all_items = []
    print(" merge dữ liệu VnExpress + báo Thanh Niên...\n")

    # Merge toàn bộ dữ liệu VnExpress
    vnexpress_count = 0
    for jsonl_file in Path("data/raw").rglob("*.jsonl"):
        if "thanhnien" in jsonl_file.name.lower():  
            continue
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    # Đảm bảo có trường "label"
                    if "label" not in item and "labeling" in item:
                        item["label"] = item["labeling"].get("target_label")
                    all_items.append(item)
                    vnexpress_count += 1

    print(f" Đã đọc {vnexpress_count:,} bài từ VnExpress")

    # Merge dữ liệu Thanh Niên 
    thanh_nien_count = 0
    thanh_nien_files = list(Path("data/raw").rglob("*thanhnien*.jsonl")) + \
                    list(Path(".").rglob("*thanhnien*.jsonl"))  # tìm linh hoạt

    for file_path in thanh_nien_files:
        print(f" Đang đọc: {file_path.name}")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    # Đảm bảo có trường "label"
                    if "label" not in item and "labeling" in item:
                        item["label"] = item["labeling"].get("target_label")
                    all_items.append(item)
                    thanh_nien_count += 1

    print(f" Đã đọc {thanh_nien_count:,} bài từ Thanh Niên")

    # Lưu file merged
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "dataset_merged.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    print("\n" + "="*60)
    print(" MERGE HOÀN THÀNH!")
    print(f"Tổng số bài: {len(all_items):,}")
    print(f"   - VnExpress : {vnexpress_count:,}")
    print(f"   - Thanh Niên: {thanh_nien_count:,}")
    print(f"File output: {output_file}")
    print("="*60)

if __name__ == "__main__":
    merge_all_sources()