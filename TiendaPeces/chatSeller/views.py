from django.shortcuts import render
from llama_cpp import Llama
import os

# Create your views here.
def chatSellerIndex(request):
	print(os.getcwd())
	answer=""
	msg=request.POST.get("message")
	print(msg)

	if request.method == 'POST':
		print(msg)
		
		llm = Llama(
		  model_path="../models/mixtral-8x7b-v0.1.Q6_K.gguf", 
		  n_ctx=2048, 
		  n_threads=24,        
		  n_gpu_layers=35         # The number of layers to offload to GPU, if you have GPU acceleration available
		)
		output = llm(
		  "{prompt}", # Prompt
		  max_tokens=512,  # Generate up to 512 tokens
		  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
		  echo=True        # Whether to echo the prompt
		)


		llm = Llama(model_path="../models/mixtral-8x7b-v0.1.Q6_K.gguf", chat_format="llama-2")  # Set chat_format according to the model you are using
		answer=llm.create_chat_completion(
		    messages = [
		        {"role": "system", "content": "Just answer the question and take in mind you are the best seller of fishes, your task is sell the most fishes that you can, if you dont know somthing create it"},
		        {
		            "role": "user",
		            "content": msg#"Hello i want to buy a oscar fishes"
		        }
		    ]
		)
		answer=answer["choices"][0]["message"]["content"]

		print(answer)
	return render(request,"chat.html",{"chatmsg":answer})