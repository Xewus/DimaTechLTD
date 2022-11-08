from sanic import Sanic
from sanic.response import json, HTTPResponse, text
from src.settings import APP_NAME, DB_SETTINGS
from sanic.request import Request
from src.api.users import blue as blue_users
from src.api.goods import blue as blue_goods
from src.api.transactions import blue as blue_transactions


app = Sanic(name=APP_NAME)

app.config.update(DB_SETTINGS)

app.blueprint(blueprint=blue_users)
app.blueprint(blueprint=blue_goods)
app.blueprint(blueprint=blue_transactions)

@app.reload_process_start
async def reload_start(*_):
    print(">>>>>> reload_start <<<<<<")


@app.main_process_start
async def main_start(*_):
    print(">>>>>> main_start <<<<<<")

@app.on_request
async def increment_foo(request):
    if not hasattr(request.conn_info.ctx, "foo"):
        request.conn_info.ctx.foo = 0
    request.conn_info.ctx.foo += 1

@app.route("/")
async def handler(request):
    return text("Hi 😎")
  