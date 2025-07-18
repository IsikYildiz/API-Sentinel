import streamlit as st
from core.swagger_parser import load_swagger_file, extract_endpoints, get_base_url
from core.llm import prompt_attack_cases
from core.curl_generator import generate_curl_command

st.set_page_config(page_title="API Sentinel", layout="wide")
st.title("API Sentinel - API Güvenlik Analiz Aracı")

uploaded_file = st.file_uploader("Swagger JSON Dosyasını Yükleyin", type=["json"])

if uploaded_file is not None:
    swagger_json = load_swagger_file(uploaded_file)
    endpoints = extract_endpoints(swagger_json)
    base_url = get_base_url(swagger_json)

    st.success(f"✅ {len(endpoints)} endpoint bulundu. Analiz başlatılıyor...")

    for idx, ep in enumerate(endpoints):
        with st.expander(f"🔹 {ep['method']} {ep['path']}"):
            # Parametreler
            st.markdown("### Parametreler")
            if ep["parameters"]:
                for p in ep["parameters"]:
                    st.markdown(f"- {p['name']} ({p['in']}), type: {p['type']}, required: {p['required']}")
            else:
                st.markdown("Parametre bulunamadı.")

            # Curl komutu
            curl_cmd = generate_curl_command(base_url, ep)
            st.markdown("### Curl Komutu")
            st.code(curl_cmd, language="bash")

            # LLM analizi
            st.markdown("### LLM Analizi")
            llm_output = prompt_attack_cases(ep)
            st.markdown(llm_output)