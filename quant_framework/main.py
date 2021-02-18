import os

from quant_framework.internal.utils import db, strategy_loader


def main():
    strategy_folder = os.getenv('QUANT_FRAMEWORK_STRATEGY_FOLDER') or '/usr/local/quant-framework/strategies/'
    db_path = os.getenv('QUANT_FRAMEWORK_DB') or '/usr/local/quant-framework/quant_framework.db'

    engine = db.init_db(db_path)

    strategies = strategy_loader.fetch_strategies_from_directory(strategy_folder)
    db.sync_strategies(engine, strategies)


if __name__ == '__main__':
    main() 