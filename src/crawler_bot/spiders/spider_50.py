import scrapy
from scrapy.http import Response
from ..items import NewsArticleItem


class Spider_50(scrapy.Spider):
    name = "spider50"
    allowed_domains = ["vnexpress.net"]

    bong_da_links = [
        "https://vnexpress.net/hlv-australia-de-cao-viet-nam-truoc-ban-ket-u17-dong-nam-a-5065275.html",
        "https://vnexpress.net/valdano-real-nhu-lop-xe-bi-dam-thung-5065218.html",
        "https://vnexpress.net/cau-thu-tre-indonesia-xin-loi-vi-lam-hoen-o-danh-tieng-dtqg-5065231.html",
        "https://vnexpress.net/psg-gianh-giai-oscar-the-thao-5064947.html",
        "https://vnexpress.net/cau-thu-tre-indonesia-da-kungfu-vao-lung-doi-phuong-5064642.html",
        "https://vnexpress.net/hlv-u17-viet-nam-ngac-nhien-vi-indonesia-khong-chiu-tan-cong-5064617.html",
        "https://vnexpress.net/mourinho-tu-phu-sau-tran-thang-cua-benfica-5064494.html",
        "https://vnexpress.net/ha-arsenal-man-city-gianh-quyen-tu-quyet-o-ngoai-hang-anh-5064409.html",
        "https://vnexpress.net/ronaldo-giup-al-nassr-thang-dam-o-tu-ket-cup-c2-chau-a-5064398.html",
        "https://vnexpress.net/viet-nam-loai-chu-nha-indonesia-o-giai-u17-dong-nam-a-5064379.html",
        "https://vnexpress.net/luat-viet-vi-moi-cua-wenger-lan-dau-cong-nhan-ban-thang-5064313.html",
        "https://vnexpress.net/messi-ghi-ban-quyet-dinh-chien-thang-cho-inter-miami-5064207.html",
        "https://vnexpress.net/atletico-hut-danh-hieu-cup-nha-vua-5064208.html",
        "https://vnexpress.net/hlv-thai-lan-tu-chuc-khi-bi-loai-som-o-giai-u17-dong-nam-a-5064158.html",
        "https://vnexpress.net/cau-thu-clb-malaysia-cuop-cang-de-cuu-dong-doi-5064137.html",
        "https://vnexpress.net/lao-loai-thai-lan-o-giai-u17-dong-nam-a-5064130.html",
        "https://vnexpress.net/lampard-dua-coventry-tro-lai-ngoai-hang-anh-5063970.html",
        "https://vnexpress.net/10-nam-trang-tay-cua-mbappe-o-champions-league-5063908.html",
        "https://vnexpress.net/ronaldo-non-oi-o-tran-thang-cua-al-nassr-5063786.html",
        "https://vnexpress.net/vi-sao-vff-khong-chon-hlv-ngoai-cho-doi-tuyen-nu-5063584.html",
        "https://vnexpress.net/mcmanaman-cau-thu-moi-la-ong-chu-tai-real-5063429.html",
        "https://vnexpress.net/hlv-kim-sang-sik-toi-thanh-cong-vi-duoc-long-cau-thu-viet-nam-5062682.html",
        "https://vnexpress.net/henry-real-phai-nem-thu-thuoc-doc-do-chinh-ho-tao-ra-5063590.html",
        "https://vnexpress.net/messi-mua-mot-clb-o-tay-ban-nha-5063427.html",
        "https://vnexpress.net/xac-dinh-hai-cap-dau-ban-ket-europa-league-5063420.html",
        "https://vnexpress.net/kane-tuyen-chien-voi-psg-5063155.html",
        "https://vnexpress.net/duoc-doi-thu-bieu-ban-thang-sau-khi-hong-phat-den-5063150.html",
        "https://vnexpress.net/ancelotti-xin-y-kien-tong-thong-brazil-ve-viec-goi-neymar-5062873.html",
        "https://vnexpress.net/cuu-thu-mon-arsenal-va-liverpool-thiet-mang-vi-tai-nan-tau-hoa-5063397.html",
        "https://vnexpress.net/viet-nam-thang-10-0-truoc-khi-gap-indonesia-o-u17-dong-nam-a-5063342.html",
    ]
    chung_khoan_links = [
        "https://vnexpress.net/co-phieu-sacombank-nhay-vot-khi-ong-nguyen-duc-thuy-ung-cu-hdqt-5065234.html",
        "https://vnexpress.net/dien-may-xanh-lai-hon-ty-dong-moi-gio-5064859.html",
        "https://vnexpress.net/tong-giam-doc-vpbanks-nhu-cau-vay-ky-quy-cua-nha-dau-tu-hien-rat-lon-5064819.html",
        "https://vnexpress.net/vn-index-len-cao-nhat-mot-thang-ruoi-5064727.html",
        "https://vnexpress.net/loi-nhuan-chung-khoan-vix-giam-hon-60-5064201.html",
        "https://vnexpress.net/ong-do-quang-vinh-shs-muon-lot-top-5-thi-phan-moi-gioi-vao-2030-5063773.html",
        "https://vnexpress.net/dai-gia-thai-nhan-hon-3-200-ty-dong-co-tuc-sau-14-nam-thau-tom-nhua-binh-minh-5063681.html",
        "https://vnexpress.net/co-phieu-the-gioi-di-dong-tang-tran-5063723.html",
        "https://vnexpress.net/chu-tich-rong-viet-neu-kho-khan-cua-cong-ty-chung-khoan-khong-co-ngan-hang-hau-thuan-5063353.html",
        "https://vnexpress.net/co-phieu-nhom-vingroup-noi-song-5063238.html",
        "https://vnexpress.net/chu-tich-phat-dat-ly-giai-viec-mua-thap-ban-cao-co-phieu-cong-ty-5063181.html",
        "https://vnexpress.net/vpbanks-tro-thanh-co-dong-lon-tai-cong-ty-cua-ong-dang-thanh-tam-5062950.html",
        "https://vnexpress.net/loi-nhuan-cua-tcbs-tiep-tuc-tang-truong-nho-mang-cho-vay-5062834.html",
        "https://vnexpress.net/vn-index-len-1-800-diem-5062779.html",
        "https://vnexpress.net/vn-index-tang-manh-ba-phien-lien-tiep-5062291.html",
        "https://vnexpress.net/vn-index-len-cao-nhat-mot-thang-5061858.html",
        "https://vnexpress.net/nhieu-lanh-dao-doanh-nghiep-o-at-mua-ban-co-phieu-5061370.html",
        "https://vnexpress.net/chung-khoan-thien-viet-muon-bau-cuu-ceo-acb-ly-xuan-hai-vao-hoi-dong-quan-tri-5061118.html",
        "https://vnexpress.net/chung-khoan-tang-tro-lai-5060950.html",
        "https://vnexpress.net/co-nen-vao-lai-chung-khoan-sau-tin-xac-nhan-nang-hang-5060257.html",
        "https://vnexpress.net/them-cong-ty-chung-khoan-muon-vao-cau-lac-bo-lai-nghin-ty-5060469.html",
        "https://vnexpress.net/chung-khoan-giam-manh-nhat-hon-nua-thang-qua-5060512.html",
        "https://vnexpress.net/co-phieu-nao-huong-loi-khi-chung-khoan-duoc-nang-hang-5060220.html",
        "https://vnexpress.net/vn-index-tang-ky-luc-5060101.html",
        "https://vnexpress.net/chung-khoan-viet-nam-duoc-nang-hang-5059738.html",
        "https://vnexpress.net/doanh-thu-dien-may-xanh-tang-cao-5059895.html",
        "https://vnexpress.net/vpbanks-dat-muc-tieu-loi-nhuan-6-453-ty-dong-nam-2026-5060103.html",
        "https://vnexpress.net/tien-rot-vao-chung-khoan-thap-nhat-10-thang-5059613.html",
        "https://vnexpress.net/vn-index-giam-3-phien-lien-tiep-5059181.html",
        "https://vnexpress.net/chung-khoan-ky-thuong-dat-muc-tieu-loi-nhuan-ky-luc-hon-7-500-ty-dong-5058800.html",
    ]
    ho_so_pha_an_links = [
        "https://vnexpress.net/cuoc-song-bi-mat-cua-nu-tu-nhan-vuot-nguc-trong-32-nam-lan-tron-5064820.html",
        "https://vnexpress.net/sau-cu-lua-tinh-va-man-kich-thua-ke-80-trieu-bang-cua-nguoi-mau-noi-tieng-5063861.html",
        "https://vnexpress.net/ky-an-bi-an-20-nam-ve-thi-the-bi-troi-trong-can-ho-tang-13-5063339.html",
        "https://vnexpress.net/cu-nga-sau-cuoc-cai-va-vi-cho-dau-xe-5062870.html",
        "https://vnexpress.net/boc-tran-nhung-cuoc-cuu-ho-gia-truc-loi-chuc-trieu-usd-tren-dinh-everest-5062371.html",
        "https://vnexpress.net/ke-hoach-tham-nhap-giao-phai-pha-duong-day-boc-lot-tinh-duc-5061943.html",
        "https://vnexpress.net/ke-san-gai-mai-dam-30-nam-an-minh-duoi-vo-boc-binh-di-5061056.html",
        "https://vnexpress.net/ke-giet-nguoi-gia-danh-nan-nhan-nhan-tin-voi-gia-dinh-5060645.html",
        "https://vnexpress.net/vu-ba-lao-ban-chet-hang-xom-den-go-cua-gay-phan-no-5060177.html",
        "https://vnexpress.net/ke-vuot-nguc-duoc-12-ban-gai-che-cho-trong-907-ngay-dao-tau-5059676.html",
        "https://vnexpress.net/am-muu-cua-nguoi-chong-ngoai-tinh-voi-co-giup-viec-5059240.html",
        "https://vnexpress.net/hanh-trinh-pha-duong-day-tuon-lon-benh-ra-thi-truong-5058717.html",
        "https://vnexpress.net/phac-hoa-cua-cuu-canh-sat-giup-phat-hien-me-min-khet-tieng-trung-quoc-5057400.html",
        "https://vnexpress.net/chiec-mu-dam-mo-hoi-khien-ke-hiep-dam-hang-loat-bai-lo-5058321.html",
        "https://vnexpress.net/vu-an-thi-the-giau-duoi-bon-tam-khien-nuoc-anh-phai-viet-lai-luat-5057821.html",
        "https://vnexpress.net/ten-sat-nhan-hang-loat-lo-tay-tung-tich-qua-gameshow-truyen-hinh-5057344.html",
        "https://vnexpress.net/vu-am-sat-ong-trum-thoi-trang-cua-quy-ba-gucci-5056894.html",
        "https://vnexpress.net/tham-hoa-sap-toa-nha-bach-hoa-trong-20-giay-khien-502-nguoi-tu-nan-5055694.html",
        "https://vnexpress.net/vu-mat-tich-bi-an-cua-nu-sinh-sau-tai-nan-xe-hoi-5055253.html",
        "https://vnexpress.net/bi-kich-khi-o-chung-nha-voi-ga-dong-nghiep-cuong-ghen-5054810.html",
        "https://vnexpress.net/hanh-trinh-vach-toi-nguoi-bo-ngoai-tinh-cua-cau-be-11-tuoi-5054376.html",
        "https://vnexpress.net/con-ghen-cua-ong-lao-khi-tranh-gianh-nu-than-trong-mong-5053947.html",
        "https://vnexpress.net/bang-chung-tu-coi-chet-vach-toi-ga-chong-gioi-dong-kich-5053018.html",
        "https://vnexpress.net/tranh-cai-vu-chu-nha-dam-chet-tinh-dich-gay-roi-giua-dem-5052564.html",
        "https://vnexpress.net/ke-sat-nhan-tu-chui-dau-vao-luoi-sau-15-nam-ngo-thoat-toi-5052140.html",
        "https://vnexpress.net/nu-quan-tham-nga-ngua-vi-me-biet-thu-tram-ty-5051611.html",
        "https://vnexpress.net/tham-an-cua-co-gai-bi-bat-coc-nhung-911-khong-ung-cuu-5051215.html",
        "https://vnexpress.net/thu-doan-du-do-thieu-nu-den-trang-trai-biet-lap-cua-ty-phu-au-dam-5051212.html",
        "https://vnexpress.net/ky-an-nhung-goi-hang-chua-thi-the-gay-rung-dong-canada-5050226.html",
        "https://vnexpress.net/bi-kich-sau-hai-lan-mo-cua-cho-nguoi-la-cua-nu-doanh-nhan-thanh-dat-5049808.html",
    ]
    song_khoe_links = [
        "https://vnexpress.net/sai-lam-khi-bao-quan-com-thua-trong-tu-lanh-gay-ngo-doc-5064888.html",
        "https://vnexpress.net/chuyen-gia-dinh-duong-goi-y-5-loai-trai-cay-giup-on-dinh-duong-huyet-5064669.html",
        "https://vnexpress.net/chang-beo-dap-xe-giam-20-kg-trong-100-ngay-5063900.html",
        "https://vnexpress.net/xuat-tinh-hon-21-lan-trong-thang-co-the-ngua-ung-thu-tuyen-tien-liet-5064603.html",
        "https://vnexpress.net/5-nhom-nguoi-nen-han-che-uong-nuoc-mia-5065098.html",
        "https://vnexpress.net/nguy-co-nhiem-rsv-o-benh-nhan-dai-thao-duong-5065126.html",
        "https://vnexpress.net/bac-si-nhat-day-lui-benh-tat-nho-25-nam-khong-an-duong-muoi-5064535.html",
        "https://vnexpress.net/co-che-tam-nong-lanh-giup-nguoi-nhat-song-tho-5064647.html",
        "https://vnexpress.net/an-toi-muon-am-tham-gay-hai-co-the-ra-sao-5064214.html",
        "https://vnexpress.net/nang-nong-uong-bia-co-giai-duoc-nhiet-5060943.html",
        "https://vnexpress.net/bi-quyet-giup-nu-blogger-giam-18-kg-trong-3-thang-5062603.html",
        "https://vnexpress.net/3-thoi-quen-vang-giup-keo-dai-tuoi-tho-them-gan-10-nam-5062551.html",
        "https://vnexpress.net/5-thuc-pham-tot-cho-mat-nen-an-moi-ngay-5064163.html",
        "https://vnexpress.net/co-nen-hup-can-nuoc-pho-5063534.html",
        "https://vnexpress.net/chang-trai-khoi-xo-hoa-gan-nho-bo-thoi-quen-uong-tra-sua-5063656.html",
        "https://vnexpress.net/so-thich-an-noi-tang-de-lao-hoa-nguoc-cua-minh-tinh-dai-loan-5063261.html",
        "https://vnexpress.net/4-lam-tuong-khien-nguoi-benh-than-cang-duong-sinh-cang-yeu-5063482.html",
        "https://vnexpress.net/sai-lam-khi-cham-soc-da-mua-nang-nong-5064028.html",
        "https://vnexpress.net/an-tao-hay-cam-tot-hon-cho-duong-huyet-5063123.html",
        "https://vnexpress.net/lam-dung-do-uong-giai-nhiet-mua-he-gay-hai-than-5062722.html",
        "https://vnexpress.net/co-gai-dot-22-kg-mo-nho-nhay-aerobic-5061770.html",
        "https://vnexpress.net/co-nen-gop-bua-sang-voi-trua-5060568.html",
        "https://vnexpress.net/bac-si-dai-loan-canh-bao-3-mon-an-duong-pho-nhieu-muoi-tan-pha-than-5062407.html",
        "https://vnexpress.net/cach-uong-nuoc-tot-cho-tieu-hoa-5063654.html",
        "https://vnexpress.net/5-cong-dung-cua-vitamin-k-voi-suc-khoe-5063627.html",
        "https://vnexpress.net/bi-quyet-giup-nguoi-nhat-co-tuoi-tho-trung-binh-hang-dau-the-gioi-5058885.html",
        "https://vnexpress.net/an-nhieu-do-ngot-co-gay-suy-than-5057679.html",
        "https://vnexpress.net/chuyen-gia-chi-cach-rua-rau-don-gian-giup-loai-bo-thuoc-tru-sau-5062571.html",
        "https://vnexpress.net/cach-an-uong-giup-cuu-hoa-hau-han-quoc-tre-mai-khong-gia-5062625.html",
        "https://vnexpress.net/cai-gia-them-mot-ngay-song-cua-nguoi-benh-ung-thu-5057402.html",
    ]
    am_thuc_links = [
        "https://vnexpress.net/quan-banh-xeo-da-nang-hon-30-nam-giu-chan-thuc-khach-5064818.html",
        "https://vnexpress.net/mon-sup-khien-hai-nuoc-cung-nhan-lam-cha-de-5064816.html",
        "https://vnexpress.net/ly-do-gioi-tre-han-me-man-am-thuc-trung-quoc-5064654.html",
        "https://vnexpress.net/nha-hang-khong-thuc-don-khach-den-an-bang-niem-tin-5060530.html",
        "https://vnexpress.net/quan-xoi-ha-noi-khien-khach-xep-hang-vao-an-5061651.html",
        "https://vnexpress.net/bien-ba-khia-lot-thanh-mon-rieu-la-mieng-tai-ca-mau-5062280.html",
        "https://vnexpress.net/bep-truong-hatoyama-lam-dai-su-van-hoa-am-thuc-nhat-ban-tai-viet-nam-5057198.html",
        "https://vnexpress.net/an-thang-den-ngu-sac-ban-dem-o-ha-giang-5050445.html",
        "https://vnexpress.net/10-mon-an-do-nhat-the-gioi-5061810.html",
        "https://vnexpress.net/oc-be-tu-mon-binh-dan-thanh-dac-san-phap-5061457.html",
        "https://vnexpress.net/7-quan-ca-phe-o-ha-noi-duoc-tap-chi-am-thuc-my-goi-y-5061230.html",
        "https://vnexpress.net/mon-an-thach-thuc-nhat-the-gioi-duoc-lam-nhu-the-nao-5060908.html",
        "https://vnexpress.net/so-phan-cua-com-ga-hai-nam-o-dong-nam-a-5060944.html",
        "https://vnexpress.net/khach-vay-kin-quay-ban-trung-cut-u-muoi-kieu-trung-quoc-5059669.html",
        "https://vnexpress.net/10-mon-banh-mi-kep-ngon-nhat-the-gioi-5059087.html",
        "https://vnexpress.net/thuong-thuc-am-thuc-nhat-ban-tai-sabi-sky-omakase-5060531.html",
        "https://vnexpress.net/coc-ca-phe-ban-o-bangkok-duoc-tao-ra-nhu-the-nao-5059020.html",
        "https://vnexpress.net/mon-gi-tu-khoai-duoc-u-chan-3-ngay-phoi-12-nang-5058594.html",
        "https://vnexpress.net/tuc-chieu-dai-con-re-100-mon-trong-40-ngay-cua-me-vo-an-do-5057788.html",
        "https://vnexpress.net/ly-do-mi-ramen-nhat-ban-man-den-kho-hieu-5058314.html",
        "https://vnexpress.net/quan-ca-phe-cho-khach-ngam-tau-hoa-chay-qua-o-ga-hue-5057891.html",
        "https://vnexpress.net/vi-sao-nguoi-nhat-coi-trong-su-yen-tinh-nhung-hup-mi-thanh-tieng-5057589.html",
        "https://vnexpress.net/thit-trau-gac-bep-thuong-duoc-uop-gia-vi-nao-5057155.html",
        "https://vnexpress.net/quan-mi-michelin-binh-dan-khien-khach-xep-hang-o-bangkok-5055463.html",
        "https://vnexpress.net/ngam-thac-nuoc-cao-6-5-m-trong-quan-ca-phe-o-tp-hcm-5056425.html",
        "https://vnexpress.net/lau-phan-bo-mon-dac-san-quy-chau-5056492.html",
        "https://vnexpress.net/goc-toi-sau-can-bep-sao-michelin-5055898.html",
        "https://vnexpress.net/mon-da-xao-toi-ot-gay-sot-tai-trung-quoc-5055654.html",
        "https://vnexpress.net/bun-bung-la-mon-an-gi-o-ha-noi-5054635.html",
        "https://vnexpress.net/quan-bun-rieu-pho-co-nang-cap-sau-vu-khach-trung-quoc-che-ban-5054786.html",
    ]

    def __init__(
        self,
        category=None,
        label=None,
        process_id=None,
        output_dir=None,
        *args,
        **kwargs,
    ):
        # Đừng quên gọi super(), nó rất quan trọng để Scrapy hoạt động đúng
        super(Spider_50, self).__init__(*args, **kwargs)

        # Gán biến truyền vào
        if category is None:
            raise ValueError("Category is required")
        if label is None:
            raise ValueError("Label is required")
        if process_id is None:
            raise ValueError("Process ID is required")
        if output_dir is None:
            raise ValueError("Target directory is required")
        self.category = category
        self.label = label
        self.process_id = process_id
        self.output_dir = output_dir

        # Tạo link xuất phát dựa trên biến truyền vào
        self.start_urls = (
            self.bong_da_links
            + self.chung_khoan_links
            + self.ho_so_pha_an_links
            + self.song_khoe_links
            + self.am_thuc_links
        )

    def parse(self, response: Response):
        for url in self.start_urls:
            yield response.follow(url, self.parse_article)

    def parse_article(self, response: Response):
        """
        Lấy các dữ liệu cần thiết của bài báo
        """
        item = NewsArticleItem()
        metadata = {
            "doc_id": response.url.split("-")[-1].replace(
                ".html", ""
            ),  # Ví dụ cách lấy ID từ URL
            "source_name": "VnExpress",
            "source_url": response.url,
            "publish_date": response.css(
                "div.header-content.width_common > span.date::text"
            ).get(),  # Cần format lại ISO 8601
            "author": "VnExpress",
        }

        paragraphs = response.css("article.fck_detail p.Normal::text").getall()
        content = " ".join(paragraphs).strip()

        content = {
            "title": response.css("h1.title-detail::text").get(),
            "sapo": response.css("p.description::text").get(),
            "content": content,
            "word_count": len(content.split()),
        }

        labeling = {
            "original_category": response.css("ul.breadcrumb li a::text").getall(),
            "target_label": self.label,  # Logic phân loại của bạn
            "tags": response.css('meta[name="keywords"]::attr(content)').getall(),
            "is_multilabel": False,
        }

        item["metadata"] = metadata
        item["content"] = content
        item["labeling"] = labeling

        yield item
        pass
