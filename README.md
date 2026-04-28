# Actuarial-Loss-Reserving-Automation
Automated Cross-Segment IBNR reserve analysis across multiple insurance lines of business (LOBs) using the Chain Ladder Method on CAS/NAIC industry data
![Industry Reserve Distribution](reserve_distribution.png)
Algorithm: Stochastic Chain Ladder Method
Data Source: CAS Commercial Auto Data Set – 2025 Updated
Validation: Output cross referenced with manual Excel Run off triangles to ensure accuracy
### Data Pipeline & Architecture
The system utilizes a **Data-Agnostic pipeline**:
1. **Batch Loading:** Uses `glob` and `os` to automatically discover and process any CAS-formatted CSV in the `/data` directory.
2. **Dynamic Labeling:** Automatically extracts Line of Business (LOB) metadata from filenames to categorize results.
3. **Aggregated Reporting:** Concatenates individual company results into a master industry benchmark file for cross-segment comparison.
## How to Run
1. Ensure Python 3.x and pandas, numpy, matplotlib are installed. pip install pandas numpy matplotlib
2. Data Preparation
  Create a folder named CAS_Data on your local machine.
  Place the raw CAS industry CSV files into this folder.
  Datasets can be sourced from the CAS Loss Reserving Database.
3. Execution
  Open LossReserveAutomation.py.
  Update the folder_path variable to point to your CAS_Data directory.
  Update the output_folder variable to your preferred export location.
  Run the script.
4. Outputs
  Master_Actuarial_Report.csv: A consolidated dataset aggregating results across all processed lines of business.
  reserve_distribution.png: A frequency distribution plot visualizing the industry-wide reserve position (Redundancy vs. Deficiency).
