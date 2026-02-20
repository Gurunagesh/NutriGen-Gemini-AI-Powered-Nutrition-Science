import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd
import json
import PIL.Image

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="NutriGen - Gemini AI Nutritionist",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #0e1117 100%);
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px 20px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #b0b0b0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50 !important;
        color: white !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
    }
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# sidebar for API Key
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Try to get key from secrets or environment
    default_key = os.getenv("GOOGLE_API_KEY", "")
    if "GOOGLE_API_KEY" in st.secrets:
        default_key = st.secrets["GOOGLE_API_KEY"]
        
    api_key = st.text_input("Gemini API Key", value=default_key, type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
    else:
        st.warning("Please enter your Gemini API Key in the sidebar or configure it in secrets to proceed.")
    
    st.divider()
    st.markdown("### About NutriGen")
    st.info("NutriGen leverages Gemini 2.0 to provide advanced nutritional insights and meal planning.")

# Initialization of Model
model = genai.GenerativeModel('gemini-2.0-flash')

# Helper functions
def get_nutritional_info(food_query):
    prompt = f"""
    Act as a professional Clinical Nutritionist. Analyze the following food item/meal: "{food_query}".
    Provide a detailed breakdown of:
    1. Calories
    2. Macronutrients (Protein, Carbs, Fats)
    3. Essential Micronutrients (Vitamins/Minerals)
    4. Health Verdict (Benefits or potential concerns)
    
    Format the response in a structured, easy-to-read markdown style. Include a table for macros.
    """
    response = model.generate_content(prompt)
    return response.text

def generate_meal_plan(profile, duration="1 Day"):
    prompt = f"""
    Act as a highly experienced Dietitian. Create a personalized {duration} meal plan based on:
    - Age/Gender: {profile['age_gender']}
    - Objective: {profile['goal']}
    - Dietary Restrictions: {profile['restrictions']}
    - Activity Level: {profile['activity']}
    
    If duration is "7 Days", provide a table for the week summarizing Breakfast, Lunch, Dinner, and Snacks.
    Crucially, after the plan, provide a "CONSOLIDATED GROCERY LIST" for all the ingredients needed for the entire week.
    
    Return the response in clear Markdown. Use tables for the meal plan where appropriate.
    """
    response = model.generate_content(prompt)
    return response.text

def analyze_image_nutrition(image_data):
    prompt = """
    Act as a professional Clinical Nutritionist and Vision Expert. 
    Analyze the uploaded image of food. 
    1. Identify all food items in the image.
    2. Estimate the portion sizes.
    3. Provide a detailed breakdown of Calories, Protein, Carbs, and Fats.
    4. Provide a Health Verdict.
    
    Format the response in a structured markdown style with a table for macros.
    """
    response = model.generate_content([prompt, image_data])
    return response.text

# Main App UI
st.title("🥗 NutriGen: Advancing Nutrition Science")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🔍 Quick Nutri-Check", "📸 Vision Scan", "📅 Meal Planner", "💬 Virtual Coach"])

with tab1:
    st.header("Quick Nutritional Insights")
    food_input = st.text_input("Enter a food item or a whole meal (e.g., '2 boiled eggs and a bowl of oatmeal')", placeholder="What did you eat? #Enter a food item or a whole meal (e.g., '2 boiled eggs and a bowl of oatmeal')")
    
    if st.button("Analyze Nutrition"):
        if food_input:
            with st.spinner("Analyzing with AI..."):
                try:
                    result = get_nutritional_info(food_input)
                    st.markdown(f'<div class="card">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Please enter some text.")

with tab2:
    st.header("Visual Nutritional Analysis")
    st.markdown("Upload a photo of your meal to get instant AI-powered nutritional insights.")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = PIL.Image.open(uploaded_file)
        st.image(image, caption='Uploaded Meal', use_container_width=True)
        
        if st.button("Identify & Analyze Meal"):
            with st.spinner("AI is examining your plate..."):
                try:
                    result = analyze_image_nutrition(image)
                    st.markdown(f'<div class="card">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")

with tab3:
    st.header("Personalized Meal Planner")
    col1, col2 = st.columns(2)
    
    with col1:
        age_gender = st.text_input("my label for key argument",placeholder="Age & Gender (e.g., 28y Male)")
        goal = st.selectbox("Objective", ["Weight Loss", "Muscle Gain", "Maintenance", "Better Energy Levels"])
    
    with col2:
        restrictions = st.text_input("Dietary Restrictions", placeholder="e.g., Vegan, No Nuts, Low Carb")
        duration = st.radio("Plan Duration", ["1 Day", "7 Days"], horizontal=True)
        activity = st.select_slider("Activity Level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
    
    if st.button("Generate Plan"):
        profile = {
            "age_gender": age_gender,
            "goal": goal,
            "restrictions": restrictions,
            "activity": activity
        }
        with st.spinner(f"Crafting your {duration} plan..."):
            try:
                plan = generate_meal_plan(profile, duration)
                st.markdown(f'<div class="card">{plan}</div>', unsafe_allow_html=True)
                
                # Add download button for the plan
                st.download_button(
                    label="📥 Download Plan & Grocery List",
                    data=plan,
                    file_name=f"NutriGen_Plan_{duration.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Error: {e}")

with tab4:
    st.header("Virtual Nutrition Coach")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question (e.g., 'How can I get more protein as a vegan?')"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Provide context for the coach
                    system_prompt = "You are a friendly and expert Virtual Nutrition Coach. Answer the user's question concisely using scientific nutrition principles."
                    full_prompt = f"{system_prompt}\n\nUser Question: {prompt}"
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
