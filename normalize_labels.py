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

inverted_label_map = {v: k for k, v in label_map.items()}

input_file = Path("data/processed/dataset_merged.jsonl")
output_file = Path("data/processed/dataset_normalizedlabel.jsonl")


def old_code():
    with (
        open(input_file, "r", encoding="utf-8") as f_in,
        open(output_file, "w", encoding="utf-8") as f_out,
    ):
        count = 0
        for line in f_in:
            if line.strip():
                item = json.loads(line)
                old_label = item.get("label", "").strip().lower().replace(" ", "_")
                item["label"] = label_map.get(old_label, item["label"])
                f_out.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1


def new_code():
    """
    Chuẩn hóa nhãn trong trường 'labeling' -> 'target_label' dựa trên label_map.
    Loại các bài báo có nội dung rỗng
    Chuyển content: { content: "..." } thành content: { "body_cleaned": "..." }
    """

    with (
        open(input_file, "r", encoding="utf-8") as f_in,
        open(output_file, "w", encoding="utf-8") as f_out,
    ):
        for line in f_in:
            if line.strip():
                item = json.loads(line)
                labeling_field = item.get("labeling", "")
                target_label_field = labeling_field.get("target_label", "")

                has_no_content_content_value = (
                    not item.get("content", "").get("content", "").strip()
                )
                has_body_cleaned_field = "body_cleaned" in item.get("content", {})
                has_content_content_field = "content" in item.get("content", {})

                if (
                    has_no_content_content_value
                    and not has_body_cleaned_field
                    and has_content_content_field
                ):
                    print(
                        f"Warning: Item with ID '{item.get('id', 'unknown')}' has empty content. Skipping item."
                    )
                    continue

                must_change_label = target_label_field in label_map.values()
                if must_change_label:
                    old_label = target_label_field
                    new_label = inverted_label_map.get(old_label, target_label_field)
                    labeling_field["target_label"] = new_label
                    item["labeling"] = labeling_field

                must_change_content_field = (
                    has_content_content_field
                    and not has_body_cleaned_field
                    and not has_no_content_content_value
                )
                if must_change_content_field:
                    item["content"]["body_cleaned"] = item["content"].pop("content")

                f_out.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    new_code()
    print(f"Đã chuẩn hóa: {output_file}")
