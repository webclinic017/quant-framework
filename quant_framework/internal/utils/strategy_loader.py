import hashlib
import importlib.machinery
import os
import sys

from quant_framework.strategies.strategy import Strategy as StrategyInterface
from quant_framework.internal.models import Strategy as StrategyModel


def fetch_strategies_from_directory(strategy_directory):
    '''
    Traverses the specified strategy_directory, and returns every class that inherits from the 'Strategy' interface
    '''

    for f in os.listdir(strategy_directory):
        if f.endswith('.py'):
            module_name = f[:-3]  # chop off the .py extension
            if module_name in sys.modules.keys():
                continue  # we've already loaded this module, so no reason to repeat

            path = os.path.join(strategy_directory, f)

            # Import the python module in a generic fashion
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)

    # Get all user-defined classes that inherit from the quant framework 'Strategy' abstract class,
    # and convert these to an array of Strategy Models that can be written to the database
    strat_models = []
    for c in StrategyInterface.__subclasses__():
        file_path = os.path.abspath(sys.modules[c.__module__].__file__)

        strat_models.append(StrategyModel(
            name=c.name,
            description=c.description,
            interval=c.interval,
            class_name=c.__name__,
            file_path=file_path,
            fingerprint=_generate_fingerprint(file_path)
        ))
    
    return strat_models


def _generate_fingerprint(file_path):
    '''
    Takes a specified strategy class and crates a fingerprint from the contents of the strategy
    This is really just a simple hashing of the entire contents of the strategy file. In this way,
    we will be able to detect when the logic of a strategy changes, as its fingrprint will have changed
    '''
    BUF_SIZE = 65536  # read as 64 kb chunks

    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            
            sha1.update(data)

    return sha1.hexdigest()