import pathlib
from views import index, answers, db_tab, poll
from settings import BASE_DIR


PROJECT_ROOT = pathlib.Path(__file__).parent

def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get('/{q_id}/answers', answers)
    app.router.add_get('/poll', poll)
    app.router.add_get('/db_tab', db_tab)
    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')