import streamlit as st
import os
from openai import OpenAI
from pdf_engine import get_pdf_content

st.set_page_config(page_title="Financial Intelligence Agent", page_icon="📈")
st.title("📈 Sovereign Financial Analyst")
st.caption("Deep Reasoning over massive financial reports via NVIDIA Nemotron")

# Reutilizamos tu lógica de Secrets para la API Key
api_key = os.environ.get("NVIDIA_API_KEY") or st.sidebar.text_input("NVIDIA API Key", type="password")

uploaded_file = st.file_uploader("Upload a Financial Report (PDF)", type="pdf")

if uploaded_file and api_key:
    if st.button("🔍 Run Intelligence Audit"):
        with st.spinner("Reading full document (Long Context Mode)..."):
            doc_text = get_pdf_content(uploaded_file)
        
        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
        
        with st.spinner("Nemotron is analyzing cross-sectional risks..."):
            prompt = f"""
            Act as a Senior Hedge Fund Analyst. Analyze this corporate report for:
            1. **Hidden Risks**: Identifying subtle warnings in the text.
            2. **Data Consistency**: Check if statements on different pages contradict each other.
            3. **Executive Sentiment**: Evaluate the real confidence of the management.
            
            Full Document Content:
            {doc_text}
            """
            
            response = client.chat.completions.create(
                model="nvidia/nemotron-3-super-120b-a12b",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            st.success("Analysis Complete")
            st.markdown(response.choices[0].message.content)
