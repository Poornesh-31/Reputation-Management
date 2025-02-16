import os
import vertexai
import requests
import json
from flask import Flask, render_template, request
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv
import re

# ✅ Load environment variables
load_dotenv()

# ✅ Initialize Vertex AI
PROJECT_ID = "peak-stream-449519-r4"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# ✅ Initialize Gemini AI Model
gemini_model = GenerativeModel("gemini-pro")

# ✅ Initialize Flask app
app = Flask(__name__)
app.debug = True  

# ✅ Google Custom Search with filtering
def google_search(company_name):
<<<<<<< Updated upstream
    query = f"{company_name} employee reviews salary work culture career growth work-life balance"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": os.getenv('API_KEY'), "cx": os.getenv('SEARCH_ENGINE_ID'), "q": query, "num": 5}
    response = requests.get(url, params=params)
    response.raise_for_status()
    search_results = response.json()
    
    allowed_sources = ["linkedin.com", "glassdoor.com", "reddit.com", "quora.com"]
    return [
        {"title": item.get("title"), "snippet": item.get("snippet"), "link": item.get("link")}
        for item in search_results.get("items", [])
        if any(source in item.get("link", "") for source in allowed_sources)
    ]

=======
    query = f"{company_name} employee reviews salary work culture career growth work-life balance site:linkedin.com OR site:glassdoor.com OR site:indeed.com OR site:bloomberg.com OR site:quora.com OR site:reddit.com"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": os.getenv('API_KEY'),
        "cx": os.getenv('SEARCH_ENGINE_ID'),
        "q": query,
        "num": 7
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Filter for only relevant websites and remove job postings
    allowed_sources = ["linkedin.com", "glassdoor.com", "indeed.com", "bloomberg.com", "quora.com", "reddit.com"]
    filtered_results = [
        {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        }
        for item in search_results.get("items", [])
        if any(source in item.get("link", "") for source in allowed_sources)
        and not re.search(r'job|hiring|apply', item.get("title", "").lower())
    ]

    return filtered_results

>>>>>>> Stashed changes
# ✅ AI Summary with improved prompt and JSON parsing
def generate_summary(search_results, company_name):
    prompt = f"""
        Provide a structured JSON summary for '{company_name}' focusing on job-seeker insights. 
        The JSON should include the following keys with real, company-specific insights:
        {{
            "{company_name} Summary": {{
                "Salary & Compensation": "Average salary ranges and bonuses.",
                "Work Culture & Environment": "Overview of company culture.",
                "Work-Life Balance": "Insights into flexibility and work hours.",
                "Career Growth & Promotions": "Opportunities for growth.",
                "Employee Benefits": "Key perks and benefits."
            }}
        }}
        Only return the JSON object without extra text or explanations.
    """

    response = gemini_model.generate_content(prompt)

    # ✅ Print entire response for debugging
    print("AI Full Response:", response.text)

    # ✅ Try extracting JSON using regex
    match = re.search(r'\{.*\}', response.text.strip(), re.DOTALL)

    if match:
        try:
            # ✅ Print matched JSON for debugging
            print("Matched JSON String:", match.group(0))
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return {"error": "Failed to parse AI response."}
    else:
        print("No JSON response detected.")
        return {"error": "No JSON response from AI."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    company_name = request.form['company_name']
    search_results = google_search(company_name)
    summary_data = generate_summary(search_results, company_name)

    if "error" in summary_data:
        return render_template('index.html', error=summary_data["error"])

    return render_template('summary.html',
                           company=company_name,
                           summary=summary_data.get(f"{company_name} Summary", {}),
                           search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)