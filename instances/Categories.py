from app import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    projects = db.relationship('Project', secondary='project_categories', back_populates='categories')

    def __repr__(self):
        return f"Category(id={self.id!r}, name={self.name!r})"

def create_predefined_categories():
    categories = [
        "Blockchain", "Stablecoin", "ETH & equivalent", "BTC & equivalent",
        "Lending", "Yield Aggregator", "DEX", "Derivatives", "Liquid Staking",
        "NFT", "Bridges", "DeFi", "Oracles", "Gaming", "RWA", "Memecoin"
    ]
    for category_name in categories:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            new_category = Category(name=category_name)
            db.session.add(new_category)
    db.session.commit()
