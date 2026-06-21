# GenHealth AI - Longevity Optimizer 🧬

GenHealth AI is a specialized Streamlit web application designed for functional longevity medicine, clinical epidemiology, and functional genomics. By cross-referencing ancestral heritage, geographic environment, and personalized quantitative biomarkers, the tool interfaces with Azure OpenAI (`gpt-4o`) to generate clinical-grade preventive health assessments and actionable daily intervention roadmaps.

---

## 🚀 Features

* **Multi-Tab Profile Builder:** Separates inputs cleanly into **Ancestral & Biological Profiles** and **Longevity KPIs & Lifestyle Pillars**.
* **Ancestral Mismatch Engine:** Integrates ethnic cohort risks (e.g., South Asian, African Diaspora, East Asian) with current environmental geolocations.
* **Automated Biomarker Assessment:** Real-time processing of key longevity metrics including BMI, Blood Pressure, HbA1c, VO2 Max, and Resting Heart Rate.
* **Dynamic Report Engine:** Instantly parses structured LLM text responses and compiles them into a downloadable, cleanly formatted clinical PDF using `fpdf`.
* **Robust Global Guardrails:** Built-in persistent medical disclaimers on both the UI sidebar and the generated PDF report.

---

## 🛠️ Tech Stack & Dependencies

* **Frontend UI:** [Streamlit](https://streamlit.io/)
* **AI Orchestration:** [Azure OpenAI SDK](https://github.com/openai/openai-python)
* **Document Generation:** [FPDF2](https://github.com/py-pdf/fpdf2)
* **Environment Management:** [python-dotenv](https://github.com/theofidry/django-dotenv)

---

## 📋 Requirements

Before launching the app, ensure you have the required TrueType Unicode fonts in your root directory to support extended typography, or the app will gracefully fall back to the default Helvetica layout rendering.

### Dependencies
Create a `requirements.txt` file containing:
```text
streamlit
openai
python-dotenv
fpdf2
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
```bash
   git clone [https://github.com/your-username/genhealth-ai.git](https://github.com/your-username/genhealth-ai.git)
   cd genhealth-ai
   ```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory of the project and populate it with your specific Azure OpenAI deployment keys:
```env
   AZURE_OPENAI_API_KEY="your-azure-api-key-here"
   AZURE_OPENAI_ENDPOINT="[https://your-resource-name.openai.azure.com/](https://your-resource-name.openai.azure.com/)"
   AZURE_GPT4O_DEPLOYMENT="your-gpt4o-deployment-name"
   ```

4. **Add Optional Fonts (Highly Recommended):**
   To prevent formatting warnings or styling fallbacks when rendering PDFs, place the following font files in your project root:
   * `dejavu-sans.book.ttf`
   * `dejavu-sans.bold.ttf`

---

## 🖥️ Running the Application

Launch the Streamlit service via your command line interface:

```bash
streamlit run app.py
```

Once running, navigate to the local URL provided in your terminal (typically `http://localhost:8501`).

---

## 🔒 Security & Data Architecture

* **Cached Client Instances:** The Azure OpenAI client connection is isolated inside a `@st.cache_resource` wrapper to prevent connection leaks across user re-runs.
* **State Preservation:** Results are committed to Streamlit's `session_state` cache mechanism (`st.session_state.ai_output`), preventing loss of generated text data when adjusting secondary configuration layouts or downloading reports.
* **Zero Persistent Storage:** Data input fields remain running completely inside local server volatile memory parameters—ensuring underlying biometric attributes are never written to disk or database surfaces without explicit consent.
