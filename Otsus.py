import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.filters import threshold_otsu

# Load the dataset
file_path = "/Users/rakesh/Desktop/Final_Flood_Analysis.csv"

try:
    df = pd.read_csv(file_path)
    print(" CSV file loaded successfully!")
except FileNotFoundError:
    print(f" File not found at {file_path}")
    exit()

# Extract and validate columns
required_columns = {"File_Name", "Longitude", "Latitude", "dB_Value", "Flood_Status"}
missing = required_columns - set(df.columns)
if missing:
    raise KeyError(f" Missing columns: {missing}")

# Group files into Pre-Flood and Post-Flood
df_pre = df[df["File_Name"].str.contains("preflood", case=False, na=False)]
df_post = df[df["File_Name"].str.contains("postflood", case=False, na=False)]

# Compress by coordinate (average per location)
df_pre_grouped = df_pre.groupby(["Longitude", "Latitude"]).agg({"dB_Value": "mean"}).reset_index()
df_post_grouped = df_post.groupby(["Longitude", "Latitude"]).agg({"dB_Value": "mean"}).reset_index()

#  Apply Otsu's Threshold
if not df_pre_grouped["dB_Value"].empty:
    threshold_pre = threshold_otsu(df_pre_grouped["dB_Value"].dropna().to_numpy())
    print(f" Otsu’s Threshold for Pre-Flood: {threshold_pre:.2f}")
else:
    threshold_pre = None
    print("⚠ Pre-Flood data is empty!")

if not df_post_grouped["dB_Value"].empty:
    threshold_post = threshold_otsu(df_post_grouped["dB_Value"].dropna().to_numpy())
    print(f" Otsu’s Threshold for Post-Flood: {threshold_post:.2f}")
else:
    threshold_post = None
    print("⚠ Post-Flood data is empty!")

# Histogram Comparison with Otsu's thresholds
plt.figure(figsize=(12, 6))
sns.histplot(df_pre_grouped["dB_Value"], bins=50, kde=True, color="blue", label="Pre-Flood dB", alpha=0.6)
if threshold_pre:
    plt.axvline(threshold_pre, color="blue", linestyle="--", label=f"Pre-Flood Otsu = {threshold_pre:.2f}")

sns.histplot(df_post_grouped["dB_Value"], bins=50, kde=True, color="green", label="Post-Flood dB", alpha=0.6)
if threshold_post:
    plt.axvline(threshold_post, color="green", linestyle="--", label=f"Post-Flood Otsu = {threshold_post:.2f}")

plt.xlabel("dB Value")
plt.ylabel("Frequency")
plt.title("Histogram Comparison of Aggregated Pre- and Post-Flood dB Values with Otsu Thresholds")
plt.legend()
plt.grid(True)
plt.show()

print("Histogram and Otsu analysis completed!")
