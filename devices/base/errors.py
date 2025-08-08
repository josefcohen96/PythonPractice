"""
Standard device-related exception names.
Implementations of devices should raise these
to signal specific, expected error conditions.
"""

class DeviceError(Exception):
    """Base class for all device-related errors."""

class DeviceTimeout(DeviceError):
    """No response from device within allowed time."""

class CapabilityMissing(DeviceError):
    """Attempted operation not in device capabilities."""

class OutOfRange(DeviceError):
    """Provided value is outside allowed range for this device."""

class DeviceBusy(DeviceError):
    """Device is currently busy and cannot perform the requested operation."""

class ProtocolError(DeviceError):
    """Unexpected or invalid data/protocol from device."""
