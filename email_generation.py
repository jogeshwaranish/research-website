import google.generativeai as genai

genai.configure(api_key="AIzaSyAS6fzwC7bqyKmcs24Om3jGPrgro9BUweQ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a outline for a cold email to a professor which is broad")
print(response.text)