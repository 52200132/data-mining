# Cài đặt cho dự án

## 1. Cài poetry bằng pipx

```
pip install pipx
python -m pipx ensurepath
pipx install poetry
```

## 2. Tạo môi trường ảo

```
python -m venv .venv
```

## 3. Cài đặt thư viện

```
poetry config virtualenvs.in-project true
poetry install
```

# Chạy crawl dữ liệu

```
poetry run scrapy crawl vnexpress -a category=bong-da -a label="Thể thao" -a process_id=1 -a output_dir=data/raw/the-thao
```

Tạo file theo mẫu `run_all.example.py`
Ví dụ: tạo `run_all.py` cùng cấp với `run_all.example.py` và chạy

```
poetry run python run_all.py
```
