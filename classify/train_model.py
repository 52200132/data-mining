"""
classify/train_model.py
Pipeline huấn luyện mô hình phân loại bài báo
Bước 1: Rule-based (baseline)
Bước 2: TF-IDF + Logistic Regression
Bước 3: So sánh kết quả

Chạy: poetry run python classify/train_model.py
"""

from datetime import datetime
import json
import pickle
import numpy as np
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

TIMESTAMP_VERSION = "1778567005"

NOW_TIMESTAMP = int(datetime.now().timestamp())


# load dataset da xu ly
def load_dataset(path: str = f"data/processed/dataset_final_{TIMESTAMP_VERSION}.jsonl"):
    texts, labels = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line.strip())
            if item.get("text_cleaned") and item.get("label"):
                texts.append(item["text_cleaned"])
                labels.append(item["label"])
    print(f"Đã load {len(texts):,} bài | {len(set(labels))} chủ đề")
    return texts, labels


# RULE-BASED CLASSIFIER (Baseline)
TOPIC_KEYWORDS = {
    "Thể thao": [
        "bóng_đá",
        "cầu_thủ",
        "giải_đấu",
        "trận_đấu",
        "vận_động_viên",
        "huy_chương",
        "thể_thao",
        "bàn_thắng",
        "câu_lạc_bộ",
        "hlv",
        "vô_địch",
        "tuyển",
        "huấn_luyện_viên",
        "sân_vận_động",
        "tennis",
        "bơi_lội",
        "điền_kinh",
        "bóng_rổ",
        "cầu_lông",
        "đua_xe",
    ],
    "Kinh doanh": [
        "doanh_nghiệp",
        "thị_trường",
        "chứng_khoán",
        "tài_chính",
        "ngân_hàng",
        "lợi_nhuận",
        "đầu_tư",
        "xuất_khẩu",
        "gdp",
        "cổ_phiếu",
        "doanh_thu",
        "kinh_doanh",
        "bất_động_sản",
        "khởi_nghiệp",
        "startup",
        "thương_mại",
        "nhập_khẩu",
    ],
    "Pháp luật": [
        "tòa_án",
        "bị_cáo",
        "xét_xử",
        "tội_phạm",
        "hình_sự",
        "điều_tra",
        "bắt_giữ",
        "luật",
        "phiên_tòa",
        "kết_án",
        "công_an",
        "cơ_quan_điều_tra",
        "bản_án",
        "vi_phạm",
        "khởi_tố",
        "truy_tố",
        "thi_hành_án",
        "phạt_tù",
    ],
    "Công nghệ": [
        "công_nghệ",
        "phần_mềm",
        "trí_tuệ_nhân_tạo",
        "smartphone",
        "ai",
        "internet",
        "robot",
        "ứng_dụng",
        "kỹ_thuật_số",
        "chip",
        "điện_thoại",
        "máy_tính",
        "dữ_liệu",
        "chatgpt",
        "mạng_xã_hội",
        "iphone",
        "android",
        "cybersecurity",
        "blockchain",
    ],
    "Giải trí": [
        "nghệ_sĩ",
        "âm_nhạc",
        "phim",
        "ca_sĩ",
        "diễn_viên",
        "showbiz",
        "nhạc",
        "điện_ảnh",
        "hoa_hậu",
        "sao",
        "concert",
        "album",
        "gameshow",
        "truyền_hình",
        "đạo_diễn",
        "rapper",
        "idol",
        "liveshow",
        "mv",
        "phim_truyện",
    ],
    "Chính trị - Xã hội": [
        "chính_phủ",
        "bộ_trưởng",
        "nghị_quyết",
        "chính_sách",
        "xã_hội",
        "dân_sinh",
        "giao_thông",
        "quy_định",
        "nhà_nước",
        "quốc_hội",
        "ủy_ban",
        "hội_đồng",
        "nghị_định",
        "thủ_tướng",
        "đề_xuất",
        "chủ_tịch",
        "bộ",
        "sở",
        "phường_xã",
    ],
    "Sức khỏe": [
        "bệnh_viện",
        "bác_sĩ",
        "bệnh_nhân",
        "sức_khỏe",
        "y_tế",
        "vaccine",
        "điều_trị",
        "thuốc",
        "dịch_bệnh",
        "phẫu_thuật",
        "ung_thư",
        "tim_mạch",
        "đái_tháo_đường",
        "dinh_dưỡng",
        "covid",
        "virus",
        "kháng_sinh",
        "nội_soi",
        "xét_nghiệm",
    ],
    "Du lịch": [
        "du_lịch",
        "khách_sạn",
        "điểm_đến",
        "tour",
        "resort",
        "biển",
        "di_tích",
        "tham_quan",
        "danh_lam",
        "khách_du_lịch",
        "đặt_phòng",
        "visa",
        "hành_lý",
        "phong_cảnh",
        "ẩm_thực",
        "homestay",
        "cảnh_quan",
        "vé_máy_bay",
        "checkin",
        "backpacker",
    ],
    "Giáo dục": [
        "học_sinh",
        "sinh_viên",
        "trường",
        "giáo_viên",
        "đại_học",
        "thi_cử",
        "giáo_dục",
        "chương_trình",
        "tuyển_sinh",
        "bộ_giáo_dục",
        "học_bổng",
        "điểm_số",
        "kỳ_thi",
        "phụ_huynh",
        "lớp_học",
        "thpt",
        "thcs",
        "trung_học",
        "đề_thi",
        "tiến_sĩ",
    ],
    "Khoa học": [
        "nghiên_cứu",
        "khoa_học",
        "phát_hiện",
        "vũ_trụ",
        "gen",
        "tế_bào",
        "thí_nghiệm",
        "nhà_khoa_học",
        "công_trình",
        "dna",
        "hành_tinh",
        "thiên_văn",
        "vật_lý",
        "hóa_học",
        "sinh_học",
        "tiến_hóa",
        "biến_đổi_khí_hậu",
        "năng_lượng",
        "phân_tử",
        "não",
    ],
}


