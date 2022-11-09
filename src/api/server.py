from sanic import Sanic
from tortoise.contrib.sanic import register_tortoise

from src.api.goods import blue as blue_goods
from src.api.transactions import blue as blue_transactions
from src.api.users import blue as blue_users
from src.db.models import create_first_user
from src.settings import APP_NAME, DEBUG, TORTOISE_CONFIG, AppConfig

app = Sanic(name=APP_NAME)

app.blueprint(blueprint=blue_users)
app.blueprint(blueprint=blue_goods)
app.blueprint(blueprint=blue_transactions)

register_tortoise(
    app,
    **TORTOISE_CONFIG
)

@app.listener("before_server_start")
async def before_server_start(app, loop):
    await create_first_user()
