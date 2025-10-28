from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow frontend JS to communicate with backend

# ---------------------------
# 1️⃣ Load Crop Data
# ---------------------------
try:
    crop_data = pd.read_csv("data/crop_production_data.csv")
    print("✅ Crop data loaded successfully!")
except FileNotFoundError:
    crop_data = pd.DataFrame()
    print("⚠️ crop_production_data.csv not found in /data folder")

# ---------------------------
# 2️⃣ Load Rainfall Data
# ---------------------------
try:
    rainfall_data = pd.read_csv("data/Sub_Division_IMD_2017.csv")
    print("✅ Rainfall data loaded successfully!")
except FileNotFoundError:
    rainfall_data = pd.DataFrame()
    print("⚠️ Rainfall dataset not found in /data folder")

# ---------------------------
# 3️⃣ Home Page
# ---------------------------
@app.route('/')
def home():
    return render_template('index.html')

# ---------------------------
# 4️⃣ Fetch Data (for testing)
# ---------------------------
@app.route('/fetch-data')
def fetch_data():
    if crop_data.empty:
        return jsonify({"message": "❌ Crop data not loaded"}), 404
    return jsonify({
        "message": "✅ Data fetched successfully!",
        "rows": len(crop_data),
        "columns": list(crop_data.columns)
    })

# ---------------------------
# 5️⃣ Main Q&A Route
# ---------------------------
@app.route('/ask', methods=['POST'])
def ask():
    print("✅ /ask endpoint triggered!")  # Debug message
    user_input = request.json.get('question', '').lower()

    if crop_data.empty:
        return jsonify({"answer": "⚠️ Crop data not loaded yet."})

    # --- Question 1: Top crops ---
    if "top crops" in user_input or "most produced" in user_input:
        result = crop_data.groupby('crop')['production_'].sum().nlargest(5)
        return jsonify({
            "answer": "🌾 Top 5 crops by total production:",
            "data": result.to_dict(),
            "source": "📊 Data source: District-wise, season-wise crop production statistics (data.gov.in)"
        })

    # --- Question 2: Compare state-wise production ---
    elif "compare" in user_input or "states" in user_input:
        result = crop_data.groupby('state_name')['production_'].sum().nlargest(5)
        return jsonify({
            "answer": "🏙️ Top 5 states by total crop production:",
            "data": result.to_dict(),
            "source": "📊 Data source: District-wise, season-wise crop production statistics (data.gov.in)"
        })

    # --- Question 3: Rainfall-related queries ---
    elif "rainfall" in user_input and not ("correlate" in user_input or "crop" in user_input):
        if rainfall_data.empty:
            return jsonify({
                "answer": "⚠️ Rainfall dataset not loaded. Please ensure the IMD CSV is available in /data folder."
            })

        top_rain = rainfall_data.groupby('SUBDIVISION')['ANNUAL'].mean().nlargest(5)
        return jsonify({
            "answer": "🌧️ Top 5 regions in India with highest average annual rainfall:",
            "data": top_rain.to_dict(),
            "source": "📊 Data source: India Meteorological Department (data.gov.in)"
        })

    # --- Question 4: Crop production trend ---
    elif "trend" in user_input or "year" in user_input:
        avg_yearly = crop_data.groupby('crop_year')['production_'].sum().tail(10)
        return jsonify({
            "answer": "📈 Crop production trend over the last 10 years (sample data):",
            "data": avg_yearly.to_dict(),
            "source": "📊 Data source: District-wise, season-wise crop production statistics (data.gov.in)"
        })

    # --- Question 5: Correlate rainfall and crop production ---
    elif "correlate" in user_input or ("rainfall" in user_input and "crop" in user_input):
        if rainfall_data.empty:
            return jsonify({
                "answer": "⚠️ Rainfall dataset not loaded. Cannot perform correlation."
            })

        # ---- Prepare Crop Data ----
        crop_trend = crop_data[['crop_year', 'production_']].copy()
        crop_trend = crop_trend.groupby('crop_year')['production_'].sum().reset_index()
        crop_trend.rename(columns={'crop_year': 'YEAR'}, inplace=True)
        crop_trend['YEAR'] = pd.to_numeric(crop_trend['YEAR'], errors='coerce')

        # ---- Prepare Rainfall Data ----
        rain_trend = rainfall_data[['YEAR', 'ANNUAL']].copy()
        rain_trend['YEAR'] = pd.to_numeric(rain_trend['YEAR'], errors='coerce')
        rain_trend['ANNUAL'] = pd.to_numeric(rain_trend['ANNUAL'], errors='coerce')
        rain_trend = rain_trend.groupby('YEAR')['ANNUAL'].mean().reset_index()

        # ---- Merge and Correlate ----
        merged = pd.merge(crop_trend, rain_trend, on='YEAR', how='inner').dropna()

        if len(merged) > 1:
            corr = merged['production_'].corr(merged['ANNUAL'])
            corr_text = f"{corr:.2f}"
        else:
            corr_text = "Insufficient overlapping years for correlation"

        return jsonify({
            "answer": f"📊 Correlation between rainfall and total crop production (yearly): {corr_text}",
            "data": merged.tail(10).to_dict(orient='records'),
            "source": [
                "Crop Data: District-wise crop production (data.gov.in)",
                "Rainfall Data: IMD Rainfall Dataset (data.gov.in)"
            ]
        })

    # --- Default fallback ---
    else:
        return jsonify({
            "answer": "❓ Sorry, I couldn’t understand that. Try asking about *top crops*, *state comparison*, *rainfall trends*, or *crop-rainfall correlation*."
        })

# ---------------------------
# 6️⃣ Run Flask App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
