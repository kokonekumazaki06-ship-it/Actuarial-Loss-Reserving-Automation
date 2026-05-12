# Automated IBNR Analysis & Stochastic Volatility Modeling
This repository provides a production-ready pipeline for calculating IBNR reserves using the Mack Chain Ladder method. By leveraging the CAS/NAIC industry datasets, this tool automates the construction of loss development triangles and quantifies reserve uncertainty through stochastic error estimation.
# Methodology & Algorithm
The system utilizes a **Data-Agnostic pipeline**:
1. Point Estimation: Utilizes volume-weighted age-to-age factors to project ultimate losses.
2. Stochastic Risk: Calculates the Mack Standard Error (SE) to provide a measure of parameter and process risk.
3. Relative Volatility: Derives the Coefficient of Variation (CV) to compare the risk profile across different Lines of Business (LOBs).
# How to Run
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
