import sys

from croniter import croniter
from datetime import datetime
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from quant_framework.strategies.strategy import Strategy as StrategyInterface
from quant_framework.internal.models import StrategyState, Strategy as StrategyModel
from quant_framework.internal.utils import db, strategy_loader


def run_backtest(strategy_name, start, end):
    engine = db.get_engine()

    # Change the strategy state to BACKTEST in the database
    _update_strategy_record(engine, strategy_name, StrategyState.BACKTEST.value)

    # Create a context that holds important variables 
    context = {}
    context['timestamp'] = start

    # Fetch the user-defined strategy class
    c = _extract_user_strategy_class(engine, strategy_name)
    user_strat = c(context)

    # Slice the timestamp range according to the interval of the strategy
    # The 'interval' should be cron syntax (i.e. '0 0 * * *')
    # The cronitor library creates an iterator where each 'next' value is a datetime
    # representing the next execution time
    it = croniter(user_strat.interval, start)

    # Call the built-in user-defind 'begin' function
    user_strat.begin(context)

    # At each interval's timestamp, call the strategy's 'update' function
    while context['timestamp'] < end:
        user_strat.update(context)
        context['timestamp'] = it.get_next(datetime)

    # Call the built-in user-defind 'finish' function
    user_strat.finish(context)

    # Change the strategy state to BACKTEST in the database
    _update_strategy_record(engine, strategy_name, StrategyState.IDLE.value)


def _extract_user_strategy_class(engine, strategy_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(StrategyModel) \
        .filter(StrategyModel.name == strategy_name) \
        .first()
    
    file_path = result.file_path

    # Fetch the module corresponding to the strategy class name
    # This should have been set within the strategy_loader util
    strat_class = None
    for c in StrategyInterface.__subclasses__():
        if c.__name__ == result.class_name:
            strat_class = c

    if strat_class is None:
        raise ValueError(f'No user-defined class found with the name {strategy_name}')

    return strat_class


def _update_strategy_record(engine, strategy_name, state):
    with engine.connect() as conn:
        update_stmt = update(StrategyModel) \
            .where(StrategyModel.name==strategy_name) \
            .values(state=state)

        conn.execute(update_stmt)
