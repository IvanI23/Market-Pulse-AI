import pandas as pd
import sys
import os
from scipy.stats import pearsonr

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from config import CORRELATION_THRESHOLD, P_VALUE_THRESHOLD, MAX_LAG_DAYS, MIN_DATA_POINTS

def prepare_data(data):
    if not data:
        return None
    
    df = pd.DataFrame(data)
    df['price_change_pct'] = ((df['price_after'] - df['price_before']) / df['price_before']) * 100
    return df

def calculate_correlation(df):
    return pearsonr(df['score'], df['price_change_pct'])

def analyze_by_sentiment_label(df):
    return df.groupby('label')['price_change_pct'].agg(['mean', 'count', 'std']).round(4)

def analyze_distribution(df):
    results = {}
    for label in df['label'].unique():
        subset = df[df['label'] == label]['price_change_pct']
        results[label] = {
            'mean': subset.mean(),
            'median': subset.median(),
            'std': subset.std(),
            'min': subset.min(),
            'max': subset.max(),
            'count': len(subset)
        }
    return results

def time_lag_analysis(df, max_lag=MAX_LAG_DAYS):
    if len(df) <= max_lag:
        return "Insufficient data for lag analysis"
    
    df = df.copy()
    df['published_at'] = pd.to_datetime(df['published_at'])
    df_sorted = df.sort_values('published_at').reset_index(drop=True)
    
    lag_results = {}
    for lag in range(1, max_lag + 1):
        if len(df_sorted) > lag:
            df_sorted[f'price_lag_{lag}'] = df_sorted['price_change_pct'].shift(lag)
            valid_data = df_sorted.dropna(subset=['score', f'price_lag_{lag}'])
            
            if len(valid_data) > MIN_DATA_POINTS:
                lag_corr, lag_p = pearsonr(valid_data['score'], valid_data[f'price_lag_{lag}'])
                lag_results[lag] = {'correlation': lag_corr, 'p_value': lag_p}
            else:
                lag_results[lag] = {'correlation': None, 'p_value': None}
    
    return lag_results

def interpret_correlation(corr, p_value):
    if abs(corr) > 0.7:
        strength = "Strong"
    elif abs(corr) > 0.3:
        strength = "Moderate"
    else:
        strength = "Weak"
    
    direction = "positive" if corr > 0 else "negative"
    significant = p_value < P_VALUE_THRESHOLD
    
    recommendation = ('Use sentiment for alerts/trading' 
                     if abs(corr) > CORRELATION_THRESHOLD and significant 
                     else 'Sentiment may not be reliable for price prediction')
    
    return {
        'strength': strength,
        'direction': direction,
        'significant': significant,
        'recommendation': recommendation
    }

def print_analysis_summary(df):
    corr, p_value = calculate_correlation(df)
    interpretation = interpret_correlation(corr, p_value)
    
    print("\n=== ANALYSIS SUMMARY ===")
    print(f"📊 Dataset: {len(df)} news articles")
    print(f"📈 Overall correlation: {corr:.4f}")
    print(f"🎯 Statistical significance: {'✅ Significant' if interpretation['significant'] else '❌ Not significant'}")
    print(f"📈 Finding: {interpretation['strength']} {interpretation['direction']} correlation")
    print(f"💡 Recommendation: {interpretation['recommendation']}")
    
    return {
        'correlation': corr,
        'p_value': p_value,
        'significant': interpretation['significant'],
        'recommendation': interpretation['recommendation']
    }
