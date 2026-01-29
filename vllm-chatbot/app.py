import streamlit as st
from chatbot import ConversationalChatbot
import time


st.set_page_config(
    page_title="vLLM Chatbot with Memory",
    page_icon="🤖",
    layout="wide"
)


if "chatbot" not in st.session_state:
    # Create placeholder for loading status
    loading_placeholder = st.empty()
    
    with loading_placeholder.container():
        st.info("🚀 Initializing chatbot...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate loading stages with progress updates
        status_text.text("📦 Downloading model files...")
        progress_bar.progress(20)
        
        # Actually load the model
        try:
            status_text.text("🔧 Loading model into memory...")
            progress_bar.progress(40)
            
            st.session_state.chatbot = ConversationalChatbot()
            
            progress_bar.progress(80)
            status_text.text("✅ Model loaded successfully!")
            progress_bar.progress(100)
            time.sleep(0.5)  # Brief pause to show completion
            
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            st.stop()
    
    # Clear loading UI
    loading_placeholder.empty()
    st.session_state.messages = []
    st.success("✅ Chatbot ready! Start chatting below.")
    time.sleep(1)
    st.rerun()

with st.sidebar:
    st.title("⚙️ Settings")
    
    # Show model info
    if "chatbot" in st.session_state:
        st.info(f"📌 Model: {st.session_state.chatbot.model_name.split('/')[-1]}")
    
    st.divider()
    
    mode = st.selectbox(
        "Chat Mode",
        ["assistant", "coding", "creative", "technical"],
        help="Choose the chatbot's specialty mode"
    )
    if st.button("Apply Mode"):
        st.session_state.chatbot.set_mode(mode)
        st.success(f"Switched to {mode} mode!")
    
    st.divider()
    
    st.subheader("Generation Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1,
                           help="Higher = more creative")
    top_p = st.slider("Top-p", 0.0, 1.0, 0.9, 0.05,
                     help="Nucleus sampling threshold")
    max_tokens = st.slider("Max Tokens", 50, 2048, 512, 50,
                          help="Maximum response length")
    
    st.divider()
    
    # Conversation stats
    if st.session_state.messages:
        st.metric("Messages", len(st.session_state.messages))
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chatbot.clear_history()
        st.session_state.messages = []
        st.rerun()


st.title("🤖 Interactive Chatbot with Memory")
st.caption("Powered by vLLM • Context-aware conversations")


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.chatbot.chat(
                prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
