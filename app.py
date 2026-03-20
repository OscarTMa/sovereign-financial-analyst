import streamlit as st
import os
from openai import OpenAI
from pypdf import PdfReader
from fpdf import FPDF
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sovereign Financial Analyst", page_icon="📈", layout="wide")

# --- FUNCIÓN PARA GENERAR PDF DE DESCARGA ---
def create_downloadable_pdf(text, query):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Financial Intelligence Report", ln=True)
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Analysis for: {query}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    # Limpiamos caracteres especiales para evitar errores de codificación en el PDF
    clean_text = text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 7, clean_text)
    
    # Retornamos los bytes directamente sin el .encode() adicional que causaba el error
    return pdf.output()

# --- FUNCIÓN DE EXTRACCIÓN DE PDF ---
def get_pdf_content(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for i, page in enumerate(reader.pages):
        content = page.extract_text()
        text += f"\n--- PAGE {i+1} ---\n{content}"
    return text

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Agent Settings")
    st.caption("Powered by NVIDIA Nemotron 3 Super (120B)")
    api_key = os.environ.get("NVIDIA_API_KEY") or st.text_input("NVIDIA API Key", type="password")
    st.divider()
    st.info("Analysis Model: nvidia/nemotron-3-super-120b-a12b")

# --- INTERFAZ PRINCIPAL ---
st.title("📈 Private Financial Intelligence Analyst")
uploaded_file = st.file_uploader("Upload a Financial Report (PDF)", type="pdf")

if uploaded_file:
    st.success(f"File '{uploaded_file.name}' ready.")
    user_query = st.text_input("Ask a specific question about this report:", placeholder="e.g., Identify the 3 main blind spots.")

    if st.button("🚀 Run Deep Analysis"):
        if not api_key:
            st.error("Please provide an NVIDIA API Key.")
        else:
            try:
                with st.spinner("Nemotron is analyzing the full context..."):
                    doc_text = get_pdf_content(uploaded_file)
                    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
                    
                    full_prompt = f"Act as a Senior Analyst. Context: {doc_text}\n\nQuestion: {user_query}\n\nAnalysis:"
                    
                    response = client.chat.completions.create(
                        model="nvidia/nemotron-3-super-120b-a12b",
                        messages=[{"role": "user", "content": full_prompt}],
                        temperature=0.1
                    )
                    
                    report_content = response.choices[0].message.content
                    st.session_state['report'] = report_content # Guardamos para descarga

                st.divider()
                st.subheader("📋 Analysis Results")
                st.markdown(report_content)

                # --- BOTÓN DE DESCARGA ---
                pdf_bytes = create_downloadable_pdf(report_content, user_query)
                st.download_button(
                    label="📥 Download Report as PDF",
                    data=pdf_bytes, # Pasamos los bytes directos
                    file_name="financial_analysis_report.pdf",
                    mime="application/pdf"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.info("Upload a PDF to begin.")
