from os import path

from sqlalchemy import bindparam, create_engine, text

from quant_framework.internal.models import Base, Strategy


def init_db(db_path):
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
        # Upsert all current strategies
        stmt = f'''
            INSERT OR REPLACE INTO strategies(name, description, interval, class_name, file_path, fingerprint)
            VALUES(:name, :description, :interval, :class_name, :file_path, :fingerprint)
            ON CONFLICT(name) DO UPDATE SET
                description=:description,
                interval=:interval,
                class_name=:class_name,
                file_path=:file_path,
                fingerprint=:fingerprint;
        '''

        for strat in strategies:
            conn.execute(stmt, {
                'name': strat.name,
                'description': strat.description,
                'interval': strat.interval,
                'class_name': strat.class_name,
                'file_path': strat.file_path,
                'fingerprint': strat.fingerprint
            })

        # Delete all strategies that aren't around anymore
        names = [strat.name for strat in strategies]

        stmt = f'''
            DELETE FROM strategies
            WHERE name NOT IN :names;
        '''

        # Need to use an expanding 'bindparam' here since we want to substitute a list param
        t = text(stmt)
        t = t.bindparams(bindparam('names', expanding=True))

        conn.execute(t, {'names': names})
