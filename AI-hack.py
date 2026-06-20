import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# 1. Page Configuration & Custom Styling
st.set_page_config(
    page_title="GenHealth AI - UN SDG 3 Tracker",
    page_icon="🧬",
    layout="wide"
)

st.header("🧬 GenHealth AI", divider= "rainbow")
st.caption("Bringing Genetic Health to Modern Environments")
st.markdown("---")

# 2. Optimized & Cached Azure OpenAI Client Factory
@st.cache_resource
def get_azure_client():
    # Gracefully falls back to empty strings if environment variables aren't set yet
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    return AzureOpenAI(
        api_key=api_key,
        api_version="2024-06-01",
        azure_endpoint=endpoint
    )

# Instantiate the global optimized client
client = get_azure_client()

# Deployment/Model Name (Change this to your specific deployment name on Azure portal)
DEPLOYMENT_NAME = os.getenv("AZURE_GPT4O_DEPLOYMENT")

# 3. Main Split Interface Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 User Ancestral Profile")
    ancestry = st.selectbox(
        "Select Regional/Genetic Ancestry Profile:",
        [
            "South Asian (Indian subcontinent)", 
            "African Diaspora / West African", 
            "East Asian (Japanese, Chinese, Korean)", 
            "Hispanic / Latino (Central/Mesoamerican)", 
            "Northern European (Fair skin/Celtic)"
        ]
    )
    current_location = st.text_input("Current Residence City & Country", value="Frankfurt, Germany")
    health_goal = st.selectbox("Primary Preventive Goal", ["Metabolic/Diabetes Prevention", "Cardiovascular Protection", "General Longevity"])

with col2:
    st.subheader("📊 Current Baseline Metrics")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Biological Sex", ["Male", "Female", "Intersex"])
    
    bmi_calc_col1, bmi_calc_col2 = st.columns(2)
    with bmi_calc_col1:
        weight = st.number_input("Weight (kg)", value=72)
    with bmi_calc_col2:
        height = st.number_input("Height (cm)", value=175)
    
    # Calculate BMI locally to include in the context
    calculated_bmi = round(weight / ((height/100) ** 2), 1)
    st.info(f"Calculated Baseline BMI: **{calculated_bmi}**")

# 4. Trigger Analysis & Backend Processing Pipeline
st.markdown("---")
if st.button("🚀 Run Bio-Environmental Optimization Analysis", type="primary"):
    
    # Validation check to ensure variables exist before hitting the Azure endpoint
    if not os.getenv("AZURE_OPENAI_API_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"):
        st.error("⚠️ Environment variables 'AZURE_OPENAI_API_KEY' or 'AZURE_OPENAI_ENDPOINT' are missing! Please set them in your terminal environment before running.")
    else:
        with st.spinner("AI analyzing Evolutionary Knowledge Graph Database..."):
            try:
                # Structural medical system prompt to restrict hallucinations
                system_prompt = (
                    "You are the clinical data engine of a health platform focusing on evolutionary mismatch biology and "
                    "nutrigenomics. Evaluate genetic/ethnic vulnerabilities against geographic and environmental shifts. "
                    "Provide clear, peer-reviewed, yet highly actionable lifestyle recommendations."
                )
                
                user_content = f"""
                Analyze the following user profile:
                - Ancestry: {ancestry}
                - Current Location: {current_location}
                - Primary Goal: {health_goal}
                - Age/Sex: {age} year old {gender}
                - Calculated BMI: {calculated_bmi}
                
                Generate an optimization profile with TWO strict components:
                1. GENETIC MISMATCH ANALYSIS: What specific verified biological trait/vulnerability is at risk given their environment? Mention key marker guidelines (e.g., MASALA study for South Asians, APOL1 for African diaspora, PNPLA3 for Hispanic, SLCO1B1 for East Asian, Fitzpatrick skin types).
                2. SPECIFIC RECOMMENDATIONS: Ancestry-driven micro targets.
                """
                
                # Fetch Response via the globally cached client object
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.3
                )
                
                ai_output = response.choices[0].message.content
                
                # Render results side-by-side with universal baselines
                result_col1, result_col2 = st.columns([3, 2])
                
                with result_col1:
                    st.success("🎯 Hyper-Personalized Ancestral Adaptations")
                    st.markdown(ai_output)
                    
                with result_col2:
                    st.warning("📋 Universal Health Baselines (Essential Foundations)")
                    st.markdown("""
                    While your ancestral biology requires specific adjustments, do not overlook the fundamental baselines below:
                    
                    * **Physical Activity (Anti-Sedentary):** Aim for a minimum of 150 minutes of moderate aerobic activity weekly. Break up sitting blocks every 45 minutes with a 3-minute walking break.
                      
                    * **Sleep Hygiene Optimization:** Target 7-9 hours of continuous sleep. Maintain a cool ambient room temperature (~18°C) and completely cut out blue light screens 60 minutes before bed.
                      
                    * **Hydration Core Metrics:** Excluding caffeinated drinks, prioritize consuming roughly 35 mL of water per kg of lean body weight daily.
                      
                    * **Stress Management:** Incorporate 10 minutes of box breathing or down-regulation work daily to regulate cortisol spikes which harm metabolic processing.
                    """)
                    
                    st.markdown("---")
                    st.info(
                        "💡 **UN SDG 3 Compliance Metric:** Note how the left column shifts radically depending on "
                        "ancestry inputs to offset geographic anomalies, whereas the right column tracks uniform "
                        "behavior control targets."
                    )
                    
            except Exception as e:
                st.error(f"Failed to pull recommendations from Azure OpenAI backend pipeline: {e}")