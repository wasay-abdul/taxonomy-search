__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pandas as pd
import chromadb
import streamlit as st

client = chromadb.PersistentClient(path="taxonomy_db")
taxonomy_collection = client.get_collection("taxonomy_collection")


st.title('Taxonomy Search')


keyword_val = st.text_input("Enter keyword to search the taxonomy", key="keyword")
results_n = st.text_input("Enter number of simliar markets you would like to look at")

# Convert results_n to integer, using a default value if conversion fails
try:
    results_n = int(results_n)
except ValueError:
    results_n = 5  # Default value if input is not a valid integer


results = taxonomy_collection.query(
        query_texts=[keyword_val],
        n_results=results_n
        )

ids_flat = [item for sublist in results['ids'] for item in sublist]
distances_flat = [item for sublist in results['distances'] for item in sublist]
sources_flat = [item['source'] for sublist in results['metadatas'] for item in sublist]
documents_flat = [item for sublist in results['documents'] for item in sublist]

# Ensure equal lengths by checking the smallest list size to avoid index mismatch
min_length = min(len(ids_flat), len(distances_flat), len(sources_flat), len(documents_flat))

# Create a DataFrame
df = pd.DataFrame({
    'ID': ids_flat[:min_length],
    'Similarity Score': distances_flat[:min_length],
    'Market Name': sources_flat[:min_length]
})


# Display the DataFrame
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Search', on_click=click_button)

if st.session_state.clicked:
    st.write(df)       
    st.caption("Lower score is better match") 
