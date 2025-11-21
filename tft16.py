import streamlit as st
import itertools

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="TFT Set 16: Ryze Exodia Tool", page_icon="🧙‍♂️", layout="wide")

# --- DỮ LIỆU SET 16 (CẬP NHẬT) ---
REGION_DATA = {
    "Bilgewater":   {"thresholds": [3, 5, 7, 10]},
    "Demacia":      {"thresholds": [3, 5, 7, 11]},
    "Freljord":     {"thresholds": [3, 5, 7]},
    "Ionia":        {"thresholds": [3, 5, 7, 10]},
    "Ixtal":        {"thresholds": [3, 5, 7]},
    "Noxus":        {"thresholds": [3, 5, 7, 10]},
    "Piltover":     {"thresholds": [3, 5, 7, 9]}, 
    "Shadow Isles": {"thresholds": [2, 3, 4, 5]},
    "Shurima":      {"thresholds": [2, 3, 4, 6]},
    "Targon":       {"thresholds": [1, 2, 3, 4]}, # Kích mốc 1
    "Void":         {"thresholds": [2, 4, 6, 9]},
    "Yordle":       {"thresholds": [2, 4, 6, 8]},
    "Zaun":         {"thresholds": [3, 5, 7]}
}

CLASS_DATA = {
    "Bruiser": [2, 4, 6], "Defender": [2, 4, 6], "Invoker": [2, 4, 6],
    "Slayer": [2, 4, 6], "Gunslinger": [2, 4, 6], "Arcanist": [2, 4, 6],
    "Warden": [2, 3, 4], "Juggernaut": [2, 4, 6], "Longshot": [2, 4]
}

# DANH SÁCH TƯỚNG (PHÂN LOẠI ĐỘ KHÓ)
ALL_UNITS = [
    # --- DỄ (1) ---
    {"name": "Vi",           "traits": ["Piltover", "Zaun", "Defender"], "diff": 1},
    {"name": "Xin Zhao",     "traits": ["Demacia", "Ionia", "Warden"], "diff": 1},
    {"name": "Poppy",        "traits": ["Demacia", "Yordle", "Juggernaut"], "diff": 1},
    {"name": "Kennen",       "traits": ["Ionia", "Yordle", "Defender"], "diff": 1},
    {"name": "Illaoi",       "traits": ["Bilgewater", "Bruiser"], "diff": 1},
    {"name": "Taric",        "traits": ["Targon", "Warden"], "diff": 1},
    {"name": "Cho'Gath",     "traits": ["Void", "Juggernaut"], "diff": 1},
    {"name": "Renekton",     "traits": ["Shurima", "Bruiser"], "diff": 1},
    {"name": "Malzahar",     "traits": ["Void", "Disruptor"], "diff": 1},
    {"name": "Viego",        "traits": ["Shadow Isles", "Quickstriker"], "diff": 1},
    {"name": "Jinx",         "traits": ["Zaun", "Gunslinger"], "diff": 1},
    {"name": "Warwick",      "traits": ["Zaun", "Challenger"], "diff": 1},
    
    # --- TRUNG BÌNH (2) ---
    {"name": "Ziggs",        "traits": ["Zaun", "Yordle", "Longshot"], "diff": 2},
    {"name": "Fizz",         "traits": ["Bilgewater", "Yordle"], "diff": 2},
    {"name": "Graves",       "traits": ["Bilgewater", "Gunslinger"], "diff": 2},
    {"name": "Aphelios",     "traits": ["Targon", "Deadeye"], "diff": 2},
    {"name": "Gwen",         "traits": ["Shadow Isles", "Slayer"], "diff": 2},
    {"name": "Kai'Sa",       "traits": ["Void", "Longshot"], "diff": 2},
    {"name": "Azir",         "traits": ["Shurima", "Emperor"], "diff": 2},
    {"name": "Sejuani",      "traits": ["Freljord", "Defender"], "diff": 2},
    {"name": "Nasus",        "traits": ["Shurima", "Juggernaut"], "diff": 2},
    {"name": "Shen",         "traits": ["Ionia", "Invoker"], "diff": 2},
    {"name": "Jarvan IV",    "traits": ["Demacia", "Defender"], "diff": 2},
    {"name": "Galio",        "traits": ["Demacia", "Invoker"], "diff": 2},

    # --- KHÓ / 5 TIỀN (3) ---
    {"name": "Veigar",       "traits": ["Yordle", "Arcanist"], "diff": 3},
    {"name": "Aurelion Sol", "traits": ["Targon", "Invoker"], "diff": 3},
    {"name": "Aatrox",       "traits": ["Noxus", "Slayer", "Darkin"], "diff": 3},
    {"name": "Sion",         "traits": ["Noxus", "Bruiser"], "diff": 3},
    {"name": "Baron",        "traits": ["Void", "Bruiser"], "diff": 3},
    {"name": "Ryze (Clone)", "traits": ["Rune Mage"], "diff": 3},
    {"name": "Ahri",         "traits": ["Ionia", "Arcanist"], "diff": 3},
    {"name": "Bel'Veth",     "traits": ["Void", "Empress"], "diff": 3},
]

