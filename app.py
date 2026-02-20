import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from core import constants, calculation

# Page Config
st.set_page_config(
    page_title="MTGA イベント期待値計算機",
    page_icon="🃏",
    layout="wide",
)

# --- Sidebar: Global Settings (Economy) ---
st.sidebar.header("経済設定 💰")

# Currency Conversion Rates
with st.sidebar.expander("通貨価値設定", expanded=True):
    gems_to_yen = st.number_input(
        "1ジェムあたりの円 (例: 0.75)", 
        value=constants.DEFAULT_CURRENCY_SETTINGS["gems_to_yen"],
        step=0.01,
        format="%.4f"
    )
    
    pack_value_gems = st.number_input(
        "1パックのジェム価値",
        value=constants.DEFAULT_CURRENCY_SETTINGS["pack_to_gems"],
        step=10
    )
    
    gold_to_gems_rate = st.number_input(
        "1ゴールドあたりのジェム (例: 0.15)",
        value=constants.DEFAULT_CURRENCY_SETTINGS["gold_to_gems"],
        step=0.01,
        format="%.4f"
    )

    pip_value_gems = st.number_input(
        "1 PIPのジェム価値",
        value=constants.DEFAULT_CURRENCY_SETTINGS["pip_to_gems"],
        step=50
    )
    
    box_value_yen = st.number_input(
        "1ボックスの円価格",
        value=constants.DEFAULT_CURRENCY_SETTINGS["box_to_yen"],
        step=1000
    )

    collector_box_value_yen = st.number_input(
        "1コレクターボックスの円価格",
        value=constants.DEFAULT_CURRENCY_SETTINGS.get("collector_box_to_yen", 35000),
        step=1000
    )

    usd_to_yen = st.number_input(
        "1 USDあたりの円 (ドル円レート)",
        value=constants.DEFAULT_CURRENCY_SETTINGS.get("usd_to_yen", 150.0),
        step=1.0,
        format="%.1f"
    )

    rare_value_gems = st.number_input(
        "ドラフト/シールド等で取得するレアカードの価値 (ジェム)",
        value=0, # Default 0 as requested "fixed value might be ok" but user said 1.4 rares... let's default to 0 and let user set it. Or maybe 20? 
        # User said "Expectation 1.4 rares/pack".
        # Let's set default 20 (duplicate protection) * 1.4? No, just unit value.
        step=10,
        help="重複保護の場合は20ジェム、パック価値換算なら200ジェムなど"
    )

# Create settings dictionary
currency_settings = {
    "gems_to_yen": gems_to_yen,
    "pack_to_gems": pack_value_gems,
    "gold_to_gems": gold_to_gems_rate,
    "pip_to_gems": pip_value_gems,
    "box_to_yen": box_value_yen,
    "collector_box_to_yen": collector_box_value_yen,
    "usd_to_yen": usd_to_yen,
}

# --- Sidebar: Links ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 開発者・リンク 🔗")
st.sidebar.markdown("- [X (@goodbey2nd)](https://x.com/goodbey2nd)")
st.sidebar.markdown("- [YouTube (おだんごTV)](http://youtube.com/@odango_tv)")

# --- Main Area: Block 1 - Event Configuration ---
st.title("MTGA イベント期待値計算機 📊")

st.header("1. イベント設定 ⚙️")

