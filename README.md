# AI-Data-Visualization-Agent
An AI-powered data visualization agent built with Streamlit and Groq. Upload any CSV dataset, ask natural-language questions, and get automatically generated Python code + visualizations like line charts, scatter plots, heatmaps, boxplots, and more. No paid APIs required — runs completely locally with free Groq LLM integration.

# 📊 AI Data Visualization Agent using Streamlit + Groq

This project is an **AI-powered data analysis and visualization system** built with **Streamlit**, **Groq LLM**, **Pandas**, and **Matplotlib**.

You can upload **any CSV dataset**, ask natural-language questions, and the AI will:

- Understand your query  
- Generate Python code  
- Execute the code locally  
- Produce visualizations (line charts, scatter plots, boxplots, heatmaps, KDE plots, etc.)  
- Display results instantly  

This project **does not require Together AI** or any paid API keys.  
It only uses **Groq API (completely free, no credit card needed)**.

---

## 🚀 Features

- Upload any CSV dataset
- Ask questions in natural language
- Automatically generate Python analysis code
- Safe local execution of code (no remote sandbox needed)
- Wide range of chart types supported:
  - Line chart  
  - Scatter plot  
  - Box plot  
  - Violin plot  
  - Correlation heatmap  
  - KDE density plot  
  - Area chart  
  - And more  
- Automatically detects valid Groq models available to your account
- Works completely on local machine (VS Code recommended)

---

## 🧠 Technology Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend LLM | Groq API (Llama 3 models) |
| Python Execution | Local environment (secure `exec`) |
| Data Processing | Pandas |
| Visualization | Matplotlib |

---

## 🛠️ Installation

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd <your-project-folder>
