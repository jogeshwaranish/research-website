import google.generativeai as genai

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a outline for a cold email to a professor which is broad")
print(response.text)