# Default Currency Conversion Rates
DEFAULT_CURRENCY_SETTINGS = {
    "gems_to_yen": 0.75,  # Example: 20000 gems = 15000 yen approx
    "gold_to_gems": 0.15, # Standard draft buying rate (10000 gold = 1500 gems)
    "pack_to_gems": 30,   # Conservative value (duplicate protection for rare)
    "pip_to_gems": 200,   # Rough estimate, needs user adjustment
    "box_to_yen": 15000,  # Example play booster box price
    "collector_box_to_yen": 35000, # Example collector booster box price
}

# Event Presets
EVENT_PRESETS = {
    "プレミア・ドラフト": {
        "max_wins": 7,
        "max_losses": 3,
        "format": "BO1",
        "guaranteed_packs": 3,
        "entry_fee": {"Gems": 1500, "Gold": 10000},
        "payouts": [
            {"wins": 0, "Gems": 50, "Packs": 1},
            {"wins": 1, "Gems": 100, "Packs": 1},
            {"wins": 2, "Gems": 250, "Packs": 2},
            {"wins": 3, "Gems": 1000, "Packs": 2},
            {"wins": 4, "Gems": 1400, "Packs": 3},
            {"wins": 5, "Gems": 1600, "Packs": 4},
            {"wins": 6, "Gems": 1800, "Packs": 5},
            {"wins": 7, "Gems": 2200, "Packs": 6},
        ]
    },
    "マッチ・ドラフト": {
        "max_wins": 3,
        "max_losses": 3, # Actually matches are fixed to 3 usually, but let's treat as max wins 3
        "format": "BO3", 
        "guaranteed_packs": 3,
        "entry_fee": {"Gems": 1500, "Gold": 10000},
        "payouts": [
            {"wins": 0, "Gems": 0, "Packs": 1},
            {"wins": 1, "Gems": 0, "Packs": 1},
            {"wins": 2, "Gems": 1000, "Packs": 3},
            {"wins": 3, "Gems": 2500, "Packs": 6, "PIP": 2},
        ]
    },
    "クイック・ドラフト": {
        "max_wins": 7,
        "max_losses": 3,
        "format": "BO1",
        "guaranteed_packs": 3,
        "entry_fee": {"Gems": 750, "Gold": 5000},
        "payouts": [
            {"wins": 0, "Gems": 50, "Packs": 1.20}, # Probability based packs handled as float? Or usually 1 pack + 20% chance
            {"wins": 1, "Gems": 100, "Packs": 1.22},
            {"wins": 2, "Gems": 200, "Packs": 1.24},
            {"wins": 3, "Gems": 300, "Packs": 1.26},
            {"wins": 4, "Gems": 450, "Packs": 1.30},
            {"wins": 5, "Gems": 650, "Packs": 1.35},
            {"wins": 6, "Gems": 850, "Packs": 1.40},
            {"wins": 7, "Gems": 950, "Packs": 2.00},
        ]
    },
    "構築イベント (BO1)": {
        "max_wins": 7,
        "max_losses": 3,
        "format": "BO1",
        "guaranteed_packs": 0,
        "entry_fee": {"Gems": 375, "Gold": 2500},
        "payouts": [
            {"wins": 0, "Gems": 25, "Packs": 0},
            {"wins": 1, "Gems": 50, "Packs": 0},
            {"wins": 2, "Gems": 75, "Packs": 0},
            {"wins": 3, "Gems": 200, "Packs": 0},
            {"wins": 4, "Gems": 300, "Packs": 0},
            {"wins": 5, "Gems": 400, "Packs": 0}, # + rare cards mechanism ignored for now or treated as packs?
            {"wins": 6, "Gems": 450, "Packs": 0},
            {"wins": 7, "Gems": 500, "Packs": 0, "PIP": 1}, 
        ]
    },
    "アリーナ・ダイレクト (プレイブースター)": {
        "max_wins": 7,
        "max_losses": 2,
        "format": "BO1",
        "guaranteed_packs": 6,
        "entry_fee": {"Gems": 6000},
        "payouts": [
            {"wins": 0, "Gems": 0, "Packs": 0},
            {"wins": 1, "Gems": 0, "Packs": 0},
            {"wins": 2, "Gems": 0, "Packs": 0},
            {"wins": 3, "Gems": 2700, "Packs": 8},
            {"wins": 4, "Gems": 5400, "Packs": 16},
            {"wins": 5, "Gems": 8100, "Packs": 24},
            {"wins": 6, "Gems": 0, "Box": 1},
            {"wins": 7, "Gems": 0, "Box": 2},
        ]
    },
    "アリーナ・ダイレクト (コレクターブースター)": {
        "max_wins": 7,
        "max_losses": 2,
        "format": "BO1",
        "guaranteed_packs": 6,
        "entry_fee": {"Gems": 8000},
        "payouts": [
            {"wins": 0, "Gems": 0, "Packs": 0},
            {"wins": 1, "Gems": 0, "Packs": 0},
            {"wins": 2, "Gems": 0, "Packs": 0},
            {"wins": 3, "Gems": 3600, "Packs": 8},
            {"wins": 4, "Gems": 7200, "Packs": 16},
            {"wins": 5, "Gems": 10800, "Packs": 24},
            {"wins": 6, "Gems": 14400, "Packs": 32},
            {"wins": 7, "Gems": 0, "Collector Box": 1},
        ]
    },
}
