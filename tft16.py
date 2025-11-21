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

# --- DỮ LIỆU ---
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
    "Quickstriker": [2, 3, 4, 5], "Disruptor": [2, 4], "Vanquisher": [2, 3, 4, 5],
    "Heroic": [1]
}

# GALIO UNIT
GALIO_UNIT = {"name": "Galio", "traits": ["Demacia", "Invoker", "Heroic"], "cost": 5, "diff": 3}

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
    {"name": "Aatrox", "traits": ["Darkin", "Slayer"], "cost": 5, "diff": 3},
    {"name": "Sett", "traits": ["Ionia", "The Boss"], "cost": 5, "diff": 3},
    {"name": "Volibear", "traits": ["Freljord", "Bruiser"], "cost": 5, "diff": 3},
    {"name": "Xerath", "traits": ["Shurima", "Ascendant"], "cost": 5, "diff": 3},
    
    # UNLOCKABLES
    {"name": "Mel", "traits": ["Noxus", "Disruptor"], "cost": 5, "diff": 3},
    {"name": "Bard", "traits": ["Caretaker"], "cost": 2, "diff": 2},
    {"name": "Orianna", "traits": ["Piltover", "Invoker"], "cost": 2, "diff": 2},
    {"name": "Poppy", "traits": ["Demacia", "Yordle", "Juggernaut"], "cost": 1, "diff": 1},
    {"name": "Graves", "traits": ["Bilgewater", "Gunslinger"], "cost": 2, "diff": 2},
    {"name": "Yorick", "traits": ["Shadow Isles", "Warden"], "cost": 2, "diff": 2},
    {"name": "Tryndamere", "traits": ["Freljord", "Slayer"], "cost": 2, "diff": 2},
    {"name": "Darius", "traits": ["Noxus", "Defender"], "cost": 3, "diff": 2},
    {"name": "Gwen", "traits": ["Shadow Isles", "Disruptor"], "cost": 3, "diff": 2},
    {"name": "Kennen", "traits": ["Ionia", "Yordle", "Defender"], "cost": 1, "diff": 1},
    {"name": "LeBlanc", "traits": ["Noxus", "Invoker"], "cost": 3, "diff": 2},
    {"name": "Diana", "traits": ["Targon"], "cost": 4, "diff": 2},
    {"name": "Fizz", "traits": ["Bilgewater", "Yordle"], "cost": 1, "diff": 2},
    {"name": "Kai'Sa", "traits": ["Void", "Longshot", "Assimilator"], "cost": 4, "diff": 2},
    {"name": "Kalista", "traits": ["Shadow Isles", "Vanquisher"], "cost": 4, "diff": 2},
    {"name": "Nasus", "traits": ["Shurima"], "cost": 4, "diff": 2},
    {"name": "Renekton", "traits": ["Shurima"], "cost": 4, "diff": 2},
    {"name": "Singed", "traits": ["Zaun", "Juggernaut"], "cost": 4, "diff": 2},
    {"name": "Veigar", "traits": ["Yordle", "Arcanist"], "cost": 4, "diff": 3},
    {"name": "Warwick", "traits": ["Zaun", "Quickstriker"], "cost": 1, "diff": 1},
    {"name": "Yone", "traits": ["Ionia", "Slayer"], "cost": 1, "diff": 1},
]

# --- NEW ALGORITHM: DIVERSITY CHECK ---
def solve_comp_diverse(pool, slots, user_emblems, prioritize_strength=False):
    # 1. Pool Preparation
    region_units = [u for u in pool if any(t in REGION_DATA for t in u['traits'])]
    targon = [u for u in pool if "Targon" in u['traits']]
    high_cost_neutral = [u for u in pool if u['cost'] >= 4 and u not in region_units]
    
    if prioritize_strength:
        sorted_pool = sorted(region_units + high_cost_neutral, key=lambda x: x['cost'], reverse=True)
        final_pool = sorted_pool[:22]
        final_pool = list({v['name']:v for v in final_pool + targon}.values())
    else:
        connectors = [u for u in region_units if len([t for t in u['traits'] if t in REGION_DATA]) >= 2]
        others = [u for u in region_units if u not in connectors]
        final_pool = connectors + targon + others[:15]

    limit_max = 1500000
    loop_count = 0
    
    # Store top candidates
    candidates = [] # List of tuples (score_tuple, details)

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
        
        # GALIO Logic
        demacia_count = traits.get("Demacia", 0)
        has_galio = False
        final_team = list(team)
        
        if demacia_count >= 5:
            has_galio = True
            final_team.append(GALIO_UNIT)
            for t in GALIO_UNIT['traits']:
                traits[t] = traits.get(t, 0) + 1
        
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
            elif cl == "Heroic" and c >= 1:
                c_score += 1
                c_list.append(f"Heroic({c})")

        bonus_score = 5 if has_galio else 0 
        
        # Primary score includes Bonus, but we keep r_score separate for diversity check
        if prioritize_strength:
            sort_key = (r_score + bonus_score, total_cost, c_score)
        else:
            sort_key = (r_score + bonus_score, c_score, total_cost)
            
        details = (final_team, r_list, c_list, has_galio, r_score + bonus_score)
        
        # We keep a buffer of good candidates
        candidates.append((sort_key, details))
    
    # --- DIVERSITY FILTERING ---
    # Sort all candidates by score
    candidates.sort(key=lambda x: x[0], reverse=True)
    
    final_top_3 = []
    
    if candidates:
        # Option 1: Absolute Best
        opt1 = candidates[0]
        final_top_3.append(opt1)
        best_r_score = opt1[1][4] # Get r_score from details
        
        # Option 2: Find best team with DIFFERENT Region Score (e.g., 4 instead of 5)
        # If not found, find one with significantly different cost/classes
        opt2 = None
        for cand in candidates:
            r_val = cand[1][4]
            if r_val < best_r_score: # Strict diversity in regions
                opt2 = cand
                break
        
        if not opt2: # If no different region count exists, pick next best
             if len(candidates) > 1: opt2 = candidates[1]
        
        if opt2:
            final_top_3.append(opt2)
            
            # Option 3: Find best team with DIFFERENT Region Score from both
            opt3 = None
            r_val_2 = opt2[1][4]
            
            for cand in candidates:
                r_val = cand[1][4]
                if r_val < r_val_2 and r_val < best_r_score:
                    opt3 = cand
                    break
            
            if not opt3: # Fallback
                # Find something not equal to opt1 and opt2 indices
                for cand in candidates:
                    if cand != opt1 and cand != opt2:
                        opt3 = cand
                        break
            
            if opt3:
                final_top_3.append(opt3)

    return final_top_3

