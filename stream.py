import streamlit as st
import requests

st.title("Skill Search")

# User input
query = st.text_input("Enter your query:")

# Button to trigger search
if st.button("Search"):
    if query.strip():
        try:
            # Send POST request to your FastAPI endpoint
            response = requests.post(
                "https://odoo-skill-api-1.onrender.com/search",
                json={"query": query}
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Matching User IDs:")
                st.write(result)
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a query.")
