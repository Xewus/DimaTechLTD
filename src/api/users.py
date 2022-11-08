"""Эндпоинты для пользователей.
"""
from sanic import Blueprint, Request
from sanic.response import json, HTTPResponse

blue = Blueprint('users', url_prefix='/users')

@blue.route('/me')
async def me(request: Request) -> HTTPResponse:
    return json({'user': 'me'})

@blue.route('/all')
async def all_users(request: Request) -> HTTPResponse:
    return json(['user1', 'user2'])

@blue.route('/create', methods=['POST'])
async def create_user(response: Request) -> HTTPResponse:
    return json('user')

@blue.route('/login', methods=['POST'])
async def login(request: Request) -> HTTPResponse:
    return json({'Bearer': 'kjklk'})

@blue.route('/activ/<username:str>')
async def activ(request: Request, username: str) -> HTTPResponse:
    if username.endswith('1'):
        username += '0'
    else:
        username += '1'
    return json({'user': username})