# --- UI LAYOUT ---
st.title("🧙‍♂️ TFT Set 16: Ryze Tool")

with st.sidebar:
    st.header("⚙️ Config")
    level = st.selectbox("Level:", [8, 9, 10, 11])
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("🚀 FIND DIVERSE TEAMS", type="primary", use_container_width=True)
    st.markdown("---")
    with st.expander("🧩 Region Emblems (Optional)", expanded=False):
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
    tab1, tab2, tab3 = st.tabs(["Low Cost", "Standard", "EXODIA (Realistic)"])
    
    pool_easy = [u for u in ALL_UNITS if u['diff'] == 1]
    pool_mid = [u for u in ALL_UNITS if u['diff'] <= 2]
    
    def render_top3_results(tab, pool, p_strength=False):
        with tab:
            if p_strength: st.caption("ℹ️ Prioritizes high cost units.")
            
            with st.spinner("Analyzing diverse strategies..."):
                top_3 = solve_comp_diverse(pool, slots, user_emblems, p_strength)
            
            if top_3:
                for rank, (score, comp) in enumerate(top_3):
                    team, r_list, c_list, has_galio, total_r = comp
                    is_expanded = (rank == 0)
                    
                    # Dynamic Title based on rank
                    if rank == 0:
                        strat_name = "👑 Option 1: MAX REGIONS (Ceiling)"
                    elif rank == 1:
                        strat_name = "⚖️ Option 2: BALANCED / VARIATION"
                    else:
                        strat_name = "🛡️ Option 3: ALTERNATIVE"

                    title_label = f"{strat_name} — {len(r_list)} Regions / {len(c_list)} Classes"
                    if has_galio: title_label += " 🔥 GALIO"
                    
                    with st.expander(title_label, expanded=is_expanded):
                        st.success(f"🌍 **Regions:** {', '.join(r_list)}")
                        if c_list: st.warning(f"🛡️ **Classes:** {', '.join(c_list)}")
                        
                        st.divider()
                        col_l, col_r = st.columns(2)
                        col_l.markdown("1. **Ryze** : <span style='color:blue'>**Rune Mage**</span>", unsafe_allow_html=True)
                        
                        idx_counter = 2
                        for u in team:
                            traits_html = []
                            for t in u['traits']:
                                if "Targon" in t: traits_html.append(f"<span style='color:#9C27B0'><b>{t}</b></span>")
                                elif any(t in x for x in r_list): traits_html.append(f"<span style='color:#2E7D32'><b>{t}</b></span>")
                                elif any(t in x for x in c_list): traits_html.append(f"<span style='color:#E65100'><b>{t}</b></span>")
                                else: traits_html.append(f"<span style='color:#555'>{t}</span>")
                            
                            name_display = u['name']
                            if u['name'] == "Galio":
                                name_display = "✨ GALIO (FREE)"
                            
                            row_html = f"{idx_counter}. **{name_display}** : {' '.join(traits_html)}"
                            
                            if idx_counter - 2 < (len(team) // 2): col_r.markdown(row_html, unsafe_allow_html=True)
                            else: col_l.markdown(row_html, unsafe_allow_html=True)
                            idx_counter += 1
            else:
                st.warning("No valid team found.")

    render_top3_results(tab1, pool_easy, False)
    render_top3_results(tab2, pool_mid, False)
    render_top3_results(tab3, ALL_UNITS, True)

elif not run:
    st.info("👈 Select Level and click **FIND DIVERSE TEAMS**.")



