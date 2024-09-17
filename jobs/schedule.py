import os, sys
from apscheduler.schedulers.background import BlockingScheduler
from app import app
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from projects.aave.fetch_data import fetch_store_rates as aave
from projects.compound.fetch_rates import fetch_store_rates as compound
from projects.curve.fetch_store_data import fetch_store_data as curve
from projects.curve.fetch_store_data import get_crvusd as crv_usd

from projects.gearbox.fetch_data import fetch_store_data as gearbox
from projects.morpho.fetch_data_morpho import fetch_data_metamorpho as morpho
from projects.pendle.fetch_data import fetch_data as pendle
from projects.spark.fetch_rates import get_all_data as spark
from projects.yearn.get_yearn_data import fetch_yearn as yearn
from projects.fx.fetch_data import fetch_store_data as fx
from projects.clearpool.fetch_data import fetch_store_rates as clearpool
from projects.lido.get_rate import get_data_steth as lido
from projects.rocketpool.fetch_data import get_data_reth as rocketpool
from projects.ethena.get_data import get_data as ethena
from projects.optimism.get_data import get_token_data as optimism
from projects.silo.get_data import get_token_data as silo
from projects.stargate.get_data import get_data as stargate
from projects.paypal.get_data import get_supply as paypal
from projects.wBTC.get_data import get_store_data as wbtc
from projects.jito.get_data import get_supply as jito
from projects.avax.get_data import get_data as avax
from projects.coinbase.get_data import token_data as coinbase
from projects.coinbase.cbBTC.get_data import token_data as cbbtc
from projects.wETH.get_data import token_data as weth
from projects.liquity.get_data import get_token as liquity
from projects.abracadabra.get_data import get_token as abra
from projects.orca.get_data import get_info as orca
from projects.ripple.get_data import token_data as ripple
from projects.tron.get_data import token_data as tron
from projects.uniswap.get_data import get_uniswap_pools as uniswap
from projects.polkadot.get_data import get_token_data as polkadot
from projects.cardano.get_data import token_data as cardano
from projects.curve.pool_data import get_pools as curve_pools
from projects.bitcoin.get_data import get_data as bitcoin
from projects.fantom.get_data import get_data as fantom
from projects.mantle.get_data import get_data as mantle
from projects.maker.get_data import get_data as maker
from projects.etherfi.get_data import get_data as etherfi
from projects.bnb.get_data import get_data as bnb
from projects.circle.get_data import get_data as circle
from projects.tether.get_data import get_data as tether
from projects.ethereum.get_data import get_data as ethereum
from projects.threshold.get_data import get_token_data as tbtc
from projects.lombard.get_data import get_token_data as lombart












from scripts.get_price_supply import get_price_supply


from scripts.stablecoin_fetch import get_stablecoin_data as stablecoin

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FETCH_INTERVAL_MINUTES = 30
STABLECOIN_INTERVAL_MINUTES = 60

sched = BlockingScheduler()

def log_and_execute(func, func_name):
    """Log execution of the given function with error handling."""
    try:
        func()  # Execute the function
    except Exception as e:
        logger.error(f"Error fetching {func_name} data: {e}")


def fetch_store_data():
    """Fetch data for all defined projects."""
    tasks = {
        "Aave": aave,
        "Curve": curve,
        "Curve Pools": curve_pools,
        "Gearbox": gearbox,
        "Maker DSR": spark,
        "Maker": maker,
        "Compound": compound,
        "Morpho": morpho,
        "Yearn": yearn,
        "Pendle": pendle,
        "FX": fx,
        "Clearpool": clearpool,
        "Lido": lido,
        "RocketPool":rocketpool,
        "Ethena":ethena,
        "CurveUSD": crv_usd,
        "Optimism": optimism,
        "Silo":silo,
        "Stargate":stargate,
        "Paypal":paypal,
        "wBTC":wbtc,
        "Jito":jito,
        "Avax":avax,
        "coinbase":coinbase,
        "cbbtc":cbbtc,
        "wETH":weth,
        "liquity": liquity,
        "Abracadabra":abra,
        "Orca":orca,
        "Ripple":ripple,
        "Tron":tron,
        "Uniswap":uniswap,
        "Polkadot":polkadot,
        "Cardano":cardano,
        "Bitcoin":bitcoin,
        "Fantom":fantom,
        "Mantle":mantle,
        "EtherFi":etherfi,
        "BNB":bnb,
        "Circle":circle,
        "Tether":tether,
        "Ethereum":ethereum,
        "tbtc":tbtc,
        "lombart":lombart
    }

    with app.app_context():
        logger.info(f"Fetching Yields Data")
        for name, task in tasks.items():
            try:
                log_and_execute(task, name)
                print(f"executed {name}")
            except Exception as e:
                print(e)



def fetch_price_supply():
    with app.app_context():
        log_and_execute(get_price_supply, "Token Info")


sched.add_job(fetch_store_data, 'interval', minutes=FETCH_INTERVAL_MINUTES)
sched.add_job(get_price_supply, 'interval', minutes=30)

if __name__ == '__main__':

    fetch_store_data()
    fetch_price_supply()

    sched.start()
