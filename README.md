# Production AI Travel Concierge

A production-grade web application built using **LangChain (LCEL)**, **Streamlit**, and **OpenRouter (DeepSeek)**, monitored with **Langfuse**.

## 📁 Project Structure
- `app.py`: Main interactive Streamlit frontend web application.
- `requirements.txt`: Python package dependency listings.

## 🚀 Local Setup Instructions
1. Clone this repository to your machine.
2. Initialize and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the application dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.streamlit/secrets.toml` file to hold your environmental keys locally:
   ```toml
   OPENROUTER_API_KEY = "your_key"
   LANGFUSE_PUBLIC_KEY = "your_key"
   LANGFUSE_SECRET_KEY = "your_key"
   LANGFUSE_HOST = "https://cloud.langfuse.com"
   ```
5. Launch the application server locally:
   ```bash
   streamlit run app.py
   ```