# Event Configuration
with st.container():
    # Event Preset Selection
    preset_names = list(constants.EVENT_PRESETS.keys()) + ["カスタム設定"]
    selected_preset_name = st.selectbox("イベントの種類を選択", preset_names)

    if selected_preset_name != "カスタム設定":
        preset_data = constants.EVENT_PRESETS[selected_preset_name]
        
        # Get event format type from preset
        preset_event_format_type = preset_data.get("event_format_type", "normal")
        
        if preset_event_format_type == "fixed_rounds":
            # Fixed rounds format
            default_event_format_type = "fixed_rounds"
            default_num_rounds = preset_data.get("num_rounds", 3)
            default_max_wins = default_num_rounds  # For display purposes
            default_max_losses = 3  # Dummy value
        else:
            # Normal format
            default_event_format_type = "normal"
            default_max_wins = preset_data.get("max_wins", 7)
            default_max_losses = preset_data.get("max_losses", 3)
            default_num_rounds = 3  # Dummy value
        
        default_format = preset_data["format"]
        default_entry_gems = preset_data["entry_fee"].get("Gems", 0)
        default_entry_gold = preset_data["entry_fee"].get("Gold", 0)
        default_guaranteed_packs = preset_data.get("guaranteed_packs", 0)
        
    else:
        # Default defaults for Custom
        default_max_wins = 7
        default_max_losses = 3
        default_format = "BO1"
        default_entry_gems = 0
        default_entry_gold = 0
        default_guaranteed_packs = 0
        default_event_format_type = "normal"
        default_num_rounds = 3
        preset_data = {}

    # Event Format Type Selection
    # When preset changes, update the format type
    if 'last_preset' not in st.session_state:
        st.session_state.last_preset = selected_preset_name
        st.session_state.event_format_type = "通常形式（N勝/M敗抜け）" if default_event_format_type == "normal" else "固定ラウンド形式（スイスドロー風）"
    elif st.session_state.last_preset != selected_preset_name:
        # Preset changed, update to new preset's format
        st.session_state.last_preset = selected_preset_name
        st.session_state.event_format_type = "通常形式（N勝/M敗抜け）" if default_event_format_type == "normal" else "固定ラウンド形式（スイスドロー風）"
    
    # Initialize event_format_type in session state if not present
    if 'event_format_type' not in st.session_state:
        st.session_state.event_format_type = "通常形式（N勝/M敗抜け）" if default_event_format_type == "normal" else "固定ラウンド形式（スイスドロー風）"
    
    event_format_type = st.radio(
        "イベント形式",
        ["通常形式（N勝/M敗抜け）", "固定ラウンド形式（スイスドロー風）"],
        key="event_format_type",
        horizontal=True
    )
    
    # Event Parameters Inputs (conditional based on format type)
    if event_format_type == "通常形式（N勝/M敗抜け）":
        max_wins = st.number_input("最大勝利数", min_value=1, max_value=15, value=default_max_wins)
        max_losses = st.number_input("最大敗北数", min_value=1, max_value=5, value=default_max_losses)
        num_rounds = None
    else:
        # 固定ラウンド形式
        num_rounds = st.number_input("ラウンド数", min_value=1, max_value=10, value=default_num_rounds)
        max_wins = num_rounds  # For payout table display
        max_losses = None
    
    match_format = st.radio("マッチ形式", ["BO1", "BO3"], index=0 if default_format == "BO1" else 1)

    
    st.subheader("参加費")
    c1, c2 = st.columns(2)
    entry_gems = c1.number_input("参加費 (ジェム)", value=default_entry_gems, step=100)
    entry_gold = c2.number_input("参加費 (ゴールド)", value=default_entry_gold, step=500)
    
    # Payment Method Selection
    payment_method = st.radio("支払い方法", ["ジェム", "ゴールド"], horizontal=True)

    entry_cost_dict = {}
    if payment_method == "ジェム":
        if entry_gems > 0: entry_cost_dict["Gems"] = entry_gems
    else:
        if entry_gold > 0: entry_cost_dict["Gold"] = entry_gold

    st.subheader("参加賞 (カード取得)")
    cc1, cc2 = st.columns(2)
    guaranteed_packs = cc1.number_input("開封/ドラフトするパック数", value=default_guaranteed_packs, min_value=0, step=1)
    rares_per_pack = cc2.number_input("1パックあたりのレア期待値", value=1.4, step=0.1, format="%.1f")
    
    # Calculate Guaranteed Return
    guaranteed_gems = guaranteed_packs * rares_per_pack * rare_value_gems

    if guaranteed_gems > 0:
        st.info(f"カード取得による還元: {guaranteed_gems:,.0f} ジェム相当 (EVに加算されます)")

    # --- Payout Configuration ---
    st.subheader("報酬構造")
    
    if selected_preset_name != "カスタム設定":
        payout_list = preset_data.get("payouts", [])
    else:
        payout_list = []

    # Initialize generic payout structure for DataEditor
    data_rows = []
    keys = ["Gems", "Packs", "PIP", "Gold", "Box", "Collector Box", "USD"]
    
    current_payouts_dict = {item['wins']: item for item in payout_list}
    
    for w in range(max_wins + 1):
        row = {"Wins": w}
        if w in current_payouts_dict:
            for k in keys:
                row[k] = current_payouts_dict[w].get(k, 0)
        else:
            for k in keys:
                row[k] = 0
        data_rows.append(row)
        
    payout_df = pd.DataFrame(data_rows).set_index("Wins")
    
    edited_payout_df = st.data_editor(
        payout_df,
        column_config={
            "Gems": st.column_config.NumberColumn("ジェム", min_value=0, step=10),
            "Packs": st.column_config.NumberColumn("パック", min_value=0, step=1),
            "PIP": st.column_config.NumberColumn("PIP", min_value=0, step=1),
            "Gold": st.column_config.NumberColumn("ゴールド", min_value=0, step=100),
            "Box": st.column_config.NumberColumn("ボックス", min_value=0, step=1),
            "Collector Box": st.column_config.NumberColumn("コレクターボックス", min_value=0, step=1),
            "USD": st.column_config.NumberColumn("USD", min_value=0, step=100),
        },
        disabled=["Wins"],
        use_container_width=True
    )
    
    # Convert back
    payouts_config = []
    for w, row in edited_payout_df.iterrows():
        p_dict = {}
        for k in keys:
            if row[k] > 0:
                p_dict[k] = row[k]
        payouts_config.append(p_dict)


