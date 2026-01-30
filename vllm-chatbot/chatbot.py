from vllm import LLM, SamplingParams
import gc
import torch
from typing import List, Dict

class ConversationalChatbot:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" ):
        self.history: List[Dict] = []
        self.system_instruction: str = "You are a helpful and professional assistant"
        self.model_name = model_name
        self.llm = self.load_model()
    
    def load_model(self, progress_callback=None):
        """Load vLLM model with progress tracking"""
        print(f"Loading model {self.model_name}...")
        
        if progress_callback:
            progress_callback(40, "Initializing vLLM engine...")
        
        llm = LLM(
        model=self.model_name,
        max_model_len=2048,
        gpu_memory_utilization=0.75,  # Changed from 0.9 to 0.75
        enforce_eager=True,
        trust_remote_code=True
    )
        
        if progress_callback:
            progress_callback(100, "Model ready!")
        
        print("Model loaded successfully!")
        return llm

    
    def set_mode(self, mode: str):
        "Swtich between Modes"
        modes = {
                "assistant: You are a helpful and professional assistant",
                "coding: You are an expert coding assistant, please provide clear, well commented code with explanations"
                "creative: You are a creative writing assistant. Write engaging and imaginative content"
                "technical: You are a technical documentation expert. Provide clear, precise technical explanations."  
                }
        self.system_instruction = modes.get(mode, modes["assistant"])
        print(f"Switched to {mode} mode")

    def construct_prompt(self, user_input: str) -> List[Dict]:
        # Build Conversation with history
        recent_history = self.history[-8:]
        conversation = [{"role": "system", "content": self.system_instruction}
                        ] + recent_history + [
                        {"role": "user", "content": user_input}]
        return conversation

    def generate_response(self, conversation: List[Dict], temperature: float = 0.7, top_p: float = 0.9, max_tokens: int = 512) -> str:
        # Generate Response using vLLM via chat API
        sampling_params = SamplingParams (
                            temperature= temperature,
                            top_p= top_p,
                            max_tokens= max_tokens)
        
        outputs = self.llm.chat(conversation, sampling_params)
        reply = outputs[0].outputs[0].text
        return reply

    def chat(self, user_input: str, **kwargs) -> str:
        # Main Chat Method       
        conversation = self.construct_prompt(user_input)
        bot_response = self.generate_response(conversation, **kwargs)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": bot_response})

        return bot_response
    
    def clear_history(self):
        # Reset conversation history
        self.history = []
        print("Conversation history cleared")
        
