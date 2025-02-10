import os
import vertexai
import requests
import json
from flask import Flask, render_template, request
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Set the correct service account JSON file
GOOGLE_CLOUD_CREDENTIALS = r"E:\Reputation Management\peak-stream-key.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CLOUD_CREDENTIALS

# ✅ Force correct region and initialize Vertex AI
PROJECT_ID = "peak-stream-449519-r4"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)  # ✅ Ensure correct region

# ✅ Initialize Gemini AI Model
gemini_model = GenerativeModel("gemini-pro")

# ✅ Initialize Flask app
app = Flask(__name__)
app.debug = True  

# ✅ Function to perform Google Custom Search with filtering
def google_search(query):
    print(f"🔍 Searching Google for: {query}")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv('API_KEY'),
        "cx": os.getenv('SEARCH_ENGINE_ID'),
        "q": query,
        "num": 5  
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()

        # ✅ Filtering: Remove job postings, ads, and irrelevant content
        filtered_results = []
        blocked_keywords = ["hiring", "careers", "jobs", "apply", "recruitment", "salary", "discount", "offer", "buy", "sale"]

        for item in search_results.get("items", []):
            title = item.get("title", "").lower()
            snippet = item.get("snippet", "").lower()
            link = item.get("link", "")

            if any(keyword in title or keyword in snippet for keyword in blocked_keywords):
                continue  

            filtered_results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": link
            })

        return filtered_results

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during API request: {e}")
        return []

# ✅ Function to generate a company reputation summary using Gemini AI
# ✅ Function to generate a company reputation summary using Gemini AI
def generate_summary(search_results, company_name):
    try:
        if not search_results:
            return "⚠️ No relevant search results found to generate a summary."

        # 🔹 Format search results
        search_summary = "\n".join([
            f"{item['title']} - {item['snippet']} ({item['link']})"
            for item in search_results
        ])

        # 🔹 AI Prompt for a Clean and Well-Formatted Summary
        prompt = f"""
        Generate a **concise and professional** reputation summary for **{company_name}**, based on the latest search results.

        ### **Instructions:**
        - **Write in three clear paragraphs**, covering:
          1️⃣ **Positive Aspects**  
          2️⃣ **Negative Aspects**  
          3️⃣ **Overall Impression**  
        - **DO NOT use bullet points, lists, stars (`*`), or unnecessary symbols**.
        - **Use complete sentences** and ensure **smooth paragraph transitions**.
        - **Keep it structured, neutral, and easy to read**.
        - **Ensure the text follows a justified format**.

        ### **Example Format:**
        ---
        ## {company_name} Reputation Summary  

        {company_name} is a well-established company known for [key strengths]. Customers appreciate its [positive aspects], making it a preferred choice for [products/services]. Its commitment to [strengths] has helped it gain a strong market presence.  

        Despite its success, some concerns have been raised regarding [negative aspects], including [specific issues]. Customers have reported challenges related to [criticism], which has led to discussions about potential improvements. Addressing these concerns could help enhance its overall reputation.  

        Overall, {company_name} remains a reputable brand in [industry]. While there are areas for improvement, it continues to offer [valuable aspects] and serves as a trusted choice for [target audience].  
        ---

        Now, generate the summary in this **clean and justified format**.
        """

        print("🔍 Sending refined prompt to Gemini AI...")
        response = gemini_model.generate_content(prompt)

        # ✅ Extract AI-generated text with proper formatting
        if response and hasattr(response, 'text'):
            return response.text.strip()  # ✅ Ensure clean output
        else:
            return "⚠️ AI service did not return a valid response."

    except Exception as e:
        print(f"❌ Error with Gemini AI: {e}")
        return "⚠️ AI service encountered an error while generating the summary."

# ✅ Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    company_name = request.form['company_name']
    if not company_name:
        return render_template('index.html', error="Please enter a company name.")

    search_results = google_search(company_name)
    summary_text = generate_summary(search_results, company_name)

    return render_template('summary.html', company=company_name, summary=summary_text)

if __name__ == '__main__':
    app.run(debug=True)
