import os
import threading
import time

from quant_framework.internal.utils import db, strategy_loader
from quant_framework.internal.www import app


def main():
    strategy_folder = os.getenv('QUANT_FRAMEWORK_STRATEGY_FOLDER') or '/usr/local/quant-framework/strategies/'
    db_path = os.getenv('QUANT_FRAMEWORK_DB') or '/usr/local/quant-framework/quant_framework.db'

    # Initialize our database
    engine = db.init_db(db_path)

    def _refresh_db():
        strategies = strategy_loader.fetch_strategies_from_directory(strategy_folder)
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
