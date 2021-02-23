import dateutil.parser
import json

from flask import Flask, request
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from quant_framework.internal.models import Strategy, DataProvider
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
            results_fmt.append(result.as_dict())

        return json.dumps(results_fmt)

    @flask_app.route('/api/data-provider', methods=['POST'])
    def create_data_provider():
        data_provider_name = request.json['name']
        class_name = request.json['class_name']
        init_kwargs = request.json['init_kwargs']
        
        with engine.connect() as conn:
            insert_stmt = insert(DataProvider).values(
                name=data_provider_name,
                class_name=class_name,
                init_kwargs=init_kwargs
            )
            conn.execute(insert_stmt)

        return {"success": True}

    
    @flask_app.route('/api/backtest', methods=['POST'])
    def trigger_backtest():
        strategy_name = request.json['strategy']
        data_provider_name = request.json['data_provider']
        start = dateutil.parser.parse(request.json['start'])
        end = dateutil.parser.parse(request.json['end'])
        
        backtest.run_backtest(strategy_name=strategy_name, data_provider_name=data_provider_name, start=start, end=end)

        return {"success": True}

    return flask_app
