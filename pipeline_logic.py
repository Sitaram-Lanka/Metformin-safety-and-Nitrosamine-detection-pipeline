
import pandas as pd
import numpy as np

ADI_MCG_PER_DAY = 0.096

def load_data(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["ndma_mcg_mid"] = (df["ndma_mcg_min"] + df["ndma_mcg_max"]) / 2.0
    df["detected"] = (df["ndma_mcg_max"] > 0).astype(int)
    df["formulation_ER"] = (df["formulation"] == "ER").astype(int)
    return df

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    X = pd.DataFrame({
        "formulation_ER": df["formulation_ER"],
        "dose_g": df["dose_mg"] / 1000.0,
    })
    return X
