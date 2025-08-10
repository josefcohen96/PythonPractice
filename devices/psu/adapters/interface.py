from abc import ABC, abstractmethod

class AdapterInterface(ABC):
    @abstractmethod
    def connect(self) -> None: 
        """"""
    @abstractmethod
    def disconnect(self) -> None: 
        """"""
    @abstractmethod
    def is_connected(self) -> bool:
        """"""


    # reads
    # @abstractmethod
    # def read_voltage(self) -> float: 
    #     """"""
    # @abstractmethod
    # def read_current(self) -> float: 
    #     """"""
    # @abstractmethod
    # def read_temp(self) -> float: 
    #     """"""
    # @abstractmethod
    # def read_output(self) -> bool: 
    #     """"""