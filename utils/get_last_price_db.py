from sqlalchemy import desc, func

from app import app, db

from instances.TokenData import TokenData as Table


def get_latest_price(token_name):
    latest_price = Table.query.filter(func.lower(Table.token) == func.lower(token_name)).order_by(desc(Table.timestamp)).first()
    if latest_price:
        return latest_price.price
    else:
        return 0

if __name__ == '__main__':
    app.run(debug=True)
