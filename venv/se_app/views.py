import aiohttp_jinja2
from aiohttp import web
import math
import db
# import json
from utils import se_query_update
from redis_db import redis_set, redis_get, dict_date2str


@aiohttp_jinja2.template('index_tab.html')
async def db_tab(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(
            'SELECT se_query.id as q_id, se_query.query_text as q_text, ' +
            'se_query.date as q_date, ' +
            'answer.id as a_id, answer.header as a_header, answer.date as a_date, answer.link as a_link, answer.score as a_score ' +
            'FROM se_query INNER JOIN (answer INNER JOIN query_answer ON answer.id = query_answer.answer_id) ' +
            'ON se_query.id = query_answer.query_id ORDER BY se_query.id DESC, a_date DESC'
        )
        records = await cursor.fetchall()
        se_queries = [dict(q) for q in records]
        return {'queries': se_queries}


async def paginate(request):
    baseurl = request.path
    page_cfg = request.app['config']['page']
    try:
        page_cfg['limit'] = int(request.query['page_limit'])
    except KeyError:
        pass
    try:
        page_number = int(request.rel_url.query['page'])
    except KeyError:
        page_number = 1
    return page_number, page_cfg, baseurl


@aiohttp_jinja2.template('index.html')
async def index(request):
    try:
        return await redis_get(request)
    except:
        page_number, page_cfg, _ = await paginate(request)
        async with request.app['db'].acquire() as conn:
            records, count_q = await db.get_queries(conn, page_cfg['limit'], page_number)
            queries = [dict(q) for q in records]
            await dict_date2str(queries)
            #page_range = range(1, math.ceil(count_q/page_cfg['limit'])+1)
            page_range = math.ceil(count_q / page_cfg['limit'])
            result = {'queries': queries, 'page_cfg': page_cfg, 'page_number': page_number, 'page_range': page_range }
            await redis_set(request, result)
            return result


@aiohttp_jinja2.template('answers.html')
async def answers(request):
    try:
        return await redis_get(request)
    except:
        page_number, page_cfg, baseurl = await paginate(request)
        async with request.app['db'].acquire() as conn:
            records, count_a, q_text = await db.get_answers(conn,
                                                    request.match_info['q_id'],
                                                    page_cfg['limit'],
                                                    page_number)
            answers = [dict(q) for q in records]
            await dict_date2str(answers)
            page_range = math.ceil(count_a / page_cfg['limit'])
            result = {'answers': answers, 'q_text': q_text, 'page_cfg': page_cfg, 'baseurl': baseurl,
                    'page_number': page_number, 'page_range': page_range}
            await redis_set(request, result)
            return result


@aiohttp_jinja2.template('poll.html')
async def poll(request):
    _, page_cfg, baseurl = await paginate(request)
    try:
        search_text = request.rel_url.query['search_text']
        q_id = await se_query_update(request.app, search_text)
        baseurl = "/"+str(q_id)+"/answers"
        raise web.HTTPFound(baseurl)
    except KeyError:
        pass
    return {'page_cfg': page_cfg, 'baseurl': baseurl}
