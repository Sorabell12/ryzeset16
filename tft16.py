import streamlit as st
import itertools

# --- 1. PAGE CONFIGURATION & COMPACT CSS ---
st.set_page_config(page_title="TFT Set 16 Optimizer", page_icon="⚡", layout="wide")

# --- CSS HACK: REMOVE PADDING TO FIT SCREEN ---
st.markdown("""
    <style>
        /* Xóa khoảng trắng thừa ở trên cùng trang web */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        /* Thu gọn khoảng cách các phần tử */
        .st-emotion-cache-1y4p8pa {
            padding-top: 0rem;
        }
        /* Làm tiêu đề nhỏ lại một chút */
        h1 {
            font-size: 1.8rem !important;
            margin-bottom: 0rem !important;
        }
        /* Tối ưu hiển thị trên mobile/khung nhỏ */
        div[data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU (GIỮ NGUYÊN) ---
REGION_DATA = {
    "Bilgewater":   {"thresholds": [3, 5, 7, 10]},
    "Demacia":      {"thresholds": [3, 5, 7, 11]},
    "Freljord":     {"thresholds": [3, 5, 7]},
    "Ionia":        {"thresholds": [3, 5, 7, 10]},
    "Ixtal":        {"thresholds": [3, 5, 7]},
    "Noxus":        {"thresholds": [3, 5, 7, 10]},
    "Piltover":     {"thresholds": [2, 4, 6]},
    "Shadow Isles": {"thresholds": [2, 3, 4, 5]},
    "Shurima":      {"thresholds": [2, 3, 4, 6]},
    "Targon":       {"thresholds": [1, 2, 3, 4]},
    "Void":         {"thresholds": [2, 4, 6, 9]},
    "Yordle":       {"thresholds": [2, 4, 6, 8]},
    "Zaun":         {"thresholds": [3, 5, 7]}
}

CLASS_DATA = {
    "Bruiser": [2, 4, 6], "Defender": [2, 4, 6], "Invoker": [2, 4, 6],
    "Slayer": [2, 4, 6], "Gunslinger": [2, 4, 6], "Arcanist": [2, 4, 6],
    "Warden": [2, 3, 4, 5], "Juggernaut": [2, 4, 6], "Longshot": [2, 3, 4, 5],
    "Quickstriker": [2, 3, 4, 5], "Disruptor": [2, 4], "Vanquisher": [2, 3, 4, 5]
}

ALL_UNITS = [
    # 1 COST
    {"name": "Anivia", "traits": ["Freljord", "Invoker"], "cost": 1, "diff": 1},
    {"name": "Blitzcrank", "traits": ["Zaun", "Juggernaut"], "cost": 1, "diff": 1},
    {"name": "Briar", "traits": ["Noxus", "Slayer", "Juggernaut"], "cost": 1, "diff": 1},
    {"name": "Caitlyn", "traits": ["Piltover", "Longshot"], "cost": 1, "diff": 1},
    {"name": "Illaoi", "traits": ["Bilgewater", "Bruiser"], "cost": 1, "diff": 1},
    {"name": "Jarvan IV", "traits": ["Demacia", "Defender"], "cost": 1, "diff": 1},
    {"name": "Jhin", "traits": ["Ionia", "Gunslinger"], "cost": 1, "diff": 1},
    {"name": "Kog'Maw", "traits": ["Void", "Arcanist", "Longshot"], "cost": 1, "diff": 1},
    {"name": "Lulu", "traits": ["Yordle", "Arcanist"], "cost": 1, "diff": 1},
    {"name": "Qiyana", "traits": ["Ixtal", "Slayer"], "cost": 1, "diff": 1},
    {"name": "Rumble", "traits": ["Yordle", "Defender"], "cost": 1, "diff": 1},
    {"name": "Shen", "traits": ["Ionia", "Bruiser"], "cost": 1, "diff": 1},
    {"name": "Sona", "traits": ["Demacia", "Invoker"], "cost": 1, "diff": 1},
    {"name": "Viego", "traits": ["Shadow Isles", "Quickstriker"], "cost": 1, "diff": 1},
    {"name": "Vi", "traits": ["Piltover", "Zaun", "Defender"], "cost": 1, "diff": 1},
    {"name": "Xin Zhao", "traits": ["Demacia", "Ionia", "Warden"], "cost": 1, "diff": 1},
    {"name": "Yasuo", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1},
    # 2 COST
    {"name": "Aphelios", "traits": ["Targon"], "cost": 2, "diff": 1},
    {"name": "Ashe", "traits": ["Freljord", "Quickstriker"], "cost": 2, "diff": 1},
    {"name": "Cho'Gath", "traits": ["Void", "Juggernaut"], "cost": 2, "diff": 1},
    {"name": "Ekko", "traits": ["Zaun", "Disruptor"], "cost": 2, "diff": 1},
    {"name": "Neeko", "traits": ["Ixtal", "Arcanist", "Defender"], "cost": 2, "diff": 1},
    {"name": "Rek'Sai", "traits": ["Void", "Vanquisher"], "cost": 2, "diff": 1},
    {"name": "Sion", "traits": ["Noxus", "Bruiser"], "cost": 2, "diff": 1},
    {"name": "Teemo", "traits": ["Yordle", "Longshot"], "cost": 2, "diff": 1},
    {"name": "Tristana", "traits": ["Yordle", "Gunslinger"], "cost": 2, "diff": 1},
    {"name": "Twisted Fate", "traits": ["Bilgewater", "Quickstriker"], "cost": 2, "diff": 1},
    # 3 COST
    {"name": "Ahri", "traits": ["Ionia", "Arcanist"], "cost": 3, "diff": 1},
    {"name": "Dr. Mundo", "traits": ["Zaun", "Bruiser"], "cost": 3, "diff": 1},
    {"name": "Draven", "traits": ["Noxus", "Quickstriker"], "cost": 3, "diff": 1},
    {"name": "Gangplank", "traits": ["Bilgewater", "Slayer", "Vanquisher"], "cost": 3, "diff": 1},
    {"name": "Jinx", "traits": ["Zaun", "Gunslinger"], "cost": 3, "diff": 1},
    {"name": "Leona", "traits": ["Targon"], "cost": 3, "diff": 1},
    {"name": "Loris", "traits": ["Piltover", "Warden"], "cost": 3, "diff": 1},
    {"name": "Malzahar", "traits": ["Void", "Disruptor"], "cost": 3, "diff": 1},
    {"name": "Milio", "traits": ["Ixtal", "Invoker"], "cost": 3, "diff": 1},
    {"name": "Nautilus", "traits": ["Bilgewater", "Juggernaut", "Warden"], "cost": 3, "diff": 1},
    {"name": "Sejuani", "traits": ["Freljord", "Defender"], "cost": 3, "diff": 1},
    {"name": "Vayne", "traits": ["Demacia", "Longshot"], "cost": 3, "diff": 1},
    {"name": "Zoe", "traits": ["Targon"], "cost": 3, "diff": 1},
    # 4 COST
    {"name": "Ambessa", "traits": ["Noxus", "Vanquisher"], "cost": 4, "diff": 2},
    {"name": "Bel'Veth", "traits": ["Void", "Slayer"], "cost": 4, "diff": 2},
    {"name": "Braum", "traits": ["Freljord", "Warden"], "cost": 4, "diff": 2},
    {"name": "Garen", "traits": ["Demacia", "Defender"], "cost": 4, "diff": 2},
    {"name": "Lissandra", "traits": ["Freljord", "Invoker"], "cost": 4, "diff": 2},
    {"name": "Lux", "traits": ["Demacia", "Arcanist"], "cost": 4, "diff": 2},
    {"name": "Miss Fortune", "traits": ["Bilgewater", "Gunslinger"], "cost": 4, "diff": 2},
    {"name": "Seraphine", "traits": ["Piltover", "Disruptor"], "cost": 4, "diff": 2},
    {"name": "Swain", "traits": ["Noxus", "Arcanist", "Juggernaut"], "cost": 4, "diff": 2},
    {"name": "Taric", "traits": ["Targon"], "cost": 4, "diff": 2},
    {"name": "Wukong", "traits": ["Ionia", "Bruiser"], "cost": 4, "diff": 2},
    {"name": "Yunara", "traits": ["Ionia", "Quickstriker"], "cost": 4, "diff": 2},
    # 5 COST
    {"name": "Annie", "traits": ["Dark Child", "Arcanist"], "cost": 5, "diff": 3},
    {"name": "Azir", "traits": ["Shurima", "Emperor", "Disruptor"], "cost": 5, "diff": 3},
    {"name": "Fiddlesticks", "traits": ["Harvester", "Vanquisher"], "cost": 5, "diff": 3},
    {"name": "Kindred", "traits": ["Eternal", "Quickstriker"], "cost": 5, "diff": 3},
    {"name": "Lucian & Senna", "traits": ["Soulbound", "Gunslinger"], "cost": 5, "diff": 3},
    {"name": "Ornn", "traits": ["Blacksmith", "Warden"], "cost": 5, "diff": 3},
    {"name": "Shyvana", "traits": ["Dragonborn", "Juggernaut"], "cost": 5, "diff": 3},
    {"name": "Zilean", "traits": ["Chronokeeper", "Invoker"], "cost": 5, "diff": 3},
    {"name": "Galio (Heroic)", "traits": ["Demacia", "Heroic"], "cost": 5, "diff": 3},
    # UNLOCKABLES
    {"name": "Bard", "traits": ["Caretaker"], "cost": 2, "diff": 2},
    {"name": "Orianna", "traits": ["Piltover", "Invoker"], "cost": 2, "diff": 2},
    {"name": "Poppy", "traits": ["Demacia", "Yordle", "Juggernaut"], "cost": 1, "diff": 1},
    {"name": "Graves", "traits": ["Bilgewater", "Gunslinger"], "cost": 2, "diff": 2},
    {"name": "Yorick", "traits": ["Shadow Isles", "Warden"], "cost": 2, "diff": 2},
    {"name": "Tryndamere", "traits": ["Freljord", "Slayer"], "cost": 2, "diff": 2},
    {"name": "Darius", "traits": ["Noxus", "Defender"], "cost": 3, "diff": 2},
    {"name": "Gwen", "traits": ["Shadow Isles", "Disruptor"], "cost": 3, "diff": 2},
    {"name": "Kennen", "traits": ["Ionia", "Yordle", "Defender"], "cost": 1, "diff": 1},
    {"name": "Kobuko & Yuumi", "traits": ["Yordle", "Bruiser", "Invoker"], "cost": 3, "diff": 2},
    {"name": "LeBlanc", "traits": ["Noxus", "Invoker"], "cost": 3, "diff": 2},
    {"name": "Diana", "traits": ["Targon"], "cost": 4, "diff": 2},
    {"name": "Fizz", "traits": ["Bilgewater", "Yordle"], "cost": 1, "diff": 2},
    {"name": "Kai'Sa", "traits": ["Void", "Longshot", "Assimilator"], "cost": 4, "diff": 2},
    {"name": "Kalista", "traits": ["Shadow Isles", "Vanquisher"], "cost": 4, "diff": 2},
    {"name": "Nidalee", "traits": ["Ixtal", "Huntress"], "cost": 4, "diff": 2},
    {"name": "Nasus", "traits": ["Shurima"], "cost": 4, "diff": 2},
    {"name": "Renekton", "traits": ["Shurima"], "cost": 4, "diff": 2},
    {"name": "Rift Herald", "traits": ["Void", "Bruiser"], "cost": 4, "diff": 2},
    {"name": "Singed", "traits": ["Zaun", "Juggernaut"], "cost": 4, "diff": 2},
    {"name": "Skarner", "traits": ["Ixtal"], "cost": 4, "diff": 2},
    {"name": "Veigar", "traits": ["Yordle", "Arcanist"], "cost": 4, "diff": 3},
    {"name": "Warwick", "traits": ["Zaun", "Quickstriker"], "cost": 1, "diff": 1},
    {"name": "Yone", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1},
    # 7 COST & EXODIA
    {"name": "Aatrox (Unlock)", "traits": ["Darkin", "Slayer"], "cost": 5, "diff": 3},
    {"name": "Aurelion Sol", "traits": ["Targon", "Star Forger"], "cost": 7, "diff": 3},
    {"name": "Baron Nashor", "traits": ["Void", "Riftscourge"], "cost": 7, "diff": 3},
    {"name": "Brock", "traits": ["Ixtal"], "cost": 7, "diff": 3},
    {"name": "Mel", "traits": ["Noxus", "Disruptor"], "cost": 5, "diff": 3},
    {"name": "Ryze (Clone)", "traits": ["Rune Mage"], "cost": 7, "diff": 3},
    {"name": "Sett", "traits": ["Ionia", "The Boss"], "cost": 5, "diff": 3},
    {"name": "Sylas", "traits": ["Chainbreaker", "Arcanist", "Defender"], "cost": 7, "diff": 3},
    {"name": "T-Hex", "traits": ["Piltover", "Gunslinger", "HexMech"], "cost": 5, "diff": 3},
    {"name": "Tahm Kench", "traits": ["Bilgewater", "Glutton", "Bruiser"], "cost": 5, "diff": 3},
    {"name": "Thresh", "traits": ["Shadow Isles", "Warden"], "cost": 1, "diff": 1},
    {"name": "Volibear", "traits": ["Freljord", "Bruiser"], "cost": 5, "diff": 3},
    {"name": "Xerath", "traits": ["Shurima", "Ascendant"], "cost": 5, "diff": 3},
    {"name": "Zaahen", "traits": ["Darkin", "Immortal"], "cost": 7, "diff": 3},
    {"name": "Ziggs (Unlock)", "traits": ["Zaun", "Yordle", "Longshot"], "cost": 5, "diff": 3}
]

# --- ALGORITHM ---
def solve_comp(pool, slots, user_emblems, prioritize_strength=False):
    best_score = (-1, -1, -1)
    best_comp = None
    
    region_units = [u for u in pool if any(t in REGION_DATA for t in u['traits'])]
    targon = [u for u in pool if "Targon" in u['traits']]
    high_cost_neutral = [u for u in pool if u['cost'] >= 5 and u not in region_units]
    
    if prioritize_strength:
        sorted_pool = sorted(region_units + high_cost_neutral, key=lambda x: x['cost'], reverse=True)
        final_pool = sorted_pool[:25]
        final_pool = list({v['name']:v for v in final_pool + targon}.values())
    else:
        connectors = [u for u in region_units if len([t for t in u['traits'] if t in REGION_DATA]) >= 2]
        others = [u for u in region_units if u not in connectors]
        final_pool = connectors + targon + others[:15]

    limit_max = 1500000
    loop_count = 0

    for team in itertools.combinations(final_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        
        names = [u['name'] for u in team]
        if len(set(names)) < len(names): continue

        traits = {}
        total_cost = 0
        for u in team:
            total_cost += u.get('cost', 1)
            for t in u['traits']:
                traits[t] = traits.get(t, 0) + 1
        for emb, count in user_emblems.items():
            traits[emb] = traits.get(emb, 0) + count
        
        r_score = 0
        r_list = []
        for r, data in REGION_DATA.items():
            c = traits.get(r, 0)
            if c >= data['thresholds'][0]:
                r_score += 1
                r_list.append(f"{r}({c})")

        c_score = 0
        c_list = []
        for cl, thresholds in CLASS_DATA.items():
            c = traits.get(cl, 0)
            if c >= thresholds[0]:
                c_score += 1
                c_list.append(f"{cl}({c})")

        if prioritize_strength:
            current_score = (r_score, total_cost, c_score)
        else:
            current_score = (r_score, c_score, total_cost)
            
        if current_score > best_score:
            best_score = current_score
            best_comp = (team, r_list, c_list, total_cost)
    
    return best_score, best_comp

# --- COMPACT UI LAYOUT ---
st.title("🧙‍♂️ TFT Set 16: Ryze Tool")
st.markdown("**Fit-to-Screen Edition**: Optimized for laptop & desktop viewing.")

# Sidebar Compact
with st.sidebar:
    st.header("⚙️ Config")
    level = st.selectbox("Level:", [8, 9, 10, 11])
    
    # Use EXPANDER to save vertical space
    with st.expander("🧩 Region Emblems (Click to Open)", expanded=True):
        user_emblems = {}
        c1, c2 = st.columns(2)
        keys = sorted(REGION_DATA.keys())
        mid = len(keys)//2
        with c1:
            for k in keys[:mid]:
                v = st.number_input(k, 0, 3, key=k)
                if v: user_emblems[k]=v
        with c2:
            for k in keys[mid:]:
                v = st.number_input(k, 0, 3, key=k)
                if v: user_emblems[k]=v
    
    run = st.button("🚀 FIND BEST TEAM", type="primary", use_container_width=True)

# Main Area
if run:
    slots = level - 1
    
    tab1, tab2, tab3 = st.tabs(["Low Cost", "Standard", "EXODIA"])
    
    pool_easy = [u for u in ALL_UNITS if u['diff'] == 1]
    pool_mid = [u for u in ALL_UNITS if u['diff'] <= 2]
    pool_hard = ALL_UNITS
    
    def render_compact_result(tab, pool, p_strength=False):
        with tab:
            s, comp = solve_comp(pool, slots, user_emblems, p_strength)
            if comp:
                team, r_list, c_list, t_cost = comp
                
                # Compact Metrics in one row
                m1, m2, m3 = st.columns(3)
                m1.metric("Regions", s[0])
                m2.metric("Total Cost", t_cost)
                m3.metric("Traits", len(c_list))
                
                st.divider()
                
                # Compact List
                st.markdown("##### 📋 Suggested Units:")
                # Split into 2 tight columns
                col_l, col_r = st.columns(2)
                
                # Ryze fixed
                col_l.markdown("1. **Ryze** (7🟡) : <span style='color:blue'>**Rune Mage**</span>", unsafe_allow_html=True)
                
                for i, u in enumerate(team):
                    traits_html = []
                    for t in u['traits']:
                        if "Targon" in t: traits_html.append(f"<span style='color:#9C27B0'><b>{t}</b></span>")
                        elif any(t in x for x in r_list): traits_html.append(f"<span style='color:#2E7D32'><b>{t}</b></span>")
                        elif any(t in x for x in c_list): traits_html.append(f"<span style='color:#E65100'><b>{t}</b></span>")
                        else: traits_html.append(f"<span style='color:#555'>{t}</span>")
                    
                    row_html = f"{i+2}. **{u['name']}** ({u['cost']}🟡) : {' '.join(traits_html)}"
                    
                    if i < (len(team) // 2): # Fill Right column first since Ryze is on Left
                        col_r.markdown(row_html, unsafe_allow_html=True)
                    else:
                        col_l.markdown(row_html, unsafe_allow_html=True)
                        
                st.divider()
                st.success(f"🌍 **Regions:** {', '.join(r_list)}")
            else:
                st.warning("No valid team found.")

    render_compact_result(tab1, pool_easy, False)
    render_compact_result(tab2, pool_mid, False)
    render_compact_result(tab3, pool_hard, True)

else:
    st.info("👈 Select options in the sidebar and click **FIND BEST TEAM**.")
