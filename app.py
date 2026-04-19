import streamlit as st
import random

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="⚔️ RETRO KOMBAT",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
#  CHARACTER DATA
# ══════════════════════════════════════════════════════════════
CHARACTERS = {
    "SCORPIO": {
        "title": "THE FIRE DEMON",
        "emoji": "🔥",
        "color": "#FF4444",
        "glow": "#FF2200",
        "bg": "rgba(80,0,0,0.9)",
        "border": "#FF4444",
        "hp": 200, "max_energy": 100,
        "description": "A demonic warrior who harnesses the raw power of hellfire. Brutal combos and devastating fire magic.",
        "stats": {"STR": 8, "SPD": 7, "DEF": 5, "MAG": 9},
        "moves": {
            "Flaming Punch": {
                "damage": (15, 25), "energy_cost": 5, "type": "physical",
                "desc": "A swift punch wreathed in flame", "emoji": "👊",
                "effect": None
            },
            "Spear Throw": {
                "damage": (28, 42), "energy_cost": 22, "type": "physical",
                "desc": "GET OVER HERE! 45% stun chance", "emoji": "🗡️",
                "effect": "stun", "effect_chance": 0.45, "effect_duration": 1
            },
            "Inferno Blast": {
                "damage": (35, 50), "energy_cost": 35, "type": "fire",
                "desc": "Unleashes hellfire — burns 3 turns (8/turn)", "emoji": "🔥",
                "effect": "burn", "effect_chance": 1.0, "effect_duration": 3, "effect_damage": 8
            },
            "☠ HELLFIRE": {
                "damage": (72, 98), "energy_cost": 60, "type": "ultimate",
                "desc": "SCORPIO'S FINISHING BLOW!", "emoji": "💀",
                "effect": "burn", "effect_chance": 1.0, "effect_duration": 2, "effect_damage": 12
            },
        }
    },
    "FROST": {
        "title": "THE ICE QUEEN",
        "emoji": "❄️",
        "color": "#44CCFF",
        "glow": "#00AAFF",
        "bg": "rgba(0,15,55,0.9)",
        "border": "#44CCFF",
        "hp": 175, "max_energy": 130,
        "description": "An ice sorceress who freezes enemies solid. Control specialist — slows, locks, and shatters.",
        "stats": {"STR": 5, "SPD": 8, "DEF": 7, "MAG": 10},
        "moves": {
            "Ice Punch": {
                "damage": (12, 22), "energy_cost": 5, "type": "physical",
                "desc": "A freezing crystalline jab", "emoji": "🥊",
                "effect": None
            },
            "Ice Shards": {
                "damage": (25, 40), "energy_cost": 20, "type": "ice",
                "desc": "Launches razor-sharp ice projectiles", "emoji": "❄️",
                "effect": None
            },
            "Deep Freeze": {
                "damage": (18, 28), "energy_cost": 35, "type": "ice",
                "desc": "Encases the enemy in solid ice for 2 turns!", "emoji": "🧊",
                "effect": "freeze", "effect_chance": 1.0, "effect_duration": 2
            },
            "❄ BLIZZARD": {
                "damage": (60, 88), "energy_cost": 58, "type": "ultimate",
                "desc": "FROST'S ULTIMATE — ARCTIC DEVASTATION!", "emoji": "🌨️",
                "effect": "freeze", "effect_chance": 1.0, "effect_duration": 1
            },
        }
    },
    "SHADOW": {
        "title": "THE PHANTOM NINJA",
        "emoji": "🥷",
        "color": "#BB44FF",
        "glow": "#9900CC",
        "bg": "rgba(18,0,45,0.9)",
        "border": "#BB44FF",
        "hp": 155, "max_energy": 145,
        "description": "A phantom ninja who strikes from pure darkness. Highest burst damage — glass cannon fighter.",
        "stats": {"STR": 10, "SPD": 10, "DEF": 3, "MAG": 7},
        "moves": {
            "Shuriken": {
                "damage": (12, 22), "energy_cost": 5, "type": "physical",
                "desc": "Flings deadly ninja stars", "emoji": "⭐",
                "effect": None
            },
            "Shadow Strike": {
                "damage": (30, 50), "energy_cost": 22, "type": "physical",
                "desc": "Teleports behind and strikes critical zones", "emoji": "⚡",
                "effect": None
            },
            "Vanish": {
                "damage": (0, 0), "energy_cost": 28, "type": "defend",
                "desc": "Disappears — counters next attack with 20-35 dmg!", "emoji": "🌀",
                "effect": "vanish"
            },
            "☠ DEATH SHADOW": {
                "damage": (82, 118), "energy_cost": 68, "type": "ultimate",
                "desc": "SHADOW'S ULTIMATE — FROM THE ABYSS!", "emoji": "👤",
                "effect": None
            },
        }
    },
    "TITAN": {
        "title": "THE EARTH COLOSSUS",
        "emoji": "🗿",
        "color": "#44FF88",
        "glow": "#00CC44",
        "bg": "rgba(0,28,12,0.9)",
        "border": "#44FF88",
        "hp": 265, "max_energy": 80,
        "description": "A massive colossus of earth and stone. Lowest speed, highest health — an unstoppable mountain.",
        "stats": {"STR": 10, "SPD": 3, "DEF": 10, "MAG": 2},
        "moves": {
            "Rock Smash": {
                "damage": (18, 32), "energy_cost": 5, "type": "physical",
                "desc": "Crushes with immense stone fists", "emoji": "🪨",
                "effect": None
            },
            "Ground Slam": {
                "damage": (35, 54), "energy_cost": 22, "type": "physical",
                "desc": "Shockwave tremor — 50% stun chance", "emoji": "💥",
                "effect": "stun", "effect_chance": 0.5, "effect_duration": 1
            },
            "Stone Armor": {
                "damage": (0, 0), "energy_cost": 28, "type": "defend",
                "desc": "Hardens body — next hit reduced 75%!", "emoji": "🛡️",
                "effect": "armor"
            },
            "🌋 EARTHQUAKE": {
                "damage": (65, 94), "energy_cost": 55, "type": "ultimate",
                "desc": "TITAN'S ULTIMATE — TECTONIC ANNIHILATION!", "emoji": "🌋",
                "effect": "stun", "effect_chance": 0.65, "effect_duration": 1
            },
        }
    },
    "STORM": {
        "title": "THE LIGHTNING LORD",
        "emoji": "⚡",
        "color": "#FFEE44",
        "glow": "#FFCC00",
        "bg": "rgba(38,32,0,0.9)",
        "border": "#FFEE44",
        "hp": 185, "max_energy": 115,
        "description": "Master of electricity and thunder. Unpredictable and electrifyingly fast — reflects attacks back!",
        "stats": {"STR": 7, "SPD": 9, "DEF": 6, "MAG": 8},
        "moves": {
            "Zap": {
                "damage": (14, 26), "energy_cost": 5, "type": "electric",
                "desc": "Quick electric discharge", "emoji": "⚡",
                "effect": None
            },
            "Lightning Bolt": {
                "damage": (30, 48), "energy_cost": 22, "type": "electric",
                "desc": "Calls down a lightning strike", "emoji": "🌩️",
                "effect": None
            },
            "Static Field": {
                "damage": (0, 0), "energy_cost": 28, "type": "defend",
                "desc": "Generates field — reflects next attack!", "emoji": "🔄",
                "effect": "reflect"
            },
            "🌪 THUNDERCLAP": {
                "damage": (70, 98), "energy_cost": 60, "type": "ultimate",
                "desc": "STORM'S ULTIMATE — DIVINE THUNDER!", "emoji": "🌪️",
                "effect": "stun", "effect_chance": 0.4, "effect_duration": 1
            },
        }
    },
}

