from flask import Flask, jsonify
import sys, os
import humanize
from datetime import datetime

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from app import app, db
from instances.MoneyMarketRate import MoneyMarketRate as Table

stablecoins = [
    "USDC",
    "USDT",
    "DAI",
    "USDe",
    "USDD",
    "pyUSD",
    "FRAX",
    "crvUSD",
    "GHO",
    "LUSD",
    "USDA",
    "sDai",
    "sFrax",
    "FRAX",
]

def get_stablecoin_rates():
    with app.app_context():
        subquery = (
                db.session.query(
                    Table.token,
                    Table.protocol,
                    Table.collateral,
                    Table.chain,
                    db.func.max(Table.timestamp).label('latest')
                )
                .group_by(Table.token, Table.protocol, Table.collateral, Table.chain)
                .subquery()
            )

        latest_rates = db.session.query(Table).join(
            subquery,
            (Table.token == subquery.c.token) &
            (Table.protocol == subquery.c.protocol) &
            (Table.chain == subquery.c.chain) &
            ((Table.collateral == subquery.c.collateral) | (Table.collateral.is_(None) & subquery.c.collateral.is_(None))) &
            (Table.timestamp == subquery.c.latest)
        ).filter(Table.tvl > 1000, Table.token.in_(stablecoins)
        ).order_by(Table.tvl.desc()).all()
        rates_list = [
            {
                **rate.to_dict(),
                'tvl_formatted': f"{rate.tvl:,.0f}" if rate.tvl is not None else 0,
                'liquidity_rate_formatted': f"{rate.liquidity_rate:,.2f}" if rate.liquidity_rate is not None else 0,
                'humanized_timestamp': humanize.naturaltime(datetime.utcnow() - rate.timestamp)
            }
            for rate in latest_rates
        ]

        return jsonify(rates_list)
