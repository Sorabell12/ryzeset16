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
    "Immortal": [1]
}

UNIQUE_TRAITS = [
    "Heroic", "The Boss", "Emperor", "Ascendant", "Star Forger", "Caretaker", 
    "Rune Mage", "Assimilator", "Huntress", "Glutton", "Blacksmith", "Soulbound", 
    "Eternal", "Dragonborn", "Chronokeeper", "Dark Child", "Harvester", "HexMech",
    "Chainbreaker", "Riftscourge", "Immortal"
]

GALIO_UNIT = {"name": "Galio", "traits": ["Demacia", "Invoker", "Heroic"], "cost": 5, "diff": 3, "role": "tank"}

ALL_UNITS = [
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
    {"name": "Vi", "traits": ["Piltover", "Zaun", "Defender"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Xin Zhao", "traits": ["Demacia", "Ionia", "Warden"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Yasuo", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1, "role": "carry"},
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
    {"name": "Kobuko & Yuumi", "traits": ["Yordle", "Bruiser", "Invoker"], "cost": 3, "diff": 2, "role": "tank"},
    
    # 4 COST
    {"name": "Taric", "traits": ["Targon"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Ambessa", "traits": ["Noxus", "Vanquisher"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Bel'Veth", "traits": ["Void", "Slayer"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Braum", "traits": ["Freljord", "Warden"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Garen", "traits": ["Demacia", "Defender"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Lissandra", "traits": ["Freljord", "Invoker"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Lux", "traits": ["Demacia", "Arcanist"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Miss Fortune", "traits": ["Bilgewater", "Gunslinger"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Seraphine", "traits": ["Piltover", "Disruptor"], "cost": 4, "diff": 2, "role": "supp"},
    {"name": "Swain", "traits": ["Noxus", "Arcanist", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Wukong", "traits": ["Ionia", "Bruiser"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Yunara", "traits": ["Ionia", "Quickstriker"], "cost": 4, "diff": 2, "role": "carry"},
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
    {"name": "Aatrox", "traits": ["Darkin", "Slayer"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Annie", "traits": ["Dark Child", "Arcanist"], "cost": 5, "diff": 3, "role": "carry"}, 
    {"name": "Azir", "traits": ["Shurima", "Emperor", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Fiddlesticks", "traits": ["Harvester", "Vanquisher"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Kindred", "traits": ["Eternal", "Quickstriker"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Lucian & Senna", "traits": ["Soulbound", "Gunslinger"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Ornn", "traits": ["Blacksmith", "Warden"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Shyvana", "traits": ["Dragonborn", "Juggernaut"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Zilean", "traits": ["Chronokeeper", "Invoker"], "cost": 5, "diff": 3, "role": "supp"},
    {"name": "Sett", "traits": ["Ionia", "The Boss"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Volibear", "traits": ["Freljord", "Bruiser"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Xerath", "traits": ["Shurima", "Ascendant"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Mel", "traits": ["Noxus", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Ziggs", "traits": ["Zaun", "Yordle", "Longshot"], "cost": 5, "diff": 3, "role": "carry"},

    # 7 COST
    
    # LOWER UNLOCKABLES
    {"name": "Bard", "traits": ["Caretaker"], "cost": 2, "diff": 2, "role": "supp"},
    {"name": "Orianna", "traits": ["Piltover", "Invoker"], "cost": 2, "diff": 2, "role": "supp"},
    {"name": "Poppy", "traits": ["Demacia", "Yordle", "Juggernaut"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "Graves", "traits": ["Bilgewater", "Gunslinger"], "cost": 2, "diff": 2, "role": "carry"},
    {"name": "Yorick", "traits": ["Shadow Isles", "Warden"], "cost": 2, "diff": 2, "role": "tank"},
    {"name": "Tryndamere", "traits": ["Freljord", "Slayer"], "cost": 2, "diff": 2, "role": "carry"},
    {"name": "Darius", "traits": ["Noxus", "Defender"], "cost": 3, "diff": 2, "role": "tank"},
    {"name": "Gwen", "traits": ["Shadow Isles", "Disruptor"], "cost": 3, "diff": 2, "role": "carry"},
    {"name": "Kennen", "traits": ["Ionia", "Yordle", "Defender"], "cost": 1, "diff": 1, "role": "tank"},
    {"name": "LeBlanc", "traits": ["Noxus", "Invoker"], "cost": 3, "diff": 2, "role": "carry"},
    {"name": "Fizz", "traits": ["Bilgewater", "Yordle"], "cost": 1, "diff": 2, "role": "carry"},
    {"name": "Warwick", "traits": ["Zaun", "Quickstriker"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Yone", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1, "role": "carry"},
]

# --- ALGORITHM ---
def solve_three_strategies(pool, slots, user_emblems, prioritize_strength=False):
    region_units = [u for u in pool if any(t in REGION_DATA for t in u['traits'])]
    targon = [u for u in pool if "Targon" in u['traits']]
    
    if prioritize_strength:
        # EXODIA POOL
        high_cost = [u for u in pool if u['cost'] >= 4]
        mid_cost = [u for u in pool if u['cost'] == 3]
        efficient_low = [u for u in region_units if u['cost'] < 3 and len(u['traits']) >= 3]
        
        raw_pool = high_cost + mid_cost + efficient_low + targon
        final_pool = list({v['name']:v for v in raw_pool}.values())
        final_pool.sort(key=lambda x: x['cost'] + (1 if len(x['traits'])>=3 else 0), reverse=True)
        final_pool = final_pool[:35] 
    else:
        connectors = [u for u in region_units if len([t for t in u['traits'] if t in REGION_DATA]) >= 2]
        others = [u for u in region_units if u not in connectors]
        final_pool = connectors + targon + others[:16]

    limit_max = 1500000
    loop_count = 0
    candidates = []

    for team in itertools.combinations(final_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        if len(set([u['name'] for u in team])) < len(team): continue

        traits = {}
        tank_count = 0
        names = [u['name'] for u in team]
        
        for u in team:
            if u.get('role') == 'tank': tank_count += 1
            for t in u['traits']:
                traits[t] = traits.get(t, 0) + 1
            if u['name'] == "Annie": # Tibbers Effect
                traits['Arcanist'] = traits.get('Arcanist', 0) + 1
                
        for emb, count in user_emblems.items():
            traits[emb] = traits.get(emb, 0) + count
        
        # Galio
        has_galio = False
        final_team = list(team)
        if traits.get("Demacia", 0) >= 6:
            has_galio = True
            final_team.append(GALIO_UNIT)
            tank_count += 1
            for t in GALIO_UNIT['traits']: traits[t] = traits.get(t, 0) + 1
        
        r_score = 0
        unused_emblem_penalty = 0
        for r, data in REGION_DATA.items():
            if traits.get(r, 0) >= data['thresholds'][0]: 
                r_score += 1
            elif user_emblems.get(r, 0) > 0:
                unused_emblem_penalty -= 15
        
        c_score = 0
        for cl, thresholds in CLASS_DATA.items():
            if traits.get(cl, 0) >= thresholds[0]: c_score += 1
            
        for u_trait in UNIQUE_TRAITS:
            if traits.get(u_trait, 0) >= 1:
                unit_with_trait = next((u for u in final_team if u_trait in u['traits']), None)
                if unit_with_trait:
                    is_supported = False
                    for other_t in unit_with_trait['traits']:
                        if other_t == u_trait: continue
                        if other_t in REGION_DATA and traits.get(other_t, 0) >= REGION_DATA[other_t]['thresholds'][0]: is_supported = True
                        if other_t in CLASS_DATA and traits.get(other_t, 0) >= CLASS_DATA[other_t][0]: is_supported = True
                    if is_supported: c_score += 1

        balance_penalty = 0
        if tank_count < 2: balance_penalty = -5 
        elif tank_count < 3 and slots >= 8: balance_penalty = -2
        
        # --- SLOT TAX FOR ANNIE ---
        annie_penalty = 0
        if "Annie" in names:
            annie_penalty = -12 # Heavy penalty for taking 2 slots
        
        targon_bonus = 3 if traits.get("Targon", 0) >= 1 else 0
        if "Taric" in names: targon_bonus += 3
        
        final_r = r_score + (5 if has_galio else 0)
        
        # Smart Score updated with Annie Penalty
        smart_score = (final_r * 3.5) + c_score + balance_penalty + unused_emblem_penalty + targon_bonus + annie_penalty
        
        r_list_fmt = [f"{r}({traits[r]})" for r in REGION_DATA if traits.get(r,0) >= REGION_DATA[r]['thresholds'][0]]
        c_list_fmt = [f"{c}({traits[c]})" for c in CLASS_DATA if traits.get(c,0) >= CLASS_DATA[c][0]]
        
        for u_trait in UNIQUE_TRAITS:
            if traits.get(u_trait, 0) >= 1:
                unit_with_trait = next((u for u in final_team if u_trait in u['traits']), None)
                if unit_with_trait:
                    is_supported = False
                    for other_t in unit_with_trait['traits']:
                        if other_t == u_trait: continue
                        if other_t in REGION_DATA and traits.get(other_t, 0) >= REGION_DATA[other_t]['thresholds'][0]: is_supported = True
                        if other_t in CLASS_DATA and traits.get(other_t, 0) >= CLASS_DATA[other_t][0]: is_supported = True
                    if is_supported: c_list_fmt.append(f"{u_trait}")
        
        if traits.get("Darkin", 0) >= 1: c_list_fmt.append(f"Darkin({traits['Darkin']})")

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
    
    candidates.sort(key=lambda x: x['smart_score'], reverse=True)
    opt3 = candidates[0]
    for cand in candidates:
        if cand['team'] != opt1['team'] and cand['team'] != opt2['team']:
            opt3 = cand
            break
    
    return [opt1, opt2, opt3]

# --- UI ---
st.title("🧙‍♂️ TFT Set 16: Ryze AI Tool")
st.markdown("**Strategic Diversity:** Targon Priority + Annie Slot Tax.")

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
    tab1, tab2, tab3 = st.tabs(["Low Cost", "Standard", "EXODIA (Smart Value)"])
    
    pool_easy = [u for u in ALL_UNITS if u['diff'] == 1]
    pool_mid = [u for u in ALL_UNITS if u['diff'] <= 2]
    
    def render(tab, pool, p_str=False):
        with tab:
            if p_str: st.caption("Prioritizes **Taric/Targon** & Slot Efficiency.")
            with st.spinner("Analyzing strategies..."):
                res = solve_three_strategies(pool, slots, user_emblems, p_str)
            
            if res:
                labels = [
                    "👑 Option 1: BEST BALANCED (AI Choice)",
                    "🌍 Option 2: MAX REGIONS (Ryze Max Power)",
                    "🛡️ Option 3: ALTERNATIVE VARIATION"
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
                        cl.markdown("1. **Ryze** <span style='color:blue'>**(Carry)**</span>", unsafe_allow_html=True)
                        
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
                            
                            txt = f"{idx}. **{name}**{unit_note} {role_icon} : {' '.join(traits_html)}"
                            
                            if idx-2 < len(team)/2: cr.markdown(txt, unsafe_allow_html=True)
                            else: cl.markdown(txt, unsafe_allow_html=True)
                            idx += 1
            else:
                st.warning("No valid team found.")

    render(tab1, pool_easy)
    render(tab2, pool_mid)
    render(tab3, ALL_UNITS, True)

elif not run:
    st.info("👈 Select Level -> Click FIND TEAMS")