# ham rule-base
def rule_based_classify(text: str) -> tuple[str, dict]:
    text_lower = text.lower()
    scores = {
        topic: sum(text_lower.count(kw) for kw in keywords)
        for topic, keywords in TOPIC_KEYWORDS.items()
    }
    best_topic = max(scores, key=scores.get)
    # neu ko co tu khoa nao khop thi la khong xac dinh
    if scores[best_topic] == 0:
        return "Không xác định", scores
    return best_topic, scores


def evaluate_rule_based(texts: list, labels: list, sample_size: int = 2000):
    """Đánh giá rule-based trên mẫu ngẫu nhiên"""
    print("\n" + "-" * 50)
    print("Step 1: RULE-BASED Quy Tac")
    print(" " * 50)

    # lay mau danh gia nhanh
    n = min(sample_size, len(texts))
    indices = np.random.choice(len(texts), n, replace=False)
    sample_texts = [texts[i] for i in indices]
    sample_labels = [labels[i] for i in indices]

    predictions = [rule_based_classify(t)[0] for t in sample_texts]

    # tinh accuracy
    correct = sum(p == l for p, l in zip(predictions, sample_labels))
    accuracy = correct / n

    print(f"Đánh giá trên {n:,} bài ngẫu nhiên:")
    print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    print(
        "\n Rule-based thường đạt 50-70% — đây là baseline để so sánh\n"
        "     Mô hình TF-IDF+LR sẽ vượt trội hơn nhiều."
    )
    return accuracy


# TF-IDF + LOGISTIC REGRESSION
def train_tfidf_lr(
    texts: list,
    labels: list,
    test_size: float = 0.2,
    max_features: int = 50000,
):
    """
    Huấn luyện TF-IDF vectorizer + Logistic Regression.
    Trả về (vectorizer, model, X_test_vec, y_test, y_pred)
    """
    print("\n" + "-" * 50)
    print("Step 2: TF-IDF + LOGISTIC REGRESSION")
    print("-" * 50)

    # chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=test_size,
        random_state=42,
        stratify=labels,
    )
    print(f"Train: {len(X_train):,} bài | Test: {len(X_test):,} bài")

    # sublinear_tf=True: dung log(tf) thay vi tf thô se giam anh huong tu xuat hien qua nhieu
    # min_df=2: bỏ noise
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,  # bo tu xuat hien hon 95% vi qua pho bien ko phan biet dc
        sublinear_tf=True,
        analyzer="word",
    )
    print(f"\nTF-IDF vectorizing (max {max_features:,} features)...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    print(f"Feature matrix: {X_train_vec.shape[0]:,} × {X_train_vec.shape[1]:,}")

    # max_iter=1000: dam bao hoi tu
    lr_model = LogisticRegression(
        C=5.0,
        max_iter=1000,
        solver="lbfgs",
        class_weight="balanced",  # can bang khi so bai cua moi chu de co su chenh lech
        random_state=42,
        # n_jobs=-1, khi chay code thi do skl phien ban moi nhat khong con dung tham so nay nua, khong anh huong code, comment de nhin cmd dep
    )
    print("\n Đang Train Logistic Regression")
    lr_model.fit(X_train_vec, y_train)

    # du doan va danh gia
    y_pred = lr_model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)

    print(f"\n KẾT QUẢ TRÊN TẬP TEST:")
    print(f"  Accuracy : {acc:.4f} ({acc*100:.1f}%)")
    print(f"  F1-Macro : {f1_macro:.4f} ({f1_macro*100:.1f}%)")
    print("\nChi tiết từng chủ đề:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Cross-validation (5-fold)
    print("Cross-validation (5-fold)...")
    cv_scores = cross_val_score(
        lr_model, X_train_vec, y_train, cv=5, scoring="accuracy", n_jobs=-1
    )
    print(f"  CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    return vectorizer, lr_model, X_test_vec, y_test, y_pred


# VISUALIZATIONS
def plot_confusion_matrix(y_test, y_pred, class_names: list, output_dir: Path):
    cm = confusion_matrix(y_test, y_pred, labels=class_names)

    # Normalize để hiển thị tỉ lệ %
    cm_normalized = cm.astype(float) / cm.sum(axis=1, keepdims=True)

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    # Raw counts
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=axes[0],
    )
    axes[0].set_title("Confusion Matrix (Số lượng)", fontsize=14)
    axes[0].set_ylabel("Thực tế")
    axes[0].set_xlabel("Dự đoán")
    axes[0].tick_params(axis="x", rotation=45)

    # Normalized
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=axes[1],
    )
    axes[1].set_title("Confusion Matrix (Tỉ lệ %)", fontsize=14)
    axes[1].set_ylabel("Thực tế")
    axes[1].set_xlabel("Dự đoán")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    path = output_dir / f"confusion_matrix_{NOW_TIMESTAMP}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"\n Confusion matrix đã lưu: {path}")


