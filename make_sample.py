# make_sample.py
import pandas as pd

# Read only first 10000 rows of metadata.csv
df = pd.read_csv("metadata.csv", low_memory=False, nrows=10000)

# Save the small sample
df.to_csv("metadata_sample.csv", index=False)

print("Sample file created: metadata_sample.csv")
