<<<<<<< HEAD
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
=======
import streamlit as st
import requests

st.set_page_config(page_title="Skill Search", page_icon="🔍", layout="centered")

st.title("🔎 Skill Match Finder")

query = st.text_input("Enter your query below to find people offering the required skills:")

if st.button("🔎 Search"):
    if query.strip():
        try:
            response = requests.post(
                "http://127.0.0.1:8000/search",  # "https://odoo-skill-api.onrender.com",
                json={"query": query}
            )

            if response.status_code == 200:
                results = response.json().get("results", [])

                if results:
                    st.success(f"✅ Found {len(results)} matching user(s):\n")
                    for user in results:
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown("🧑‍💼")
                            with col2:
                                st.markdown(f"""
                                **👤 Name:** {user.get('name', 'N/A')}  
                                **🆔 ID:** `{user.get('id', 'N/A')}`  
                                **📍 City:** {user.get('city', 'N/A')}  
                                **📆 Availability:** {", ".join(user.get('availability', []))}
                                """)
                            st.markdown("---")
                else:
                    st.warning("No matching users found.")
            else:
                st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
    else:
        st.warning("⚠️ Please enter a query.")
>>>>>>> d74a9fc (Bug fixed in main)
