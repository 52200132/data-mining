def format_vnexpress(date_str: str) -> str:
    """
    Xử lý chuỗi ngày tháng đặc thù của VnExpress
    Ví dụ: 'Thứ sáu, 12/4/2026, 21:00 (GMT+7)'
    """
    temp = date_str.split(", ")
    return temp[1] + ", " + temp[2]


# Mapping domain với hàm xử lý tương ứng
DOMAIN_FORMATTERS = {"vnexpress.net": format_vnexpress}


def format_date(date_str: str, domain: str) -> str:
    """
    Chuẩn hóa về dạng DD/MM/YYYY, HH:MM (GMT+7)
    """
    formatter = DOMAIN_FORMATTERS.get(domain)
    if formatter:
        return formatter(date_str)
    raise ValueError(f"Không có formatter cho domain: {domain}")
