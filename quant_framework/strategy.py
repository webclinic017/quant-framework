from abc import ABC, abstractmethod


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

    @abstractmethod
    def begin(self, timestamp):
        '''
        Run once at the beginning of the strategy execution
        '''
        pass

    @abstractmethod
    def update(self, timestamp):
        '''
        Re-run for each `interval` window
        '''
        pass

    @abstractmethod
    def finish(self, timestamp):
        '''
        Run once upon completion of the strategy execution
        '''
        pass
