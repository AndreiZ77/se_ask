from sqlalchemy import create_engine, MetaData

from se_app.settings import get_config
from se_app.db import se_query, answer, query_answer

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

def delete_tables(engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[se_query, answer, query_answer])

def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[se_query, answer, query_answer])

def sample_data(engine):
    conn = engine.connect()
    conn.execute(se_query.insert(), [
        {'query_text': 'python', 'date': '2019-10-05 17:17:49.629+02'},
        {'query_text': 'java', 'date': '2019-10-06 15:17:49.629+02'}
    ])
    conn.execute(answer.insert(), [
        {'header': 'Learn Numerical methods in Python', 'date': '2017-09-21 17:17:49.629+02', 'score': 0},
        {'header': 'Physical simulation in python', 'date': '2014-09-30 17:17:49.629+02', 'score': 2},
        {'header': 'Installing sympy package in python', 'date': '2019-09-29 17:17:49.629+02', 'score': 1},
        {'header': 'Java library for SDP', 'date': '2011-10-27 14:17:49.629+02', 'score': 1}
    ])
    conn.execute(query_answer.insert(), [
        {'query_id': 1, 'answer_id': 1},
        {'query_id': 1, 'answer_id': 2},
        {'query_id': 1, 'answer_id': 3},
        {'query_id': 2, 'answer_id': 4},
    ])
    conn.close()

if __name__ == '__main__':
    config = get_config()
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)
    delete_tables(engine)
    create_tables(engine)
    #sample_data(engine)