import argparse

from datetime import datetime, timedelta

from quant_framework.strategies.mock_buy_and_hold import MockBuyAndHold, RunMode

strategies = {
    'mock_buy_and_hold': MockBuyAndHold()
}

def main():
    parser = argparse.ArgumentParser(description='Using the quant framework to run a specified strategy')
    parser.add_argument('strategy', help='The name of the strategy we want to run')
    parser.add_argument('--start-date', required=True, help='The start date of the backtest in the format YYYY-mm-dd')
    parser.add_argument('--end-date', required=True, help='The end date of the backtest in the format YYYY-mm-dd')
    parser.add_argument('--interval', required=True, type=int,
                        help='The number of days to wait between portfolio rebalancing attempts')

    args = parser.parse_args()
    strategy = strategies[args.strategy]
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
    interval = args.interval

    # Execute the strategy
    strategy.begin(start_date)
    delta = end_date - start_date

    for i in range(0, delta.days + 1, interval):
        day = start_date + timedelta(i)
        strategy.update(day)

    strategy.finish(end_date)