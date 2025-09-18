# Part 4: Streamlit Application
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from wordcloud import WordCloud

# -------------------------------
# Part 1: Load Data and Explore
# -------------------------------
st.title("CORD-19 Data Explorer")
st.write("Exploring COVID-19 research papers dataset (metadata.csv)")

# Load CSV
df = pd.read_csv("metadata.csv", low_memory=False)

# -------------------------------
# Part 2: Data Cleaning & Preparation
# -------------------------------
# Make a copy and clean key columns
df_clean = df.copy()

# Ensure publish_time is datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Drop rows without publish_time or title
df_clean = df_clean.dropna(subset=['publish_time', 'title']).copy()

# Extract year as numeric
df_clean['year'] = df_clean['publish_time'].dt.year

# Abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

# Fill missing journal/source with 'Unknown' to avoid plot errors
df_clean['journal'] = df_clean['journal'].fillna('Unknown')
if 'source_x' in df_clean.columns:
    df_clean['source_x'] = df_clean['source_x'].fillna('Unknown')

# -------------------------------
# Part 3: Analysis & Visualizations
# -------------------------------
st.subheader("Analysis & Visualizations")

# Sidebar filter: year range
min_year = int(df_clean['year'].min())
max_year = int(df_clean['year'].max())
year_range = st.sidebar.slider("Select year range", min_year, max_year, (min_year, max_year))

filtered_df = df_clean[(df_clean['year'] >= year_range[0]) & (df_clean['year'] <= year_range[1])]
st.write(f"Papers from {year_range[0]} to {year_range[1]}: {len(filtered_df)}")

# 1️⃣ Publications by Year
year_counts = filtered_df['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_title("Publications by Year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
st.pyplot(fig1)

# 2️⃣ Top 10 Journals
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax2, palette="viridis")
ax2.set_title("Top 10 Journals Publishing COVID-19 Research")
ax2.set_xlabel("Number of Papers")
st.pyplot(fig2)

# 3️⃣ Most Common Words in Titles
words = []
for title in filtered_df['title'].dropna():
    words += re.findall(r'\w+', title.lower())
common_words = Counter(words).most_common(20)

st.subheader("Most Frequent Words in Titles (Top 20)")
st.write(common_words)

# 3️⃣a Word Cloud of Titles
st.subheader("Word Cloud of Paper Titles")
text = " ".join(filtered_df['title'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
ax_wc.imshow(wordcloud, interpolation='bilinear')
ax_wc.axis('off')
st.pyplot(fig_wc)

# 4️⃣ Distribution by Source
if 'source_x' in filtered_df.columns:
    st.subheader("Distribution of Papers by Source")
    source_counts = filtered_df['source_x'].value_counts().head(10)
    fig3, ax3 = plt.subplots()
    sns.barplot(x=source_counts.values, y=source_counts.index, ax=ax3, palette="magma")
    ax3.set_xlabel("Number of Papers")
    st.pyplot(fig3)

# -------------------------------
# Part 5: Data Sample
# -------------------------------
st.subheader("Sample of Filtered Data")
st.write(filtered_df[['title', 'journal', 'year', 'abstract']].head(10))

st.write("Streamlit app ready! Use the sidebar to filter by year.")