# --- HÀM TÍNH TOÁN TỐI ƯU ---
def solve_comp(pool, slots, user_emblems):
    best_score = (-1, -1) # (Region Score, Class Score)
    best_comp = None
    
    # Tối ưu hóa Pool để chạy nhanh ở Lv 10/11
    # Luôn lấy các tướng kết nối (2 region trở lên) và Targon
    connectors = [u for u in pool if len([t for t in u['traits'] if t in REGION_DATA]) >= 2]
    targon = [u for u in pool if "Targon" in u['traits']]
    
    # Lấy phần còn lại
    others = [u for u in pool if u not in connectors and u not in targon]
    
    # Nếu level cao (10, 11), ta cần mở rộng pool filler một chút để đủ tướng điền vào chỗ trống
    filler_count = 14 if slots >= 9 else 12
    final_pool = connectors + targon + others[:filler_count]

    # Giới hạn vòng lặp an toàn (Safety Break)
    # Lv 10/11 có tổ hợp rất lớn, ta tăng giới hạn lên để tìm kỹ hơn
    limit_max = 3000000 
    loop_count = 0

    for team in itertools.combinations(final_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break # Dừng nếu chạy quá lâu

        # Kiểm tra trùng tên tướng (Set 16 có thể có tướng trùng tên nhưng khác phiên bản, ở đây ta giả định Unique Name)
        names = [u['name'] for u in team]
        if len(set(names)) < len(names): continue

        # 1. Tính Trait
        traits = {}
        for u in team:
            for t in u['traits']:
                traits[t] = traits.get(t, 0) + 1
        # Cộng Ấn
        for emb, count in user_emblems.items():
            traits[emb] = traits.get(emb, 0) + count
        
        # 2. Tính Điểm Region
        r_score = 0
        r_list = []
        for r, data in REGION_DATA.items():
            c = traits.get(r, 0)
            if c >= data['thresholds'][0]:
                r_score += 1
                r_list.append(f"{r} ({c})")

        # 3. Tính Điểm Class
        c_score = 0
        c_list = []
        for cl, thresholds in CLASS_DATA.items():
            c = traits.get(cl, 0)
            if c >= thresholds[0]:
                c_score += 1
                c_list.append(f"{cl} ({c})")

        # 4. So sánh & Cập nhật
        if r_score > best_score[0]:
            best_score = (r_score, c_score)
            best_comp = (team, r_list, c_list)
        elif r_score == best_score[0]:
            if c_score > best_score[1]:
                best_score = (r_score, c_score)
                best_comp = (team, r_list, c_list)
    
    return best_score, best_comp

# --- GIAO DIỆN NGƯỜI DÙNG (UI) ---
st.title("🧙‍♂️ TFT Set 16: Ryze Exodia Builder")
st.markdown("""
Công cụ tìm đội hình tối ưu nhất cho **Ryze** dựa trên cơ chế: 
*"Ryze hưởng lợi từ tất cả Vùng Đất kích hoạt nhưng không đóng góp vào kích hệ."*
""")

# Cột bên trái: Nhập liệu
with st.sidebar:
    st.header("⚙️ Cấu hình Đội hình")
    
    # Cập nhật thêm Level 10, 11
    level = st.selectbox(
        "Cấp độ / Slot tướng:", 
        [8, 9, 10, 11], 
        index=0,
        help="Chọn 10 hoặc 11 nếu bạn có Lõi Level Up hoặc Vương Miện."
    )
    
    st.markdown("---")
    st.header("🧩 Số lượng Ấn đang có")
    st.caption("Nhập số lượng ấn bạn đang sở hữu:")
    
    user_emblems = {}
    # Tạo 2 cột nhập liệu cho gọn
    col1, col2 = st.columns(2)
    keys = sorted(REGION_DATA.keys())
    half = len(keys) // 2
    
    with col1:
        for r in keys[:half]:
            val = st.number_input(f"{r}", min_value=0, max_value=3, step=1, key=f"emb_{r}")
            if val > 0: user_emblems[r] = val
            
    with col2:
        for r in keys[half:]:
            val = st.number_input(f"{r}", min_value=0, max_value=3, step=1, key=f"emb_{r}")
            if val > 0: user_emblems[r] = val

    st.markdown("---")
    run_btn = st.button("🚀 TÌM ĐỘI HÌNH NGAY", type="primary")

# Phần hiển thị kết quả chính
if run_btn:
    # Ryze chiếm 1 slot, nên số slot cần tìm là Level - 1
    slots_needed = level - 1
    st.toast(f"Đang tính toán hàng triệu tổ hợp cho Lv {level}...", icon="⏳")
    
    # Tạo các tab kết quả
    tab1, tab2, tab3 = st.tabs(["🟢 Dễ (Tiết kiệm)", "🟡 Tiêu chuẩn (Meta)", "🔴 EXODIA (Max Ping)"])
    
    # Logic Pool tướng cho từng độ khó
    pools = {
        "easy": [u for u in ALL_UNITS if u['diff'] == 1],
        "medium": [u for u in ALL_UNITS if u['diff'] <= 2],
        "hard": ALL_UNITS # Exodia lấy tất cả tướng
    }
    
    # Hàm hiển thị kết quả con
    def show_result(pool_key, tab_obj):
        s, comp = solve_comp(pools[pool_key], slots_needed, user_emblems)
        with tab_obj:
            if comp:
                team, r_list, c_list = comp
                
                # Hiển thị Metric thống kê
                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("Vùng Đất (Ryze Buff)", f"{s[0]}", delta="Kích hoạt")
                col_m2.metric("Hệ Nghề (Team Buff)", f"{s[1]}", delta="Liên kết")
                col_m3.metric("Số tướng", f"{len(team)} + Ryze")
                
                st.markdown("### 📋 Danh sách tướng:")
                st.info(f"**1. Ryze (Rune Mage)** - *Vị trí trung tâm*")
                
                # Chia cột hiển thị tướng cho đẹp
                c_left, c_right = st.columns(2)
                for idx, u in enumerate(team):
                    # Highlight trait được kích hoạt
                    traits_str = ""
                    for t in u['traits']:
                        is_act = any(t in x for x in r_list + c_list)
                        if is_act:
                            traits_str += f"<span style='color:#4CAF50; font-weight:bold'>{t.upper()}</span>, "
                        else:
                            traits_str += f"{t}, "
                    
                    # In ra màn hình (chia đều 2 cột)
                    display_text = f"**{idx+2}. {u['name']}** ({traits_str.strip(', ')})"
                    if idx < len(team) / 2:
                        with c_left: st.markdown(f"- {display_text}", unsafe_allow_html=True)
                    else:
                        with c_right: st.markdown(f"- {display_text}", unsafe_allow_html=True)
                
                st.markdown("---")
                # Hiển thị chi tiết buff
                exp_r = st.expander("🌍 Xem chi tiết Buff Vùng Đất (Ryze nhận được)", expanded=True)
                exp_r.success(", ".join(r_list))
                
                exp_c = st.expander("🛡️ Xem chi tiết Hệ Tộc (Cả đội nhận được)", expanded=True)
                exp_c.warning(", ".join(c_list))
                
            else:
                st.error(f"Không tìm được đội hình phù hợp với {slots_needed} slot. Hãy thử giảm bớt điều kiện hoặc tăng Level.")

    # Chạy hiển thị
    show_result("easy", tab1)
    show_result("medium", tab2)
    show_result("hard", tab3)

else:
    # Màn hình chờ
    st.info("👈 Vui lòng chọn **Level** và nhập **Số lượng Ấn** ở cột bên trái, sau đó bấm nút **TÌM ĐỘI HÌNH**.")
    st.markdown("""
    #### 💡 Mẹo chơi Ryze Set 16:
    1. **Targon (Mốc 1):** Luôn cố gắng kẹp 1 unit Targon (Taric/Aphelios) vì Ryze sẽ nhận ngay hiệu ứng Targon chỉ với 1 slot.
    2. **Unit Đa Hệ:** Các tướng như **Vi** (Piltover/Zaun), **Ziggs** (Zaun/Yordle), **Kennen** (Ionia/Yordle) là chìa khóa vàng.
    3. **Lv 10/11:** Ở cấp độ này, hãy chọn Tab **"🔴 EXODIA"** để tìm đội hình dùng tướng 5 tiền mạnh nhất.
    """)