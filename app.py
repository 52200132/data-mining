"""
app/app.py — Web app phân loại bài báo tiếng Việt
Chạy: streamlit run app/app.py
"""

import pickle
import re
import unicodedata
from pathlib import Path
from collections import Counter

import streamlit as st
import numpy as np

# import underthesea
try:
    from underthesea import word_tokenize

    HAS_UNDERTHESEA = True
except ImportError:
    HAS_UNDERTHESEA = False

# CẤU HÌNH TRANG
st.set_page_config(
    page_title="Phân loại bài báo",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# LOAD MODEL (cache để không reload mỗi lần user nhập)
MODEL_DIR = Path("models")
TIMESTAMP_VERSION = "1778575137"  # Cập nhật khi train lại model để tránh cache cũ


@st.cache_resource
def load_models():
    vec_path = MODEL_DIR / f"vectorizer_{TIMESTAMP_VERSION}.pkl"
    model_path = MODEL_DIR / f"lr_model_{TIMESTAMP_VERSION}.pkl"

    if not vec_path.exists() or not model_path.exists():
        return None, None

    with open(vec_path, "rb") as f:
        vectorizer = pickle.load(f)
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return vectorizer, model


# PREPROCESSING

STOPWORDS = {
    "thì",
    "là",
    "mà",
    "của",
    "và",
    "các",
    "những",
    "được",
    "trong",
    "có",
    "cho",
    "với",
    "về",
    "từ",
    "này",
    "đó",
    "theo",
    "tại",
    "khi",
    "để",
    "đã",
    "sẽ",
    "đang",
    "bị",
    "do",
    "vì",
    "nên",
    "nhưng",
    "còn",
    "hay",
    "hoặc",
    "như",
    "cũng",
    "vẫn",
    "đều",
    "chỉ",
    "rất",
    "một",
    "hai",
    "ba",
    "tôi",
    "bạn",
    "họ",
    "chúng",
    "ta",
    "ông",
    "bà",
    "anh",
    "chị",
    "em",
    "người",
    "năm",
    "ngày",
    "tháng",
    "hôm",
    "nay",
    "đây",
    "kia",
    "ai",
    "gì",
    "nào",
    "đâu",
    "sao",
    "thế",
    "không",
    "chưa",
    "hơn",
    "nhất",
    "nhiều",
    "ít",
    "lại",
    "lên",
    "xuống",
    "ra",
    "vào",
}


def preprocess(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    text = re.sub(r"[^\w\s\u00C0-\u024F\u1E00-\u1EFF]", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    if HAS_UNDERTHESEA:
        text = word_tokenize(text, format="text")
    words = [w for w in text.split() if w not in STOPWORDS and len(w) > 1]
    return " ".join(words)


# RULE-BASED
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
        "bản_án",
        "vi_phạm",
        "khởi_tố",
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
        "thủ_tướng",
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
        "dinh_dưỡng",
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
        "phong_cảnh",
        "ẩm_thực",
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
        "kỳ_thi",
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
        "dna",
        "hành_tinh",
        "vật_lý",
        "hóa_học",
    ],
}

TOPIC_ICONS = {
    "Thể thao": "",
    "Kinh doanh": "",
    "Pháp luật": "",
    "Công nghệ": "",
    "Giải trí": "",
    "Chính trị - Xã hội": "",
    "Sức khỏe": "",
    "Du lịch": "",
    "Giáo dục": "",
    "Khoa học": "",
}


def rule_based_classify(text: str) -> tuple[str, dict]:
    text_lower = text.lower()
    scores = {
        topic: sum(text_lower.count(kw) for kw in kws)
        for topic, kws in TOPIC_KEYWORDS.items()
    }
    best = max(scores, key=scores.get)
    return (best if scores[best] > 0 else "Không xác định"), scores


# du doan ket qua bang LR Model


def predict_lr(text_cleaned: str, vectorizer, model) -> tuple[str, dict]:
    """Trả về (nhãn dự đoán, dict xác suất)"""
    vec = vectorizer.transform([text_cleaned])
    proba = model.predict_proba(vec)[0]
    classes = model.classes_
    prob_dict = dict(zip(classes, proba))
    pred = classes[np.argmax(proba)]
    return pred, prob_dict


# Giao dien


def main():
    st.title("Web app phân loại by Nhóm 26")
    st.title(" Phân loại chủ đề bài báo tiếng Việt")
    st.caption("Nhập tiêu đề + nội dung bài báo => hệ thống tự động phân loại chủ đề")

    # ── Sidebar ──
    with st.sidebar:
        st.header(" Cài đặt")
        method = st.radio(
            "Phương pháp phân loại",
            ["TF-IDF + Logistic Regression", "Rule-based (từ khóa)", "So sánh cả hai"],
            index=0,
        )
        st.divider()
        st.markdown("**Các chủ đề hỗ trợ:**")
        for topic, icon in TOPIC_ICONS.items():
            st.markdown(f"{icon} {topic}")

        st.divider()
        if not HAS_UNDERTHESEA:
            st.warning(
                " `underthesea` chưa cài!!.\n\n"
                "Chạy: `pip install underthesea`\n\n"
                "Độ chính xác sẽ giảm khi không có tách từ."
            )

    # Load model
    vectorizer, model = load_models()
    model_loaded = vectorizer is not None and model is not None

    if not model_loaded and method != "Rule-based (từ khóa)":
        st.warning(
            "Chưa tìm thấy model đã train. "
            "Chạy `python classify/train_model.py` trước, "
            "hoặc chọn **Rule-based** để dùng thử ngay."
        )

    # Input
    st.subheader(" Nhập nội dung bài báo")

    col1, col2 = st.columns([3, 1])
    with col1:
        title_input = st.text_input(
            "Tiêu đề bài báo", placeholder="VD: Arsenal liệu có cú ăn 2 mùa này?"
        )
    with col2:
        st.write("")  # spacer

    content_input = st.text_area(
        "Nội dung bài báo", height=200, placeholder="Dán nội dung bài báo vào đây..."
    )

    # ── Demo articles ──
    with st.expander(" Chọn bài mẫu từ data để test"):
        demo_articles = {
            "Bóng đá (Thể thao)": (
                "Đội tuyển Việt Nam thắng Thái Lan 2-0",
                "Tối qua, đội tuyển quốc gia Việt Nam đã có trận đấu xuất sắc, "
                "đánh bại Thái Lan với tỷ số 2-0 trong trận chung kết AFF Cup. "
                "Hai bàn thắng được ghi bởi Nguyễn Văn A và Trần Văn B. "
                "Huấn luyện viên trưởng cho biết các cầu thủ đã thi đấu hết mình.",
            ),
            "Chứng khoán (Kinh doanh)": (
                "VN-Index tăng mạnh phiên giao dịch hôm nay",
                "Thị trường chứng khoán Việt Nam ghi nhận phiên tăng mạnh khi VN-Index "
                "tăng 15 điểm lên mức 1250. Cổ phiếu ngân hàng và bất động sản dẫn dắt "
                "đà tăng. Dòng tiền ngoại mua ròng 500 tỷ đồng. Các chuyên gia tài chính "
                "nhận định thị trường sẽ tiếp tục tăng trưởng trong quý tới.",
            ),
            "Vaccine (Sức khỏe)": (
                "Bộ Y tế khuyến cáo tiêm vaccine nhắc lại",
                "Bộ Y tế vừa ban hành khuyến cáo về việc tiêm mũi vaccine nhắc lại "
                "cho các nhóm nguy cơ cao. Theo các bác sĩ tại bệnh viện, việc tiêm "
                "nhắc lại giúp tăng cường miễn dịch và phòng ngừa biến chứng. "
                "Các điểm tiêm chủng trên toàn quốc sẽ triển khai từ tuần tới.",
            ),
        }
        demo_choice = st.selectbox("Chọn bài mẫu", list(demo_articles.keys()))
        if st.button("Tải bài mẫu"):
            title_input, content_input = demo_articles[demo_choice]
            st.rerun()

    # Classify button
    if st.button("🔍 Phân loại", type="primary", use_container_width=True):
        combined = f"{title_input} {content_input}".strip()

        if len(combined) < 20:
            st.error("Vui lòng nhập ít nhất 20 ký tự!")
            return

        with st.spinner("Đang xử lý..."):
            cleaned = preprocess(combined)

        st.divider()
        st.subheader("📊 Kết quả phân loại")

        # ── Rule-based ──
        if method in ["Rule-based (từ khóa)", "So sánh cả hai"]:
            rb_pred, rb_scores = rule_based_classify(cleaned)
            icon = TOPIC_ICONS.get(rb_pred, "📰")

            with st.container():
                st.markdown("####  Rule-based")
                if rb_pred != "Không xác định":
                    st.success(f"{icon} **{rb_pred}**")
                else:
                    st.warning(
                        " Không xác định được chủ đề (văn bản quá ngắn hoặc không có từ khóa)"
                    )

                with st.expander("Xem điểm từng chủ đề (rule-based)"):
                    sorted_scores = sorted(rb_scores.items(), key=lambda x: -x[1])
                    for topic, score in sorted_scores:
                        if score > 0:
                            bar = "█" * score
                            st.text(
                                f"{TOPIC_ICONS.get(topic,'')} {topic:25s} {bar} ({score})"
                            )

        # LR Model
        if method in ["TF-IDF + Logistic Regression", "So sánh cả hai"]:
            if model_loaded:
                lr_pred, lr_proba = predict_lr(cleaned, vectorizer, model)
                icon = TOPIC_ICONS.get(lr_pred, "📰")
                confidence = lr_proba[lr_pred] * 100

                with st.container():
                    st.markdown("#### TF-IDF + Logistic Regression")
                    col_a, col_b = st.columns([2, 1])
                    with col_a:
                        confidence_color = (
                            "green"
                            if confidence >= 70
                            else "orange" if confidence >= 50 else "red"
                        )
                        st.markdown(
                            f"<h3 style='color:{confidence_color}'>"
                            f"{icon} {lr_pred}</h3>",
                            unsafe_allow_html=True,
                        )
                    with col_b:
                        st.metric("Độ tin cậy", f"{confidence:.1f}%")

                    # bieu do xac suat
                    with st.expander("Xem xác suất tất cả chủ đề"):
                        sorted_proba = sorted(lr_proba.items(), key=lambda x: -x[1])
                        topics_list = [
                            f"{TOPIC_ICONS.get(t,'')} {t}" for t, _ in sorted_proba
                        ]
                        proba_values = [v for _, v in sorted_proba]

                        import pandas as pd

                        chart_data = pd.DataFrame(
                            {
                                "Chủ đề": topics_list,
                                "Xác suất": proba_values,
                            }
                        ).set_index("Chủ đề")
                        st.bar_chart(chart_data)
            else:
                st.info(
                    " Model chưa được train. Chạy `poetry run classify/train_model.py` trước."
                )

        # ── So sánh ──
        if method == "So sánh cả hai" and model_loaded:
            st.divider()
            rb_pred_final, _ = rule_based_classify(cleaned)
            lr_pred_final, lr_proba_final = predict_lr(cleaned, vectorizer, model)

            st.markdown("### So sánh hai phương pháp")
            c1, c2 = st.columns(2)
            with c1:
                st.info(
                    f"**Rule-based:** {TOPIC_ICONS.get(rb_pred_final,'')} {rb_pred_final}"
                )
            with c2:
                conf = lr_proba_final[lr_pred_final] * 100
                st.success(
                    f"**LR Model:** {TOPIC_ICONS.get(lr_pred_final,'')} {lr_pred_final} ({conf:.0f}%)"
                )

            if rb_pred_final == lr_pred_final:
                st.success(" Cả hai phương pháp **đồng thuận** về chủ đề!")
            else:
                st.warning(
                    " Hai phương pháp **không đồng thuận**. "
                    "Kết quả từ TF-IDF + LR thường đáng tin hơn."
                )

        # Debug: Văn bản đã xử lý
        with st.expander(" Xem văn bản sau tiền xử lý"):
            st.text(cleaned[:500] + ("..." if len(cleaned) > 500 else ""))
            st.caption(f"Số từ sau xử lý: {len(cleaned.split())}")

    # Footer
    st.divider()
    st.caption(
        "📌 Dự án: Phân loại văn bản bài báo | "
        "Trường Đại học Tôn Đức Thắng | 2026 | "
        "Võ Văn Sáng & Đỗ Xuân Thắng"
    )


if __name__ == "__main__":
    main()
