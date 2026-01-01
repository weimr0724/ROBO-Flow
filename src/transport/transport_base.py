from abc import ABC, abstractmethod
from typing import Optional, Tuple

Angles = Tuple[float, float, float]

class Transport(ABC):
    """Abstract transport interface (Serial, Simulator, TCP, etc.)."""

    @abstractmethod
    def send(self, angles: Angles, speed: int = 100) -> None:
        pass

    @abstractmethod
    def read_feedback(self) -> Optional[Angles]:
        """Return (a1,a2,a3) if available; otherwise None."""
        pass

    @abstractmethod
    def close(self) -> None:
        pass
