from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'
    session_id = db.Column(db.Integer, primary_key=True)
    src_ip = db.Column(db.String(45))
    dst_ip = db.Column(db.String(45))
    src_port = db.Column(db.Integer)
    dst_port = db.Column(db.Integer)
    protocol = db.Column(db.String(10))
    packet_count = db.Column(db.Integer)
    byte_count = db.Column(db.BigInteger)
    duration = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Anomaly(db.Model):
    __tablename__ = 'anomalies'
    anomaly_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.session_id'))
    score = db.Column(db.Float)
    is_anomaly = db.Column(db.Boolean)
    detected_at = db.Column(db.DateTime, server_default=db.func.now())
