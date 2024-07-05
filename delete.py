from db_config import app, db, MoneyMarketRate

def delete_aave_protocol():
    with app.app_context():
        try:
            # Delete all records with protocol 'Aave'
            num_deleted = MoneyMarketRate.query.filter_by(protocol='DSR').delete()

            # Commit the changes
            db.session.commit()
            print(f"Deleted {num_deleted} records with protocol 'Aave'")

        except Exception as e:
            db.session.rollback()
            print(f"Error deleting records: {e}")

if __name__ == '__main__':
    delete_aave_protocol()
