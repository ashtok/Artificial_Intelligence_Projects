# vLLM Conversational Chatbot with Memory

A context-aware AI chatbot built with vLLM and Streamlit, demonstrating efficient LLM inference and conversation management.

## Features
- **Context Memory**: Maintains conversation history across multiple turns
- **Multiple Modes**: Assistant, Coding, Creative Writer, Technical Expert
- **Configurable Parameters**: Adjustable temperature, top-p, max tokens
- **High-Performance Inference**: Powered by vLLM
- **Real-time Metrics**: Message counter and conversation stats

## Tech Stack
- **vLLM**: Efficient LLM inference engine
- **Streamlit**: Interactive web interface
- **PyTorch**: Deep learning framework
- **uv**: Fast Python package manager
- **Model**: TinyLlama-1.1B-Chat

## Setup
```bash
# Install dependencies
uv add vllm streamlit torch

# Run the chatbot
uv run streamlit run app.py
