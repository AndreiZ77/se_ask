import aioredis
import json

async def dict_date2str(mydict):
    for item in mydict:
        item['date'] = item['date'].strftime('%d.%m.%Y %H:%M:%S')


async def redis_set(request, result):
    r = request.app['redis']
    data = json.dumps(result)
    await r.setex(request.path_qs, int(request.app['config']['redis']['time']), str(data))
    # print('set:', request.path_qs, data)


async def redis_get(request):
    r = request.app['redis']
    data = await r.get(request.path_qs)
    print(data)
    if data:
        result = json.loads(data)
        # print('get:', request.path_qs, str(result))
    return result


async def init_redis(app):
    conf = app['config']['redis']
    redis = await aioredis.create_redis_pool(
        (conf['host'], conf['port']),
        db=conf['db'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'])
    app['redis'] = redis

async def close_redis(app):
    app['redis'].close()
    await app['redis'].wait_closed()