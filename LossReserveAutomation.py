import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

folder_path = '/Users/kokonenn/Downloads/CAS_data'
output_path = '/Users/kokonenn/Downloads/Master_Actuarial_Report.csv'
plot_dir = '/Users/kokonenn/Desktop/'

all_files = glob.glob(os.path.join(folder_path, "*.csv"))
all_lob_results = []

for file in all_files:
    lob = os.path.basename(file).split('.')[0]
    print(f"Processing Line of Business: {lob}")
    
    try:
        df = pd.read_csv(file)
    except Exception as e:
        print(f"Skipping {file} due to error: {e}")
        continue

    companies = df['GRNAME'].unique()
    final_summary = []

    for co in companies:
        co_data = df[df['GRNAME'] == co].copy()
        
        triangle = co_data.pivot_table(index='AccidentYear', columns='DevelopmentLag', 
                                       values='IncurredLosses', aggfunc='sum')
        
        if triangle.empty or triangle.shape[1] < 2:
            continue
            
        n = triangle.shape[1] 
        
        f = []
        sigmas = []
        
        for i in range(n - 1):
            column_j = triangle.iloc[:(n-1-i), i]
            column_j_plus_1 = triangle.iloc[:(n-1-i), i+1]
            
            sum_j = column_j.sum()
            
            if sum_j == 0 or np.isnan(sum_j):
                f_i = 1.0 
            else:
                f_i = column_j_plus_1.sum() / sum_j
            f.append(f_i)
            
            if (n - 1 - i) > 1 and sum_j > 0:
                valid_mask = (column_j > 0)
                if valid_mask.any():
                    var_sum = sum(column_j[valid_mask] * ((column_j_plus_1[valid_mask] / column_j[valid_mask]) - f_i)**2)
                    variance = (1 / (n - 2 - i)) * var_sum
                    sigmas.append(variance)
                else:
                    sigmas.append(0)
            else:
                sigmas.append(sigmas[-1] if len(sigmas) > 0 else 0)

        cdfs = [1.0]
        for val in reversed(f):
            cdfs.append(cdfs[-1] * val)
        cdfs.reverse()

        latest_losses = [triangle.iloc[i].dropna().iloc[-1] for i in range(len(triangle))]
        ultimate_losses = [loss * cdf for loss, cdf in zip(latest_losses, cdfs)]
        
        total_ultimate = sum(ultimate_losses)
        total_incurred = sum(latest_losses)
        total_ibnr = total_ultimate - total_incurred

        mse_sum = 0
        if total_ibnr > 0 and total_incurred > 0:
            for i in range(1, n):
                year_ultimate = ultimate_losses[i]
                year_incurred = latest_losses[i]
                
                idx = min(n-1-i, len(sigmas)-1)
                denom = sum(triangle.iloc[:(n-idx-1), idx])
                
                if denom > 0:
                    mse_sum += (year_ultimate**2) * (sigmas[idx] / f[idx]**2) * (1/year_incurred + 1/denom)
        
        standard_error = np.sqrt(mse_sum) if mse_sum > 0 else 0

        final_summary.append({
            'LOB': lob,
            'Company': co,
            'Total Incurred': total_incurred,
            'Ultimate Loss': total_ultimate,
            'IBNR Reserve': total_ibnr,
            'Mack SE': standard_error,
            'CV': (standard_error / total_ibnr) if total_ibnr > 0 else 0
        })

    if final_summary:
        lob_df = pd.DataFrame(final_summary)
        all_lob_results.append(lob_df)
        
        plt.figure(figsize=(10, 6))
        clean_plot_df = lob_df[np.isfinite(lob_df['IBNR Reserve'])]
        
        if len(clean_plot_df) > 5:
            lower, upper = clean_plot_df['IBNR Reserve'].quantile([0.05, 0.95])
            plot_data = clean_plot_df[clean_plot_df['IBNR Reserve'].between(lower, upper)]
        else:
            plot_data = clean_plot_df

        plt.hist(plot_data['IBNR Reserve'], bins=25, color='#007acc', edgecolor='white')
        plt.axvline(0, color='red', linestyle='--')
        plt.title(f'Mack IBNR Distribution: {lob}', fontsize=14)
        plt.xlabel('Reserve Amount ($)')
        plt.ylabel('Company Count')
        
        plt.savefig(os.path.join(plot_dir, f'Reserve_Dist_{lob}.png'))
        plt.close()

if all_lob_results:
    master_df = pd.concat(all_lob_results)
    master_df.to_csv(output_path, index=False)
    print(f"\nSuccess! Total Companies Processed: {len(master_df)}")
    print(f"Report saved to: {output_path}")
    print(f"Graphs saved to: {plot_dir}")
else:
    print("No data was processed. Check your folder_path and CSV formats.")
