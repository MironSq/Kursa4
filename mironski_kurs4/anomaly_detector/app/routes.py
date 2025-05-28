import os
import yaml
from flask import Flask, request, render_template, jsonify
from anomaly_detector.app.models import db, Session, Anomaly

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
cfg = yaml.safe_load(open(os.path.join(BASE_DIR, 'config', 'config.yaml')))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{cfg['db']['user']}:{cfg['db']['password']}@"
    f"{cfg['db']['host']}:{cfg['db']['port']}/{cfg['db']['database']}"
)
db.init_app(app)

@app.before_request
def init_db():
    db.create_all()

# теперь принимаем и GET, и POST
@app.route('/train', methods=['GET','POST'])
def train():
    from anomaly_detector.ml.train_model import train_model
    train_model()
    return jsonify({'status': 'model trained'})

@app.route('/detect', methods=['GET','POST'])
def detect_route():
    from anomaly_detector.ml.predict import detect
    # очищаем старые записи и заносим новые
    db.session.query(Anomaly).delete()
    sessions = Session.query.all()
    for r in detect(sessions):
        db.session.add(Anomaly(
            session_id=r['session_id'],
            score=r['score'],
            is_anomaly=r['is_anomaly']
        ))
    db.session.commit()
    return jsonify({'status':'detection done'})

@app.route('/data')
def data():
    sessions = Session.query.order_by(Session.created_at.desc()).limit(50).all()
    anomalies = {a.session_id: a for a in Anomaly.query.all()}
    normal, anom = [], []
    for s in sessions:
        rec = {
            'session_id': s.session_id,
            'packet_count': s.packet_count,
            'byte_count': s.byte_count,
            'duration': s.duration,
            'time': s.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        if s.session_id in anomalies and anomalies[s.session_id].is_anomaly:
            rec['score'] = float(anomalies[s.session_id].score)
            anom.append(rec)
        else:
            normal.append(rec)
    return jsonify({'anomalies':anom, 'normal':normal})

@app.route('/')
def index():
    return render_template('index.html')
