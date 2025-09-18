import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re

# Load data
df = pd.read_csv("metadata.csv", low_memory=False)

# Show basic info
print("Data shape:", df.shape)
print(df.info())
print(df.isnull().sum())

# Clean data
df = df.dropna(subset=['publish_time', 'title'])
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract_word_count'] = df['abstract'].fillna('').apply(lambda x: len(x.split()))

# Analysis: Publications by year
year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,4))
plt.bar(year_counts.index, year_counts.values)
plt.title('Publications by Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.tight_layout()
plt.savefig('publications_by_year.png')
plt.close()

# Analysis: Top 10 journals
top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(8,4))
sns.barplot(x=top_journals.values, y=top_journals.index)
plt.title('Top 10 Journals')
plt.xlabel('Number of Papers')
plt.tight_layout()
plt.savefig('top_journals.png')
plt.close()

# Word frequency in titles
words = []
for title in df['title'].dropna():
    words += re.findall(r'\w+', title.lower())
common_words = Counter(words).most_common(20)
print("Most common words in titles:", common_words)

print("Data cleaning and basic analysis complete. Charts saved as PNG files.")
