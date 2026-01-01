# Centralized configuration for the framework (single source of truth).

CONTROL_HZ = 50
DT = 1.0 / CONTROL_HZ

# Angle limits (degrees)
ANGLE_MIN = 0.0
ANGLE_MAX = 180.0

# Logging
LOG_DIR = "logs"

# Replay
REPLAY_DEFAULT_SPEED = 1.0  # 1.0 = real-time-ish
REPLAY_DEFAULT_DT = 0.02    # fallback dt if no t_sec column

# Vision defaults
VISION_CAM_INDEX = 0
VISION_WIDTH = 640
VISION_HEIGHT = 480

# Serial defaults
DEFAULT_PORT = "COM4"
DEFAULT_BAUD = 115200
SERIAL_TIMEOUT = 0.0  # non-blocking-ish
