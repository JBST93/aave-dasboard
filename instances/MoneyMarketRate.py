from app import db
from datetime import datetime

class MoneyMarketRate(db.Model):
    __tablename__ = "money_market_rate"
    __table_args__ = (
        db.Index('ix_money_market_protocol_chain_timestamp', 'protocol', 'chain', 'timestamp'),
        db.Index('ix_money_market_token_timestamp', 'token', 'timestamp'),
    )

    id = db.Column(db.Integer, primary_key=True)
    protocol = db.Column(db.String(50), nullable=False, index=True)
    token = db.Column(db.String(50), nullable=False, index=True)
    # Use db.JSON for SQLite/PostgreSQL compatibility (JSONB is PostgreSQL-only)
    collateral = db.Column(db.JSON, nullable=True)
    liquidity_rate = db.Column(db.Float, nullable=False)
    liquidity_reward_rate = db.Column(db.Float, nullable=True)
    liquidity_reward_token = db.Column(db.String(50), nullable=True)
    borrow_rate = db.Column(db.Float, nullable=False)
    chain = db.Column(db.String(20), nullable=False, index=True)
    tvl = db.Column(db.Float, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'protocol': self.protocol,
            'token': self.token,
            'liquidity_rate': self.liquidity_rate,
            'liquidity_reward_rate': self.liquidity_reward_rate,
            'liquidity_reward_token': self.liquidity_reward_token,
            'collateral': self.collateral if isinstance(self.collateral, list) else [self.collateral],
            'borrow_rate': self.borrow_rate,
            'tvl': self.tvl,
            'chain': self.chain,
            'timestamp': self.timestamp.isoformat(),  # Convert datetime to string
            'tvl_formatted': getattr(self, 'tvl_formatted', None),
            'liquidity_rate_formatted': getattr(self, 'liquidity_rate_formatted', None),
            'humanized_timestamp': getattr(self, 'humanized_timestamp', None),
        }

    def __repr__(self) -> str:
        return f"MoneyMarketRate (id={self.id!r}, protocol={self.protocol!r}, token={self.token!r}, chain={self.chain!r})"
