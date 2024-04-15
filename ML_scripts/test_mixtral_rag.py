from llama_cpp import Llama

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = Llama(
  model_path="./mixtral-8x7b-v0.1.Q6_K.gguf",  # Download the model file first
  n_ctx=2048,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=24,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=35         # The number of layers to offload to GPU, if you have GPU acceleration available
)

# Simple inference example
output = llm(
  "{prompt}", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=True        # Whether to echo the prompt
)

# Chat Completion API

llm = Llama(model_path="./mixtral-8x7b-v0.1.Q6_K.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
p=llm.create_chat_completion(
    messages = [
        {"role": "system", "content": "You are the best seller of fishes, your task is sell the most fishes that you can, if you dont know somthing create it"},
        {
            "role": "user",
            "content": "Hello i want to buy a oscar fishe"
        }
    ]
)
print(p["choices"][0])#["content"])
