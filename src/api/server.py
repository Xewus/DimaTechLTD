import logging
import sys

from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from src.api.bills import blue as blue_bills
from src.api.goods import blue as blue_goods
from src.api.transactions import blue as blue_transactions
from src.api.users import blue as blue_users
from src.db.models import create_first_user
from src.settings import APP_NAME, DEBUG, TORTOISE_CONFIG, AppConfig

fmt = logging.Formatter(
    fmt="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.DEBUG)
logger_db_client.addHandler(sh)

logger_tortoise = logging.getLogger("tortoise")
logger_tortoise.setLevel(logging.DEBUG)
logger_tortoise.addHandler(sh)



app = Sanic(name=APP_NAME)

app.blueprint(blueprint=blue_users)
app.blueprint(blueprint=blue_goods)
app.blueprint(blueprint=blue_bills)
app.blueprint(blueprint=blue_transactions)

print(app.blueprints)

register_tortoise(
    app,
    **TORTOISE_CONFIG
)

@app.listener("before_server_start")
async def before_server_start(app, loop):
    await create_first_user()
