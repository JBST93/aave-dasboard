# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Aave Dashboard is a Flask-based DeFi yield monitoring platform that fetches lending/borrowing rates from 40+ protocols (Aave, Compound, Curve, Morpho, Yearn, etc.), stores them in PostgreSQL, and exposes them via REST APIs.

## Commands

```bash
# Run Flask development server
python app.py

# Run background job scheduler (fetches yield data every 30 min)
python jobs/schedule.py
# Or alternatively:
python run_jobs.py

# Test a specific protocol fetcher
python projects/compound/fetch_rates.py
python projects/aave/fetch_data.py

# Database migrations
flask db migrate
flask db upgrade
```

## Architecture

### Data Flow
1. **Fetchers** (`projects/*/fetch_data.py`) connect to smart contracts via Web3 or external APIs
2. **Job Scheduler** (`jobs/schedule.py`) runs fetchers every 30 minutes using APScheduler
3. **Database Models** (`instances/*.py`) store yield rates, money market rates, stablecoin data
4. **API Scripts** (`scripts/*.py`) query and format data for API responses
5. **Flask Routes** (`app.py`) expose REST endpoints

### Key Directories
- `projects/` - Protocol-specific fetchers (aave/, compound/, curve/, morpho/, etc.). Each contains `fetch_data.py` and contract ABIs
- `instances/` - SQLAlchemy models: `YieldRate`, `MoneyMarketRate`, `Stablecoin`, `TokenData`, `Projects`
- `scripts/` - API response formatters: `yields.py`, `stablecoin_yield.py`, `get_project_info.py`
- `utils/` - Shared utilities: `get_price.py` (multi-source price fetching), `get_supply_evm.py`, `load_abi.py`

### Database Models
- **YieldRate**: Yield farming rates (market, project, yield_rate_base, yield_rate_reward, tvl, chain)
- **MoneyMarketRate**: Lending/borrow rates (protocol, token, liquidity_rate, borrow_rate, collateral)
- **Stablecoin**: Stablecoin metadata (token, price, supply, circulating)
- **TokenData**: Token price/supply tracking with historical deltas
- **Project**: Protocol metadata (name, ticker, logo, category, chain, contract)

### API Endpoints
- `GET /api/yield_rates` - All yield rates (filtered by TVL > $1000, timestamp < 3 hours)
- `GET /api/stablecoin_yield_rates` - Stablecoin-specific yields
- `GET /api/eth_yields` - ETH/wETH yields
- `GET /api/projects` - All tracked projects with price/supply data
- `GET /api/stablecoin_info` - Stablecoin metadata
- `/admin/*` - CRUD interface for managing projects

## Environment Variables

Required in `.env`:
```
APP_SETTINGS=config.DevelopmentConfig
DATABASE_URL2=postgresql://user:password@localhost:5432/aave_dashboard
INFURA_KEY=your_infura_api_key
```

## Patterns

### Protocol Fetcher Pattern
Each protocol in `projects/` follows this pattern:
1. Define contract addresses and chain configs
2. Connect via Web3 using Infura
3. Call smart contract methods to get rates
4. Calculate APY from raw values
5. Store `YieldRate` or `MoneyMarketRate` records

### Database Context
All database operations require Flask app context:
```python
with app.app_context():
    records = db.session.query(YieldRate).filter(...).all()
```

### Data Deduplication
API responses deduplicate by (project, chain, smart_contract, information), keeping only the latest timestamp.

## Multi-Chain Support

**EVM**: Ethereum, Arbitrum, Optimism, Polygon, Avalanche, Base (via Web3 + Infura)
**Non-EVM**: Solana (via `utils/get_supply_solana.py`)
