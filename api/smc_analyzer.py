from statistics import mean, stdev

def identify_imbalances(prices, volume, window=5):
    """Identify SMC imbalances in price action"""
    imbalances = []
    
    for i in range(window, len(prices)-1):
        # Check for price gaps
        gap_up = prices[i-1] < prices[i]
        gap_down = prices[i-1] > prices[i]
        
        # Volume analysis
        avg_volume = mean(volume[i-window:i])
        high_volume = volume[i] > avg_volume * 1.5
        
        # Price movement
        price_change = abs(prices[i] - prices[i-1])
        avg_change = mean([abs(prices[j] - prices[j-1]) for j in range(i-window+1, i+1)])
        significant_move = price_change > avg_change * 1.5
        
        if (gap_up or gap_down) and high_volume and significant_move:
            imbalances.append({
                'index': i,
                'price': prices[i],
                'type': 'bullish' if gap_up else 'bearish',
                'strength': round((price_change / avg_change) * (volume[i] / avg_volume), 2)
            })
    
    return imbalances

def find_fair_value_gaps(prices, window=3):
    """Identify Fair Value Gaps (FVG)"""
    fvgs = []
    
    for i in range(window, len(prices)-1):
        # Calculate local high and low
        local_high = max(prices[i-window:i])
        local_low = min(prices[i-window:i])
        current_price = prices[i]
        
        # Check for gaps above/below local range
        gap_up = current_price > local_high * 1.01  # 1% gap
        gap_down = current_price < local_low * 0.99  # 1% gap
        
        if gap_up or gap_down:
            fvgs.append({
                'index': i,
                'price': current_price,
                'type': 'bullish' if gap_up else 'bearish',
                'gap_size': round(abs(current_price - (local_high if gap_up else local_low)), 2)
            })
    
    return fvgs

def identify_liquidity_levels(prices, volume, window=10):
    """Identify liquidity levels based on price and volume"""
    levels = []
    
    for i in range(window, len(prices)-1):
        # Calculate local stats
        local_prices = prices[i-window:i+1]
        local_volumes = volume[i-window:i+1]
        avg_volume = mean(local_volumes)
        
        # Price swing points
        is_high = prices[i] == max(local_prices)
        is_low = prices[i] == min(local_prices)
        
        # Volume confirmation
        high_volume = volume[i] > avg_volume * 1.2
        
        if (is_high or is_low) and high_volume:
            levels.append({
                'index': i,
                'price': prices[i],
                'type': 'resistance' if is_high else 'support',
                'strength': round(volume[i] / avg_volume, 2)
            })
    
    return levels

def analyze_smc(prices, volume):
    """Perform complete SMC analysis"""
    analysis = {
        'imbalances': identify_imbalances(prices, volume),
        'fvgs': find_fair_value_gaps(prices),
        'liquidity_levels': identify_liquidity_levels(prices, volume)
    }
    
    # Add trend analysis
    if len(prices) >= 20:
        recent_trend = 'bullish' if mean(prices[-10:]) > mean(prices[-20:-10]) else 'bearish'
        analysis['trend'] = {
            'direction': recent_trend,
            'strength': round(abs(mean(prices[-10:]) - mean(prices[-20:-10])) / stdev(prices[-20:]), 2)
        }
    
    return analysis