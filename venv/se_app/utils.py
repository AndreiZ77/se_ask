# utils.py
import requests
import json

#from sqlalchemy import create_engine
#from settings import get_config, DSN
from db import save_records


async def se_query_update(app, search_text):
    # URL, для API запроса
    url = 'http://api.stackexchange.com/2.2/search?order=desc&site=stackoverflow'
    #url = 'http://api.stackexchange.com/2.2/search?order=desc&site=ru.stackoverflow'
    se_sort = 'creation'
    # Параметры запроса
    params = {
        'sort': se_sort, #creation / activity / votes / relevance
        'intitle': search_text,
    }
    r = requests.get(url=url, params=params)
    items = r.json()["items"]
    if items:
        async with app['db'].acquire() as conn:
            q_id = await save_records(conn, items, search_text)
            return q_id





