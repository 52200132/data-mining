import json
import glob
from pathlib import Path
from collections import defaultdict

# Các topic gộp 
topics = {
    "giai-tri": "data/raw/giai-tri",
    "kinh-doanh": "data/raw/kinh-doanh",
    "chinh-tri-xa-hoi": "data/raw/chinh-tri-xa-hoi"
}

print(" Bắt đầu gộp riêng từng topic...\n")

for topic_name, folder_path in topics.items():
    merged_data = []
    files = glob.glob(f"{folder_path}/*.jsonl")
    
    if not files:
        print(f"Không tìm thấy file nào trong: {folder_path}")
        continue
    
    print(f"Đang gộp topic: **{topic_name}** ({len(files)} file)")
    
    for file_path in files:
        file_name = Path(file_path).name
        count = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        item = json.loads(line)
                        # Thêm thông tin topic gốc
                        if 'labeling' not in item:
                            item['labeling'] = {}
                        item['labeling']['crawl_topic'] = topic_name
                        merged_data.append(item)
                        count += 1
        except Exception as e:
            print(f"    Lỗi file {file_name}: {e}")
            continue
        
        print(f"   => {file_name}: {count} bài")
    
    # Tạo thư mục merged 
    output_dir = Path("data/raw/merged")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"merged_{topic_name}.jsonl"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in merged_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"   => Hoàn thành {topic_name}: {len(merged_data)} bài → {output_file}\n")

print("="*70)
print("GỘP RIÊNG TỪNG TOPIC XONG!")
print("="*70)