import argparse
import pathlib
import trafaret as T

from trafaret_config import commandline

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'se_app.yaml'

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

TRAFARET = T.Dict({
    T.Key('postgres'):
        T.Dict({
            'database': T.String(),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'minsize': T.Int(),
            'maxsize': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
    T.Key('page'):
        T.Dict({
            'limit': T.Int(),
            'sorting': T.Int(),
        }),
    T.Key('redis'):
        T.Dict({
            'host': T.String(),
            'port': T.Int(),
            'db': T.Int(),
            'minsize': T.Int(),
            'maxsize': T.Int(),
            'time': T.Int(),
        }),
})


def get_config(argv=None):
    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )
    # ignore unknown options
    options, unknown = ap.parse_known_args(argv)
    config = commandline.config_from_options(options, TRAFARET)
    return config



# import pathlib
# import yaml
#
# BASE_DIR = pathlib.Path(__file__).parent.parent
# config_path = BASE_DIR / 'config' / 'se_app.yaml'
#
# def get_config(path):
#     with open(path) as f:
#         config = yaml.safe_load(f)
#     return config
#
# config = get_config(config_path)