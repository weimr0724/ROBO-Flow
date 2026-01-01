from typing import Optional, Tuple
import time
import pandas as pd

Angles = Tuple[float, float, float]

class ReplayInput:
    """
    Replays target angles from a CSV log.
    Expected columns:
      t_sec (optional), target_a1,target_a2,target_a3
    """

    def __init__(self, csv_path: str, speed: float = 1.0, fallback_dt: float = 0.02):
        self.df = pd.read_csv(csv_path)
        self.i = 0
        self.speed = max(0.1, float(speed))
        self.fallback_dt = fallback_dt

        self.has_t = "t_sec" in self.df.columns
        self.t0 = float(self.df["t_sec"].iloc[0]) if self.has_t else 0.0
        self.prev_t = None
        self.last_tick = time.time()

    def next(self) -> Optional[Angles]:
        if self.i >= len(self.df):
            return None

        row = self.df.iloc[self.i]

        # pacing
        if self.has_t:
            t = float(row["t_sec"] - self.t0)
            if self.prev_t is None:
                self.prev_t = t
            dt = max(0.0, (t - self.prev_t) / self.speed)
            time.sleep(dt)
            self.prev_t = t
        else:
            # fixed pace
            time.sleep(self.fallback_dt / self.speed)

        a1 = float(row["target_a1"])
        a2 = float(row["target_a2"])
        a3 = float(row["target_a3"])
        self.i += 1
        return (a1, a2, a3)

    def close(self):
        pass
