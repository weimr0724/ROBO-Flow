import time
from typing import Optional, Tuple

from ..config import DT
from ..controllers.joint_mapping import JointMappingController
from ..transport.transport_base import Transport, Angles
from .logger import RunLogger

class ControlPipeline:
    """Orchestrates the control loop: Input -> Controller -> Transport -> Logger."""

    def __init__(self, mode: str, transport_name: str, transport: Transport,
                 input_source, controller: JointMappingController, logger: RunLogger):
        self.mode = mode
        self.transport_name = transport_name
        self.transport = transport
        self.input_source = input_source
        self.controller = controller
        self.logger = logger
        self.running = True

    def step(self):
        # 1) Get input
        inp = self.input_source.next()
        if inp is None:
            # No input frame available; keep last state.
            return

        # 2) Compute target angles
        if self.mode == "manual":
            a1, a2, a3 = inp
            target = self.controller.from_manual(a1, a2, a3)

        elif self.mode == "vision":
            dx_norm, dy_norm = inp
            target = self.controller.from_vision(dx_norm, dy_norm)

        elif self.mode == "replay":
            target = self.controller.from_replay(inp)

        else:
            raise ValueError(f"Unknown mode: {self.mode}")

        # 3) Send to transport
        self.transport.send(target, speed=100)

        # 4) Read feedback (optional)
        fb = self.transport.read_feedback()

        # 5) Log
        self.logger.write(target, fb)

    def run(self):
        """Run at ~50Hz (DT)."""
        try:
            while self.running:
                t0 = time.time()
                self.step()
                elapsed = time.time() - t0
                sleep_s = max(0.0, DT - elapsed)
                time.sleep(sleep_s)
        finally:
            self.logger.close()
            self.transport.close()
            self.input_source.close()
