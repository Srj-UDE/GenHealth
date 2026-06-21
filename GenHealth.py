import streamlit as st
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from fpdf import FPDF
import re
from datetime import datetime  # Added for timestamp generation

# Load variables from .env file
load_dotenv()

# 1. Page Configuration & Styling
st.set_page_config(
    page_title="GenHealth AI - Longevity Optimizer",
    page_icon="🧬",
    layout="wide"
)

st.header("🧬 GenHealth AI", divider="rainbow")
st.markdown("##### Ancestral data. Modern optimization.")
st.markdown("---")

# --- GLOBAL SIDEBAR MEDICAL DISCLAIMER ---
with st.sidebar:
    st.markdown("### ⚠️ Medical Disclaimer")
    st.warning(
        "This report is for informational purposes only and is not medical advice, diagnosis, or treatment. Consult a qualified healthcare professional regarding any health concerns or before making medical decisions."
    )
    st.markdown("---")
    st.caption("v0.7.3 | Latest updated: June 21, 2026")

# 2. Optimized & Cached Azure OpenAI Client Factory
@st.cache_resource
def get_azure_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-06-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

client = get_azure_client()
DEPLOYMENT_NAME = os.getenv("AZURE_GPT4O_DEPLOYMENT")

# 3. PDF Writer Function with Name, Ancestral & Biomarker Data
def create_pdf_bytes(markdown_text, profile_data, user_name=""):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)

    # Register TrueType Unicode font files.
    try:
        pdf.add_font("DejaVu", style="", fname="dejavu-sans.book.ttf")
        pdf.add_font("DejaVu", style="B", fname="dejavu-sans.bold.ttf")
        font_family = "DejaVu"
    except Exception:
        # Fallback to standard core fonts if DejaVu TTF files are missing
        font_family = "Helvetica"

    pdf.add_page()

    def write_multicell(text, height=6):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            w=pdf.epw,
            h=height,
            text=text
        )

    # --- HEADER BLOCKS ---
    pdf.set_font(font_family, "B", 16)
    write_multicell("GENHEALTH AI - BIOMARKER ANALYSIS", 10)
    pdf.ln(1)
    
    # Render Current Generation Date
    current_date = datetime.now().strftime("%B %d, %Y")
    pdf.set_font(font_family, "", 10)
    write_multicell(f"DATE: {current_date.upper()}", 4)
    pdf.ln(2)
    
    # Conditionally display the user's name if provided
    if user_name.strip():
        pdf.set_font(font_family, "B", 12)
        write_multicell(f"PREPARED FOR: {user_name.strip().upper()}", 8)
        pdf.ln(1)
    
    pdf.set_font(font_family, "B", 11)
    write_multicell("PATIENT BASELINE PROFILE & BIOMARKERS", 8)
    pdf.ln(2)
    
    # --- Profile metadata key-value printing via consecutive sequential text writes ---
    for key, value in profile_data.items():
        pdf.set_x(pdf.l_margin)
        pdf.set_font(font_family, "B", 10)
        pdf.write(h=6, txt=f"{key}: ")
        pdf.set_font(font_family, "", 10)
        pdf.write(h=6, txt=f"{value}\n")
    
    pdf.ln(4)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
    pdf.ln(4)

    # Clean text of complex markdown anomalies and unmappable dashes
    safe_text = markdown_text
    safe_text = safe_text.replace("–", "-").replace("—", "-")
    
    lines = safe_text.splitlines()

    for raw_line in lines:
        line = raw_line.rstrip()

        # Empty line
        if not line.strip():
            pdf.ln(3)
            continue

        # Horizontal rule
        if line.strip() in {"---", "***"}:
            y = pdf.get_y()
            pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
            pdf.ln(4)
            continue

        # Main Section Headers (1., 2., 3.) matching markdown "# " or "## "
        if line.startswith("# ") or line.startswith("## "):
            header_text = line.lstrip("# ").strip().replace("**", "")
            pdf.set_font(font_family, "B", 14)
            pdf.ln(2)
            write_multicell(header_text, 8)
            pdf.ln(2)
            continue

        # Sub-headers (###)
        if line.startswith("### "):
            sub_text = line[4:].replace("**", "").strip()
            pdf.set_font(font_family, "B", 11)
            write_multicell(sub_text, 7)
            pdf.ln(1)
            continue

        # Check if line acts as a bold structural inline title like "**Title**" or "**Title:**"
        is_inline_bold_title = line.strip().startswith("**") and ("**" in line.strip()[2:])
        
        # Clean out all double asterisks from regular text streams entirely
        clean_line_text = line.replace("**", "").replace("*", "").strip()

        # Bullet points rendering
        if line.strip().startswith("- ") or line.strip().startswith("* ") or line.strip().startswith("• "):
            pdf.set_font(font_family, "", 10)
            bullet_body = re.sub(r"^[-*•]\s*", "", line).replace("**", "").replace("*", "").strip()
            write_multicell(f"• {bullet_body}", 6)
            continue

        # Dynamic font sizing weight assignment based on structural context flag
        if is_inline_bold_title and len(clean_line_text) < 60:
            pdf.set_font(font_family, "B", 10)
            write_multicell(clean_line_text, 6)
        else:
            pdf.set_font(font_family, "", 10)
            write_multicell(clean_line_text, 6)

    # --- APPENDED PDF MEDICAL DISCLAIMER ---
    pdf.ln(8)
    y = pdf.get_y()
    pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y) # Separator line
    pdf.ln(4)
    
    pdf.set_font(font_family, "B", 8)
    write_multicell("CLINICAL DISCLAIMER:", 6)
    pdf.set_font(font_family, "", 8)
    disclaimer_text = (
        "This analysis is for educational and longevity optimization tracking purposes only. It does not constitute medical advice, diagnosis, or treatment. Always consult your healthcare provider before making changes to your medication, diet, or lifestyle."
    )
    write_multicell(disclaimer_text, 4)

    pdf_output = pdf.output()
    return bytes(pdf_output) if isinstance(pdf_output, (bytearray, bytes)) else pdf_output



