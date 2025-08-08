import pandas as pd
import os
import sys
from datetime import date

from app.db import get_sentiment_data, store_sentiment_price_effects
from app.analysis_utils import (
    prepare_data, calculate_correlation, analyze_by_sentiment_label,
    analyze_distribution, time_lag_analysis,
    print_analysis_summary
)
import app.config as config
from app.config import (
    ensure_directories, DASHBOARD_DATA_DIR, SENTIMENT_ANALYSIS_FILE,
    CORRELATION_SUMMARY_FILE, LABEL_ANALYSIS_FILE,
    CORRELATION_THRESHOLD, P_VALUE_THRESHOLD
)

def get_data():
    print("📊 Getting sentiment data from database...")
    
    data = get_sentiment_data()
    if not data:
        print("❌ No sentiment data found. Run nlp_engine.py first!")
        return None
    
    df = prepare_data(data)
    print(f"✅ Prepared {len(df)} records for analysis")
    print(f"Date range: {df['published_at'].min()} to {df['published_at'].max()}")
    
    return df

def correlation_analysis(df):
    print("\n🔹 CORRELATION ANALYSIS")
    print("=" * 50)
    
    corr, p_value = calculate_correlation(df)
    significant = p_value < P_VALUE_THRESHOLD
    
    print(f"Correlation: {corr:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Dataset size: {len(df)}")
    print(f"Statistically {'significant' if significant else 'not significant'}")
    
    return {
        'overall_correlation': corr,
        'p_value': p_value,
        'dataset_size': len(df),
        'date_range_start': df['published_at'].min(),
        'date_range_end': df['published_at'].max()
    }

def group_analysis(df):
    print("\n🔹 GROUP ANALYSIS")
    print("=" * 50)
    
    grouped = analyze_by_sentiment_label(df)
    print("Average price change by sentiment:")
    print(grouped)
    
    return [
        {
            'label': label,
            'avg_price_change_pct': row['mean'],
            'count': row['count'],
            'std_dev': row['std']
        }
        for label, row in grouped.iterrows()
    ]

def distribution_analysis(df):
    print("\n🔹 DISTRIBUTION ANALYSIS")
    print("=" * 50)
    
    results = analyze_distribution(df)
    
    for label, stats in results.items():
        print(f"\n{label.upper()} Headlines:")
        print(f"   • Count: {stats['count']}")
        print(f"   • Mean: {stats['mean']:+.2f}%")
        print(f"   • Median: {stats['median']:+.2f}%")
        print(f"   • Min/Max: {stats['min']:+.2f}% / {stats['max']:+.2f}%")
        print(f"   • Std Dev: {stats['std']:.2f}%")

def lag_analysis(df):
    print("\n🔹 TIME-LAG ANALYSIS")
    print("=" * 50)
    
    lag_results = time_lag_analysis(df)
    
    if isinstance(lag_results, str):
        print(lag_results)
    else:
        print("Lag correlation analysis:")
        for lag, result in lag_results.items():
            if result['correlation'] is not None:
                print(f"   • {lag} day lag: {result['correlation']:+.3f} (p={result['p_value']:.4f})")
            else:
                print(f"   • {lag} day lag: Insufficient data")

def save_results(correlation_stats, group_stats, df):
    print("\n💾 SAVING RESULTS")
    print("=" * 50)
    
    ensure_directories()
    
    detailed_path = os.path.join(DASHBOARD_DATA_DIR, SENTIMENT_ANALYSIS_FILE)
    df.to_csv(detailed_path, index=False)
    print(f"✅ Detailed data: {detailed_path}")
    
    correlation_df = pd.DataFrame([correlation_stats])
    correlation_path = os.path.join(DASHBOARD_DATA_DIR, CORRELATION_SUMMARY_FILE)
    correlation_df.to_csv(correlation_path, index=False)
    print(f"✅ Correlation summary: {correlation_path}")
    
    group_df = pd.DataFrame(group_stats)
    group_path = os.path.join(DASHBOARD_DATA_DIR, LABEL_ANALYSIS_FILE)
    group_df.to_csv(group_path, index=False)
    print(f"✅ Group analysis: {group_path}")
    
    return detailed_path, correlation_path, group_path

def print_conclusion(correlation_stats):
    print("\n🚦 CONCLUSION")
    print("=" * 50)
    
    corr = correlation_stats['overall_correlation']
    p_val = correlation_stats['p_value']
    
    if abs(corr) > CORRELATION_THRESHOLD and p_val < P_VALUE_THRESHOLD:
        print("✅ SENTIMENT HAS PREDICTIVE VALUE!")
        direction = "increases" if corr > 0 else "decreases"
        print(f"   • Positive sentiment → Price {direction}")
        print("   • Justifies alert system and dashboard")
    elif abs(corr) > CORRELATION_THRESHOLD:
        print("⚠️  MODERATE CORRELATION (not statistically significant)")
        print("   • Need more data to confirm relationship")
    else:
        print("❌ WEAK CORRELATION")
        print("   • Sentiment may not predict price movement")
        print("   • Consider other factors or longer time periods")

def run_analysis():
    print("🚀 MARKET PULSE AI - CORRELATION ANALYSIS")
    print("=" * 60)
    
    df = get_data()
    if df is None:
        return

    store_sentiment_price_effects(df)
    
    correlation_stats = correlation_analysis(df)
    group_stats = group_analysis(df)
    distribution_analysis(df)
    lag_analysis(df)
    
    save_results(correlation_stats, group_stats, df)
    
    print_analysis_summary(df)
    print_conclusion(correlation_stats)

if __name__ == "__main__":
    run_analysis()
