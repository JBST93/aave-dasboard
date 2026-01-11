"""
Initialize the database with all tables and default data.

Usage:
    python scripts/init_db.py

This script:
1. Creates all database tables from SQLAlchemy models
2. Seeds default categories for project classification
3. Prints status and next steps
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db


def init_database():
    """Initialize database tables and seed default data."""
    with app.app_context():
        print("Initializing database...")
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print()

        # Create all tables
        db.create_all()
        print("[OK] All tables created")

        # Import models to show what was created
        from instances.YieldRate import YieldRate
        from instances.MoneyMarketRate import MoneyMarketRate
        from instances.TokenData import TokenData
        from instances.Stablecoin import Stablecoin
        from instances.Projects import Project
        from instances.Categories import Category

        # Seed categories if empty
        if Category.query.count() == 0:
            categories = [
                "Blockchain",
                "Stablecoin",
                "ETH & equivalent",
                "BTC & equivalent",
                "Lending",
                "Yield Aggregator",
                "DEX",
                "Derivatives",
                "Liquid Staking",
                "NFT",
                "Bridges",
                "DeFi",
                "Oracles",
                "Gaming",
                "RWA",
                "Memecoin"
            ]
            for name in categories:
                db.session.add(Category(name=name))
            db.session.commit()
            print(f"[OK] Seeded {len(categories)} categories")
        else:
            print(f"[OK] Categories already exist ({Category.query.count()} found)")

        # Show table summary
        print()
        print("Tables created:")
        print(f"  - yield_rate")
        print(f"  - money_market_rate")
        print(f"  - token_data")
        print(f"  - stablecoin")
        print(f"  - projects")
        print(f"  - categories")

        print()
        print("=" * 50)
        print("Database ready!")
        print()
        print("Next steps:")
        print("  1. Run the app:        python app.py")
        print("  2. Fetch yield data:   python jobs/schedule.py")
        print("  3. View admin panel:   http://localhost:5000/admin")
        print()


if __name__ == '__main__':
    init_database()
