from typing import Tuple
from ..config import ANGLE_MIN, ANGLE_MAX

Angles = Tuple[float, float, float]

def clamp(x: float, lo: float = ANGLE_MIN, hi: float = ANGLE_MAX) -> float:
    try:
        x = float(x)
    except Exception:
        return lo
    return max(lo, min(hi, x))

class JointMappingController:
    """
    Minimal controller:
    - manual mode: uses user angles directly
    - vision mode: uses dx,dy to adjust a1,a2 (simple proportional mapping)
    Replace this with IK / constraints / smoothing later.
    """

    def __init__(self, base: Angles = (90.0, 90.0, 90.0), kx: float = 25.0, ky: float = 25.0):
        self.base = base
        self.kx = kx
        self.ky = ky

    def from_manual(self, a1: float, a2: float, a3: float) -> Angles:
        return (clamp(a1), clamp(a2), clamp(a3))

    def from_vision(self, dx_norm: float, dy_norm: float) -> Angles:
        # dx_norm, dy_norm expected in [-1, 1]
        a1 = self.base[0] + dx_norm * self.kx
        a2 = self.base[1] - dy_norm * self.ky
        a3 = self.base[2]
        return (clamp(a1), clamp(a2), clamp(a3))

    def from_replay(self, angles: Angles) -> Angles:
        return (clamp(angles[0]), clamp(angles[1]), clamp(angles[2]))
