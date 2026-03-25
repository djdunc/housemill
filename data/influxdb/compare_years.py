import os
import pandas as pd
import matplotlib.pyplot as plt

try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    pass

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return None
    
    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)
    df['_time'] = pd.to_datetime(df['_time'])
    df = df.sort_values('_time').reset_index(drop=True)
    
    time_diff_mins = df['_time'].diff(-1).abs().dt.total_seconds() / 60.0
    
    df['duration_mins'] = time_diff_mins.fillna(10.0)
    df.loc[df['duration_mins'] > 15, 'duration_mins'] = 10.0
    
    df['year'] = df['_time'].dt.year
    df['month_num'] = df['_time'].dt.month
    df['hour'] = df['_time'].dt.hour
    return df

def generate_report(dfs, output_dir):
    if not dfs:
        print("No data available.")
        return
        
    df = pd.concat(dfs, ignore_index=True)
    df = df.sort_values('_time').reset_index(drop=True)
    
    years_present = sorted(df['year'].unique())
    title_years = " vs ".join(map(str, years_present))
    
    readme_content = f"# Water Height Comparison ({title_years})\n\n"
    readme_content += "This document compares the sonar distance data across the captured years, tracking flood events using the 830mm and 570mm thresholds.\n\n"
    
    thresholds = [830, 570]
    
    for threshold in thresholds:
        print(f"Processing threshold {threshold}mm...")
        
        df['is_below'] = df['water_height_mm'] < threshold
        df['prev_is_below'] = df.groupby('year')['is_below'].shift(1).fillna(False)
        df['event_start'] = df['is_below'] & ~df['prev_is_below']
        df['event_id'] = df['event_start'].cumsum()
        
        # Mask out rows that aren't part of an event
        df.loc[~df['is_below'], 'event_id'] = pd.NA
        
        readme_content += f"## Threshold: < {threshold}mm\n\n"
        
        # 1. Yearly Statistics Table
        readme_content += "### Yearly Statistics\n"
        stats_rows = []
        for year in years_present:
            y_df = df[df['year'] == year]
            ev_df = y_df[y_df['is_below']].copy()
            
            if ev_df.empty:
                stats_rows.append([str(year), "0", "0.00", "0.00", "0.00", "0.0%"])
                continue
            
            events = ev_df.groupby('event_id').agg(
                duration=('duration_mins', 'sum'),
                start_hour=('hour', 'first')
            )
            
            total_events = len(events)
            total_duration_hrs = events['duration'].sum() / 60.0
            avg_duration = events['duration'].mean()
            std_duration = events['duration'].std() if total_events > 1 else 0.0
            
            daytime_events = events[(events['start_hour'] >= 8) & (events['start_hour'] < 19)].shape[0]
            daytime_pct = (daytime_events / total_events) * 100 if total_events > 0 else 0
            
            stats_rows.append([
                str(year),
                str(total_events),
                f"{total_duration_hrs:.2f}",
                f"{avg_duration:.2f}",
                f"{std_duration:.2f}",
                f"{daytime_pct:.1f}%"
            ])
            
        headers_stats = ["Year", "Total Events", "Total Duration (Hrs)", "Avg Duration (Mins)", "Std Dev (Mins)", "Daytime Events (8am-7pm) %"]
        readme_content += "| " + " | ".join(headers_stats) + " |\n"
        readme_content += "|" + "|".join(["---"] * len(headers_stats)) + "|\n"
        for row in stats_rows:
            readme_content += "| " + " | ".join(row) + " |\n"
        readme_content += "\n"
        
        # 2. Monthly Breakdown & Plot
        monthly = df.groupby(['year', 'month_num']).apply(
            lambda x: pd.Series({
                'events': x['event_start'].sum(),
                'duration_hrs': x.loc[x['is_below'], 'duration_mins'].sum() / 60.0
            })
        ).reset_index()
        
        pivot_events = monthly.pivot(index='month_num', columns='year', values='events').fillna(0)
        pivot_duration = monthly.pivot(index='month_num', columns='year', values='duration_hrs').fillna(0)
        
        for m in range(1, 13):
            if m not in pivot_events.index:
                pivot_events.loc[m] = 0
                pivot_duration.loc[m] = 0
                
        pivot_events = pivot_events.sort_index()
        pivot_duration = pivot_duration.sort_index()
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        pivot_events.index = month_names
        pivot_duration.index = month_names
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        pivot_events.plot(kind='bar', ax=ax1, color=colors[:len(pivot_events.columns)])
        ax1.set_title(f'Number of Events (< {threshold}mm)')
        ax1.set_ylabel('Events Count')
        ax1.set_xlabel('Month')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend(title="Year")
        
        pivot_duration.plot(kind='bar', ax=ax2, color=colors[:len(pivot_duration.columns)])
        ax2.set_title(f'Total Duration in Hours (< {threshold}mm)')
        ax2.set_ylabel('Hours')
        ax2.set_xlabel('Month')
        ax2.tick_params(axis='x', rotation=45)
        ax2.legend(title="Year")
        
        plt.tight_layout()
        plot_filename = f'comparison_plot_{threshold}mm.png'
        plt.savefig(os.path.join(output_dir, plot_filename), dpi=150)
        plt.close()
        
        readme_content += f"![Comparison Plot {threshold}mm]({plot_filename})\n\n"
        
        readme_content += "### Number of Events (Monthly)\n"
        headers_monthly = ["Month"] + [str(y) for y in pivot_events.columns]
        readme_content += "| " + " | ".join(headers_monthly) + " |\n"
        readme_content += "|" + "|".join(["---"] * len(headers_monthly)) + "|\n"
        for month in pivot_events.index:
            row = [month] + [str(int(val)) for val in pivot_events.loc[month].values]
            readme_content += "| " + " | ".join(row) + " |\n"
        readme_content += "\n"
        
        readme_content += "### Total Duration in Hours (Monthly)\n"
        readme_content += "| " + " | ".join(headers_monthly) + " |\n"
        readme_content += "|" + "|".join(["---"] * len(headers_monthly)) + "|\n"
        for month in pivot_duration.index:
            row = [month] + [f"{val:.2f}" for val in pivot_duration.loc[month].values]
            readme_content += "| " + " | ".join(row) + " |\n"
        readme_content += "\n"

    readme_path = os.path.join(output_dir, 'readme.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)
        
    print(f"Generated {readme_path} and plots successfully.")

if __name__ == "__main__":
    base_dir = "/Users/dunc/Dropbox/code/CASA/housemill/data/influxdb"
    
    file_24 = os.path.join(base_dir, "housemill_2024.csv")
    file_25 = os.path.join(base_dir, "housemill_2025.csv")
    
    valid_dfs = []
    
    df_24 = process_file(file_24)
    if df_24 is not None: valid_dfs.append(df_24)
        
    df_25 = process_file(file_25)
    if df_25 is not None: valid_dfs.append(df_25)
        
    if valid_dfs:
        generate_report(valid_dfs, base_dir)
    else:
        print("No datasets were able to be loaded. Aborting.")