# 4. Data Entry Organized via Layout Tabs
tab1, tab2 = st.tabs(["🧬 1. Ancestral & Biological Profile", "📊 2. Longevity KPIs & Lifestyle Baseline"])

with tab1:
    st.markdown("### 📈 Ancestral & Baseline KPIs")
    
    # Optional Name Input text field
    user_name = st.text_input("User / Patient Full Name", value="")
    
    col1, col2 = st.columns(2)
    with col1:
        ancestry = st.selectbox(
            "Select Regional/ Ancestry Profile:",
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
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Biological Sex", ["Male", "Female", "Intersex"])
        weight = st.number_input("Weight (kg)", value=72)
        height = st.number_input("Height (cm)", value=175)
        calculated_bmi = round(weight / ((height/100) ** 2), 1)
        st.info(f"Calculated Baseline BMI: **{calculated_bmi}**")

with tab2:
    st.markdown("### 📈 Biomarkers & Quantitative KPIs")
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    
    with kpi_col1:
        bp_sys = st.number_input("Systolic Blood Pressure (mmHg)", min_value=50, max_value=250, value=None)
        bp_dia = st.number_input("Diastolic Blood Pressure (mmHg)", min_value=30, max_value=150, value=None)
        hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=20.0, value=None, step=0.1, help="Blood sugar control marker over past 3 months")
        
    with kpi_col2:
        vo2_max = st.number_input("VO2 Max (mL/kg/min)", min_value=10, max_value=90, value=None, help="Cardiorespiratory fitness level marker")
        rhr = st.number_input("Resting Heart Rate (BPM)", min_value=30, max_value=200, value=None)
    
    with kpi_col3:
        sleep_hours = st.slider("Average Nightly Sleep (Hours)", 4.0, 12.0, 7.5, step=0.5)
        social_ties = st.select_slider("Social Connection Quality", options=["Isolated", "Moderate/Average", "Strong Supportive Circle"], value="Moderate/Average")

    st.markdown("### 🍎 Qualitative Lifestyle Pillars")
    life_col1, life_col2, life_col3 = st.columns(3)
    
    with life_col1:
        diet_type = st.selectbox("Current Dietary Pattern", ["Mediterranean/Whole Foods", "Standard Western (Processed/High-Carb)", "Plant-Based", "Traditional Ancestral"])
    with life_col2:
        alcohol = st.selectbox("Weekly Alcohol Intake", ["None/Rarely", "Moderate (1-2 drinks/day)", "High (>2 drinks/day)"])
    with life_col3:
        smoking = st.checkbox("Active Smoker (or history of heavy smoking)", value=False)


# 5. Trigger Analysis & Session Management Engine
st.markdown("---")

if "ai_output" not in st.session_state:
    st.session_state.ai_output = None

