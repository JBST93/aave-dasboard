from app import db
from datetime import datetime

class YieldRate(db.Model):
    __tablename__ = "yield_rate"

    id = db.Column(db.Integer, primary_key=True)

    market = db.Column(db.String(100), nullable=False)
    project = db.Column(db.String(100), nullable=False)

    information = db.Column(db.String(150), nullable=True)

    yield_rate_base = db.Column(db.Float, nullable=False)

    yield_rate_reward = db.Column(db.Float, nullable=True)
    yield_token_reward = db.Column(db.String(50), nullable=True)

    tvl = db.Column(db.Float, nullable=False, default=0)

    chain = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    smart_contract = db.Column(db.String(150), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'market': self.market,
            'project': self.project,
            'information': self.information if isinstance(self.information, list) else [self.information],
            'yield_rate_base': self.yield_rate_base,
            'yield_rate_base': getattr(self, 'liquidity_rate_formatted', None),
            'yield_rate_reward': self.yield_rate_reward,
            'yield_token_reward': self.yield_token_reward,
            'tvl': self.tvl,
            'tvl_formatted': getattr(self, 'tvl_formatted', None),
            'chain': self.chain,
            'type': self.type,
            'smart_contract': self.smart_contract,
            'timestamp': self.timestamp.isoformat(),  # Convert datetime to string
            'humanized_timestamp': getattr(self, 'humanized_timestamp', None),
        }

    def __repr__(self) -> str:
        return f"YieldRate (id={self.id!r}, protocol={self.project!r}, market={self.market!r}, chain={self.chain!r})"
