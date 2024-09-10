from app import db
from datetime import datetime
from .Associations import project_categories


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    protocol_name = db.Column(db.String(100), nullable=False, unique=True)
    token_ticker = db.Column(db.String(20), nullable=False)
    logo_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    category_main = db.Column(db.String(50), nullable=True)
    website = db.Column(db.String(255))
    forum = db.Column(db.String(255))
    alert = db.Column(db.Text)
    token_decimals = db.Column(db.Integer)
    chain_main = db.Column(db.String(50))
    contract_main = db.Column(db.String(100))
    snapshot_name = db.Column(db.String(100))
    github_link = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now)

    # Relationship with categories
    categories = db.relationship('Category', secondary='project_categories', back_populates='projects')

    def to_dict(self):
        return {
            'id': self.id,
            'protocol_name': self.protocol_name,
            'token_ticker': self.token_ticker,
            'logo_url': self.logo_url,
            'description': self.description,
            'category_main': self.category_main,
            'website': self.website,
            'forum': self.forum,
            'alert': self.alert,
            'token_decimals': self.token_decimals,
            'chain_main': self.chain_main,
            'contract_main': self.contract_main,
            'snapshot_name': self.snapshot_name,
            'github_link': self.github_link,
            'timestamp': self.timestamp.isoformat(),
            'categories': [category.name for category in self.categories]
        }

    def __repr__(self):
        return f"Project(id={self.id!r}, protocol_name={self.protocol_name!r}, token_ticker={self.token_ticker!r})"
