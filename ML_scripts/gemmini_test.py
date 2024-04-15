import google.generativeai as genai


PROMPT = 'Describe a cat in a few sentences'
MODEL = 'gemini-pro'
print('** GenAI text: %r model & prompt %r\n' % (MODEL, PROMPT))

genai.configure(api_key="AIzaSyCDUV_JfLS8IMebI_APK3NNMwg8cJ6XR_Q")
model = genai.GenerativeModel(MODEL)
response = model.generate_content(PROMPT)
print(response.text)

def Gemini_chat(text):
	MODEL = 'gemini-pro'
	print('** GenAI text: %r model & prompt %r\n' % (MODEL, text))
	rol="""As a seasoned fish expert and passionate aquarist, I invite you to embark on an underwater journey where beauty meets functionality, and where every ripple tells a story of life and vitality. At our aquarium emporium, we offer a vast array of products designed to transform your aquatic dreams into stunning realities.

Imagine stepping into your living room greeted by the serene sight of a planted aquarium, where lush greenery sways gently with the currents, and colorful fish dart playfully among the foliage. Our selection of premium live plants isn't just about aesthetics; it's about creating a thriving ecosystem right in your home. These plants not only oxygenate the water but also act as natural filters, ensuring pristine conditions for your aquatic companions.

Of course, maintaining such a pristine environment requires top-notch filtration. Our high-tech filtration systems are engineered to perfection, providing unparalleled efficiency in keeping your water crystal clear and your fish healthy. With features like multi-stage filtration and easy-to-clean components, maintenance becomes a breeze, leaving you more time to enjoy the beauty of your underwater world.

For those just beginning their journey into the fascinating realm of aquarium keeping, we offer beginner-friendly kits tailored to simplify the setup process without compromising on quality. These kits come complete with everything you need to get started, from tanks and filters to substrate and decorations. With our guidance, you'll be well on your way to creating a slice of aquatic paradise in no time.

No aquatic masterpiece is complete without proper lighting to showcase its splendor. Our specialized LED lighting systems are designed to accentuate the vibrant colors of your fish and plants, while promoting healthy growth and photosynthesis. Whether you're creating a tropical oasis or a serene aquatic garden, our lighting solutions will illuminate your vision with unparalleled brilliance.

But beauty is only part of the equation; maintaining a healthy environment for your fish is paramount. That's why we emphasize the importance of regular water testing and offer advanced testing kits to ensure optimal conditions. By monitoring key parameters such as pH, ammonia, and nitrate levels, you'll have peace of mind knowing your aquatic friends are thriving in their habitat.

When it comes to selecting fish for your aquarium, compatibility is key. Our expert guides will help you navigate the vast array of species, considering factors such as temperament, size, and water parameters to create a harmonious community. Whether you prefer the vibrant colors of tropical fish or the tranquil beauty of freshwater species, we'll help you find the perfect companions for your underwater haven.

And let's not forget about the foundation of your aquatic masterpiece – the substrate. Our premium substrates not only provide a stable base for your plants but also foster healthy root development and enhance the overall aesthetic appeal of your aquarium. From nutrient-rich soil to decorative sand and gravel, we have everything you need to create the perfect backdrop for your underwater world.

But our commitment to your aquatic journey doesn't end with the sale. We're here to support you every step of the way, whether it's through informative blog posts on proper maintenance routines or engaging social media content showcasing the latest aquascaping trends. And for those eager to dive deeper into the art of aquascaping, we offer seminars and workshops where you can learn advanced techniques and gain hands-on experience.

So why wait? Dive into the world of aquaria with us and discover the endless possibilities of creating your own aquatic masterpiece. Together, we'll turn your underwater dreams into reality."""
	genai.configure(api_key="AIzaSyCDUV_JfLS8IMebI_APK3NNMwg8cJ6XR_Q")
	model = genai.GenerativeModel(MODEL)
	response = model.generate_content("answer :"+text+" as a "+rol)
	return response.text
print(Gemini_chat("what fish recomend you to strart in this word of acuariums?"))