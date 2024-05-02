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

# Display the DataFrame
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

st.button('Search', on_click=click_button)

if st.session_state.clicked:
    for i in range(len(results['ids'][0])):
        st.write(results['metadatas'][0][i]['source'])
        score = round(results['distances'][0][i], 2)
        st.write(f"Score: {score}")
st.caption("Lower score is better match")        