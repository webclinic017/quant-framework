import sys

from croniter import croniter
from datetime import datetime
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from quant_framework.brokers import MockBroker
from quant_framework.data_providers import DataProvider as DataProviderInterface
from quant_framework.strategies.strategy import Strategy as StrategyInterface
from quant_framework.internal.models import StrategyState, Strategy as StrategyModel, DataProvider as DataProviderModel
from quant_framework.internal.utils import db, strategy_loader


def run_backtest(strategy_name, data_provider_name, start, end):
    engine = db.get_engine()

    # Change the strategy state to BACKTEST in the database
    _update_strategy_record(engine, strategy_name, StrategyState.BACKTEST.value)

    # Create a context that holds important variables 
    context = {}
    context['current_timestamp'] = start

    # Fetch the data provider the user wants to use
    dp, init_kwargs = _extract_data_provider_class(engine, data_provider_name)
    context['data_provider'] = dp(**init_kwargs)

    # Assume tha the broker is always a mock broker for backtesting
    # We don't want to actually modify any paper or live portfolio for backtesting
    broker = MockBroker(context)
    context['broker'] = broker

    # Fetch the user-defined strategy class
    c = _extract_user_strategy_class(engine, strategy_name)
    user_strat = c(context)

    # Slice the current_timestamp range according to the interval of the strategy
    # The 'interval' should be cron syntax (i.e. '0 0 * * *')
    # The cronitor library creates an iterator where each 'next' value is a datetime
    # representing the next execution time
    it = croniter(user_strat.interval, start)

    # Call the built-in user-defind 'begin' function
    user_strat.begin(context)

    # At each interval's current_timestamp, call the strategy's 'update' function
    while context['current_timestamp'] < end:
        user_strat.update(context)
        context['current_timestamp'] = it.get_next(datetime)

    # Call the built-in user-defind 'finish' function
    user_strat.finish(context)

    # Change the strategy state to BACKTEST in the database
    _update_strategy_record(engine, strategy_name, StrategyState.IDLE.value)


def _extract_data_provider_class(engine, data_provider_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(DataProviderModel) \
        .filter(DataProviderModel.name == data_provider_name) \
        .first()

    # Fetch the module corresponding to the data provider class name
    dp_class = None
    for c in DataProviderInterface.__subclasses__():
        if c.__name__ == result.class_name:
            dp_class = c

    if dp_class is None:
        raise ValueError(f'No data provider class found with the name {data_provider_name}')

    # Parse the data provider init kwargs into a format usable by the
    # python init function
    return dp_class, result.init_kwargs


def _extract_user_strategy_class(engine, strategy_name):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(StrategyModel) \
        .filter(StrategyModel.name == strategy_name) \
        .first()

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
