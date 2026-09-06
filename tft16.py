import streamlit as st
from PIL import Image
import re
import unicodedata
import torch
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

# ==========================================
# THUỐC GIẢI: ÉP BỎ QUA KIỂM TRA SSL
# ==========================================
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
old_request = requests.Session.request
def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)
requests.Session.request = new_request
# ==========================================

st.set_page_config(page_title="AI Quét Phường Nha Trang", page_icon="📍", layout="centered")

# ==========================================
# 1. CƠ SỞ DỮ LIỆU & LOGIC XỬ LÝ ĐỊA CHỈ
# ==========================================
NHA_TRANG_WARD_DB = {
    "thong nhat": {
        "name": "Thống Nhất",
        "rules": [
            {"min": 1, "max": 150, "ward": "Vạn Thạnh"},
            {"min": 151, "max": 99999, "ward": "Phương Sài"}
        ]
    },
    "le hong phong": {
        "name": "Lê Hồng Phong",
        "rules": [
            {"min": 1, "max": 200, "ward": "Phước Hải"},
            {"min": 201, "max": 500, "ward": "Phước Tân"},
            {"min": 501, "max": 99999, "ward": "Phước Long"}
        ]
    },
    "thai nguyen": {
        "name": "Thái Nguyên",
        "rules": [
            {"type": "even", "min": 2, "max": 100, "ward": "Phước Tân"},
            {"type": "odd", "min": 1, "max": 99, "ward": "Phương Sài"}
        ]
    },
    "tran phu": {
        "name": "Trần Phú",
        "rules": [
            {"min": 1, "max": 30, "ward": "Xương Huân"},
            {"min": 32, "max": 100, "ward": "Lộc Thọ"}
        ]
    },
    "2 thang 4": {
        "name": "2 Tháng 4",
        "rules": [
            {"min": 1, "max": 200, "ward": "Vạn Thạnh"},
            {"min": 400, "max": 1000, "ward": "Vĩnh Phước"}
        ]
    },
    "hai thang tu": { 
        "name": "2 Tháng 4",
        "rules": [
            {"min": 1, "max": 200, "ward": "Vạn Thạnh"},
            {"min": 400, "max": 1000, "ward": "Vĩnh Phước"}
        ]
    },
    "yersin": {
        "name": "Yersin",
        "rules": [
            {"min": 1, "max": 19, "ward": "Lộc Thọ"},
            {"min": 20, "max": 49, "ward": "Vạn Thắng"}
        ]
    },
    "ba trieu": {
        "name": "Bà Triệu",
        "rules": [
            {"min": 1, "max": 99999, "ward": "Phương Sài"}
        ]
    },
    "luong dinh cua": {
        "name": "Lương Định Của",
        "rules": [
            {"min": 1, "max": 99999, "ward": "Ngọc Hiệp"}
        ]
    },
    "ngo gia tu": {
        "name": "Ngô Gia Tự",
        "rules": [
            {"min": 1, "max": 99999, "ward": "Tân Lập"}
        ]
    }
}

WAREHOUSE_DB = {
    "Phước Long": "NHA TRANG HUB", "Vĩnh Trường": "NHA TRANG HUB", "Vĩnh Nguyên": "NHA TRANG HUB", "Phước Đồng": "NHA TRANG HUB",
    "Vĩnh Lương": "NHA TRANG 02 HUB", "Vĩnh Phương": "NHA TRANG 02 HUB", "Vĩnh Ngọc": "NHA TRANG 02 HUB", "Vĩnh Hòa": "NHA TRANG 02 HUB",
    "Vĩnh Thạnh": "NHA TRANG 03 HUB", "Vĩnh Trung": "NHA TRANG 03 HUB", "Vĩnh Hiệp": "NHA TRANG 03 HUB", "Vĩnh Thái": "NHA TRANG 03 HUB",
    "Phước Hải": "NHA TRANG 04 HUB", "Lộc Thọ": "NHA TRANG 04 HUB", "Tân Tiến": "NHA TRANG 04 HUB", "Tân Lập": "NHA TRANG 04 HUB", "Phước Hòa": "NHA TRANG 04 HUB", "Phước Tân": "NHA TRANG 04 HUB",
    "Vĩnh Phước": "NHA TRANG 05 HUB", "Vĩnh Thọ": "NHA TRANG 05 HUB", "Vĩnh Hải": "NHA TRANG 05 HUB",
    "Xương Huân": "NHA TRANG 06 HUB", "Vạn Thạnh": "NHA TRANG 06 HUB", "Phương Sơn": "NHA TRANG 06 HUB", "Phương Sài": "NHA TRANG 06 HUB", "Vạn Thắng": "NHA TRANG 06 HUB", "Ngọc Hiệp": "NHA TRANG 06 HUB"
}

