from typing import Optional, Tuple
from .transport_base import Transport, Angles

class SimTransport(Transport):
    """A safe simulator transport that echoes targets as feedback."""

    def __init__(self):
        self.last_sent: Angles = (90.0, 90.0, 90.0)

    def send(self, angles: Angles, speed: int = 100) -> None:
        self.last_sent = angles

    def read_feedback(self) -> Optional[Angles]:
        # In sim mode, feedback is identical to the last target.
        return self.last_sent

    def close(self) -> None:
        pass
