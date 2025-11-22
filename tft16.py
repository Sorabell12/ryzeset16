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
    </style>
""", unsafe_allow_html=True)

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

# --- UNIT LISTS (CORRECTED) ---
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
    {"name": "Garen", "traits": ["Demacia", "Defender"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Lissandra", "traits": ["Freljord", "Invoker"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Lux", "traits": ["Demacia", "Arcanist"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Miss Fortune", "traits": ["Bilgewater", "Gunslinger"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Seraphine", "traits": ["Piltover", "Disruptor"], "cost": 4, "diff": 2, "role": "supp"},
    {"name": "Swain", "traits": ["Noxus", "Arcanist", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Wukong", "traits": ["Ionia", "Bruiser"], "cost": 4, "diff": 2, "role": "tank"},
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

# --- NEW ALGORITHM: SYNERGY NETWORK BUILDER ---
def build_synergy_pool(base_pool, user_emblems, prioritize_strength=False):
    # 1. Hạt giống từ Ấn (Seeds)
    seed_traits = set(user_emblems.keys())
    seed_traits.add("Targon") # Luôn tìm Targon
    
    seed_units = [u for u in base_pool if any(t in seed_traits for t in u['traits'])]
    
    # 2. Xác định các Class liên quan (Linked Classes)
    # Ví dụ: Có Sejuani (Freljord) -> Linked Class = Defender, Bruiser
    linked_classes = set()
    for u in seed_units:
        for t in u['traits']:
            if t in CLASS_DATA: 
                linked_classes.add(t)
    
    final_pool = []
    seen_names = set()

    # 3. Thêm tướng Hạt giống
    for u in seed_units:
        if u['name'] not in seen_names:
            final_pool.append(u)
            seen_names.add(u['name'])
            
    # 4. Thêm tướng Liên kết (Có chung Class với hạt giống)
    # Ví dụ: Có Sejuani -> Lấy thêm Braum (Defender), Shen (Defender)
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

    # 5. Điền chỗ trống bằng tướng đắt tiền (nếu còn thiếu)
    if len(final_pool) < 45:
        expensive_fillers = [u for u in base_pool if u['cost'] >= 4 and u['name'] not in seen_names]
        final_pool.extend(expensive_fillers)

    # 6. Sắp xếp
    if prioritize_strength:
        # Đắt tiền lên đầu -> Để itertools xét trước -> Braum/Sejuani ưu tiên hơn Anivia
        final_pool.sort(key=lambda x: (x['cost'], len(x['traits'])), reverse=True)
    else:
        # Rẻ tiền lên đầu
        final_pool.sort(key=lambda x: x['cost'])
        
    return final_pool[:45]

# --- ALGORITHM 1: UNLOCK MISSION (FIX: FORCED DIVERSITY) ---
def solve_unlock_mission(pool, slots, user_emblems):
    candidates = []
    limit_max = 2000000 
    loop_count = 0

    # Lấy tất cả tướng có hệ Vùng Đất
    region_units = [u for u in pool if any(t in REGION_DATA for t in u['traits'])]
    
    # --- FIX: BẮT BUỘC ĐA DẠNG ---
    # Lấy 2 tướng rẻ nhất từ MỖI vùng đất để đảm bảo không vùng nào bị bỏ rơi
    forced_pool = []
    for r in REGION_DATA.keys():
        units_in_region = [u for u in region_units if r in u['traits']]
        units_in_region.sort(key=lambda x: x['cost'])
        forced_pool.extend(units_in_region[:3]) # Lấy 3 con rẻ nhất mỗi vùng
    
    # Gộp và lọc trùng
    region_units.sort(key=lambda x: x['cost'])
    combined_pool = forced_pool + region_units[:25] # Thêm 25 con rẻ nhất chung
    search_pool = list({v['name']:v for v in combined_pool}.values())

    for team in itertools.combinations(search_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        if len(set([u['name'] for u in team])) < len(team): continue

        traits = {}
        total_cost = 0
        
        for u in team:
            total_cost += u.get('cost', 1)
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
                "regions": active_list
            })
            if len(candidates) >= 5: break
    
    candidates.sort(key=lambda x: (-x['active_count'], x['cost']))
    return candidates[:3]

# --- ALGORITHM 2: STANDARD OPTIMIZER (SYNERGY LOGIC) ---
def solve_three_strategies(pool, slots, user_emblems, prioritize_strength=False):
    
    # SỬ DỤNG SYNERGY POOL THAY VÌ LỌC CỨNG
    final_pool = build_synergy_pool(pool, user_emblems, prioritize_strength)

    limit_max = 2000000
    loop_count = 0
    candidates = []

    for team in itertools.combinations(final_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        if len(set([u['name'] for u in team])) < len(team): continue

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
        
        c_score = 0
        active_classes_set = set()
        for cl, thresholds in CLASS_DATA.items():
            if traits.get(cl, 0) >= thresholds[0]: 
                c_score += 1
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
        elif targon_c > 1: useless_unit_penalty -= 20
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
                        if is_supported: c_score += 1

        balance_penalty = 0
        if tank_count < 2: balance_penalty = -10 
        
        targon_bonus = 0
        if "Taric" in names: targon_bonus += 20
        annie_penalty = -12 if "Annie" in names else 0
        
        final_r = r_score + (5 if has_galio else 0)
        
        # --- DYNAMIC SCORING (PURE) ---
        strength_score = 0
        if prioritize_strength:
            strength_score = team_total_cost * 2.0 

        smart_score = (final_r * 25.0) + \
                      (c_score * 12.0) + \
                      strength_score + \
                      balance_penalty + unused_emblem_penalty + targon_bonus + annie_penalty + useless_unit_penalty
        
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
    level = st.selectbox("Level:", [8, 9, 10, 11])
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("🚀 FIND TEAMS", type="primary")
    st.markdown("---")
    with st.expander("🧩 Region Emblems", expanded=False):
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

if run:
    slots = level - 1
    tab1, tab2, tab3, tab4 = st.tabs(["Low Cost (Eco)", "Standard", "EXODIA", "🔓 UNLOCK RYZE"])
    
    pool_easy_eco = [u for u in STANDARD_UNITS if u['cost'] <= 3] 
    pool_mid = [u for u in ALL_UNITS if u['diff'] <= 2]

    # UNLOCK MISSION TAB
    with tab4:
        st.info("🏆 **Mission:** Activate 5 Regions to Unlock Ryze.")
        st.caption("Only uses STANDARD units (Base Pool) to calculate.")
        
        unlock_pool = [u for u in STANDARD_UNITS] 
        
        def render_unlock(sub_tab, u_pool):
            with sub_tab:
                with st.spinner("Calculating cheapest 5-Region comps..."):
                    res = solve_unlock_mission(u_pool, level, user_emblems) 
                
                if res:
                    for i, data in enumerate(res):
                        expanded = (i==0)
                        title = f"🎯 Option {i+1}: {data['active_count']} Regions (Cost: {data['cost']}🟡)"
                        
                        with st.expander(title, expanded=expanded):
                            st.success(f"**Active:** {', '.join(data['regions'])}")
                            cols = st.columns(2)
                            
                            active_region_names = [r.split('(')[0] for r in data['regions']]

                            idx = 1
                            for u in data['team']:
                                col = cols[(idx-1) % 2]
                                
                                traits_html = []
                                for t in u['traits']:
                                    if t in active_region_names:
                                        traits_html.append(f"<span style='color:#2E7D32'><b>{t}</b></span>")
                                    else:
                                        traits_html.append(f"<span style='color:#555'>{t}</span>")
                                
                                col.markdown(f"{idx}. **{u['name']}** ({u['cost']}🟡) : {' '.join(traits_html)}", unsafe_allow_html=True)
                                idx += 1
                else:
                    st.error("Cannot find 5 regions using Standard Units.")
        
        render_unlock(st.container(), unlock_pool)

    def render(tab, pool, p_str=False):
        with tab:
            if p_str: st.caption("Prioritizes Strength & High Cost Units.")
            elif pool == pool_easy_eco: st.caption("Uses Cost 1, 2, 3 units for max synergy.")
            
            with st.spinner("Analyzing strategies..."):
                res = solve_three_strategies(pool, slots, user_emblems, p_str)
            
            if res:
                labels = [
                    "👑 Option 1: BEST BALANCED (AI Choice)",
                    "🌍 Option 2: MAX REGIONS (Ryze Max Power)",
                    "🛡️ Option 3: MAX SYNERGY (Trait Count)"
                ]
                
                for i, data in enumerate(res):
                    if not data: continue
                    team = data['team']
                    r_l = data['r_list']
                    c_l = data['c_list']
                    
                    expanded = (i==0)
                    title = f"{labels[i]}: {len(r_l)} Regions / {len(c_l)} Classes"
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
                            if u['name'] == "Annie": unit_note = " (+Tibbers)"
                            
                            for t in u['traits']:
                                if "Targon" in t: traits_html.append(f"<span style='color:#9C27B0'><b>{t}</b></span>")
                                elif t in UNIQUE_TRAITS or t == "Darkin": traits_html.append(f"<span style='color:#B8860B'><b>{t}</b></span>")
                                elif any(t in x for x in r_l): traits_html.append(f"<span style='color:#2E7D32'><b>{t}</b></span>")
                                elif any(t in x for x in c_l): traits_html.append(f"<span style='color:#E65100'><b>{t}</b></span>")
                                else: traits_html.append(f"<span style='color:#555'>{t}</span>")

                            name = "✨ GALIO (FREE)" if u['name'] == "Galio" else u['name']
                            if u['name'] == "Taric": name = "💎 TARIC"
                            if u['name'] == "Ornn": name = "🔨 ORNN"
                            
                            txt = f"{idx}. **{name}**{unit_note} ({u['cost']}🟡) {role_icon} : {' '.join(traits_html)}"
                            
                            if idx-2 < len(team)/2: cr.markdown(txt, unsafe_allow_html=True)
                            else: cl.markdown(txt, unsafe_allow_html=True)
                            idx += 1
            else:
                st.warning("No valid team found.")

    render(tab1, pool_easy_eco)
    render(tab2, pool_mid, True) 
    render(tab3, ALL_UNITS, True)

elif not run:
    st.info("👈 Select Level -> Click FIND TEAMS")
