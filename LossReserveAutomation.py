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

