from abc import ABC, abstractmethod

class BaseAgent(ABC):
    @abstractmethod
    def run(self, input_data=None):
        """Execute the agent's task"""
        pass