# --- Calculation & Analysis ---




# --- Core Logic Execution ---




# --- Main Area: Block 2 - Visualizations ---

st.header("2. 分析と可視化 📈")

st.subheader("分析パラメーター")
c_p1, c_p2 = st.columns(2)
target_currency = c_p1.radio("表示通貨", ["Gems", "Yen"], horizontal=True, format_func=lambda x: "ジェム" if x == "Gems" else "円")

# Win rate control with slider and input box
with c_p2:
    st.write("あなたのゲーム勝率 (%)")
    
    # Use a single key for session state
    if 'game_wr' not in st.session_state:
        st.session_state.game_wr = 50.0
    
    # Slider
    slider_wr = st.slider(
        "ゲーム勝率スライダー", 
        min_value=0.0, 
        max_value=100.0, 
        value=st.session_state.game_wr, 
        step=0.1,
        format="%.1f%%",
        label_visibility="collapsed"
    )
    
    # Number input
    input_wr = st.number_input(
        "勝率入力",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.game_wr,
        step=0.1,
        format="%.1f",
        label_visibility="collapsed"
    )
    
    # Determine which value changed and update session state
    # Priority: input box > slider (if both differ, use input)
    if input_wr != st.session_state.game_wr:
        st.session_state.game_wr = input_wr
        st.rerun()
    elif slider_wr != st.session_state.game_wr:
        st.session_state.game_wr = slider_wr
        st.rerun()

user_game_wr = st.session_state.game_wr / 100.0

# User Calculation
user_match_wr = calculation.calculate_match_win_rate(user_game_wr, match_format)

# Use appropriate simulation function based on event format type
if event_format_type == "固定ラウンド形式（スイスドロー風）":
    user_probs = calculation.simulate_fixed_rounds_event(user_match_wr, num_rounds)
else:
    user_probs = calculation.simulate_event(user_match_wr, max_wins, max_losses)
user_ev = calculation.calculate_ev(user_probs, payouts_config, entry_cost_dict, currency_settings, target_currency)

# Add guaranteed value
guaranteed_val_converted = calculation.convert_currency(guaranteed_gems, "Gems", target_currency, currency_settings)
user_ev += guaranteed_val_converted

# Global Calculation for Chart
win_rates_range = np.linspace(0, 1.0, 101)
ev_results = []

for wr in win_rates_range:
    match_wr = calculation.calculate_match_win_rate(wr, match_format)
    
    # Use appropriate simulation function based on event format type
    if event_format_type == "固定ラウンド形式（スイスドロー風）":
        final_probs = calculation.simulate_fixed_rounds_event(match_wr, num_rounds)
    else:
        final_probs = calculation.simulate_event(match_wr, max_wins, max_losses)
    ev = calculation.calculate_ev(final_probs, payouts_config, entry_cost_dict, currency_settings, target_currency)
    ev += guaranteed_val_converted # Add here too
    ev_results.append(ev)

