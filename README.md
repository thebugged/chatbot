
<div align="center">
  <br />
    <a href="#" target="_blank">
      <img src="https://github.com/user-attachments/assets/your-banner-image-here" alt="AI Chat App Banner">
    </a>
  <br />

  <div>
    <img src="https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB" alt="python" />
    <img src="https://img.shields.io/badge/-Streamlit-black?style=for-the-badge&logoColor=white&logo=streamlit&color=FF4B4B" alt="streamlit" />
    <img src="https://img.shields.io/badge/-LangChain-black?style=for-the-badge&logoColor=white&logo=chainlink&color=375BD2" alt="langchain" />
    <img src="https://img.shields.io/badge/-OpenRouter-black?style=for-the-badge&logoColor=white&logo=openai&color=412991" alt="openrouter" />
  </div>

  <h3 align="center">Chatbot</h3>

   <div align="center">
     An intelligent AI assistant that can analyze images, answer questions, and engage in natural conversations across multiple topics.
    </div>
</div>
<br/>


## Setup & Installation

**Prerequisites**

Ensure you have the following installed:

- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

**Installation**

1. Clone the repository:
```bash
git clone https://github.com/thebugged/chatbot.git
```

2. Change into the project directory:
```bash
cd chatbot
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenRouter API credentials:
   - Get your API key from [OpenRouter](https://openrouter.ai/)
   - Create a `.streamlit/secrets.toml` file:
   ```toml
   MODEL_NAME = "anthropic/claude-3-sonnet"
   OPENROUTER_API_KEY = "your_openrouter_api_key_here"
   OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
   ```

**Running the Application**

1. Start the Streamlit server:
```bash
streamlit run main.py
```

2. Open your browser and navigate to `http://localhost:8501`

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#)



