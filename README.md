# 🥗 NutriGen: Gemini-AI Powered Nutrition Science

NutriGen is a web-based application designed to democratize access to advanced nutritional science using Google's Gemini AI.

## 🚀 Features (MVP)
1. **Quick Nutri-Check:** Instant breakdown of macros and micros from any text-based food input.
2. **Vision Scan:** Upload images of your meals for AI-powered identification and nutritional analysis.
3. **AI Meal Planner:** Personalized 1-day meal plans based on your profile and goals.
4. **Virtual Coach:** Interactive chat for all your nutrition-related queries.

**@LIVE-DEMO:** [NutriGen-Streamlit-App](https://nutrigen-gemini.streamlit.app/)

## 🛠️ Local Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Setup:**
   - Obtain a Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
   - Open the `.env` file and replace `your_gemini_api_key_here` with your actual key.
   - Alternatively, you can enter the key directly in the app's sidebar.

3. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## 🌐 Deployment (Streamlit Cloud)

1. **Push to GitHub:** Ensure your code is pushed to a public or private GitHub repository.
2. **Connect to Streamlit Cloud:**
   - Log in to [Streamlit Cloud](https://share.streamlit.io/).
   - Click "New app" and select your repository, branch, and `app.py`.
3. **Configure Secrets:**
   - Go to the app settings in Streamlit Cloud.
   - Navigate to **"Secrets"**.
   - Add your API key in the following TOML format:
     ```toml
     GOOGLE_API_KEY = "your_actual_gemini_api_key"
     ```
4. **Deploy:** Click "Deploy" and your app will be live!

## 🏗️ Tech Stack
- **Frontend:** Streamlit
- **AI Backend:** Google Gemini 2.0 Flash
- **Language:** Python
- **Styling:** Custom CSS for a premium dark-mode experience.
"# NutriGen-Gemini-AI-Powered-Nutrition-Science" 
