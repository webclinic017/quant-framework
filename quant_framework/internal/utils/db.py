from os import path

from sqlalchemy import create_engine, delete
from sqlalchemy.dialects.postgresql import insert

from quant_framework.internal.configuration import conf
from quant_framework.internal.models import Base, Strategy


def get_engine():
    db_url = conf['db_url']
    engine = create_engine(db_url)
    return engine


def init_db(engine):
    Base.metadata.create_all(engine)


def sync_strategies(engine, strategies):
    '''
    Sync the state of our database table to match the provided strategies:
    1. Delete any rows in the DB table that do not correspond to the strategies array
    2. Upsert each strategy in the provided array
    '''
    with engine.connect() as conn:
        # Upsert all current strategies
        for strat in strategies:
            insert_stmt = insert(Strategy).values(
                name=strat.name,
                description=strat.description,
                interval=strat.interval,
                class_name=strat.class_name,
                file_path=strat.file_path,
                fingerprint=strat.fingerprint
            )

            insert_stmt = insert_stmt.on_conflict_do_nothing(
                index_elements=['name']
            )
            
            conn.execute(insert_stmt)

        # Delete all strategies that aren't around anymore
        names = [strat.name for strat in strategies]

        delete_stmt = delete(Strategy).where(
            ~Strategy.name.in_(names)
        )

        conn.execute(delete_stmt)
