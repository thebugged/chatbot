import base64 as _b64
import streamlit as st
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
)


MODEL_NAME = st.secrets["MODEL_NAME"]
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_BASE_URL = st.secrets["OPENROUTER_BASE_URL"]

llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.4,
)

# helper functions
def time_context_now() -> str:
    h = datetime.now().hour
    if 5 <= h < 12:
        return "morning"
    if 12 <= h < 17:
        return "afternoon"
    if 17 <= h < 21:
        return "evening"
    return "night"

TITLE_PROMPT = """You write short, friendly chat titles that ASK or ENGAGE.
                Rules:
                - 2–6 words, casual and welcoming.
                - Always ask a question or invite conversation.
                - Use proper punctuation (questions, invitations).
                - Address one individual directly, not generic.
                - Avoid cheesy greetings like "Good morning sunshine."
                - Fit the given time of day naturally.
                Return ONLY the title text.
                Examples:
                Time: morning -> What's on your agenda?
                Time: morning -> Coffee ready? Let's chat
                Time: afternoon -> How's it going so far?
                Time: afternoon -> Need a quick break?
                Time: evening -> Ready to unwind?
                Time: evening -> What's on your mind?
                Time: night -> Can't sleep either?
                Time: night -> What's keeping you up?
                """

def generate_title_for(time_context: str) -> str:
    prompt = f"{TITLE_PROMPT}\nTime: {time_context} ->"
    try:
        resp = llm.invoke([HumanMessage(content=prompt)])
        title = (resp.content or "").strip().strip('"').strip("'")
        return title or {
            "morning": "What's on your agenda?",
            "afternoon": "How's it going so far?", 
            "evening": "Ready to unwind?",
            "night": "Can't sleep either?",
        }[time_context]
    except Exception:
        return {
            "morning": "What's on your agenda?",
            "afternoon": "How's it going so far?",
            "evening": "Ready to unwind?", 
            "night": "Can't sleep either?",
        }[time_context]

def file_to_data_url(uploaded_file) -> str:
    data = uploaded_file.read()
    b64 = _b64.b64encode(data).decode("utf-8")
    mime = uploaded_file.type or "image/png"
    return f"data:{mime};base64,{b64}"

def render_history():
    for msg in st.session_state["render_messages"]:
        with st.chat_message(msg["role"]):
            if msg.get("content"):
                st.write(msg["content"])
            for img in msg.get("images", []):
                st.image(img, caption="attached image", use_container_width=True)

def handle_api_error(error):
    """Handle different types of API errors with user-friendly messages"""
    error_str = str(error)
    
    if "429" in error_str or "Rate limit exceeded" in error_str:
        st.error("🚫 **Rate Limit Reached**")
        st.info("""
        **You've hit the daily free model limit.**
        
        **Options to continue:**
        - Add credits to your OpenRouter account for unlimited access
        - Wait until tomorrow for the limit to reset
        - Try switching to a different model in your settings
        """)
        return True
    elif "401" in error_str or "authentication" in error_str.lower():
        st.error("🔑 **Authentication Error**")
        st.info("Please check your API key in the app settings.")
        return True
    elif "400" in error_str:
        st.error("❌ **Bad Request**")
        st.info("There was an issue with your request. Please try again.")
        return True
    else:
        st.error("⚠️ **Connection Error**")
        st.info("Unable to connect to the AI service. Please check your internet connection and try again.")
        return True

st.session_state.setdefault("render_messages", [])
st.session_state.setdefault("lc_messages", [])

# cache the dynamic title once per time block
now_block = time_context_now()
if ("app_title" not in st.session_state) or (st.session_state.get("app_title_block") != now_block):
    st.session_state["app_title"] = generate_title_for(now_block)
    st.session_state["app_title_block"] = now_block

st.title(st.session_state["app_title"])
st.caption("Images use more tokens than text, rate limit will run out faster with them")

render_history()

prompt = st.chat_input(
    "Say something...",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)

if prompt:
    text = getattr(prompt, "text", None) or (prompt.get("text") if isinstance(prompt, dict) else None)
    files = getattr(prompt, "files", None) or (prompt.get("files") if isinstance(prompt, dict) else None)
    files = files or []
    
    content_parts = []
    if text:
        content_parts.append({"type": "text", "text": text})
    
    image_previews = []
    for f in files[:4]:
        data_url = file_to_data_url(f)
        content_parts.append({"type": "image_url", "image_url": data_url})
        image_previews.append(f)
    
    if not content_parts:
        st.stop()
    
    st.session_state["render_messages"].append({
        "role": "user",
        "content": text or "",
        "images": image_previews,
    })
    
    with st.chat_message("user"):
        if text:
            st.write(text)
        for img in image_previews:
            st.image(img, caption="attached image", use_container_width=True)
    
    st.session_state["lc_messages"].append(HumanMessage(content=content_parts))
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = llm.invoke(st.session_state["lc_messages"])
                assistant_text = response.content if isinstance(response.content, str) else str(response.content)
                
                st.session_state["render_messages"].append({
                    "role": "assistant",
                    "content": assistant_text,
                    "images": [],
                })
                st.session_state["lc_messages"].append(AIMessage(content=assistant_text))
                st.write(assistant_text)
                
            except Exception as e:
                st.session_state["render_messages"].pop()  
                st.session_state["lc_messages"].pop()   
                handle_api_error(e)

# clear button
if st.session_state["render_messages"]:
    if st.button("Clear chat"):
        st.session_state["render_messages"].clear()
        st.session_state["lc_messages"].clear()
        st.rerun()