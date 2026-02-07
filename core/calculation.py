import numpy as np

def calculate_match_win_rate(game_win_rate, format="BO1"):
    """
    Calculates the match win rate based on the game win rate.
    
    Args:
        game_win_rate (float): The probability of winning a single game (0.0 to 1.0).
        format (str): "BO1" or "BO3".
        
    Returns:
        float: The probability of winning the match.
    """
    p = game_win_rate
    if format == "BO1":
        return p
    elif format == "BO3":
        # Match win: 2-0 or 2-1
        # P(2-0) = p^2
        # P(2-1) = 2 * p * (1-p) * p = 2 * p^2 * (1-p)
        # Total = p^2 + 2p^2 - 2p^3 = 3p^2 - 2p^3
        return 3 * (p**2) - 2 * (p**3)
    else:
        raise ValueError(f"Unknown format: {format}")

def simulate_event(match_win_rate, max_wins, max_losses):
    """
    Calculates the probability distribution of event results.
    
    Args:
        match_win_rate (float): The probability of winning a match.
        max_wins (int): Maximum number of wins before event ends.
        max_losses (int): Maximum number of losses before event ends.
        
    Returns:
        dict: A dictionary mapping number of wins (int) to probability (float).
              e.g., {0: 0.1, 1: 0.2, ..., 7: 0.05}
    """
    # Dynamic programming table: dp[w][l] = probability of being at w wins and l losses
    dp = np.zeros((max_wins + 1, max_losses + 1))
    dp[0][0] = 1.0
    
    final_probs = {w: 0.0 for w in range(max_wins + 1)}
    
    for w in range(max_wins + 1):
        for l in range(max_losses + 1):
            if dp[w][l] == 0:
                continue
            
            # Check if event has already ended
            if w == max_wins or l == max_losses:
                final_probs[w] += dp[w][l] # Add to final results, handled by loop order?
                # Actually, if we reach this state, we don't transition out. 
                # This loop structure visits states. We need to handle transitions.
                continue

            current_prob = dp[w][l]
            
            # Transition: Win
            if w + 1 <= max_wins:
                dp[w + 1][l] += current_prob * match_win_rate
            
            # Transition: Loss
            if l + 1 <= max_losses:
                dp[w][l + 1] += current_prob * (1 - match_win_rate)
                
    # Correct generic extraction of final probabilities
    # The loop above pushes probabilities forward.
    # We need to collect probabilities where the event ENDS.
    results = {}
    
    # Event ends with max_wins
    results[max_wins] = sum(dp[max_wins][l] for l in range(max_losses))
    
    # Event ends with max_losses (but strictly less than max_wins)
    for w in range(max_wins):
        results[w] = dp[w][max_losses]
        
    return results

def calculate_ev(event_probs, payouts, costs, currency_settings, target_currency="Gems"):
    """
    Calculates the Expected Value (EV) of the event.
    
    Args:
        event_probs (dict): Probability of each win count.
        payouts (list): List of payout dictionaries (must match win counts).
        costs (dict): Entry fee (e.g., {"Gems": 1500}).
        currency_settings (dict): Conversion rates.
        target_currency (str): "Gems" or "Yen".
        
    Returns:
        float: Expected Value in target currency.
    """
    total_ev = 0.0
    
    # Convert costs to target currency
    entry_cost = 0.0
    for currency, amount in costs.items():
        entry_cost += convert_currency(amount, currency, target_currency, currency_settings)
        
    for wins, prob in event_probs.items():
        if wins < len(payouts):
            reward = payouts[wins]
            reward_value = 0.0
            for r_type, r_amount in reward.items(): # r_type: Gems, Packs, etc.
                reward_value += convert_currency(r_amount, r_type, target_currency, currency_settings)
            
            total_ev += prob * reward_value
            
    return total_ev - entry_cost

def convert_currency(amount, from_curr, to_curr, settings):
    """
    Helper to convert currency values.
    """
    # Base unit: Gems
    
    # 1. Convert to Gems
    value_in_gems = 0.0
    if from_curr == "Gems":
        value_in_gems = amount
    elif from_curr == "Gold":
        value_in_gems = amount * settings.get("gold_to_gems", 0.0)
    elif from_curr == "Packs":
        value_in_gems = amount * settings.get("pack_to_gems", 0.0)
    elif from_curr == "PIP":
        value_in_gems = amount * settings.get("pip_to_gems", 0.0)
    elif from_curr == "Box":
         # Play Booster Box
         yen_val = amount * settings.get("box_to_yen", 0.0)
         if settings.get("gems_to_yen", 0) > 0:
             value_in_gems = yen_val / settings.get("gems_to_yen")
         else:
             value_in_gems = 0
    elif from_curr == "Collector Box":
         yen_val = amount * settings.get("collector_box_to_yen", 0.0)
         if settings.get("gems_to_yen", 0) > 0:
             value_in_gems = yen_val / settings.get("gems_to_yen")
         else:
             value_in_gems = 0
    else:
        # Fallback for unknown types or direct gems
        value_in_gems = 0 

    # 2. Convert Gems to Target
    if to_curr == "Gems":
        return value_in_gems
    elif to_curr == "Yen":
        return value_in_gems * settings.get("gems_to_yen", 0.0)
    else:
        return 0.0
