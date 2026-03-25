import pandas as pd
import sys
import numpy as np

def analyze_water_level(file_path):
    print(f"Loading data from {file_path}...\n")
    df = pd.read_csv(file_path)
    
    # Parse datetime and sort
    df['_time'] = pd.to_datetime(df['_time'])
    df = df.sort_values('_time').reset_index(drop=True)
    
    # Calculate the duration of each reading
    # Assume each reading lasts until the next timestamp.
    # We use a cap (e.g., 20 minutes) so massive gaps don't inflate the "time under water".
    # Typical frequency seems to be 10 minutes.
    time_diff_mins = df['_time'].diff(-1).abs().dt.total_seconds() / 60.0
    # Fill NaN (last row) and cap at 15 minutes to be safe against data dropouts
    df['duration_mins'] = time_diff_mins.fillna(10.0)
    df.loc[df['duration_mins'] > 15, 'duration_mins'] = 10.0
    
    # Create a Month column for grouping (YYYY-MM)
    df['month'] = df['_time'].dt.strftime('%Y-%m')
    
    thresholds = [830, 570]
    
    for threshold in thresholds:
        print(f"{'='*50}")
        print(f"ANALYSIS FOR HEIGHT < {threshold}mm")
        print(f"{'='*50}")
        
        # Boolean mask
        df['is_below'] = df['water_height_mm'] < threshold
        
        # Identify discrete events (goes from False to True)
        # Shift mask to see previous row's state
        df['prev_is_below'] = df['is_below'].shift(1).fillna(False)
        df['event_start'] = df['is_below'] & ~df['prev_is_below']
        
        # Calculate total metrics
        total_mins = df.loc[df['is_below'], 'duration_mins'].sum()
        total_hours = total_mins / 60.0
        total_events = df['event_start'].sum()
        
        print(f"Overall Total Duration: {total_hours:.2f} hours (or {total_mins:.1f} minutes)")
        print(f"Overall Total Events:   {total_events}")
        print("-" * 50)
        
        # Group by month
        monthly_stats = []
        for month, group in df.groupby('month'):
            hrs = group.loc[group['is_below'], 'duration_mins'].sum() / 60.0
            evts = group['event_start'].sum()
            monthly_stats.append({
                'Month': month,
                'Events Count': evts,
                'Duration (Hours)': hrs
            })
            
        stats_df = pd.DataFrame(monthly_stats)
        # Format hours to 2 decimal places
        stats_df['Duration (Hours)'] = stats_df['Duration (Hours)'].round(2)
        print(stats_df.to_string(index=False))
        print("\n")

if __name__ == "__main__":
    file_path = "/Users/dunc/Dropbox/code/CASA/housemill/data/influxdb/housemill_2024.csv"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    analyze_water_level(file_path)
