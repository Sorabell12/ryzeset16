import streamlit as st
import itertools

# --- 1. PAGE CONFIG & CSS ---
st.set_page_config(page_title="TFT Set 16 Optimizer", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 1rem 1rem 0rem 1rem; }
        section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
        div.stButton > button {
            width: 100%; background-color: #FF4B4B; color: white; font-weight: bold; border: none;
        }
        div.stButton > button:hover { background-color: #FF0000; color: white; }
        .streamlit-expanderHeader { font-weight: bold; font-size: 1.1rem; }
        /* Custom scrollbar for emblem inputs */
        .stNumberInput input { padding-right: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL LANGUAGE DICTIONARY ---
T = {
    "Tiếng Việt": {
        "title": "🧙‍♂️ TFT Mùa 16: Tool Ryze AI",
        "subtitle": "**Đa dạng chiến thuật:** Tối ưu hóa toàn diện.",
        "config": "⚙️ Cấu hình",
        "level": "Cấp độ (Level):",
        "btn_find": "🚀 TÌM ĐỘI HÌNH",
        "emb_region": "🌍 Ấn Vùng Đất (Region Emblems)",
        "emb_class": "🛡️ Ấn Tộc/Hệ (Class Emblems)",
        "donate_title": "### ☕ Ủng hộ Dev",
        "donate_btn": "☕ Buy Me a Coffee", 
        "tabs": ["Giá Rẻ (Eco)", "Tiêu Chuẩn (Standard)", "EXODIA (Tối Thượng)", "🔓 MỞ KHÓA RYZE"],
        "mission_info": "🏆 **Nhiệm vụ:** Kích hoạt 5 Vùng Đất để mở khóa Ryze.",
        "tag_basic": "🟢 **SHOP CƠ BẢN (CÓ SẴN)**",
        "tag_unlock": "🟠 **CẦN MỞ KHÓA ({})**",
        "err_unlock": "Không tìm thấy cách kích 5 vùng với số slot hiện tại.",
        "err_combat": "Không tìm thấy đội hình phù hợp.",
        "spinner_unlock": "Đang tính toán lộ trình rẻ nhất...",
        "spinner_combat": "Đang tìm đồng đội cho Ryze...",
        "res_option": "Lựa chọn",
        "res_regions": "Vùng đất",
        "res_cost": "Vàng",
        "active": "**Kích hoạt:**",
        "labels": [
            "👑 Lựa chọn 1: CÂN BẰNG NHẤT",
            "🌍 Lựa chọn 2",
            "🛡️ Lựa chọn 3"
        ]
    },
    "English": {
        "title": "🧙‍♂️ TFT Set 16: Ryze AI Tool",
        "subtitle": "**Strategic Diversity:** Full Optimization.",
        "config": "⚙️ Config",
        "level": "Level:",
        "btn_find": "🚀 FIND TEAMS",
        "emb_region": "🌍 Region Emblems",
        "emb_class": "🛡️ Class/Trait Emblems",
        "donate_title": "### ☕ Support Dev",
        "donate_btn": "☕ Buy Me a Coffee",
        "tabs": ["Low Cost (Eco)", "Standard", "EXODIA", "🔓 UNLOCK RYZE"],
        "mission_info": "🏆 **Mission:** Activate 5 Regions to Unlock Ryze.",
        "tag_basic": "🟢 **BASIC SHOP (AVAILABLE)**",
        "tag_unlock": "🟠 **REQUIRES {} UNLOCK(S)**",
        "err_unlock": "Cannot find 5 regions with current slots.",
        "err_combat": "No valid team found.",
        "spinner_unlock": "Calculating best paths...",
        "spinner_combat": "Finding teammates for Ryze...",
        "res_option": "Option",
        "res_regions": "Regions",
        "res_cost": "Gold",
        "active": "**Active:**",
        "labels": [
            "👑 Option 1: BEST BALANCED",
            "🌍 Option 2",
            "🛡️ Option 3"
        ]
    }
}


# --- DATASETS ---
REGION_DATA = {
    "Bilgewater":   {"thresholds": [3, 5, 7, 10]}, "Demacia": {"thresholds": [3, 5, 7, 11]},
    "Freljord":     {"thresholds": [3, 5, 7]}, "Ionia": {"thresholds": [3, 5, 7, 10]},
    "Ixtal":        {"thresholds": [3, 5, 7]}, "Noxus": {"thresholds": [3, 5, 7, 10]},
    "Piltover":     {"thresholds": [2, 4, 6]}, "Shadow Isles": {"thresholds": [2, 3, 4, 5]},
    "Shurima":      {"thresholds": [2, 3, 4, 6]}, "Targon": {"thresholds": [1, 2, 3, 4]},
    "Void":         {"thresholds": [2, 4, 6, 9]}, "Yordle": {"thresholds": [2, 4, 6, 8]},
    "Zaun":         {"thresholds": [3, 5, 7]}
}

CLASS_DATA = {
    "Bruiser": [2, 4, 6], "Defender": [2, 4, 6], "Invoker": [2, 4, 6],
    "Slayer": [2, 4, 6], "Gunslinger": [2, 4, 6], "Arcanist": [2, 4, 6],
    "Warden": [2, 3, 4, 5], "Juggernaut": [2, 4, 6], "Longshot": [2, 3, 4, 5],
    "Quickstriker": [2, 3, 4, 5], "Disruptor": [2, 4], "Vanquisher": [2, 3, 4, 5],
    "Darkin": [1, 2, 3],
    "Heroic": [1], "The Boss": [1], "Emperor": [1], "Ascendant": [1], 
    "Star Forger": [1], "Caretaker": [1], "Rune Mage": [1], "Assimilator": [1],
    "Huntress": [1], "Glutton": [1], "Blacksmith": [1], "Soulbound": [1],
    "Eternal": [1], "Dragonborn": [1], "Chronokeeper": [1], "Dark Child": [1],
    "Harvester": [1], "HexMech": [1], "Chainbreaker": [1], "Riftscourge": [1],
    "Immortal": [1], "Empress": [1]
}

UNIQUE_TRAITS = list(CLASS_DATA.keys())[-22:]

GALIO_UNIT = {"name": "Galio", "traits": ["Demacia", "Invoker", "Heroic"], "cost": 5, "diff": 3, "role": "tank"}

# --- UNIT LISTS ---
STANDARD_UNITS = [
    # 1 COST
    {"name": "Anivia", "traits": ["Freljord", "Invoker"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Blitzcrank", "traits": ["Zaun", "Juggernaut"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Briar", "traits": ["Noxus", "Slayer", "Juggernaut"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Caitlyn", "traits": ["Piltover", "Longshot"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Illaoi", "traits": ["Bilgewater", "Bruiser"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Jarvan IV", "traits": ["Demacia", "Defender"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Jhin", "traits": ["Ionia", "Gunslinger"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Kog'Maw", "traits": ["Void", "Arcanist", "Longshot"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Lulu", "traits": ["Yordle", "Arcanist"], "cost": 1, "diff": 1, "role": "supp"},
    {"name": "Qiyana", "traits": ["Ixtal", "Slayer"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Rumble", "traits": ["Yordle", "Defender"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Shen", "traits": ["Ionia", "Bruiser"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Sona", "traits": ["Demacia", "Invoker"], "cost": 1, "diff": 1, "role": "supp"},
    {"name": "Viego", "traits": ["Shadow Isles", "Quickstriker"], "cost": 1, "diff": 1, "role": "carry"},

    # 2 COST
    {"name": "Aphelios", "traits": ["Targon"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Ashe", "traits": ["Freljord", "Quickstriker"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Cho'Gath", "traits": ["Void", "Juggernaut"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Ekko", "traits": ["Zaun", "Disruptor"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Neeko", "traits": ["Ixtal", "Arcanist", "Defender"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Rek'Sai", "traits": ["Void", "Vanquisher"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Sion", "traits": ["Noxus", "Bruiser"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Teemo", "traits": ["Yordle", "Longshot"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Tristana", "traits": ["Yordle", "Gunslinger"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Twisted Fate", "traits": ["Bilgewater", "Quickstriker"], "cost": 2, "diff": 1, "role": "carry"},
    {"name": "Vi", "traits": ["Piltover", "Zaun", "Defender"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Xin Zhao", "traits": ["Demacia", "Ionia", "Warden"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Yasuo", "traits": ["Ionia", "Slayer"], "cost": 2, "diff": 1, "role": "carry"},

    # 3 COST
    {"name": "Ahri", "traits": ["Ionia", "Arcanist"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Dr. Mundo", "traits": ["Zaun", "Bruiser"], "cost": 3, "diff": 1, "role": "tank"},
    {"name": "Draven", "traits": ["Noxus", "Quickstriker"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Gangplank", "traits": ["Bilgewater", "Slayer", "Vanquisher"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Jinx", "traits": ["Zaun", "Gunslinger"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Leona", "traits": ["Targon"], "cost": 3, "diff": 1, "role": "tank"},
    {"name": "Loris", "traits": ["Piltover", "Warden"], "cost": 3, "diff": 1, "role": "tank"},
    {"name": "Malzahar", "traits": ["Void", "Disruptor"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Milio", "traits": ["Ixtal", "Invoker"], "cost": 3, "diff": 1, "role": "supp"},
    {"name": "Nautilus", "traits": ["Bilgewater", "Juggernaut", "Warden"], "cost": 3, "diff": 1, "role": "tank"},
    {"name": "Sejuani", "traits": ["Freljord", "Defender"], "cost": 3, "diff": 1, "role": "tank"},
    {"name": "Vayne", "traits": ["Demacia", "Longshot"], "cost": 3, "diff": 1, "role": "carry"},
    {"name": "Zoe", "traits": ["Targon"], "cost": 3, "diff": 1, "role": "carry"},

    # 4 COST
    {"name": "Taric", "traits": ["Targon"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Ambessa", "traits": ["Noxus", "Vanquisher"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Bel'Veth", "traits": ["Void", "Slayer", "Empress"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Braum", "traits": ["Freljord", "Warden"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Garen", "traits": ["Demacia", "Defender"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Lissandra", "traits": ["Freljord", "Invoker"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Lux", "traits": ["Demacia", "Arcanist"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Miss Fortune", "traits": ["Bilgewater", "Gunslinger"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Seraphine", "traits": ["Piltover", "Disruptor"], "cost": 4, "diff": 2, "role": "supp"},
    {"name": "Swain", "traits": ["Noxus", "Arcanist", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Wukong", "traits": ["Ionia", "Bruiser"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Yunara", "traits": ["Ionia", "Quickstriker"], "cost": 4, "diff": 2, "role": "carry"},

    # 5 COST
    {"name": "Aatrox", "traits": ["Darkin", "Slayer"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Annie", "traits": ["Dark Child", "Arcanist"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Azir", "traits": ["Shurima", "Emperor", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Fiddlesticks", "traits": ["Harvester", "Vanquisher"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Kindred", "traits": ["Eternal", "Quickstriker"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Lucian & Senna", "traits": ["Soulbound", "Gunslinger"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Ornn", "traits": ["Blacksmith", "Warden"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Shyvana", "traits": ["Dragonborn", "Juggernaut"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Zilean", "traits": ["Chronokeeper", "Invoker"], "cost": 5, "diff": 3, "role": "supp"}
]

UNLOCKABLE_UNITS = [
    # 2 COST
    {"name": "Poppy", "traits": ["Demacia", "Yordle", "Juggernaut"], "cost": 2, "diff": 1, "role": "tank"},
    {"name": "Bard", "traits": ["Caretaker"], "cost": 2, "diff": 2, "role": "supp"},
    {"name": "Orianna", "traits": ["Piltover", "Invoker"], "cost": 2, "diff": 2, "role": "supp"},
    {"name": "Graves", "traits": ["Bilgewater", "Gunslinger"], "cost": 2, "diff": 2, "role": "carry"},
    {"name": "Yorick", "traits": ["Shadow Isles", "Warden"], "cost": 2, "diff": 2, "role": "tank"},
    {"name": "Tryndamere", "traits": ["Freljord", "Slayer"], "cost": 2, "diff": 2, "role": "carry"},
    # 3 COST
    {"name": "Kennen", "traits": ["Ionia", "Yordle", "Defender"], "cost": 3, "diff": 2, "role": "tank"},
    {"name": "Kobuko & Yuumi", "traits": ["Yordle", "Bruiser", "Invoker"], "cost": 3, "diff": 2, "role": "tank"},
    {"name": "Darius", "traits": ["Noxus", "Defender"], "cost": 3, "diff": 2, "role": "tank"},
    {"name": "Gwen", "traits": ["Shadow Isles", "Disruptor"], "cost": 3, "diff": 2, "role": "carry"},
    {"name": "LeBlanc", "traits": ["Noxus", "Invoker"], "cost": 3, "diff": 2, "role": "carry"},
    # 4 COST
    {"name": "Fizz", "traits": ["Bilgewater", "Yordle"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Warwick", "traits": ["Zaun", "Quickstriker"], "cost": 4, "diff": 1, "role": "carry"},
    {"name": "Yone", "traits": ["Ionia", "Slayer"], "cost": 4, "diff": 1, "role": "carry"},
    {"name": "Nidalee", "traits": ["Ixtal", "Huntress"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Skarner", "traits": ["Ixtal"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Rift Herald", "traits": ["Void", "Bruiser"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Singed", "traits": ["Zaun", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Kai'Sa", "traits": ["Void", "Longshot", "Assimilator"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Kalista", "traits": ["Shadow Isles", "Vanquisher"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Nasus", "traits": ["Shurima"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Renekton", "traits": ["Shurima"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Veigar", "traits": ["Yordle", "Arcanist"], "cost": 4, "diff": 3, "role": "carry"},
    {"name": "Diana", "traits": ["Targon"], "cost": 4, "diff": 2, "role": "carry"},
    # 5 COST
    {"name": "Sett", "traits": ["Ionia", "The Boss"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Volibear", "traits": ["Freljord", "Bruiser"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Xerath", "traits": ["Shurima", "Ascendant"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Mel", "traits": ["Noxus", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Ziggs", "traits": ["Zaun", "Yordle", "Longshot"], "cost": 5, "diff": 3, "role": "carry"},
]

ALL_UNITS = STANDARD_UNITS + UNLOCKABLE_UNITS

# --- ALGORITHM 1: UNLOCK MISSION (CACHED) ---
@st.cache_data(show_spinner=False)
def solve_unlock_mission(slots, user_emblems):
    candidates = []
    limit_max = 10000000 
    loop_count = 0

    region_units = [u for u in ALL_UNITS if any(t in REGION_DATA for t in u['traits'])]
    
    def get_unlock_score(u):
        score = 0
        if any(u['name'] == su['name'] for su in STANDARD_UNITS):
            score += 5000
        r_count = sum(1 for t in u['traits'] if t in REGION_DATA)
        if r_count >= 2: score += 1000
        for t in u['traits']:
            if t in user_emblems: score += 100
            if t == "Targon": score += 50 
        score += (10 - u['cost'])
        return score

    region_units.sort(key=get_unlock_score, reverse=True)
    
    standard_best = [u for u in region_units if any(u['name'] == su['name'] for su in STANDARD_UNITS)][:28]
    unlock_best = [u for u in region_units if any(u['name'] == uu['name'] for uu in UNLOCKABLE_UNITS)][:10]
    search_pool = standard_best + unlock_best

    for team in itertools.combinations(search_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        if len(set([u['name'] for u in team])) < len(team): continue

        traits = {}
        total_cost = 0
        unlock_count = 0
        
        for u in team:
            total_cost += u.get('cost', 1)
            if any(u['name'] == ul['name'] for ul in UNLOCKABLE_UNITS):
                unlock_count += 1
            for t in u['traits']:
                traits[t] = traits.get(t, 0) + 1
                
        for emb, count in user_emblems.items():
            traits[emb] = traits.get(emb, 0) + count
            
        active_regions = 0
        active_list = []
        for r, data in REGION_DATA.items():
            if traits.get(r, 0) >= data['thresholds'][0]:
                active_regions += 1
                active_list.append(f"{r}({traits[r]})")
        
        if active_regions >= 5:
            candidates.append({
                "team": list(team),
                "active_count": active_regions,
                "cost": total_cost,
                "regions": active_list,
                "unlock_count": unlock_count
            })
            if len(candidates) >= 20: break
    
    candidates.sort(key=lambda x: (-x['active_count'], x['unlock_count'], x['cost']))
    return candidates[:5]

# --- ALGORITHM 2: STANDARD OPTIMIZER (CACHED) ---
@st.cache_data(show_spinner=False)
def build_synergy_pool(base_pool, user_emblems, prioritize_strength=False):
    seed_traits = set(user_emblems.keys())
    seed_traits.add("Targon")
    
    seed_units = [u for u in base_pool if any(t in seed_traits for t in u['traits'])]
    linked_classes = set()
    for u in seed_units:
        for t in u['traits']:
            if t in CLASS_DATA: linked_classes.add(t)
    
    final_pool = []
    seen_names = set()

    for u in seed_units:
        if u['name'] not in seen_names:
            final_pool.append(u)
            seen_names.add(u['name'])
            
    for u in base_pool:
        if u['name'] in seen_names: continue
        has_link = False
        for t in u['traits']:
            if t in linked_classes:
                has_link = True
                break
        if has_link:
            final_pool.append(u)
            seen_names.add(u['name'])

    high_value_units = [u for u in final_pool if u['cost'] >= 4]
    for hv in high_value_units:
        for t in hv['traits']:
            if t in CLASS_DATA or t in REGION_DATA:
                partners = [p for p in base_pool if t in p['traits'] and p['name'] not in seen_names]
                for p in partners:
                    final_pool.append(p)
                    seen_names.add(p['name'])

    if len(final_pool) < 50:
        expensive_fillers = [u for u in base_pool if u['cost'] >= 4 and u['name'] not in seen_names]
        final_pool.extend(expensive_fillers)

    if prioritize_strength:
        final_pool.sort(key=lambda x: (x['cost'], len(x['traits'])), reverse=True)
    else:
        final_pool.sort(key=lambda x: x['cost'])
        
    return final_pool[:50]

@st.cache_data(show_spinner=False)
def solve_three_strategies(pool, slots, user_emblems, prioritize_strength=False):
    
    final_pool = build_synergy_pool(pool, user_emblems, prioritize_strength)

    limit_max = 2000000
    loop_count = 0
    candidates = []

    search_sizes = [slots]
    if any(u['name'] == "Annie" for u in final_pool):
        search_sizes.append(slots - 1)

    for size in search_sizes:
        for team in itertools.combinations(final_pool, size):
            loop_count += 1
            if loop_count > limit_max: break
            if len(set([u['name'] for u in team])) < len(team): continue

            slots_used = 0
            has_annie = False
            for u in team:
                if u['name'] == "Annie":
                    slots_used += 2
                    has_annie = True
                else:
                    slots_used += 1
            
            if slots_used > slots: continue
            if size == (slots - 1) and not has_annie: continue

            traits = {}
            tank_count = 0
            team_total_cost = 0 
            names = [u['name'] for u in team]
            
            for u in team:
                team_total_cost += u.get('cost', 1)
                if u.get('role') == 'tank': tank_count += 1
                for t in u['traits']:
                    traits[t] = traits.get(t, 0) + 1
                if u['name'] == "Annie": traits['Arcanist'] = traits.get('Arcanist', 0) + 1
                    
            for emb, count in user_emblems.items():
                traits[emb] = traits.get(emb, 0) + count
            
            has_galio = False
            final_team = list(team)
            if traits.get("Demacia", 0) >= 6:
                has_galio = True
                final_team.append(GALIO_UNIT)
                tank_count += 1
                for t in GALIO_UNIT['traits']: traits[t] = traits.get(t, 0) + 1
            
            r_score = 0
            active_regions_set = set()
            unused_emblem_penalty = 0
            
            for r, data in REGION_DATA.items():
                count = traits.get(r, 0)
                if count >= data['thresholds'][0]: 
                    r_score += 1
                    active_regions_set.add(r)
                    current_tier_threshold = 0
                    for t in data['thresholds']:
                        if count >= t: current_tier_threshold = t
                        else: break
                    if count > current_tier_threshold: unused_emblem_penalty -= 5
                elif user_emblems.get(r, 0) > 0:
                    unused_emblem_penalty -= 15
            
            final_r = r_score + (5 if has_galio else 0) # --- FIX: DEFINITION BEFORE USE ---
            
            final_r_penalty = 0
            if final_r == 0:
                final_r_penalty = -99999999 # Invalidate team instantly
            elif final_r < 3 and slots >= 7 and not has_galio: 
                final_r_penalty = -500

            c_score = 0
            active_classes_set = set()
            for cl, thresholds in CLASS_DATA.items():
                if traits.get(cl, 0) >= thresholds[0]: 
                    c_score += 2 
                    active_classes_set.add(cl)
            
            useless_unit_penalty = 0
            for u in final_team:
                if u['name'] in ["Ryze", "Galio", "Taric", "Ornn"]: continue
                is_contributing = False
                for t in u['traits']:
                    if t in active_regions_set or t in active_classes_set:
                        is_contributing = True
                        break
                if not is_contributing:
                    if u['cost'] <= 2: useless_unit_penalty -= 30
                    else: useless_unit_penalty -= 10

            targon_c = traits.get("Targon", 0)
            if targon_c == 1: useless_unit_penalty += 50
            elif targon_c > 1: uselesss_unit_penalty -= 20
            elif targon_c == 0: useless_unit_penalty -= 100 

            for u_trait in UNIQUE_TRAITS:
                if traits.get(u_trait, 0) >= 1:
                    if u_trait == "Blacksmith": c_score += 1
                    else:
                        unit_with_trait = next((u for u in final_team if u_trait in u['traits']), None)
                        if unit_with_trait:
                            is_supported = False
                            for other_t in unit_with_trait['traits']:
                                if other_t in active_regions_set or other_t in active_classes_set: is_supported = True
                            if is_supported: c_list_fmt.append(u_trait)

            balance_penalty = 0
            if tank_count < 2: balance_penalty = -10 
            
            targon_bonus = 0
            if "Taric" in names: targon_bonus += 20
            annie_penalty = -12 if "Annie" in names else 0
            
            strength_score = 0
            if prioritize_strength:
                strength_score = team_total_cost * 2.0 

            smart_score = (final_r * 25.0) + \
                          (c_score * 12.0) + \
                          strength_score + \
                          balance_penalty + unused_emblem_penalty + targon_bonus + annie_penalty + useless_unit_penalty + final_r_penalty # USING PENALTY HERE
            
            r_list_fmt = [f"{r}({traits[r]})" for r in REGION_DATA if traits.get(r,0) >= REGION_DATA[r]['thresholds'][0]]
            c_list_fmt = [f"{c}({traits[c]})" for c in CLASS_DATA if traits.get(c,0) >= CLASS_DATA[c][0] and c not in UNIQUE_TRAITS]
            if traits.get("Darkin", 0) >= 1: c_list_fmt.append(f"Darkin({traits['Darkin']})")
            
            for u_trait in UNIQUE_TRAITS:
                if traits.get(u_trait, 0) >= 1:
                    if u_trait == "Blacksmith": c_list_fmt.append("Blacksmith")
                    else:
                        unit_with_trait = next((u for u in final_team if u_trait in u['traits']), None)
                        if unit_with_trait:
                            is_supported = False
                            for other_t in unit_with_trait['traits']:
                                if other_t in active_regions_set or other_t in active_classes_set: is_supported = True
                            if is_supported: c_list_fmt.append(u_trait)

            candidates.append({
                "team": final_team,
                "r_score": final_r,
                "c_score": c_score,
                "smart_score": smart_score,
                "r_list": r_list_fmt,
                "c_list": c_list_fmt,
                "galio": has_galio,
                "tanks": tank_count
            })

    if not candidates: return []
    
    candidates.sort(key=lambda x: x['smart_score'], reverse=True)
    opt1 = candidates[0]
    
    candidates.sort(key=lambda x: (x['r_score'], x['smart_score']), reverse=True)
    opt2 = candidates[0]
    if opt2['team'] == opt1['team']:
        for cand in candidates:
            if cand['team'] != opt1['team']:
                opt2 = cand
                break
    
    candidates.sort(key=lambda x: (x['c_score'], x['smart_score']), reverse=True)
    opt3 = candidates[0]
    for cand in candidates:
        if cand['team'] != opt1['team'] and cand['team'] != opt2['team']:
            opt3 = cand
            break
    
    return [opt1, opt2, opt3]

# --- UI ---
st.title("🧙‍♂️ TFT Set 16: Ryze AI Tool")
st.markdown("**Strategic Diversity:** Full Optimization.")

with st.sidebar:
    st.header("⚙️ Config")
    
    # --- MULTI-LANGUAGE SELECTOR ---
    lang_options = ["English", "Tiếng Việt"] # English Default
    lang_choice = st.selectbox("🌐 Language", lang_options)
    
    t = T[lang_choice] # Current Language

    level = st.selectbox(t["level"], [8, 9, 10, 11])
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button(t["btn_find"], type="primary")
    st.markdown("---")
    
    # --- MERGED EMBLEM INPUTS ---
    r_emblems = {}
    c_emblems = {}
    
    with st.expander(t["emb_region"], expanded=False): # Default Closed
        cols = st.columns(2)
        keys = sorted(REGION_DATA.keys())
        for i, k in enumerate(keys):
            v = cols[i%2].number_input(k, 0, 3, key=f"r_{k}")
            if v: r_emblems[k] = v
            
    with st.expander(t["emb_class"], expanded=False):
        cols = st.columns(2)
        keys = sorted(list(CLASS_DATA.keys())) 
        for i, k in enumerate(keys):
            v = cols[i%2].number_input(k, 0, 3, key=f"c_{k}")
            if v: c_emblems[k] = v
            
    user_emblems = {**r_emblems, **c_emblems}

    # --- PAYPAL / BMC DONATE ---
    st.markdown("---")
    st.markdown(t["donate_title"])
    donate_url = "https://buymeacoffee.com/ngocbaocr1q"
    
    st.markdown(f"""
        <a href="{donate_url}" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #0070BA; 
                color: white; 
                padding: 12px 20px; 
                border-radius: 25px; 
                text-align: center; 
                font-weight: bold;
                font-size: 16px;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
                transition: 0.3s;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0 auto;
            ">
                {t["donate_btn"]}
            </div>
        </a>
    """, unsafe_allow_html=True)

if run:
    slots_for_unlock = level
    slots_for_combat = level - 1 
    
    tab1, tab2, tab3, tab4 = st.tabs(t["tabs"])
    
    pool_easy_eco = [u for u in STANDARD_UNITS if u['cost'] <= 3] 
    pool_mid = [u for u in ALL_UNITS if u['diff'] <= 2]

    # UNLOCK MISSION TAB
    with tab4:
        st.info(t["mission_info"])
        
        def render_unlock(sub_tab):
            with sub_tab:
                with st.spinner(t["spinner_unlock"]):
                    res = solve_unlock_mission(slots_for_unlock, user_emblems) 
                
                if res:
                    for i, data in enumerate(res):
                        expanded = (i==0)
                        u_count = data['unlock_count']
                        
                        if u_count == 0: tag = t["tag_basic"]
                        else: tag = t["tag_unlock"].format(u_count)
                            
                        title = f"{tag} | {t['res_option']} {i+1}: {data['active_count']} {t['res_regions']} ({t['res_cost']}: {data['cost']}🟡)"
                        
                        with st.expander(title, expanded=expanded):
                            st.success(f"{t['active']} {', '.join(data['regions'])}")
                            cols = st.columns(2)
                            active_region_names = [r.split('(')[0] for r in data['regions']]
                            idx = 1
                            for u in data['team']:
                                col = cols[(idx-1) % 2]
                                traits_html = []
                                for tr in u['traits']:
                                    if tr in active_region_names:
                                        traits_html.append(f"<span style='color:#2E7D32'><b>{tr}</b></span>")
                                    else:
                                        traits_html.append(f"<span style='color:#555'>{tr}</b></span>")
                                
                                unit_name_display = u['name']
                                if any(u['name'] == ul['name'] for ul in UNLOCKABLE_UNITS):
                                    unit_name_display += " 🔒"

                                col.markdown(f"{idx}. **{unit_name_display}** ({u['cost']}🟡) : {' '.join(traits_html)}", unsafe_allow_html=True)
                                idx += 1
                else:
                    st.error(t["err_unlock"])
        
        render_unlock(st.container())

    # COMBAT TABS
    def render(tab, pool, p_str=False):
        with tab:
            with st.spinner(t["spinner_combat"]):
                res = solve_three_strategies(pool, slots_for_combat, user_emblems, p_str)
            
            if res:
                for i, data in enumerate(res):
                    if not data: continue
                    team = data['team']
                    r_l = data['r_list']
                    c_l = data['c_list']
                    
                    expanded = (i==0)
                    title = f"{t['labels'][i]}: {len(r_l)} Regions / {len(c_l)} Classes"
                    if data['galio']: title += " (GALIO)"
                    
                    with st.expander(title, expanded=expanded):
                        st.success(f"Regions: {', '.join(r_l)}")
                        if c_l: st.warning(f"Classes: {', '.join(c_l)}")
                        
                        st.divider()
                        cl, cr = st.columns(2)
                        cl.markdown("1. **Ryze** (7🟡) <span style='color:blue'>**(Carry)**</span>", unsafe_allow_html=True)
                        
                        idx = 2
                        for u in team:
                            role_icon = "🛡️" if u.get('role')=='tank' else ("⚔️" if u.get('role')=='carry' else "❤️")
                            traits_html = []
                            unit_note = ""
                            if u['name'] == "Annie": unit_note += " 🐻 (2 Slots)"
                            
                            for tr in u['traits']:
                                if "Targon" in tr: traits_html.append(f"<span style='color:#9C27B0'><b>{tr}</b></span>")
                                elif tr in UNIQUE_TRAITS or tr == "Darkin": traits_html.append(f"<span style='color:#B8860B'><b>{tr}</b></span>")
                                elif any(tr in x for x in r_l): traits_html.append(f"<span style='color:#2E7D32'><b>{tr}</b></span>")
                                elif any(tr in x for x in c_l): traits_html.append(f"<span style='color:#E65100'><b>{tr}</b></span>")
                                else: traits_html.append(f"<span style='color:#555'>{tr}</b></span>")

                            name = "✨ GALIO (FREE)" if u['name'] == "Galio" else u['name']
                            if u['name'] == "Taric": name = "💎 TARIC"
                            if u['name'] == "Ornn": name = "🔨 ORNN"
                            
                            txt = f"{idx}. **{name}**{unit_note} ({u['cost']}🟡) {role_icon} : {' '.join(traits_html)}"
                            
                            if idx-2 < len(team)/2: cr.markdown(txt, unsafe_allow_html=True)
                            else: cl.markdown(txt, unsafe_allow_html=True)
                            idx += 1
            else:
                st.warning(t["err_combat"])

    render(tab1, pool_easy_eco)
    render(tab2, pool_mid, True) 
    render(tab3, ALL_UNITS, True)

elif not run:
    st.info("👈 Select Level -> Click FIND TEAMS")
