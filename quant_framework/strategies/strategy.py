from abc import ABC, abstractmethod
from enum import Enum


class RunMode(Enum):
    BACKTEST = 0
    PAPER = 1
    LIVE = 2


class Strategy(ABC):
    @property
    @abstractmethod
    def name(self):
        pass
    
    @property
    @abstractmethod
    def description(self):
        pass
    
    @property
    @abstractmethod
    def interval(self):
        pass
    
    @property
    @abstractmethod
    def run_mode(self):
        """
        Must be a value from the RunMode enum
        """
        pass

    @abstractmethod
    def begin(self, timestamp):
        """
        Run once at the beginning of the strategy execution
        """
        pass

    @abstractmethod
    def update(self, timestamp):
        """
        Re-run for each `interval` window
        """
        pass

    @abstractmethod
    def finish(self, timestamp):
        """
        Run once upon completion of the strategy execution
        """
        pass
