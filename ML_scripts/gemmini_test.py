import google.generativeai as genai


PROMPT = 'Describe a cat in a few sentences'
MODEL = 'gemini-pro'
print('** GenAI text: %r model & prompt %r\n' % (MODEL, PROMPT))

genai.configure(api_key="")
model = genai.GenerativeModel(MODEL)
response = model.generate_content(PROMPT)
print(response.text)
