from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from quant_framework.internal.models import Base, Strategy


def init_db(db_path):x
    '''
    Initialize our database and all the needed tables
    '''
    # If the DB file doesn't exist yet, create it
    if not path.exists(db_path):
        with open(db_path, 'w'):
            pass

    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)

    return engine


def sync_strategies(engine, strategies):
    '''
    Sync the state of our database table to match the provided strategies:
    1. Delete any rows in the DB table that do not correspond to the strategies array
    2. Upsert each strategy in the provided array
    '''
    with engine.connect() as conn:
        stmt = f'''
            INSERT OR REPLACE INTO strategies(name, description, interval, file_path, fingerprint)
            VALUES(:name, :description, :interval, :file_path, :fingerprint);
        '''

        for strat in strategies:
            conn.execute(stmt, {
                'name': strat.name,
                'description': strat.description,
                'interval': strat.interval,
                'file_path': strat.file_path,
                'fingerprint': strat.fingerprint
            })



