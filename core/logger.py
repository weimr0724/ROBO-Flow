import os
import csv
import time
from typing import Tuple, Optional

Angles = Tuple[float, float, float]

class RunLogger:
    """
    Writes a standard CSV log for validation and replay.
    Columns:
      t_sec,target_a1,target_a2,target_a3,actual_a1,actual_a2,actual_a3,mode,transport
    """

    def __init__(self, log_dir: str, mode: str, transport: str):
        os.makedirs(log_dir, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        self.path = os.path.join(log_dir, f"run_{ts}.csv")
        self.t0 = time.time()
        self.mode = mode
        self.transport = transport

        self.f = open(self.path, "w", newline="", encoding="utf-8")
        self.w = csv.writer(self.f)
        self.w.writerow([
            "t_sec",
            "target_a1","target_a2","target_a3",
            "actual_a1","actual_a2","actual_a3",
            "mode","transport"
        ])
        self.f.flush()

    def write(self, target: Angles, actual: Optional[Angles]):
        t_sec = time.time() - self.t0
        if actual is None:
            actual = target  # fallback for ideal/sim mode

        self.w.writerow([
            f"{t_sec:.4f}",
            f"{target[0]:.3f}", f"{target[1]:.3f}", f"{target[2]:.3f}",
            f"{actual[0]:.3f}", f"{actual[1]:.3f}", f"{actual[2]:.3f}",
            self.mode, self.transport
        ])
        # flush for crash-resilience
        self.f.flush()

    def close(self):
        try:
            self.f.close()
        except Exception:
            pass
