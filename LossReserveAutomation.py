import pandas as pd
file_path = '/Users/kokonenn/Downloads/LR_data.csv'
output_path = '/Users/kokonenn/Downloads/LR_results.csv'
df = pd.read_csv(file_path)

companies = df['GRNAME'].unique()
final_summary = []

print(f"Analyzing {len(companies)} companies. Please wait...")

for co in companies:
    co_data = df[df['GRNAME'] == co]
    triangle = co_data.pivot_table(index='AccidentYear', columns='DevelopmentLag', 
                                   values='IncurredLosses', aggfunc='sum')  
    ata = triangle.shift(-1, axis=1) / triangle
    averages = ata.mean()
    valid_averages = list(averages.dropna().values)
        
    cdfs = [1.0]
    for val in reversed(valid_averages):
        cdfs.append(cdfs[-1] * val)
    cdfs.reverse()
        
    latest_losses = [triangle.iloc[i].dropna().iloc[-1] for i in range(len(triangle))]
        
    total_ultimate = 0
    total_incurred = sum(latest_losses)

    total_ultimate = sum(loss * cdf for loss, cdf in zip(reversed(latest_losses), cdfs))
    total_incurred = sum(latest_losses)
    
    reserve = total_ultimate - total_incurred
        
    final_summary.append({
            'Company': co,
            'Total Incurred': total_incurred,
            'Ultimate Loss': total_ultimate,
            'IBNR Reserve': reserve
    })
    
results_df = pd.DataFrame(final_summary)
results_df.to_csv('/Users/kokonenn/Downloads/Actuarial_Results.csv', index=False)
    
print("Done! Open 'Actuarial_Results.csv' in your Downloads folder to see all companies.")    

import matplotlib.pyplot as plt
import numpy as np

clean_df = results_df.copy()
clean_df = clean_df[np.isfinite(clean_df['IBNR Reserve'])]

lower_bound = clean_df['IBNR Reserve'].quantile(0.05)
upper_bound = clean_df['IBNR Reserve'].quantile(0.95)
plot_data = clean_df[clean_df['IBNR Reserve'].between(lower_bound, upper_bound)]

plt.figure(figsize=(10, 6))
plt.hist(plot_data['IBNR Reserve'], bins=30, color='#007acc', edgecolor='white')

plt.axvline(0, color='red', linestyle='--', label='Breakeven (Redundant vs Deficient)')

plt.title('Industry Reserve Adequacy: IBNR Distribution', fontsize=14)
plt.xlabel('Reserve Amount ($)', fontsize=12)
plt.ylabel('Number of Companies', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.savefig('/Users/kokonenn/Desktop/reserve_distribution.png')
plt.show() 