from app import db
from datetime import datetime

class TokenData(db.Model):
    __tablename__ = "token_data"

    id = db.Column(db.Integer, primary_key=True)

    token = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=True)
    price_source = db.Column(db.String(100), nullable=True)

    tot_supply = db.Column(db.Float, nullable=True)
    circ_supply = db.Column(db.Float, nullable=True)

    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'token': self.token,
            'price': self.price,
            'price_source': self.price_source,
            'tot_supply': self.tot_supply,
            'circ_supply': self.circ_supply,
            'timestamp': self.timestamp.isoformat(),
        }

    def __repr__(self) -> str:
        return f"TokenData (id={self.id!r}, token={self.token!r}, price={self.price!r}"
