import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from groq import Groq
from io import BytesIO
import warnings
import re
import sys

warnings.filterwarnings("ignore")

pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)

def extract_code(text):
    match = pattern.search(text)
    if match:
        return match.group(1)
    return None


def execute_code(code, df):
    try:
        local_env = {"df": df, "pd": pd, "plt": plt}
        plt.clf()

        exec(code, local_env)

        if plt.get_fignums():
            buffer = BytesIO()
            plt.savefig(buffer, format="png", bbox_inches="tight")
            buffer.seek(0)
            return buffer

        return "No visualization generated."

    except Exception as e:
        return f"❌ Python Execution Error: {str(e)}"



def fetch_groq_models(api_key):
    """Fetches all available models from Groq for the user's API key."""
    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        data = response.json()

        models = [m.get("id") for m in data.get("data", [])]
        return models

    except Exception:
        return []


def main():
    st.title("📊 AI Data Visualization Agent (Groq-Powered)")
    st.write("Upload your dataset and ask questions. No paid APIs required!")

    # -------- SIDEBAR SETTINGS --------
    with st.sidebar:
        st.header("🔐 Groq Configuration")

        groq_key = st.text_input("Enter Groq API Key", type="password")
        st.markdown("[Get Free Groq API Key](https://console.groq.com/keys)")

        models = []
        if groq_key:
            with st.spinner("Fetching supported models..."):
                models = fetch_groq_models(groq_key)

        if not models:
            st.warning("No model list available. Using fallback model.")
            models = ["llama3-70b-8192"]  # guaranteed to exist

        model_name = st.selectbox("Choose Model", models)

    # -------- FILE UPLOAD --------
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)
        st.write("### 📄 Dataset Preview")
        st.dataframe(df.head())

        query = st.text_area("💬 Ask your question about the dataset:")

        if st.button("Analyze"):
            if not groq_key:
                st.error("Please provide your Groq API key.")
                return

            client = Groq(api_key=groq_key)

            system_prompt = f"""
You are a Python data analyst.
The user has uploaded a dataset which is loaded into a pandas DataFrame called df.

Here are the EXACT columns in the dataset:
{list(df.columns)}

IMPORTANT RULES:
1. You MUST ONLY use columns from the list above.
2. NEVER assume a column exists. Never invent names.
3. If the user asks something that requires unavailable columns,
   gracefully choose the closest valid columns from df.
4. ALWAYS respond ONLY with Python code inside a ```python code block```.
5. Your code must:
   - analyze df based on the user’s question
   - generate at least one matplotlib visualization
   - NOT print extra text
6. NEVER use input(), print(), or return anything.
7. ALWAYS generate a plot using plt.show().

The DataFrame is already loaded as df — DO NOT load it again.
"""

            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": query}
                        ]
                    )
                except Exception as e:
                    st.error(f"Groq API Error: {str(e)}")
                    return

            llm_output = response.choices[0].message.content
            st.write("### 🤖 AI-Generated Code")
            st.code(llm_output)

            # Extract python code
            code = extract_code(llm_output)

            if not code:
                st.error("❌ No Python code block found in the AI response.")
                return

            result = execute_code(code, df)

            if isinstance(result, BytesIO):
                st.image(result, caption="📊 Visualization")
            else:
                st.error(result)


if __name__ == "__main__":
    main()
