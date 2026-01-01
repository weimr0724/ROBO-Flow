from typing import Optional, Tuple
import time

try:
    import serial
except Exception:
    serial = None

from .transport_base import Transport, Angles
from ..config import SERIAL_TIMEOUT

def clamp(x: float, lo: float = 0.0, hi: float = 180.0) -> float:
    try:
        x = float(x)
    except Exception:
        return lo
    return max(lo, min(hi, x))

def parse_feedback_line(line: str) -> Optional[Angles]:
    """
    Expected feedback example: F,90,90,90
    """
    try:
        line = line.strip()
        if not line:
            return None
        if line.startswith("F"):
            parts = line.split(",")
            if len(parts) >= 4:
                return (float(parts[1]), float(parts[2]), float(parts[3]))
        return None
    except Exception:
        return None

class SerialTransport(Transport):
    """Serial backend: sends targets and reads optional feedback."""

    def __init__(self, port: str, baud: int = 115200):
        if serial is None:
            raise RuntimeError("pyserial is not installed. Run: pip install pyserial")

        self.ser = serial.Serial(port, baud, timeout=SERIAL_TIMEOUT)
        time.sleep(1.0)  # allow MCU to reset
        self._last_sent: Angles = (90.0, 90.0, 90.0)

    def send(self, angles: Angles, speed: int = 100) -> None:
        a1, a2, a3 = (clamp(angles[0]), clamp(angles[1]), clamp(angles[2]))
        self._last_sent = (a1, a2, a3)
        msg = f"T,{a1:.2f},{a2:.2f},{a3:.2f},{int(speed)}\n"
        try:
            self.ser.write(msg.encode("utf-8"))
        except Exception:
            pass

    def read_feedback(self) -> Optional[Angles]:
        try:
            if self.ser.in_waiting <= 0:
                return None
            line = self.ser.readline().decode("utf-8", errors="ignore")
            return parse_feedback_line(line)
        except Exception:
            return None

    def close(self) -> None:
        try:
            self.ser.close()
        except Exception:
            pass
