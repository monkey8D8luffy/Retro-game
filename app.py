import streamlit as st
import random
import time

# ==========================================
# 1. PAGE SETUP & RETRO CSS
# ==========================================
st.set_page_config(page_title="StreamKombat", layout="centered")

# Injecting retro arcade CSS (Pixel font, dark background, neon text)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"]  {
    font-family: 'Press Start 2P', monospace !important;
}
.stApp {
    background-color: #111111;
    color: #39ff14;
}
/* Health bar styling */
.stProgress > div > div > div > div {
    background-color: #ff0000;
}
/* Combat log styling */
.combat-log {
    background-color: #000000;
    border: 2px solid #39ff14;
    padding: 15px;
    height: 250px;
    overflow-y: auto;
    font-size: 10px;
    line-height: 1.8;
    color: #ffffff;
    margin-top: 20px;
}
h1, h2, h3 {
    text-align: center;
    color: #ffaa00;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GAME DATA (CHARACTERS & ABILITIES)
# ==========================================
CHARACTERS = {
    "Inferno": {
        "desc": "A fiery ninja. High damage, lower health.",
        "max_hp": 80,
        "attack_range": (8, 15),
        "special_name": "Hellfire",
        "special_desc": "Massive fire damage. Can miss.",
        "special_action": lambda: random.choice([0, 25, 30]) 
    },
    "Glacier": {
        "desc": "An ice warrior. Balanced stats, healing ability.",
        "max_hp": 100,
        "attack_range": (5, 12),
        "special_name": "Ice Shield",
        "special_desc": "Heals self and blocks some damage.",
        "special_action": lambda: -20 # Negative damage means heal
    },
    "Thunder": {
        "desc": "A lightning god. Wild, unpredictable damage.",
        "max_hp": 90,
        "attack_range": (2, 18),
        "special_name": "Lightning Strike",
        "special_desc": "Guaranteed critical hit.",
        "special_action": lambda: 22
    }
}

# ==========================================
# 3. SESSION STATE INITIALIZATION
# ==========================================
if 'stage' not in st.session_state:
    st.session_state.stage = 'select' # select, battle, game_over
if 'log' not in st.session_state:
    st.session_state.log = []

def log_msg(msg):
    st.session_state.log.insert(0, msg) # Insert at top

def reset_game():
    st.session_state.stage = 'select'
    st.session_state.log = []

# ==========================================
# 4. GAME LOGIC & SCREENS
# ==========================================
st.title("🥊 STREAM KOMBAT 🥊")

# --- SCREEN: CHARACTER SELECTION ---
if st.session_state.stage == 'select':
    st.markdown("### CHOOSE YOUR FIGHTER")
    
    cols = st.columns(3)
    for idx, (name, stats) in enumerate(CHARACTERS.items()):
        with cols[idx]:
            st.subheader(name)
            st.write(f"**HP:** {stats['max_hp']}")
            st.write(f"**Special:** {stats['special_name']}")
            st.caption(stats['desc'])
            
            if st.button(f"Select {name}", use_container_width=True):
                st.session_state.player_name = name
                st.session_state.player_hp = stats['max_hp']
                
                # Random AI Opponent
                ai_name = random.choice(list(CHARACTERS.keys()))
                st.session_state.ai_name = ai_name
                st.session_state.ai_hp = CHARACTERS[ai_name]['max_hp']
                
                st.session_state.stage = 'battle'
                log_msg(f"FIGHT! {name} vs {ai_name}")
                st.rerun()

# --- SCREEN: BATTLE STAGE ---
elif st.session_state.stage == 'battle':
    p_name = st.session_state.player_name
    a_name = st.session_state.ai_name
    p_max_hp = CHARACTERS[p_name]['max_hp']
    a_max_hp = CHARACTERS[a_name]['max_hp']

    # Display Health Bars
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"### {p_name} (You)")
        # Calculate percentage, ensuring it stays between 0.0 and 1.0
        p_pct = max(0.0, min(1.0, st.session_state.player_hp / p_max_hp))
        st.progress(p_pct)
        st.write(f"HP: {st.session_state.player_hp}/{p_max_hp}")

    with col2:
        st.markdown(f"### {a_name} (CPU)")
        a_pct = max(0.0, min(1.0, st.session_state.ai_hp / a_max_hp))
        st.progress(a_pct)
        st.write(f"HP: {st.session_state.ai_hp}/{a_max_hp}")

    st.markdown("---")
    
    # --- COMBAT MECHANICS ---
    def execute_turn(action_type):
        # 1. Player Turn
        if action_type == 'attack':
            dmg = random.randint(*CHARACTERS[p_name]['attack_range'])
            st.session_state.ai_hp -= dmg
            log_msg(f"▶ You hit {a_name} for {dmg} damage!")
        elif action_type == 'special':
            val = CHARACTERS[p_name]['special_action']()
            if val < 0: # Healing
                st.session_state.player_hp = min(p_max_hp, st.session_state.player_hp - val)
                log_msg(f"▶ You used {CHARACTERS[p_name]['special_name']} and healed {-val} HP!")
            elif val == 0:
                log_msg(f"▶ Your {CHARACTERS[p_name]['special_name']} MISSED!")
            else:
                st.session_state.ai_hp -= val
                log_msg(f"▶ You used {CHARACTERS[p_name]['special_name']} for {val} damage!")

        # Check Win Condition
        if st.session_state.ai_hp <= 0:
            st.session_state.ai_hp = 0
            st.session_state.stage = 'game_over'
            st.session_state.winner = 'Player'
            return

        # 2. AI Turn (CPU logic)
        ai_choice = random.choices(['attack', 'special'], weights=[70, 30])[0]
        if ai_choice == 'attack':
            dmg = random.randint(*CHARACTERS[a_name]['attack_range'])
            st.session_state.player_hp -= dmg
            log_msg(f"💀 {a_name} attacks you for {dmg} damage!")
        else:
            val = CHARACTERS[a_name]['special_action']()
            if val < 0:
                st.session_state.ai_hp = min(a_max_hp, st.session_state.ai_hp - val)
                log_msg(f"💀 {a_name} uses {CHARACTERS[a_name]['special_name']} and heals {-val} HP!")
            elif val == 0:
                log_msg(f"💀 {a_name} tried a special move but missed!")
            else:
                st.session_state.player_hp -= val
                log_msg(f"💀 {a_name} uses {CHARACTERS[a_name]['special_name']} for {val} damage!")

        # Check Lose Condition
        if st.session_state.player_hp <= 0:
            st.session_state.player_hp = 0
            st.session_state.stage = 'game_over'
            st.session_state.winner = 'CPU'

    # --- ACTION BUTTONS ---
    st.markdown("### COMMANDS")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🗡️ Basic Attack", use_container_width=True):
            execute_turn('attack')
            st.rerun()
    with b2:
        if st.button(f"🔥 Special: {CHARACTERS[p_name]['special_name']}", use_container_width=True):
            execute_turn('special')
            st.rerun()

    # --- COMBAT LOG ---
    st.markdown("<div class='combat-log'>", unsafe_allow_html=True)
    for msg in st.session_state.log:
        st.markdown(f"{msg}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- SCREEN: GAME OVER ---
elif st.session_state.stage == 'game_over':
    if st.session_state.winner == 'Player':
        st.success(f"FATALITY! You defeated {st.session_state.ai_name}!")
        st.balloons()
    else:
        st.error(f"GAME OVER. {st.session_state.ai_name} defeated you.")
    
    st.markdown("<div class='combat-log'>", unsafe_allow_html=True)
    for msg in st.session_state.log:
        st.markdown(f"{msg}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("INSERT COIN TO PLAY AGAIN", use_container_width=True):
        reset_game()
        st.rerun()
