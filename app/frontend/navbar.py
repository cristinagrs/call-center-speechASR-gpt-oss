import base64
import streamlit as st

def make_sidebar(config):
    with open(config.ORACLE_LOGO, "rb") as f:
        icon_base64 = base64.b64encode(f.read()).decode()
    with st.sidebar:
        
        st.markdown(
            f"""
            <div style="display: flex; align-items: right; gap: 10px;">
                <span style="font-size: 30px; font-weight: 600;">Upload & Run</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
            <style>
                .stButton>button {
                    background-color: #F80000;
                    color: white;
                    padding: 0.5em 1em;
                    font-size: 16px;
                    border-radius: 5px;
                }
            </style>
        """, unsafe_allow_html=True)

        st.write("")
        st.write("")

        uploaded_file = st.sidebar.file_uploader("Upload an Audio", type=["wav"])
        
        selected_model = st.selectbox("Select LLM:", config.LIST_GENAI_MODELS)
        run_button = st.sidebar.button("Run")

        st.write("")
        st.write("")

        return uploaded_file, run_button, selected_model