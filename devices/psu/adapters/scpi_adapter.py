from .interface import PSUAdapterInterface


class SCPI_PSUAdapter(PSUAdapterInterface):
    def __init__(self, host: str, port: int) -> None:
        pass

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    def read_voltage(self) -> float:
        pass

    def read_current(self) -> float:
        pass

    def read_temp(self) -> float:
        pass

    def read_output(self) -> bool:
        pass

    def set_voltage(self, value: float) -> None:
        pass

    def set_current_limit(self, value: float) -> None:
        pass

    def output_on(self) -> None:
        pass

    def output_off(self) -> None:
        pass

    def power_cycle(self) -> None:
        pass
