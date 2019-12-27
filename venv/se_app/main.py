import logging
import sys

from aiohttp import web
import aiohttp_jinja2
import jinja2
import aioredis

from routes import setup_routes
from settings import get_config, BASE_DIR
from db import close_pg, init_pg
from redis_db import init_redis, close_redis
#from api_poll_new import init_update
from middlewares import setup_middlewares

async def init_app(argv=None):
    app = web.Application()
    app['config'] = get_config(argv)
    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader(str(BASE_DIR / 'se_app' / 'templates')))
    # create postgresql & redis db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    app.on_startup.append(init_redis)
    app.on_cleanup.append(close_redis)
    # setup views and routes
    setup_routes(app)
    setup_middlewares(app)
    return app

def main(argv):
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(argv)
    config = get_config(argv)
    #config = app['config']
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])