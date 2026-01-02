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


Design Evolution

This project evolved from a script-based robot control implementation into a modular control framework.
The evolution was driven by engineering concerns such as extensibility, reproducibility, and failure isolation, rather than feature expansion.

Before: Script-Based Control

In the initial version, robot control logic was implemented as a single execution flow:

Input handling, control logic, and hardware communication were tightly coupled

A single input path controlled the entire system

Control behavior could only be evaluated during live execution

Debugging and comparison relied on manual observation

While functional, this structure suffered from:

Single-point failures

Limited scalability

Inability to reproduce or validate control behavior offline

After: Framework-Based Architecture

The refactored system introduces a modular framework architecture:

Input, control, transport, and validation are separated into independent layers

Each layer communicates through well-defined interfaces

Execution is decoupled from hardware via transport abstraction

All runs are logged and can be replayed deterministically

This evolution enables:

Safe extension without refactoring core logic

Offline replay and quantitative validation

Controlled experimentation independent of real-time hardware availability
