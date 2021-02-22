import os
import threading
import time

from quant_framework.internal.configuration import conf

from quant_framework.internal.utils import db, strategy_loader
from quant_framework.internal.www import app


def main():
    conf['strategy_folder'] = os.getenv('QUANT_FRAMEWORK_STRATEGY_FOLDER')
    conf['db_url'] = os.getenv('QUANT_FRAMEWORK_DB')

    # Initialize our database
    engine = db.get_engine()
    db.init_db(engine)

    def _refresh_db():
        strategies = strategy_loader.fetch_user_strategies()
        db.sync_strategies(engine, strategies)

    # Start our app in a separate thread
    flask_app = app.create_app(engine)
    flask_thread = threading.Thread(target=flask_app.run, kwargs={'debug': True, 'use_reloader': False})
    flask_thread.start()

    while True:
        # Every N seconds, refresh the strategies database
        refresh_db_thread = threading.Thread(target=_refresh_db)
        refresh_db_thread.start()
        refresh_db_thread.join()

        time.sleep(10)


if __name__ == '__main__':
    main()
