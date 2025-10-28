
🌾 Project Samarth: Intelligent Q&A System for Agriculture Insights

📖 Overview
Project Samarth is an intelligent Q&A system designed to analyze and correlate agricultural production data with climate (rainfall) patterns using official government open datasets.
It enables policymakers and researchers to derive data-backed insights directly from data.gov.in resources, combining datasets from the Ministry of Agriculture & Farmers Welfare and the India Meteorological Department (IMD).

🧠 Core Idea
The project demonstrates how open government datasets can be integrated, cleaned, and queried through an AI-inspired interface to answer natural language questions like:
- What are the top 5 crops produced in India?
- Compare rainfall and crop yield trends across states.
- Show production trends of rice over the last decade.
- Which regions have the highest rainfall and how does that affect crop output?

⚙️ Tech Stack
Frontend: HTML, CSS, JavaScript (Fetch API)
Backend: Python Flask
Data: Pandas, CSV datasets from data.gov.in
APIs: data.gov.in REST API for live datasets
Deployment: Localhost (Flask server)

🧩 System Workflow
Frontend (index.html)
↓ (POST request via Fetch API)
Flask Backend (app_flask.py)
↓
Crop Production Dataset + Rainfall Dataset
↓
Response (Aggregated, Filtered & Summarized)
↓
Displayed on Web UI

🗂️ Dataset Sources
- Crop Data: District-wise, Season-wise Crop Production Statistics (data.gov.in)
- Rainfall Data: IMD - Monthly Rainfall Dataset (data.gov.in)
- APIs Used: Live government APIs via data.gov.in

🚀 Features
✅ Interactive web interface for Q&A
✅ Integration of agricultural and rainfall data
✅ Automatic summarization and visualization-ready responses
✅ API-driven and extendable architecture
✅ Supports traceability — cites dataset sources for every insight

💻 How to Run Locally

1️⃣ Clone the Repository
git clone https://github.com/Kunalgola7503/Project_Samarth.git
cd Project_Samarth

2️⃣ Install Dependencies
python -m pip install -r requirements.txt

3️⃣ Run the Flask Server
python app_flask.py

4️⃣ Open in Browser
Navigate to: http://127.0.0.1:5000/

🧱 Folder Structure
Project_Samarth/
│
├── data/
│   ├── crop_production_data.csv
│   └── Sub_Division_IMD_2017.csv
│
├── templates/
│   └── index.html
│
├── app_flask.py
├── app.py
├── requirements.txt
└── README.md

💡 Sample Questions to Try
- Top crops in India
- Compare crop production across states
- Rainfall trends in India
- Correlate rainfall and crop production in India
- Show crop production trend over last 10 years

🧠 Architecture Highlights
- Flask backend serves an intelligent API endpoint /ask that parses natural language questions.
- Frontend sends user queries through fetch() (AJAX-style requests).
- The system dynamically aggregates and filters data using Pandas.
- Answers are formatted in structured JSON and displayed neatly on the webpage.

🛡️ Core Values
- Accuracy & Traceability: Every data point is sourced from verified government datasets.
- Transparency: Source APIs clearly cited in results.
- Extensibility: Ready to integrate future IMD APIs for deeper weather–agriculture insights.

📊 Example Output
Query: “Top crops in India”
Response:
Crop       Production (tons)
Rice       1200000
Wheat      980000
Sugarcane  850000
Cotton     720000
Maize      600000
Source: District-wise Crop Production Data (data.gov.in)

🧩 Future Scope
- Integration of live rainfall APIs from IMD.
- Support for state-wise visualization dashboards.
- AI-powered natural language understanding for complex policy questions.
- Deployment on Streamlit Cloud / Heroku for public access.

🏁 Conclusion
Project Samarth demonstrates how open government data can be transformed into an intelligent, interactive system for real-time decision support in agriculture. It bridges the gap between raw data and actionable insight.
"Open data empowers innovation — Project Samarth brings intelligence to it."