be_wr = None
for i in range(len(ev_results) - 1):
    if (ev_results[i] < 0 and ev_results[i+1] >= 0) or (ev_results[i] >= 0 and ev_results[i+1] < 0):
        y1, y2 = ev_results[i], ev_results[i+1]
        x1, x2 = win_rates_range[i], win_rates_range[i+1]
        be_wr = x1 - y1 * (x2 - x1) / (y2 - y1)
        break

currency_label = "ジェム" if target_currency == "Gems" else "円"

m1, m2, m3 = st.columns(3)
m1.metric(f"期待値 ({currency_label})", f"{user_ev:,.0f}")
m2.metric("損益分岐点勝率", f"{be_wr*100:.2f}%" if be_wr else "---")
m3.metric("マッチ勝率 (BO3)" if match_format == "BO3" else "ゲーム勝率", f"{user_match_wr*100:.2f}%")

# Chart 1: EV Curve
fig_ev = go.Figure()

fig_ev.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="損益分岐点")

fig_ev.add_trace(go.Scatter(
    x=win_rates_range * 100, 
    y=ev_results,
    mode='lines',
    name='期待値',
    fill='tozeroy', 
    fillcolor='rgba(0,100,250,0.1)'
))

fig_ev.add_trace(go.Scatter(
    x=[user_game_wr * 100],
    y=[user_ev],
    mode='markers',
    marker=dict(size=12, color='red'),
    name='あなた'
))

fig_ev.update_layout(
    title=f"期待値 vs ゲーム勝率 ({currency_label})",
    xaxis_title="ゲーム勝率 (%)",
    yaxis_title=f"純損益 ({currency_label})",
    hovermode="x unified"
)

st.plotly_chart(fig_ev, use_container_width=True)


# --- Main Area: Block 3 - Outcome Distribution ---
st.header("3. 結果の確率分布 (現在の勝率にて)")

outcomes = sorted(user_probs.keys())
probs = [user_probs[k] * 100 for k in outcomes]
labels = [f"{k}勝" for k in outcomes]

# Calculate Net Profit per outcome for coloring
outcome_profits = []
outcome_colors = []

# Calculate Entry Cost once
current_entry_cost_val = 0
for curr, amt in entry_cost_dict.items():
    current_entry_cost_val += calculation.convert_currency(amt, curr, target_currency, currency_settings)

for k in outcomes:
    reward_val = 0
    if k < len(payouts_config):
        for r_type, r_amount in payouts_config[k].items():
            reward_val += calculation.convert_currency(r_amount, r_type, target_currency, currency_settings)
    
    net = reward_val - current_entry_cost_val
    outcome_profits.append(net)
    # Red if negative, Blue if positive/zero
    outcome_colors.append('crimson' if net < 0 else 'royalblue')

# Create DataFrame for Plotly
chart_df = pd.DataFrame({
    "Result": labels,
    "Probability": probs,
    "NetProfit": outcome_profits
})

fig_dist = px.bar(
    chart_df,
    x="Result",
    y="Probability",
    color="NetProfit", # Color based on profit
    title=f"結果の頻度分布 @ 勝率 {user_game_wr*100:.1f}%",
    custom_data=["NetProfit"],
    color_continuous_scale="RdBu", # Red to Blue
    color_continuous_midpoint=0    # Center at 0
)

# Customize layout
fig_dist.update_traces(
    texttemplate='%{y:.1f}%', 
    textposition='outside',
    hovertemplate="<br>".join([
        "結果: %{x}",
        "確率: %{y:.1f}%",
        f"収支: %{{customdata[0]:,.0f}} {currency_label}",
        "<extra></extra>"
    ])
)

fig_dist.update_layout(
    yaxis=dict(range=[0, max(probs)*1.2]),
    coloraxis_colorbar=dict(title=f"収支 ({currency_label})") # Legend title
)

st.plotly_chart(fig_dist, use_container_width=True)

# Footer
st.markdown("---")
st.caption("MTGA イベント期待値計算機")
