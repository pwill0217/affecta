import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Parameters
num_agents = 12
days = 45  # About 1.5 months of data
start_date = datetime(2025, 3, 1)

# Agent list
agents = [f"AGENT_{str(i).zfill(3)}" for i in range(1, num_agents + 1)]
agent_names = ["Emma Chen", "Marcus Rodriguez", "Aisha Patel", "Tyler Brooks", 
               "Sofia Morales", "Jamal Wright", "Priya Sharma", "David Kim",
               "Fatima Ali", "Liam Thompson", "Zoe Garcia", "Noah Williams"]

# Generate dates
dates = [start_date + timedelta(days=i) for i in range(days)]

# Create empty list to hold records
records = []

for agent_id, name in zip(agents, agent_names):
    # Create baseline for each agent (some are naturally higher stress)
    base_calls = np.random.randint(35, 55)
    base_duration = np.random.uniform(6.5, 9.5)
    stress_tendency = np.random.uniform(0.3, 0.8)  # Higher = more likely to show stress
    
    for date in dates:
        # Simulate realistic variation
        calls_handled = int(np.random.normal(base_calls, 6))
        calls_handled = max(20, min(70, calls_handled))
        
        avg_call_duration = round(np.random.normal(base_duration, 1.2), 2)
        avg_acw_time = round(np.random.normal(4.5, 2.0), 2)  # After Call Work
        avg_hold_time = round(np.random.normal(2.8, 1.5), 2)
        transfers = int(np.random.normal(3, 1.5))
        
        # PTO (decreases over time, with occasional bigger usage)
        pto_balance = max(0, round(80 - (date - start_date).days * 0.8 + np.random.normal(0, 8), 1))
        pto_used = round(np.random.uniform(0, 12), 1)
        
        # Tone / Sentiment features
        avg_sentiment = round(np.random.normal(0.15, 0.35), 2)  # -1 to 1
        frustration_keywords = int(np.random.poisson(2.5))
        
        # Pitch variance (higher = more stress)
        pitch_variance = round(np.random.normal(45, 25), 1)
        
        # Simple stress score (for testing your model later)
        stress_score = round(
            (calls_handled / 55) * 0.3 +
            (avg_acw_time / 8) * 0.25 +
            (max(0, 0.4 - avg_sentiment)) * 0.25 +
            (frustration_keywords / 8) * 0.1 +
            (pitch_variance / 120) * 0.1,
            2
        )
        stress_score = min(0.98, max(0.05, stress_score))
        
        records.append({
            'agent_id': agent_id,
            'agent_name': name,
            'date': date.date(),
            'calls_handled': calls_handled,
            'avg_call_duration_min': avg_call_duration,
            'avg_acw_time_min': avg_acw_time,
            'avg_hold_time_min': avg_hold_time,
            'transfers': max(0, transfers),
            'pto_balance_hours': pto_balance,
            'pto_used_this_month': pto_used,
            'avg_sentiment_score': avg_sentiment,
            'frustration_keywords_count': frustration_keywords,
            'avg_pitch_variance': pitch_variance,
            'stress_score': stress_score
        })

# Create DataFrame
df = pd.DataFrame(records)

# Save to CSV
df.to_csv('synthetic_call_center_data.csv', index=False)
print(f"✅ Generated {len(df)} rows of data for {num_agents} agents")
print(f"File saved as: synthetic_call_center_data.csv")
print("\nColumns:", df.columns.tolist())

# Show sample
print("\nFirst 5 rows:")
print(df.head())