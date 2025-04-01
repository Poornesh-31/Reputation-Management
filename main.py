import os
import vertexai
import json
from flask import Flask, render_template, request
from vertexai.generative_models import GenerativeModel
from dotenv import load_dotenv

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

# ✅ AI Summary with structured JSON output
def generate_summary(company_name):
    prompt = f"""
    You are an AI assistant that provides structured company reputation summaries for job seekers. 
    Generate a valid **JSON object only** with insights about {company_name} in the following format:
    
    {{
        "{company_name} Summary": {{
            "Salary & Compensation": "Brief insights into salary, bonuses, and other compensation details.",
            "Work Culture & Environment": "Brief insights about the company culture, work environment, and leadership.",
            "Work-Life Balance": "Insights into working hours, flexibility, and remote work opportunities.",
            "Career Growth & Promotions": "Overview of promotions, learning opportunities, and career growth.",
            "Employee Benefits": "Summary of perks, insurance, paid leaves, and other benefits."
        }}
    }}
    
    Do not add explanations, only return a **valid JSON object**.
    """
    
    response = gemini_model.generate_content(prompt)
    print("AI Full Response:", response.text)
    
    # Log AI response to a file
    with open("ai_response.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    
    # Extract JSON properly
    try:
        json_start = response.text.find("{")
        json_end = response.text.rfind("}")
        if json_start != -1 and json_end != -1:
            json_data = response.text[json_start: json_end + 1]
            return json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return {"error": "Failed to parse AI response."}

    return {"error": "No JSON response from AI."}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary', methods=['POST'])
def summary():
    company_name = request.form['company_name']
    summary_data = generate_summary(company_name)
    
    if "error" in summary_data:
        return render_template('index.html', error=summary_data["error"])
    
    return render_template('summary.html',
                           company=company_name,
                           summary=summary_data.get(f"{company_name} Summary", {}))

if __name__ == '__main__':
    app.run(debug=True)
