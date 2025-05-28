import os
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import yaml

# грузим конфиг
cfg = yaml.safe_load(open('config/config.yaml'))

def train_model():
    # читаем признаки
    df = pd.read_csv('data/processed/features.csv')
    # оставляем только числовые поля
    X = df[['packet_count','byte_count','duration']]
    # обучаем IsolationForest
    model = IsolationForest(contamination=0.01, random_state=42)
    model.fit(X)
    # создаём директорию модели, если нужно
    path = cfg['model']['path']
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")
