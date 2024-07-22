from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Stablecoin(db.Model):
    __tablename__ = "stablecoin"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False)
    entity = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=True)
    supply = db.Column(db.Float, nullable=False)
    circulating = db.Column(db.Float, nullable=True)
    chain = db.Column(db.String(20), nullable=False)
    pegged_against = db.Column(db.String(20), nullable=False)
    info = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'entity': self.entity,
            'token': self.token,
            "price": self.price,
            "supply": self.supply,
            "circulating": self.circulating,
            "chain": self.chain,
            "pegged_against": self.pegged_against,
            "info": self.info,
            'timestamp': self.timestamp.isoformat(),
            'humanized_timestamp': getattr(self, 'humanized_timestamp', None),
        }

    def __repr__(self) -> str:
        return f"Stablecoin (id={self.id!r}, entity={self.entity!r}, token={self.token!r}, chain={self.chain!r})"