if st.button("🚀 Run Comprehensive Bio-Environmental Longevity Analysis", type="primary"):
    if not os.getenv("AZURE_OPENAI_API_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"):
        st.error("⚠️ System environment keys are missing. Configure your deployment credentials to enable AI processing.")
    else:
        with st.spinner("Analyzing Ancestry and Biomarker data..."):
            try:
                system_prompt = (
                    "You are a principal physician in Longevity Medicine, Clinical Epidemiology, and Functional Genomics. "
                    "Your core task is to calculate risk scores and clinical insights by cross-referencing the user's data "
                    "against verified, peer-reviewed medical literature and landmark ethnic cohort studies.\n\n"
                    "CRITICAL GROUNDING RULES:\n"
                    "1. Base all calculations and observations strictly on validated clinical benchmarks.\n"
                    "2. Evaluate intersections dynamically. Do not treat metrics independently.\n"
                    "3. If specific lab biomarkers are omitted, use peer-reviewed demographic data to estimate evolutionary mismatch scores.\n"
                    "4. Absolute Restriction: Do not use vague wellness buzzwords. Use Markdown formatting headers (##, ###) cleanly."
                )
                
                name_context = f"Patient Name: {user_name}\n" if user_name.strip() else ""
                
                user_content = f"""
                CRITICAL CLINICAL DOSSIER FOR ANALYSIS:
                {name_context}
                🧬 ANCESTRAL ARCHITECTURE:
                - Ethnic Heritage: {ancestry}
                - Geolocation Context: {current_location}
                - Stated Core Goal: {health_goal}
                - Demographics: {age}yo | {gender}
                
                📈 CLINICAL HEALTH KPIs:
                - Calculated BMI: {calculated_bmi}
                - Blood Pressure: {bp_sys}/{bp_dia} mmHg
                - HbA1c Level: {hba1c}%
                - VO2 Max capacity: {vo2_max} mL/kg/min
                - Resting Heart Rate: {rhr} BPM
                - Sleep Allocation: {sleep_hours} hours/night
                - Social Connection Index: {social_ties}
                
                🍏 LIFESTYLE BEHAVIORAL PATTERNS:
                - Diet Quality: {diet_type}
                - Smoking Status: {'Smoker' if smoking else 'Non-Smoker'}
                - Alcohol Intake: {alcohol}
                
                EXECUTE CRITICAL EVALUATION OUTPUT IN THREE SECTIONS using standard Markdown (## and ###):
            
                ## 1. THE ANCESTRAL INTERSECTION
                ## 2. BIOMARKER GAPS & LONGEVITY LEAKS
                ## 3. TOP 3 HYPER-TARGETED DAILY ACTIONS
                """
                
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.2
                )
                
                st.session_state.ai_output = response.choices[0].message.content
                
            except Exception as e:
                st.error(f"Failed to process request through Azure OpenAI instance pipeline: {e}")

# Rendering output and generating PDF download if data exists
if st.session_state.ai_output:
    st.success("Your Ancestry & Biomarker analysis is complete! ✅")
    st.markdown(st.session_state.ai_output)
    
    st.markdown("---")
    st.markdown("### 🖨️ Export Analysis Report")
    
    # Pack up structured summary for the PDF profile section
    blood_pressure_string = f"{bp_sys}/{bp_dia} mmHg" if (bp_sys and bp_dia) else "Not Provided"
    profile_summary = {
        "Ancestral Profile": ancestry,
        "Current Residence": current_location,
        "Primary Health Goal": health_goal,
        "Demographics": f"{age} Years Old | {gender}",
        "Calculated BMI": f"{calculated_bmi} kg/m²",
        "Blood Pressure Status": blood_pressure_string,
        "HbA1c Level": f"{hba1c}%" if hba1c else "Not Provided",
        "VO2 Max Level": f"{vo2_max} mL/kg/min" if vo2_max else "Not Provided",
        "Resting Heart Rate": f"{rhr} BPM" if rhr else "Not Provided",
        "Dietary Pattern Type": diet_type,
        "Tobacco Smoking Status": "Active Smoker" if smoking else "Non-Smoker"
    }
    
    # Generate bytes directly passing the markdown string, metadata parameters dictionary, and username input 
    pdf_bytes = create_pdf_bytes(st.session_state.ai_output, profile_summary, user_name=user_name)
    
    st.download_button(
        label="📥 Download Analysis Report (PDF)",
        data=pdf_bytes,
        file_name="GenHealth_AI_Longevity_Report.pdf",
        mime="application/pdf"
    )