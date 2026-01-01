import argparse
import os
import glob
import pygame

from .config import LOG_DIR, DEFAULT_PORT, DEFAULT_BAUD, REPLAY_DEFAULT_SPEED, REPLAY_DEFAULT_DT
from .controllers.joint_mapping import JointMappingController
from .core.logger import RunLogger
from .core.pipeline import ControlPipeline
from .transport.sim_transport import SimTransport
from .transport.serial_transport import SerialTransport
from .inputs.manual_input import ManualInput
from .inputs.replay_input import ReplayInput
from .inputs.vision_input import VisionInput


def latest_run_csv(log_dir: str = LOG_DIR):
    files = glob.glob(os.path.join(log_dir, "run_*.csv"))
    return max(files, key=os.path.getmtime) if files else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["manual", "replay", "vision"], default="manual")
    ap.add_argument("--transport", choices=["sim", "serial"], default="sim")

    ap.add_argument("--port", default=DEFAULT_PORT)
    ap.add_argument("--baud", type=int, default=DEFAULT_BAUD)

    ap.add_argument("--file", default=None, help="Replay CSV file")
    ap.add_argument("--latest", action="store_true", help="Replay latest log in logs/")
    ap.add_argument("--speed", type=float, default=REPLAY_DEFAULT_SPEED, help="Replay speed")
    args = ap.parse_args()

    # pygame is used for event loop (manual mode) and clean QUIT handling.
    pygame.init()
    pygame.display.set_mode((320, 120))
    pygame.display.set_caption("Robot Control Framework Prototype")

    # Transport
    if args.transport == "sim":
        transport = SimTransport()
    else:
        transport = SerialTransport(port=args.port, baud=args.baud)

    # Input source
    if args.mode == "manual":
        input_source = ManualInput()

    elif args.mode == "replay":
        path = args.file
        if args.latest:
            path = latest_run_csv(LOG_DIR)
        if not path:
            raise RuntimeError("Replay mode requires --file <csv> or --latest")
        input_source = ReplayInput(path, speed=args.speed, fallback_dt=REPLAY_DEFAULT_DT)

    elif args.mode == "vision":
        input_source = VisionInput(show=True)

    else:
        raise ValueError("Unknown mode")

    # Controller + logger + pipeline
    controller = JointMappingController()
    logger = RunLogger(LOG_DIR, mode=args.mode, transport=args.transport)
    pipeline = ControlPipeline(
        mode=args.mode,
        transport_name=args.transport,
        transport=transport,
        input_source=input_source,
        controller=controller,
        logger=logger
    )

    print(f"[OK] Running framework mode={args.mode}, transport={args.transport}")
    print(f"[OK] Logging to: {logger.path}")
    print("[INFO] Close the window or press ESC (manual) / 'q' (vision) to stop.")

    try:
        pipeline.run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
