import pandas as pd
import glob
import os
import numpy as np

folder_path = '/Users/kokonenn/Downloads/CAS_data'
all_files = glob.glob(os.path.join(folder_path,"*.csv"))

all_results = []

for file in all_files:
    lob = os.path.basename(file).split('.')[0]
    print(f"Analyzing Line of Business: {lob}")
    df = pd.read_csv(file)

    companies = df['GRNAME'].unique()
    final_summary = []
    
    print(f"Analyzing {len(companies)} companies. Please wait...")
    
    for co in companies:
        co_data = df[df['GRNAME'] == co]
        triangle = co_data.pivot_table(index='AccidentYear', columns='DevelopmentLag', 
                                       values='IncurredLosses', aggfunc='sum')
        
        ata = triangle.shift(-1, axis=1) / triangle
        f = ata.mean() 
        
        sigmas = []
        for col in ata.columns:
            col_variance = ata[col].var()
            sigmas.append(col_variance)
            
        valid_averages = list(f.dropna().values)
        valid_sigmas = [s for s in sigmas if not np.isnan(s)]
            
        cdfs = [1.0]
        for val in reversed(valid_averages):
            cdfs.append(cdfs[-1] * val)
        cdfs.reverse()
            
        latest_losses = [triangle.iloc[i].dropna().iloc[-1] for i in range(len(triangle))]
        total_ultimate = sum(loss * cdf for loss, cdf in zip(reversed(latest_losses), cdfs))
        total_incurred = sum(latest_losses)
        reserve = total_ultimate - total_incurred

        avg_sigma = np.nanmean(valid_sigmas) if valid_sigmas else 0
        standard_error = np.sqrt(avg_sigma * total_incurred) 

        final_summary.append({
                'Company': co,
                'Total Incurred': total_incurred,
                'Ultimate Loss': total_ultimate,
                'IBNR Reserve': reserve,
                'Standard Error': standard_error, 
                'CV': (standard_error / reserve) if reserve > 0 else 0
        })        
    results_df = pd.DataFrame(final_summary)
    results_df.to_csv('/Users/kokonenn/Downloads/Actuarial_Results.csv', index=False)
        
    print("Done! Open 'Actuarial_Results.csv' in your Downloads folder to see all companies.")    
    
    import matplotlib.pyplot as plt
import os
import glob

folder_path = '/Users/kokonenn/Downloads/CAS_Data'
all_files = glob.glob(os.path.join(folder_path, "*.csv"))

for file in all_files:
    
    lob_name = os.path.basename(file).split('.')[0]
    print(f"Processing: {lob_name}")
    
    plt.figure(figsize=(10, 6))
    
    clean_df = results_df[np.isfinite(results_df['IBNR Reserve'])]
    plot_data = clean_df[clean_df['IBNR Reserve'].between(
        clean_df['IBNR Reserve'].quantile(0.05), 
        clean_df['IBNR Reserve'].quantile(0.95)
    )]
    
    plt.hist(plot_data['IBNR Reserve'], bins=30, color='#007acc', edgecolor='white')
    plt.axvline(0, color='red', linestyle='--')
    
    plt.title(f'Industry Reserve Adequacy: {lob_name}', fontsize=14)
    plt.xlabel('Reserve Amount ($)')
    plt.ylabel('Number of Companies')
    
    graph_name = f'/Users/kokonenn/Desktop/Reserve_Dist_{lob_name}.png'
    plt.savefig(graph_name)
    
    plt.close() 

print("All Lines of Business processed. Check your Desktop for the graphs!")

