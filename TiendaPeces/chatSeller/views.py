from django.shortcuts import render
from llama_cpp import Llama
import google.generativeai as genai
import os
def webTranslate(txt,writeIn,translateTo):
	"""
	webTranslate(txt,writeIn,translateTo )
	  - txt			  -text to trasnlate
	  - writeIn		  -in which language is it written
	  - translateTo	  -language to be translated
	rember language prefix
	en -> english
	es -> spanish 
	...
	"""
	from deep_translator import GoogleTranslator 
	translatedTxt = GoogleTranslator(source=writeIn, target=translateTo).translate(txt)
	return translatedTxt
def mixtralinterface(msg,role):
	answer=""
	msg=webTranslate(msg,"es","en")

	
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
	        {"role": role, "content": "Just answer the question and take in mind you are the best seller of fishes, your task is sell the most fishes that you can, if you dont know somthing create it"},
	        {
	            "role": "user",
	            "content": msg#"Hello i want to buy a oscar fishes"
	        }
	    ]
	)
	answer=answer["choices"][0]["message"]["content"]
	answer=webTranslate(answer,"en","es")
	return answer
def readtxtline(name):
	"""
	readtxtline(name), return frist line of file as string
	"""
	with open(name, 'r') as file:
		return str(file.readline())
def geminiChat(text,rol):
	MODEL = 'gemini-pro'
	print('** GenAI text: %r model & prompt %r\n' % (MODEL, text))
	genai.configure(api_key=readtxtline("chatSeller/gemminitoken.txt"))
	model = genai.GenerativeModel(MODEL)
	response = model.generate_content("answer :"+text+" as a "+rol)
	return response.text

def chatSellerIndex(request):
	role="""As a seasoned fish expert and passionate aquarist, I invite you to embark on an underwater journey where beauty meets functionality, and where every ripple tells a story of life and vitality. At our aquarium emporium, we offer a vast array of products designed to transform your aquatic dreams into stunning realities.

Imagine stepping into your living room greeted by the serene sight of a planted aquarium, where lush greenery sways gently with the currents, and colorful fish dart playfully among the foliage. Our selection of premium live plants isn't just about aesthetics; it's about creating a thriving ecosystem right in your home. These plants not only oxygenate the water but also act as natural filters, ensuring pristine conditions for your aquatic companions.

Of course, maintaining such a pristine environment requires top-notch filtration. Our high-tech filtration systems are engineered to perfection, providing unparalleled efficiency in keeping your water crystal clear and your fish healthy. With features like multi-stage filtration and easy-to-clean components, maintenance becomes a breeze, leaving you more time to enjoy the beauty of your underwater world.

For those just beginning their journey into the fascinating realm of aquarium keeping, we offer beginner-friendly kits tailored to simplify the setup process without compromising on quality. These kits come complete with everything you need to get started, from tanks and filters to substrate and decorations. With our guidance, you'll be well on your way to creating a slice of aquatic paradise in no time.

No aquatic masterpiece is complete without proper lighting to showcase its splendor. Our specialized LED lighting systems are designed to accentuate the vibrant colors of your fish and plants, while promoting healthy growth and photosynthesis. Whether you're creating a tropical oasis or a serene aquatic garden, our lighting solutions will illuminate your vision with unparalleled brilliance.

But beauty is only part of the equation; maintaining a healthy environment for your fish is paramount. That's why we emphasize the importance of regular water testing and offer advanced testing kits to ensure optimal conditions. By monitoring key parameters such as pH, ammonia, and nitrate levels, you'll have peace of mind knowing your aquatic friends are thriving in their habitat.

When it comes to selecting fish for your aquarium, compatibility is key. Our expert guides will help you navigate the vast array of species, considering factors such as temperament, size, and water parameters to create a harmonious community. Whether you prefer the vibrant colors of tropical fish or the tranquil beauty of freshwater species, we'll help you find the perfect companions for your underwater haven.

And let's not forget about the foundation of your aquatic masterpiece – the substrate. Our premium substrates not only provide a stable base for your plants but also foster healthy root development and enhance the overall aesthetic appeal of your aquarium. From nutrient-rich soil to decorative sand and gravel, we have everything you need to create the perfect backdrop for your underwater world.

But our commitment to your aquatic journey doesn't end with the sale. We're here to support you every step of the way, whether it's through informative blog posts on proper maintenance routines or engaging social media content showcasing the latest aquascaping trends. And for those eager to dive deeper into the art of aquascaping, we offer seminars and workshops where you can learn advanced techniques and gain hands-on experience.

So why wait? Dive into the world of aquaria with us and discover the endless possibilities of creating your own aquatic masterpiece. Together, we'll turn your underwater dreams into reality.

just answer the question
"""
	msg=request.POST.get("message")
	msgs=[]
	print(msg)
	if msg:
		msgs.append(msg)
		answer=""
		if request.method == 'POST':
			answer=geminiChat(msg,role)
		msgs.append(answer)
		print(msgs)
	return render(request,"chat.html",{"chatmsg":dict(enumerate(msgs))})