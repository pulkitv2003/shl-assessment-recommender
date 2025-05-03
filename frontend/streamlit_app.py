import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", layout="centered")

st.title("🧠 SHL Assessment Recommendation Engine")
st.markdown("Get personalized SHL assessments based on your job description or hiring needs.")

st.subheader("📝 Enter a job description or hiring query:")
query = st.text_area("Example: Hiring a Java developer with good collaboration skills. 40-minute test preferred.", height=120)

top_k = st.slider("🔢 How many recommendations do you want?", 1, 10, 3)

if st.button("🔍 Get Recommendations"):
    if not query.strip():
        st.warning("⚠️ Please enter a valid query.")
    else:
        try:
            api_url = "http://localhost:5000/recommend" 
            response = requests.post(api_url, json={"query": query})
            if response.status_code == 200:
                results = response.json().get("recommendations", [])[:top_k]
                if results:
                    st.success(f"Top {len(results)} SHL assessments:")
                    for i, rec in enumerate(results, 1):
                        st.markdown(f"""
                        **{i}. [{rec['name']}]({rec['url']})**  
                        - ⏱ Duration: {rec['duration']}  
                        - 📂 Type: {rec['type']}  
                        - 🌐 Remote: {rec['remote_support']} | Adaptive: {rec['adaptive_support']}  
                        """)
                else:
                    st.info("No matching assessments found.")
            else:
                st.error("❌ API call failed. Try again later.")
        except Exception as e:
            st.error(f"Error: {e}")
