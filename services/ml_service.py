import os
import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Add root directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from utils.feature_extraction import extract_script_features, features_to_vector, FEATURE_NAMES

MODEL_DIR = Path(__file__).parent.parent / "models"
MODEL_PATH = MODEL_DIR / "ml_viral_model.pkl"
DATASET_PATH = Path(__file__).parent.parent / "data" / "datasets" / "reel_dataset.csv"

_ml_model = None
_ml_scaler = None
_ml_metrics = None

def train_ml_model(csv_path: str = None):
    global _ml_model, _ml_scaler, _ml_metrics
    
    path = Path(csv_path) if csv_path else DATASET_PATH
    if not path.exists():
        from data.generate_dataset import generate_synthetic_dataset
        generate_synthetic_dataset(output_path=str(path))
        
    df = pd.read_csv(path)
    X = df[FEATURE_NAMES].values
    y = df['viral_label'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    clf.fit(X_train_scaled, y_train)
    
    # Evaluation
    y_pred = clf.predict(X_test_scaled)
    y_prob = clf.predict_proba(X_test_scaled)[:, 1]
    
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    metrics = {
        'accuracy': round(acc * 100, 2),
        'precision': round(prec * 100, 2),
        'recall': round(rec * 100, 2),
        'f1_score': round(f1 * 100, 2),
        'confusion_matrix': cm,
        'feature_importances': dict(zip(FEATURE_NAMES, [round(float(fi), 4) for fi in clf.feature_importances_]))
    }
    
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        'model': clf,
        'scaler': scaler,
        'metrics': metrics
    }
    joblib.dump(payload, MODEL_PATH)
    
    _ml_model = clf
    _ml_scaler = scaler
    _ml_metrics = metrics
    
    print(f"ML Model trained successfully! Accuracy: {metrics['accuracy']}%")
    return metrics

def load_ml_model():
    global _ml_model, _ml_scaler, _ml_metrics
    if _ml_model is not None and _ml_scaler is not None:
        return _ml_model, _ml_scaler, _ml_metrics
        
    if not MODEL_PATH.exists():
        train_ml_model()
        return _ml_model, _ml_scaler, _ml_metrics
        
    payload = joblib.load(MODEL_PATH)
    _ml_model = payload['model']
    _ml_scaler = payload['scaler']
    _ml_metrics = payload['metrics']
    return _ml_model, _ml_scaler, _ml_metrics

def predict_ml_score(script_text: str, target_duration: int = 30) -> tuple[float, dict]:
    model, scaler, _ = load_ml_model()
    features = extract_script_features(script_text, target_duration)
    vector = features_to_vector(features)
    vector_scaled = scaler.transform(vector)
    
    # Predict continuous score probability [0.0 - 100.0]
    prob = model.predict_proba(vector_scaled)[0][1]
    raw_ml_score = round(float(prob * 100.0), 2)
    return raw_ml_score, features

def get_ml_metrics() -> dict:
    _, _, metrics = load_ml_model()
    return metrics

if __name__ == "__main__":
    train_ml_model()
