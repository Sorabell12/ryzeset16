import streamlit as st
import itertools

# --- 1. PAGE CONFIG & CSS ---
st.set_page_config(page_title="TFT Set 16 Optimizer", page_icon="🧠", layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 1rem 1rem 0rem 1rem; }
        section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
        div.stButton > button { width: 100%; background-color: #FF4B4B; color: white; font-weight: bold; border: none; }
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
    "Heroic": [1]
}

GALIO_UNIT = {"name": "Galio", "traits": ["Demacia", "Invoker", "Heroic"], "cost": 5, "diff": 3, "role": "tank"}

# --- UPDATED UNITS WITH ROLES & TRAIT EFFICIENCY ---
ALL_UNITS = [
    # 1 COST (Note: Briar updated to tank role for Juggernaut logic)
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
    # 4 COST
    {"name": "Ambessa", "traits": ["Noxus", "Vanquisher"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Bel'Veth", "traits": ["Void", "Slayer"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Braum", "traits": ["Freljord", "Warden"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Garen", "traits": ["Demacia", "Defender"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Lissandra", "traits": ["Freljord", "Invoker"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Lux", "traits": ["Demacia", "Arcanist"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Miss Fortune", "traits": ["Bilgewater", "Gunslinger"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Seraphine", "traits": ["Piltover", "Disruptor"], "cost": 4, "diff": 2, "role": "supp"},
    {"name": "Swain", "traits": ["Noxus", "Arcanist", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Taric", "traits": ["Targon"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Wukong", "traits": ["Ionia", "Bruiser"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Yunara", "traits": ["Ionia", "Quickstriker"], "cost": 4, "diff": 2, "role": "carry"},
    # 5 COST
    {"name": "Annie", "traits": ["Dark Child", "Arcanist"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Azir", "traits": ["Shurima", "Emperor", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Fiddlesticks", "traits": ["Harvester", "Vanquisher"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Kindred", "traits": ["Eternal", "Quickstriker"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Lucian & Senna", "traits": ["Soulbound", "Gunslinger"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Ornn", "traits": ["Blacksmith", "Warden"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Shyvana", "traits": ["Dragonborn", "Juggernaut"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Zilean", "traits": ["Chronokeeper", "Invoker"], "cost": 5, "diff": 3, "role": "supp"},
    {"name": "Aatrox", "traits": ["Darkin", "Slayer"], "cost": 5, "diff": 3, "role": "carry"},
    {"name": "Sett", "traits": ["Ionia", "The Boss"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Volibear", "traits": ["Freljord", "Bruiser"], "cost": 5, "diff": 3, "role": "tank"},
    {"name": "Xerath", "traits": ["Shurima", "Ascendant"], "cost": 5, "diff": 3, "role": "carry"},
    # 7 COST
    {"name": "Ryze (Clone)", "traits": ["Rune Mage"], "cost": 7, "diff": 3, "role": "carry"},
    {"name": "Sylas", "traits": ["Chainbreaker", "Arcanist", "Defender"], "cost": 7, "diff": 3, "role": "tank"},
    # UNLOCKABLES (Only Easy/Medium)
    {"name": "Mel", "traits": ["Noxus", "Disruptor"], "cost": 5, "diff": 3, "role": "carry"},
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
    {"name": "Diana", "traits": ["Targon"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Fizz", "traits": ["Bilgewater", "Yordle"], "cost": 1, "diff": 2, "role": "carry"},
    {"name": "Kai'Sa", "traits": ["Void", "Longshot", "Assimilator"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Kalista", "traits": ["Shadow Isles", "Vanquisher"], "cost": 4, "diff": 2, "role": "carry"},
    {"name": "Nasus", "traits": ["Shurima"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Renekton", "traits": ["Shurima"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Singed", "traits": ["Zaun", "Juggernaut"], "cost": 4, "diff": 2, "role": "tank"},
    {"name": "Veigar", "traits": ["Yordle", "Arcanist"], "cost": 4, "diff": 3, "role": "carry"},
    {"name": "Warwick", "traits": ["Zaun", "Quickstriker"], "cost": 1, "diff": 1, "role": "carry"},
    {"name": "Yone", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1, "role": "carry"},
]

# --- SMART ALGORITHM: VALUE OVER COST ---
def solve_comp_smart(pool, slots, user_emblems, prioritize_strength=False):
    region_units = [u for u in pool if any(t in REGION_DATA for t in u['traits'])]
    targon = [u for u in pool if "Targon" in u['traits']]
    
    # Filter High Cost but ALSO High Efficiency (3 Traits or Tank)
    # This fixes the "Briar vs Ambessa" issue. Briar (3 traits) is kept.
    
    if prioritize_strength:
        # SMART EXODIA POOL SELECTION
        # 1. Include all 5 & 7 Costs
        exodia_units = [u for u in pool if u['cost'] >= 5]
        
        # 2. Include Targon (Always good for Ryze)
        
        # 3. Include "Efficiency Monsters" (Units with 3+ Traits, regardless of cost)
        # Example: Briar (Noxus/Slayer/Juggernaut), Swain, Neeko
        efficient_units = [u for u in region_units if len(u['traits']) >= 3]
        
        # 4. Include High Cost 4-costs
        high_cost_4 = [u for u in pool if u['cost'] == 4]
        
        # Combine unique units
        raw_pool = exodia_units + targon + efficient_units + high_cost_4
        # Remove duplicates based on name
        final_pool = list({v['name']:v for v in raw_pool}.values())
        
        # Limit pool size for performance (Keep max 28 units)
        # Sort by: Cost + (1 if 3 traits) + (0.5 if Tank)
        # This ensures Briar stays in the pool even if we cut
        final_pool.sort(key=lambda x: x['cost'] + (1.5 if len(x['traits'])>=3 else 0), reverse=True)
        final_pool = final_pool[:28]
        
    else:
        # Standard Logic
        connectors = [u for u in region_units if len([t for t in u['traits'] if t in REGION_DATA]) >= 2]
        others = [u for u in region_units if u not in connectors]
        final_pool = connectors + targon + others[:16]

    limit_max = 2000000
    loop_count = 0
    candidates = []

    for team in itertools.combinations(final_pool, slots):
        loop_count += 1
        if loop_count > limit_max: break
        if len(set([u['name'] for u in team])) < len(team): continue

        traits = {}
        total_cost = 0
        tank_count = 0
        
        for u in team:
            total_cost += u.get('cost', 1)
            if u.get('role') == 'tank': tank_count += 1
            for t in u['traits']:
                traits[t] = traits.get(t, 0) + 1
        for emb, count in user_emblems.items():
            traits[emb] = traits.get(emb, 0) + count
        
        # Galio Logic
        has_galio = False
        final_team = list(team)
        if traits.get("Demacia", 0) >= 5:
            has_galio = True
            final_team.append(GALIO_UNIT)
            tank_count += 1
            for t in GALIO_UNIT['traits']: traits[t] = traits.get(t, 0) + 1
        
        r_score = 0
        for r, data in REGION_DATA.items():
            if traits.get(r, 0) >= data['thresholds'][0]: r_score += 1
        
        c_score = 0
        for cl, thresholds in CLASS_DATA.items():
            if traits.get(cl, 0) >= thresholds[0]: c_score += 1
            elif cl == "Heroic" and traits.get(cl, 0) >= 1: c_score += 1

        # Penalties & Bonuses
        balance_penalty = 0
        if tank_count < 2: balance_penalty = -5 
        elif tank_count < 3 and slots >= 8: balance_penalty = -2
        
        galio_bonus = 5 if has_galio else 0
        final_r_score = r_score + galio_bonus
        
        # --- NEW SCORING: SYNERGY > COST ---
        if prioritize_strength:
            # Prioritize: Regions -> Classes -> Cost
            # This ensures Briar (activates Juggernaut -> +1 Class) beats Ambessa (No Class -> +0)
            sort_key = (final_r_score + balance_penalty, c_score, total_cost)
        else:
            sort_key = (final_r_score + balance_penalty, c_score, total_cost)
            
        r_list = [f"{r}({traits[r]})" for r in REGION_DATA if traits.get(r,0) >= REGION_DATA[r]['thresholds'][0]]
        c_list = [f"{c}({traits[c]})" for c in CLASS_DATA if traits.get(c,0) >= CLASS_DATA[c][0] or (c=="Heroic" and traits.get(c,0)>=1)]
        
        candidates.append((sort_key, (final_team, r_list, c_list, has_galio, final_r_score, tank_count)))

    # Diversity Filter
    candidates.sort(key=lambda x: x[0], reverse=True)
    final_top_3 = []
    if candidates:
        opt1 = candidates[0]
        final_top_3.append(opt1)
        best_r = opt1[1][4]
        
        opt2 = None
        for cand in candidates:
            if cand[1][4] < best_r or abs(cand[1][5] - opt1[1][5]) >= 2:
                opt2 = cand
                break
        if not opt2 and len(candidates)>1: opt2 = candidates[1]
        
        if opt2:
            final_top_3.append(opt2)
            opt3 = None
            for cand in candidates:
                if cand != opt1 and cand != opt2 and (cand[1][4] != opt2[1][4] or cand[0] < opt2[0]):
                    opt3 = cand
                    break
            if not opt3:
                for cand in candidates:
                    if cand != opt1 and cand != opt2:
                        opt3 = cand
                        break
            if opt3: final_top_3.append(opt3)
            
    return final_top_3

# --- UI ---
st.title("🧙‍♂️ TFT Set 16: Ryze AI Tool")

with st.sidebar:
    st.header("⚙️ Config")
    level = st.selectbox("Level:", [8, 9, 10, 11])
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("🚀 FIND SMART TEAMS", type="primary")
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
            if p_str: st.caption("Prioritizes Synergy Efficiency & High Cost Units.")
            with st.spinner("Analyzing efficient combinations..."):
                res = solve_comp_smart(pool, slots, user_emblems, p_str)
            
            if res:
                for rank, (score, comp) in enumerate(res):
                    team, r_l, c_l, galio, r_val, tanks = comp
                    expanded = (rank==0)
                    
                    if rank == 0: lbl = "👑 BEST VALUE"
                    elif rank == 1: lbl = "⚔️ VARIATION"
                    else: lbl = "🛡️ ALTERNATIVE"
                    
                    title = f"{lbl}: {len(r_l)} Regions / {len(c_l)} Classes"
                    if galio: title += " (GALIO)"
                    
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
                            for t in u['traits']:
                                if "Targon" in t: traits_html.append(f"<span style='color:#9C27B0'><b>{t}</b></span>")
                                elif any(t in x for x in r_l): traits_html.append(f"<span style='color:#2E7D32'><b>{t}</b></span>")
                                elif any(t in x for x in c_l): traits_html.append(f"<span style='color:#E65100'><b>{t}</b></span>")
                                else: traits_html.append(f"<span style='color:#555'>{t}</span>")

                            if u['name'] == "Galio": name = "✨ GALIO (FREE)"
                            else: name = u['name']
                            
                            txt = f"{idx}. **{name}** {role_icon} : {' '.join(traits_html)}"
                            
                            if idx-2 < len(team)/2: cr.markdown(txt, unsafe_allow_html=True)
                            else: cl.markdown(txt, unsafe_allow_html=True)
                            idx += 1
            else:
                st.warning("No valid team found.")

    render(tab1, pool_easy)
    render(tab2, pool_mid)
    render(tab3, ALL_UNITS, True)

elif not run:
    st.info("👈 Select Level -> Click FIND SMART TEAMS")

