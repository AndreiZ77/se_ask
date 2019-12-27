import aiopg.sa
import datetime
from html import unescape
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime,
    select, join
)
#import sqlalchemy as sa

__all__ = ['se_query', 'answer', 'query_answer', 'count_queries']


meta = MetaData()

se_query = Table(
    'se_query', meta,
    Column('id', Integer, primary_key=True),
    Column('query_text', String(200), nullable=False),
    Column('date', DateTime, nullable=False, default=datetime.datetime.utcnow)
)

answer = Table(
    'answer', meta,
    Column('id', Integer, primary_key=True),
    Column('header', String(200), nullable=False),
    Column('date', DateTime, nullable=False),
    Column('link', String(200), nullable=False),
    Column('score', Integer)
)

query_answer = Table(
    'query_answer', meta,
    Column('query_id', Integer, ForeignKey('se_query.id', ondelete='CASCADE')),
    Column('answer_id', Integer, ForeignKey('answer.id', ondelete='CASCADE'))
)


async def save_records(conn, items, search_text):
    await conn.execute(se_query.insert().values({'query_text': search_text}))
    row = await (await conn.execute(
        se_query.select().order_by(se_query.c.id.desc())
    )).first()
    se_query_id = row.id
    #se_query_date = row.date
    #print(search_text, se_query_id, se_query_date.strftime('%d.%m.%Y %H:%M:%S'))
    for item in items:
        creation_date = datetime.datetime.utcfromtimestamp(int(item['creation_date']))
        header = unescape(item['title'])
        await conn.execute(answer.insert().values({'header': header, 'date': creation_date, 'link': item["link"],
                             'score': item["score"]}))
        row = await (await conn.execute(
            answer.select().order_by(answer.c.id.desc())
        )).first()
        answer_id = row.id
        #print('-', answer_id, header)
        await conn.execute(query_answer.insert().values(query_id=se_query_id, answer_id=answer_id))
    return se_query_id


async def get_queries(conn, page_limit, page_number):
    cursor = await conn.execute(
        se_query.select()
            .order_by(se_query.c.id.desc())
            .limit(page_limit)
            .offset((page_number - 1) * page_limit)
    )
    records = await cursor.fetchall()
    count_q = await conn.scalar(se_query.select().alias('se_queries').count())
    return records, count_q


async def get_answers(conn, q_id, page_limit, page_number):
    cursor = await conn.execute(
        answer.select()
            .select_from(join(answer, query_answer, query_answer.c.answer_id == answer.c.id))
            .where(query_answer.c.query_id == q_id)
            .order_by(answer.c.date.desc())
            .limit(page_limit)
            .offset((page_number - 1) * page_limit)
    )
    records = await cursor.fetchall()

    cursor = await conn.execute(se_query.select().where(se_query.c.id == q_id))
    row = await cursor.fetchall()
    query_text = row[0][1]

    # row = await conn.scalar(
    #     se_query.select(se_query.c.text)
    #         .where(se_query.c.id == q_id)
    #         .alias('query_text'))

    count_a = await conn.scalar(
        query_answer.select()
            .where(query_answer.c.query_id == q_id)
            .alias('se_answers')
            .count())
    return records, count_a, query_text


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database = conf['database'],
        user = conf['user'],
        password = conf['password'],
        host = conf['host'],
        port = conf['port'],
        minsize = conf['minsize'],
        maxsize = conf['maxsize'],
    )
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
