# 🧠 Reputation Management for Job Seekers

This project helps job seekers evaluate a company’s reputation by generating structured, AI-based summaries using real reviews from trusted platforms (like Glassdoor, Reddit, LinkedIn, etc.). It extracts public insights related to salary, work culture, career growth, and more.

---

## 🚀 Features

- 🔍 **Google Custom Search API** to fetch company reviews from top sites.
- 🤖 **Gemini-Pro (Google Vertex AI)** model to generate JSON-based company summaries.
- 🌐 **Flask Web App** for user interaction and dynamic summary display.
- 📊 Outputs structured summaries including:
  - 💰 Salary & Compensation  
  - 🏢 Work Culture & Environment  
  - ⚖️ Work-Life Balance  
  - 📈 Career Growth & Promotions  
  - 🎁 Employee Benefits  

---

## 🧩 Technologies & Tools Used

| Tool/Library             | Purpose                                     |
|--------------------------|---------------------------------------------|
| Flask                    | Backend web server                          |
| Vertex AI (Gemini-Pro)   | Generative AI model for summaries           |
| Google Custom Search API | Fetch reviews from top review platforms     |
| Python (requests, dotenv)| API calls and environment configuration     |
| HTML/Jinja Templates     | Render search form and summary on frontend  |

---

## 🏗️ Project Structure

```
.
├── main.py                 # Flask backend logic & Gemini integration
├── templates/
│   ├── index.html          # Input form UI
│   └── summary.html        # Output summary display
├── ai_response.txt         # Logs raw AI output (for debugging)
├── filtered_results.txt    # Filtered search result links
├── raw.json                # Full search result JSON
├── .env                    # API keys and credentials (excluded in Git)
├── .gitignore              # Excludes sensitive files
└── requirements.txt        # All Python dependencies
```

---

## 🛠️ How It Works (Simplified)

1. **User Input**: The user enters a company name (e.g., "Amazon").
2. **Search**: Google Custom Search pulls links from trusted sites like Glassdoor, Reddit, LinkedIn, etc.
3. **AI Summary**: Vertex AI’s Gemini model processes those and generates a **structured JSON summary**.
4. **Display**: Flask renders the company insights neatly on the website.

---

## 🧪 Steps to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Poornesh-31/Reputation-Management.git
cd Reputation-Management
```

### 2. Set Up Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add .env File

Create a `.env` file and add your credentials:

```ini
API_KEY = "your_google_api_key"
SEARCH_ENGINE_ID = "your_search_engine_id"
PROJECT_ID = "your_google_cloud_project_id"
LOCATION = "us-central1"
GOOGLE_CLOUD_CREDENTIALS = "path_to_your_service_account_json"
```

Place your service account JSON file (e.g., `peak-stream-key.json`) in the project directory but do not upload it to GitHub.

### 5. Run the Flask App

```bash
python main.py
```

Then open your browser and visit:  
👉 `http://127.0.0.1:5000/`

---

## ✅ Example Output (AI Generated for IBM)

💰 **Salary & Compensation**  
- Software Engineer: ₹8–15 LPA  
- Data Scientist: ₹12–25 LPA  
- Bonuses: Stock options + annual incentives  
- Satisfaction: Fair but mixed sentiment about pay

🏢 **Work Culture & Environment**  
- Fast-paced, collaborative, innovation-driven  
- Leaders are approachable and visionary  
- Strong emphasis on diversity & inclusion  

⚖️ **Work-Life Balance**  
- Avg. 40 hrs/week with flexibility  
- Hybrid model common  
- Moderate stress during peak deadlines  

📈 **Career Growth & Promotions**  
- Promotions every 2–3 years  
- Access to mentorship, learning platforms  
- Good job security  

🎁 **Employee Benefits**  
- Health insurance + dental/vision  
- Paid leaves, parental benefits  
- Free meals, gym membership, and travel insurance  

---

## 🔐 Security Note

Do not upload `.env` or `peak-stream-key.json` to public repositories.  
These contain sensitive credentials and must remain local.  
Use `.gitignore` to prevent accidental commits of secrets.

---

## 📬 Feedback or Contributions?

Feel free to fork the repo, raise issues, or suggest improvements.  
Let’s help job seekers make informed decisions with AI-driven company insights!

---

## 📌 Author

**Poornesh**  
🔗 [GitHub Profile](https://github.com/Poornesh-31)

