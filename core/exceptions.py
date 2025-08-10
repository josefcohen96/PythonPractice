"""Custom exceptions for the signal_lab project.

Having a dedicated exceptions module makes it easy to catch and
handle specific errors raised by instrument classes without relying on
built‑in exceptions.  This improves the clarity of error handling code.
"""


class InstrumentError(Exception):
    """Base class for instrument‑related errors."""
    pass


class ConnectionError(InstrumentError):
    """Raised when an instrument fails to connect or disconnect."""
    pass


class RangeError(InstrumentError):
    """Raised when a value is outside the allowable range for an instrument."""
    pass


class InstrumentValueError(InstrumentError):
    """Value error specific to instrument configuration/usage."""
    pass

class CapabilityMissing(InstrumentError):
    """"""
    pass

class DeviceError(InstrumentError):
    """"""
    pass

class DeviceTimeout(InstrumentError):
    """"""
    pass

class ProtocolError(InstrumentError):
    """"""
    pass
