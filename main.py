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

# ✅ Function to perform Google Custom Search with filtering
def google_search(company_name):
    print(f"🔍 Searching Google for: {company_name} job seeker insights")

    query = f"{company_name} employee reviews salary work culture career growth work-life balance"
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

        # ✅ Filtering out irrelevant content
        filtered_results = []
        allowed_sources = ["linkedin.com", "glassdoor.com", "reddit.com", "quora.com"]
        
        for item in search_results.get("items", []):
            link = item.get("link", "")
            if any(source in link for source in allowed_sources):  # ✅ Keep only relevant sources
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
def generate_summary(search_results, company_name):
    try:
        if not search_results:
            return {"error": "No relevant search results found to generate a summary."}

        # 🔹 Improved JSON-Formatted Prompt
        prompt = f"""
        Summarize the following search results about "{company_name}" strictly in **JSON format**.  
        - The summary must be **job seeker-focused**, covering:
          1. Salary & Compensation  
          2. Work Culture & Environment  
          3. Work-Life Balance  
          4. Career Growth & Promotions  
          5. Employee Benefits  

        - Use **concise bullet points (each under 30 words).**
        - Extract the **best image URL** if available.
        - **Do not add extra text before or after JSON.**
        
        ### **Expected JSON Format:**
        {{
            "summary": {{
                "Salary & Compensation": [
                    "Entry-level salaries start at $XX,XXX with annual bonuses.",
                    "Performance-based salary hikes every 2 years."
                ],
                "Work Culture & Environment": [
                    "Fast-paced and innovation-driven environment.",
                    "Encourages teamwork and leadership training."
                ],
                "Work-Life Balance": [
                    "Flexible work-from-home options available.",
                    "Paid time off and wellness programs."
                ],
                "Career Growth & Promotions": [
                    "Internal promotions based on performance.",
                    "Strong mentorship and leadership programs."
                ],
                "Employee Benefits": [
                    "Comprehensive health, dental, and vision coverage.",
                    "401(k) retirement plans and stock options."
                ]
            }},
            "image_url": "<Best available image URL, or empty string if not found>"
        }}

        ### **Search Results Data:**
        {json.dumps(search_results, indent=2)}
        """

        print("🔍 Sending JSON prompt to Gemini AI...")
        response = gemini_model.generate_content(prompt)
        if response and hasattr(response, 'text'):
            json_text = response.text.strip()

            # 🔹 Extract JSON data using regex
            match = re.search(r'\{.*\}', json_text, re.DOTALL)
            if match:
                json_data = match.group(0)

                # ✅ Parse JSON properly
                try:
                    parsed_data = json.loads(json_data)
                    return parsed_data  # ✅ Return structured JSON
                except json.JSONDecodeError as e:
                    print(f"❌ JSON Parsing Error: {e}")
                    return {"error": "Failed to parse AI response."}
            else:
                return {"error": "AI response is not in JSON format."}

        else:
            return {"error": "AI service did not return a valid response."}

    except Exception as e:
        print(f"❌ Error with Gemini AI: {e}")
        return {"error": "AI service encountered an error while generating the summary."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    company_name = request.form['company_name']
    if not company_name:
        return render_template('index.html', error="Please enter a company name.")

    search_results = google_search(company_name)
    summary_data = generate_summary(search_results, company_name)

    # ✅ Handle JSON response properly
    if "error" in summary_data:
        return render_template('index.html', error=summary_data["error"])

    return render_template(
        'summary.html',
        company=company_name,
        summary=summary_data["summary"],
        image_url=summary_data.get("image_url", ""),
        search_results=search_results
    )

if __name__ == '__main__':
    app.run(debug=True)
