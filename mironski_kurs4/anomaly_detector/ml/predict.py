import os
import yaml
import joblib

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
cfg  = yaml.safe_load(open(os.path.join(BASE, 'config', 'config.yaml')))

def detect(sessions):
    # загружаем модель
    model = joblib.load(cfg['model']['path'])
    # собираем числовые признаки
    X = [[s.packet_count, s.byte_count, s.duration] for s in sessions]
    scores = model.decision_function(X)
    preds  = model.predict(X)
    return [
      {'session_id': s.session_id, 'score':float(score), 'is_anomaly':(p==-1)}
      for s, score, p in zip(sessions, scores, preds)
    ]