ENERGY_REGEN = 12  # Energy restored each round

# ══════════════════════════════════════════════════════════════
#  CSS INJECTION
# ══════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&display=swap');

    /* ── Global Reset ── */
    html, body, .stApp {
        background: #000 !important;
        color: #fff !important;
    }
    .block-container {
        padding: 1rem 1.5rem !important;
        max-width: 100% !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }

    /* ── CRT Scanline Overlay ── */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: repeating-linear-gradient(
            0deg,
            rgba(0,0,0,0.06) 0px,
            rgba(0,0,0,0.06) 1px,
            transparent 1px,
            transparent 3px
        );
        pointer-events: none;
        z-index: 99999;
    }

    /* ── Background ── */
    .stApp {
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(80,0,0,0.15) 0%, transparent 60%),
            radial-gradient(ellipse at 80% 50%, rgba(0,0,80,0.15) 0%, transparent 60%) !important;
        background-color: #000 !important;
    }

    /* ══ TITLE SCREEN ══ */
    .game-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(1.8rem, 5vw, 3.8rem);
        text-align: center;
        background: linear-gradient(180deg, #FF6600 0%, #FF0000 40%, #FFAA00 70%, #FF4400 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 0 20px #FF4400) drop-shadow(0 0 50px #FF2200);
        animation: titlePulse 2.5s ease-in-out infinite;
        letter-spacing: 4px;
        line-height: 1.3;
        padding: 10px 0;
    }
    @keyframes titlePulse {
        0%,100% { filter: drop-shadow(0 0 15px #FF4400) drop-shadow(0 0 35px #FF2200); }
        50%      { filter: drop-shadow(0 0 35px #FF6600) drop-shadow(0 0 70px #FF4400); }
    }

    .insert-coin {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.75rem;
        color: #FFCC00;
        text-align: center;
        letter-spacing: 5px;
        animation: blink 1.2s step-end infinite;
        margin: 12px 0 30px;
    }
    @keyframes blink {
        0%,100% { opacity: 1; }
        50%      { opacity: 0; }
    }

    /* ══ BUTTONS ══ */
    .stButton button {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.52rem !important;
        background: linear-gradient(180deg, #1a1a3a 0%, #0a0a1a 100%) !important;
        color: #EEF !important;
        border: 2px solid #3333AA !important;
        border-radius: 2px !important;
        width: 100% !important;
        padding: 10px 8px !important;
        white-space: pre-line !important;
        height: auto !important;
        min-height: 58px !important;
        box-shadow: 0 0 10px rgba(60,60,180,0.35) !important;
        transition: all 0.12s ease !important;
        cursor: pointer !important;
        letter-spacing: 1px !important;
    }
    .stButton button:hover {
        background: linear-gradient(180deg, #252555 0%, #111133 100%) !important;
        border-color: #6666CC !important;
        box-shadow: 0 0 18px rgba(100,100,220,0.6), inset 0 1px 0 rgba(255,255,255,0.1) !important;
        transform: translateY(-2px) !important;
        color: #FFFFFF !important;
    }
    .stButton button:active {
        transform: translateY(1px) !important;
        box-shadow: 0 0 5px rgba(60,60,180,0.3) !important;
    }
    .stButton button:disabled {
        opacity: 0.3 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* ══ CHARACTER SELECT ══ */
    .select-header {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(1rem, 3vw, 1.6rem);
        color: #FFFF00;
        text-align: center;
        text-shadow: 0 0 20px #FFFF00, 0 0 40px #FFAA00;
        letter-spacing: 3px;
        margin-bottom: 6px;
    }
    .select-sub {
        font-family: 'Orbitron', monospace;
        font-size: 0.6rem;
        color: #666;
        text-align: center;
        letter-spacing: 6px;
        margin-bottom: 24px;
    }

    /* ══ CHAR CARD ══ */
    .char-portrait {
        border-radius: 3px;
        padding: 14px 10px;
        text-align: center;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
    }
    .char-portrait::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--char-color), transparent);
        animation: scanDown 3s linear infinite;
    }
    @keyframes scanDown {
        0%   { top: 0; opacity: 1; }
        90%  { top: 100%; opacity: 0.5; }
        100% { top: 0; opacity: 0; }
    }

    /* ══ BATTLE ARENA ══ */
    .arena-bar {
        border-radius: 3px;
        padding: 8px 16px;
        text-align: center;
        margin-bottom: 14px;
        position: relative;
    }

    .vs-text {
        font-family: 'Press Start 2P', monospace;
        font-size: 1.4rem;
        color: #FFFF00;
        text-shadow: 0 0 12px #FFFF00, 0 0 25px #FFAA00;
        animation: vsPulse 1.8s ease-in-out infinite;
    }
    @keyframes vsPulse {
        0%,100% { text-shadow: 0 0 12px #FFFF00, 0 0 25px #FFAA00; }
        50%      { text-shadow: 0 0 22px #FFFF00, 0 0 50px #FFCC00; }
    }

    .fighter-panel {
        border-radius: 3px;
        padding: 14px;
        min-height: 200px;
    }

    .fighter-sprite {
        font-size: 4.8rem;
        text-align: center;
        display: block;
        animation: float 3s ease-in-out infinite;
        margin: 6px 0;
    }
    @keyframes float {
        0%,100% { transform: translateY(0px); }
        50%      { transform: translateY(-10px); }
    }

    .fighter-name-text {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.75rem;
        text-align: center;
        letter-spacing: 2px;
    }
    .fighter-title-text {
        font-family: 'Orbitron', monospace;
        font-size: 0.42rem;
        text-align: center;
        opacity: 0.6;
        letter-spacing: 3px;
        margin-bottom: 10px;
    }

    /* ══ HP / ENERGY BARS ══ */
    .bar-label {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.42rem;
        color: #888;
        margin-bottom: 2px;
    }
    .bar-wrap {
        background: #111;
        border: 1px solid #333;
        border-radius: 1px;
        overflow: hidden;
        margin-bottom: 6px;
    }
    .bar-fill {
        height: 100%;
        position: relative;
        transition: width 0.4s ease;
    }
    .bar-fill::after {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 45%;
        background: rgba(255,255,255,0.18);
    }

    /* ══ STATUS BADGES ══ */
    .badge {
        display: inline-block;
        font-family: 'Orbitron', monospace;
        font-size: 0.42rem;
        padding: 2px 7px;
        border-radius: 2px;
        margin: 1px 2px;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* ══ COMBAT LOG ══ */
    .combat-log-wrap {
        background: #000;
        border: 2px solid #1a1a1a;
        border-radius: 3px;
        padding: 10px 12px;
        height: 270px;
        overflow-y: auto;
    }
    .log-entry {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        line-height: 1.7;
        padding: 1px 0;
    }

    /* ══ MOVE SELECTOR ══ */
    .move-section-label {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.55rem;
        color: #666;
        text-align: center;
        margin: 14px 0 8px;
        letter-spacing: 3px;
    }

    /* ══ FROZEN/STUNNED NOTICE ══ */
    .status-notice {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.65rem;
        text-align: center;
        padding: 10px;
        border-radius: 3px;
        margin: 8px 0;
        animation: blink 0.8s step-end infinite;
    }

    /* ══ GAME OVER ══ */
    .go-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(1.5rem, 4vw, 3rem);
        text-align: center;
        animation: victoryPulse 0.9s ease-in-out infinite;
        padding: 20px 0 10px;
    }
    @keyframes victoryPulse {
        0%,100% { transform: scale(1); }
        50%      { transform: scale(1.04); }
    }
    .go-sub {
        font-family: 'Press Start 2P', monospace;
        font-size: 0.85rem;
        text-align: center;
        letter-spacing: 6px;
        opacity: 0.75;
        animation: blink 1.5s step-end infinite;
    }
    .go-sprite {
        font-size: 6rem;
        text-align: center;
        display: block;
        animation: float 2s ease-in-out infinite;
    }
    .go-winner {
        font-family: 'Press Start 2P', monospace;
        font-size: 1.3rem;
        text-align: center;
        letter-spacing: 4px;
        margin: 14px 0;
    }
    .stats-box {
        border: 2px solid;
        border-radius: 4px;
        padding: 16px;
        text-align: center;
        margin: 12px auto;
    }
    .stats-row {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        color: #AAA;
        line-height: 2.4;
    }

    /* ══ SCROLLBAR ══ */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 2px; }

    /* ══ EXPANDER ══ */
    .streamlit-expanderHeader {
        font-family: 'Orbitron', monospace !important;
        font-size: 0.5rem !important;
        color: #888 !important;
        background: transparent !important;
        border: 1px solid #222 !important;
    }
    .streamlit-expanderContent {
        background: #050510 !important;
        border: 1px solid #1a1a2a !important;
    }

    /* ══ DIVIDER ══ */
    hr { border-color: #1a1a1a !important; margin: 8px 0 !important; }
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "game_state":       "title",
        "player_char":      None,
        "enemy_char":       None,
        "player_hp":        0,
        "player_max_hp":    0,
        "enemy_hp":         0,
        "enemy_max_hp":     0,
        "player_energy":    0,
        "player_max_energy":0,
        "enemy_energy":     0,
        "enemy_max_energy": 0,
        "player_status":    [],
        "enemy_status":     [],
        "combat_log":       [],
        "round_num":        1,
        "winner":           None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ══════════════════════════════════════════════════════════════
#  GAME LOGIC
# ══════════════════════════════════════════════════════════════
def start_battle(player_char: str, enemy_char: str):
    pc = CHARACTERS[player_char]
    ec = CHARACTERS[enemy_char]
    s = st.session_state
    s.player_char       = player_char
    s.enemy_char        = enemy_char
    s.player_hp         = pc["hp"]
    s.player_max_hp     = pc["hp"]
    s.enemy_hp          = ec["hp"]
    s.enemy_max_hp      = ec["hp"]
    s.player_energy     = pc["max_energy"]
    s.player_max_energy = pc["max_energy"]
    s.enemy_energy      = ec["max_energy"]
    s.enemy_max_energy  = ec["max_energy"]
    s.player_status     = []
    s.enemy_status      = []
    s.round_num         = 1
    s.winner            = None
    s.combat_log        = [
        f"⚔️  FIGHT! {player_char} vs {enemy_char}",
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
    ]
    s.game_state = "battle"


def has_status(lst, t):
    return any(x["type"] == t for x in lst)

