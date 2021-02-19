import dateutil.parser
import json

from flask import Flask, request
from sqlalchemy.orm import sessionmaker

from quant_framework.internal.models import Strategy
from quant_framework.internal.utils import backtest


def create_app(engine):
    flask_app = Flask(__name__)

    # Define the API routes
    # TODO: Refactor this after we get too many APIs

    @flask_app.route('/api/strategies', methods=['GET'])
    def strategies():
        Session = sessionmaker(bind=engine)
        session = Session()

        results = session.query(Strategy).all()

        # Convert results to a list of dictionaries
        results_fmt = []
        for result in results:
            result_dict = result.__dict__
            result_dict.pop('_sa_instance_state', None)
            results_fmt.append(result_dict)

        return json.dumps(results_fmt)
    
    @flask_app.route('/api/backtest', methods=['POST'])
    def trigger_backtest():
        strategy_name = request.json['name']
        start = dateutil.parser.parse(request.json['start'])
        end = dateutil.parser.parse(request.json['end'])
        
        backtest.run_backtest(engine=engine, strategy_name=strategy_name, start=start, end=end)

        return {"success": True}

    return flask_app
