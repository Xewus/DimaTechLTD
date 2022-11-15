import logging
import sys
from pathlib import Path

from pydantic import BaseSettings
from sanic import Sanic
from sanic_jwt import Initialize
from tortoise import Tortoise, connections
from tortoise.log import logger

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from src.api.auth import authenticate
from src.api.auth import blue as blue_auth
from src.api.auth import retrieve_user
from src.api.bills import blue as blue_bills
from src.api.products import blue as blue_products
from src.api.transactions import blue as blue_transactions
from src.api.users import blue as blue_users
from src.db.models import create_first_user
from src.settings import AppSettings, FirstUser

fmt = logging.Formatter(
    fmt="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(fmt)

# will print debug sql
logger_db_client = logging.getLogger("tortoise.db_client")
logger_db_client.setLevel(logging.WARNING)
logger_db_client.addHandler(sh)


def create_app(
    app_settings: BaseSettings = AppSettings,
    first_user: None | BaseSettings = None
) -> Sanic:
    app = Sanic(name=app_settings.APP_NAME)
    app.config.update(app_settings.dict())

    app.blueprint(blueprint=blue_auth)
    app.blueprint(blueprint=blue_users)
    app.blueprint(blueprint=blue_products)
    app.blueprint(blueprint=blue_bills)
    app.blueprint(blueprint=blue_transactions)


    Initialize(
        app,
        secret=app_settings.APP_KEY,
        algorithm=app_settings.ALGORITHM,
        expiration_delta=app_settings.ACCESS_TOKEN_EXPIRE,
        authenticate=authenticate,
        retrieve_user=retrieve_user
    )

    @app.listener("before_server_start")
    async def init_orm(app, loop):  # pylint: disable=W0612
        await Tortoise.init(
            db_url=app_settings.DB_URL,
            modules=AppSettings.DB_MODULES
        )
        logger.info(
            "Tortoise-ORM started, %s, %s",
            connections._get_storage(),
            Tortoise.apps
        )
        logger.info("Tortoise-ORM generating schema")
        await Tortoise.generate_schemas()

        if first_user is not None:
            await create_first_user(first_user)

    @app.listener("after_server_stop")
    async def close_orm(app, loop):  # pylint: disable=W0612
        await connections.close_all()
        logger.info("Tortoise-ORM shutdown")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()