def plot_top_keywords(
    vectorizer, model, class_names: list, output_dir: Path, top_n: int = 15
):
    """Hiển thị top từ quan trọng nhất cho mỗi chủ đề"""
    features = vectorizer.get_feature_names_out()
    n_classes = len(class_names)
    cols = 2
    rows = (n_classes + 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4))
    axes = axes.flatten()

    for i, (ax, class_name) in enumerate(zip(axes, class_names)):
        coef = model.coef_[i]
        top_indices = np.argsort(coef)[-top_n:][::-1]
        top_features = [features[j] for j in top_indices]
        top_values = [coef[j] for j in top_indices]

        ax.barh(range(top_n), top_values[::-1], color="steelblue")
        ax.set_yticks(range(top_n))
        ax.set_yticklabels(top_features[::-1], fontsize=9)
        ax.set_title(f"{class_name}", fontsize=11, fontweight="bold")
        ax.set_xlabel("Hệ số LR")

    # Tat axes du thua
    for ax in axes[n_classes:]:
        ax.set_visible(False)

    plt.suptitle("Top từ đặc trưng mỗi chủ đề (TF-IDF + LR)", fontsize=14, y=1.01)
    plt.tight_layout()
    path = output_dir / f"top_keywords_{NOW_TIMESTAMP}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"Top keywords đã lưu: {path}")


# LƯU MODEL Mo HINH
def save_model(vectorizer, model, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"vectorizer_{NOW_TIMESTAMP}.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(output_dir / f"lr_model_{NOW_TIMESTAMP}.pkl", "wb") as f:
        pickle.dump(model, f)
    print(f"\n Model mo hinh đã lưu tại: {output_dir}/")


# MAIN
if __name__ == "__main__":
    np.random.seed(42)

    MODEL_DIR = Path("models")
    MODEL_DIR.mkdir(exist_ok=True)

    # Load data
    texts, labels = load_dataset(
        f"data/processed/dataset_final_{TIMESTAMP_VERSION}.jsonl"
    )
    class_names = sorted(set(labels))

    # Phan phoi nhan data
    from collections import Counter

    label_dist = Counter(labels)
    print("\nPhân phối nhãn:")
    for lbl, cnt in sorted(label_dist.items(), key=lambda x: -x[1]):
        print(f"  {lbl:25s}: {cnt:,} bài")

    # Step 1: Rule-based
    rb_accuracy = evaluate_rule_based(texts, labels, sample_size=2000)

    # Steo 2: TF-IDF + LR
    vectorizer, model, X_test_vec, y_test, y_pred = train_tfidf_lr(texts, labels)

    # Step 3: Visualize
    plot_confusion_matrix(y_test, y_pred, class_names, MODEL_DIR)
    plot_top_keywords(vectorizer, model, class_names, MODEL_DIR)

    #  So sanh
    lr_acc = accuracy_score(y_test, y_pred)
    print("\n" + "=" * 60)
    print("SO SÁNH KẾT QUẢ")
    print("=" * 60)
    print(f"  Rule-based accuracy    : {rb_accuracy*100:.1f}%")
    print(f"  TF-IDF + LR accuracy   : {lr_acc*100:.1f}%")
    print(f"  Cải tiến               : +{(lr_acc - rb_accuracy)*100:.1f}%")

    # ── Lưu model ──
    save_model(vectorizer, model, MODEL_DIR)
    print("\n Done by Thang va Sang (52200145)!! Chạy: streamlit run app/app.py")
