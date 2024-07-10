from app import db
from datetime import datetime



class MoneyMarketRate(db.Model):
    __tablename__ = "money_market_rate"

    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(50), nullable=False)
    collateral = db.Column(db.String(50), nullable=True)  # New column

    liquidity_rate = db.Column(db.Float, nullable=False)
    borrow_rate = db.Column(db.Float, nullable=False)
    chain = db.Column(db.String(20), nullable=False)
    tvl = db.Column(db.Float, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'protocol': self.protocol,
            'token': self.token,
            'liquidity_rate': self.liquidity_rate,
            'collateral': self.collateral,
            'borrow_rate': self.borrow_rate,
            'tvl': self.tvl,
            'chain': self.chain,
            'timestamp': self.timestamp.isoformat(),  # Convert datetime to string
            'tvl_formatted': getattr(self, 'tvl_formatted', None),
            'liquidity_rate_formatted': getattr(self, 'liquidity_rate_formatted', None),
            'humanized_timestamp': getattr(self, 'humanized_timestamp', None)
        }

def __repr__(self) -> str:
        return f"Protocol (id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