def get_new_ward(old_ward):
    ward_map = {
        "Vạn Thạnh": "Phường Nha Trang", "Lộc Thọ": "Phường Nha Trang", "Xương Huân": "Phường Nha Trang",
        "Phương Sài": "Phường Tây Nha Trang", "Vạn Thắng": "Phường Tây Nha Trang", "Phương Sơn": "Phường Tây Nha Trang",
        "Phước Tiến": "Phường Nam Nha Trang", "Phước Hòa": "Phường Nam Nha Trang", "Tân Lập": "Phường Nam Nha Trang",
        "Phước Tân": "Phường Nam Nha Trang"
    }
    return ward_map.get(old_ward, "Chưa thay đổi")

def remove_accents(input_str):
    if not input_str:
        return ""
    return ''.join(c for c in unicodedata.normalize('NFD', input_str)
                  if unicodedata.category(c) != 'Mn').lower().strip()

def parse_and_lookup_address(raw_text):
    clean_text = remove_accents(raw_text)
    normalized_text = re.sub(r"ngo gia (ty|tu|tư)", "ngo gia tu", clean_text)
    
    found_street_key = None
    db_street_name = ""
    matched_ward = "Không xác định"
    house_num = 0
    
    for key, data in NHA_TRANG_WARD_DB.items():
        if key in normalized_text:
            found_street_key = key
            db_street_name = data["name"]
            
            parts = normalized_text.split(key)
            before_street = parts[0]
            
            matches = re.findall(r"(\d+)(?!.*\d)", before_street)
            if matches:
                house_num = int(matches[-1])
                
            for rule in data["rules"]:
                rule_type = rule.get("type")
                if rule_type == "even" and house_num % 2 != 0: continue
                if rule_type == "odd" and house_num % 2 == 0: continue
                
                rule_max = rule.get("max", 99999)
                if house_num >= rule["min"] and house_num <= rule_max:
                    matched_ward = rule["ward"]
                    break
            break
            
    if not found_street_key:
        return {"error": "Không tìm thấy tên đường trong CSDL. Vui lòng chụp rõ phần tên đường hơn."}
        
    new_ward = get_new_ward(matched_ward)
    hub = WAREHOUSE_DB.get(matched_ward, "Chưa xác định")
    
    if db_street_name == "Ngô Đến" or "con de" in normalized_text:
        hub = "NHA TRANG 05 HUB"
        
    return {
        "number": house_num,
        "street": db_street_name,
        "ward": matched_ward,
        "new_ward": new_ward,
        "hub": hub,
        "raw_text": raw_text
    }


# ==========================================
# 2. LUỒNG CHẠY GIAO DIỆN CHÍNH
# ==========================================
@st.cache_resource
def load_model():
    config = Cfg.load_config_from_name('vgg_transformer')
    config['device'] = 'cpu'
    return Predictor(config)

st.title("📍 AI Quét Phường - VietOCR")
st.markdown("Hệ thống nhận diện địa chỉ tiếng Việt cực chuẩn.")

with st.spinner("Đang khởi động AI... (Chỉ mất thời gian ở lần đầu tiên)"):
    model = load_model()

st.info("💡 **Mẹo:** Trên điện thoại, khi bấm nút bên dưới, hãy chọn **'Chụp ảnh' (Take Photo)** để mở Camera sau siêu nét của máy nhé!")

# GỌI CAMERA GỐC CỦA ĐIỆN THOẠI HOẶC CHỌN ẢNH TỪ THƯ VIỆN
img_file = st.file_uploader("📸 BẤM VÀO ĐÂY ĐỂ MỞ CAMERA", type=["jpg", "png", "jpeg"])

if img_file is not None:
    st.image(img_file, caption="Ảnh gốc", width=300)
    
    with st.spinner("🧠 AI đang đọc và phân tích địa chỉ..."):
        try:
            image = Image.open(img_file).convert("RGB")
            raw_text = model.predict(image)
            result = parse_and_lookup_address(raw_text)
            
            st.markdown("---")
            if "error" in result:
                st.error(f"❌ Lỗi: {result['error']}")
                st.warning(f"Văn bản AI đọc được: {raw_text}")
            else:
                st.success("✅ Trích xuất thành công!")
                
                col1, col2 = st.columns(2)
                col1.metric("Đường", result["street"])
                col2.metric("Số nhà", result["number"])
                
                col3, col4 = st.columns(2)
                col3.metric("Phường (Cũ)", result["ward"])
                col4.metric("Phường (Mới)", result["new_ward"])
                
                st.info(f"🚚 **Tuyến Kho Nhận: {result['hub']}**")
                
                with st.expander("Xem văn bản gốc AI đọc được"):
                    st.code(raw_text)
                    
        except Exception as e:
            st.error(f"Đã xảy ra lỗi hệ thống: {e}")
