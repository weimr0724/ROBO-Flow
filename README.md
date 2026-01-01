# ROBO-Flow
A Reproducible Robot Control
# RoboFlow

**RoboFlow** is a modular and reproducible robot control framework prototype,  
designed to explore control, replay, and validation workflows for robotic arms.

This project focuses on **engineering practices**—modularity, logging, replayability,
and quantitative validation—rather than production deployment.

---

## Key Features

- **Modular Framework Design**
  - Decoupled input, control, and transport layers
  - Easy to extend with new input sources or execution backends

- **Multiple Control Modes**
  - `manual`: real-time manual control
  - `replay`: replay recorded control logs
  - `vision` (optional): vision-based control input

- **Reproducible Logging**
  - Every run generates a timestamped CSV log
  - Logs can be replayed and validated deterministically

- **Post-run Validation**
  - Automatic MAE / Max Absolute Error computation
  - Target vs Actual and Error plots generated from logs

---

## Project Structure

```text
ROBO-Flow/
├─ src/
│  ├─ controllers/     # Control logic (e.g. joint mapping)
│  ├─ core/            # Pipeline and logger
│  ├─ inputs/          # Manual / Replay / Vision inputs
│  ├─ transport/       # Simulation or serial transport
│  ├─ run.py           # Framework entry point
│  ├─ validate.py      # Post-run validation & plotting
│  └─ config.py
├─ logs/               # Generated run_*.csv logs
├─ validation_out/     # Validation plots (auto-generated)
└─ README.md
