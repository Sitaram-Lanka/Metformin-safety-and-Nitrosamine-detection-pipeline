
import streamlit as st
import joblib
import pandas as pd
from pipeline_logic import build_features, ADI_MCG_PER_DAY

# 1. Load the Models
try:
    detection_model = joblib.load('ndma_detection_model.joblib')
    concentration_model = joblib.load('ndma_concentration_model.joblib')
except FileNotFoundError:
    st.error("Error: Model files not found. Please ensure 'ndma_detection_model.joblib' and 'ndma_concentration_model.joblib' are in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading models: {e}")
    st.stop()

st.set_page_config(layout="wide")
st.title("💊 Metformin Safety AI Dashboard")
st.markdown("### AI-Powered Risk Assessment for Nitrosamine Contaminants")

with st.sidebar:
    st.header("Input Metformin Sample Details")
    formulation = st.radio("Product Formulation", ["IR", "ER"], help="IR: Immediate Release, ER: Extended Release")
    dose = st.slider("Dose Strength (mg)", 250, 2000, 500, step=250, help="Common dose strengths for Metformin.")

if st.button("Run Safety Check"):
    st.subheader("🔬 Analysis Results")

    # Prepare input DataFrame (matching pipeline_logic's expected format)
    input_data = pd.DataFrame([{
        'formulation': formulation,
        'dose_mg': dose,
        'formulation_ER': 1 if formulation == 'ER' else 0 # Required by build_features
    }])

    # Use the build_features function from pipeline_logic.py
    X_input = build_features(input_data)

    # Predict Probability of NDMA Detection
    prob_detect = detection_model.predict_proba(X_input)[0, 1]
    st.metric(label="Probability of NDMA Detection", value=f"{prob_detect:.2%}")

    if prob_detect >= 0.5: # Threshold for considering NDMA detected
        st.warning("Potential NDMA Detected!")
        # Predict NDMA Concentration (mcg/tablet)
        predicted_mcg_per_tablet = concentration_model.predict(X_input)[0]
        predicted_mcg_per_tablet = max(0.0, predicted_mcg_per_tablet) # Ensure non-negative

        st.metric(label="Predicted NDMA (mcg/tablet)", value=f"{predicted_mcg_per_tablet:.4f}")

        # Convert to ng/day (assuming 1 tablet/day for simplicity)
        predicted_ng_per_day = predicted_mcg_per_tablet * 1000
        st.metric(label="Predicted Daily Intake (ng/day)", value=f"{predicted_ng_per_day:.1f} ng/day")

        # Check against ADI
        adi_ng_per_day = ADI_MCG_PER_DAY * 1000
        if predicted_ng_per_day > adi_ng_per_day:
            st.error(f"

⚠️ **Exceeds FDA ADI Limit!** (ADI: {adi_ng_per_day:.1f} ng/day)")
        else:
            st.info(f"

✅ Below FDA ADI Limit (ADI: {adi_ng_per_day:.1f} ng/day)")
    else:
        st.success("NDMA Detection Unlikely.")

st.markdown("--- This pipeline provides a statistical risk assessment based on regulatory data and should not substitute for laboratory testing. ---")
