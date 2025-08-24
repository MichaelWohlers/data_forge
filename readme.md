# Data Forge

A factory simulation system that generates machine data in a factory environment using design patterns.

## Overview

Data Forge provides a comprehensive factory simulation framework with the following key features:
- **ToDo**
  - Fix missing status in generate data
- **Machine Data Generation**: Creates customizable machine objects using a factory pattern
  - Simulates real-time machine data
  - Supports dynamic expansion to add new machine types without altering existing code
  - Enables realistic factory environment simulation

- **Data Pipeline Broadcasting**: Broadcasts machine data through TCP sockets
  - Emulates real factory networks by sending machine data via TCP sockets
  - Supports configurable port assignments for each machine enabling independent data streams
  - Simulates network behavior and integrates with an observer pattern
  - Provides scalable architecture

- **Data Collection**: Implements an observer pattern for data collection
  - Captures machine data in real-time
  - Enables flexible response to machine updates
  - Provides framework to analyze data from network inputs
  - Allows graceful handling of machine errors

- **Control System**: Uses a singleton pattern for centralized control
  - Centralizes simulation control to ensure one instance manages all machines and data collection
  - Prevents duplicate control logic, avoiding conflicts when starting or stopping the pipeline
  - Manages global settings like simulation speeds or error rates from a single point
  - Ensures consistent state across machines and collectors for reliable operation

## Core Concepts

### Machine
- **Attributes**: id, type, capabilities, config, state
- **Behaviors**: Generate telemetry tick, emit events, handle faults, apply control signals (start, stop, speed)

### Telemetry
- **Sample**: timestamp, machine id, metrics, status codes

### Network Stream
- **Endpoint**: host, port, protocol (TCP), serialization format (JSON), send policy (internal, batching)

### Collector (Observer)
- Subscribes to machine events/telemetry
- Processes updates
- Error handling
- Analytics hooks

### Control (Singleton)
- Global registry of machines and collectors
- Simulation clock and speed
- Error-rate knobs
- Lifecycle management (start, stop, pause)
- Configuration loading

## Machine Types

### Jet Printer

The Jet Printer machine type provides comprehensive monitoring of piezoelectric jetting processes with the following data streams:

#### 1. Piezoelectric Current Data
**Description**: Captures waveform parameters during actuation to predict deposit quality and detect inconsistencies like nozzle issues.

**Example Outputs**:
- **Rise time**: 10-20 µs (time for current to reach peak, indicating actuation speed)
- **Voltage level**: 50-100 V (applied to the piezo element for droplet ejection)
- **Current amplitude**: 2-5 A (peak current during the jetting pulse, with anomalies flagged if deviating by >5% from baseline)

**Polling Frequency**: Typically sampled per jetting event (e.g., at rates matching the jet frequency of 720,000-1,080,000 dots per hour, or about 200-300 dots per second). This allows near-real-time capture, but full waveform analysis may be batched for efficiency.

#### 2. Acoustic (Sound) Data
**Description**: Analyzes sounds emitted during jetting to identify anomalies like temperature shifts or supply failures, often processed via Fast Fourier Transform (FFT) for frequency insights.

**Example Outputs**:
- **Frequency spectrum**: Peaks at 1-5 kHz (normal jetting noise), with anomalies showing shifts to 6-10 kHz indicating issues like paste viscosity changes
- **Amplitude level**: 40-60 dB (sound intensity), where deviations >10 dB signal potential clogs or failures
- **FFT-derived features**: Energy in specific bands (e.g., 2-3 kHz band at 0.5-1.0 normalized energy units)

**Polling Frequency**: Captured per dot or short burst (e.g., every 1-5 jetting cycles, aligning with high-speed operations up to 300 dots/second). Processing is often non-real time to avoid interrupting production.

#### 3. Deposit Diameter and Drift
**Description**: Measures solder paste dot size and gradual deviations (drift) from targets, using vision systems to flag inconsistencies.

**Example Outputs**:
- **Diameter**: 330-640 µm (target range for a single dot, with drift detected if averaging window deviates by >3.3% from 500 µm baseline)
- **Drift threshold**: +15 µm over 100 dots (e.g., from 500 µm to 515 µm, triggering an alert via reconstruction error plots)
- **Circularity**: 0.95-1.0 (unitless score, where <0.9 indicates irregular shapes like satellites)

**Polling Frequency**: Assessed post-jetting via camera scans, often every few dots or per board (e.g., at resolutions supporting 720,000-1,080,000 dots/hour, or ~200-300 samples/second during active printing). Drift monitoring uses rolling averages over batches of 50-100 dots.

#### 4. Temperature Metrics
**Description**: Tracks ejector and ambient temperatures to monitor viscosity impacts on jetting performance.

**Example Outputs**:
- **Ejector temperature**: 25-35°C (optimal range, with anomalies if exceeding 40°C, correlating to viscosity drops)
- **Ambient variation**: ±2°C deviation (e.g., from 20°C baseline, triggering alerts for potential shear rate changes)
- **Viscosity proxy**: Derived drop in effective viscosity (e.g., from 100 Pa·s to 80 Pa·s due to +5°C rise)

**Polling Frequency**: Monitored continuously or at high intervals (e.g., every 1-10 seconds, or per jetting cycle in sync with 200-300 dots/second rates). This is often integrated with environmental controls for real-time adjustments.

#### 5. Other Quality Indicators
**Description**: Includes volume control, shape metrics, and defect counts from 3D imaging and statistical tests.

**Example Outputs**:
- **Deposit volume**: 5-35 nl (nanoliters per dot, with repeatability at ±10% for high-precision jobs)
- **Shape deviation**: Offset of 0-40 µm in X/Y (e.g., Cpk=1.0 accuracy at ±40 µm)
- **Satellite counts**: 0-2 per dot (unwanted secondary droplets, with increases of 50-100% flagged in high-resolution scans)

**Polling Frequency**: Evaluated per dot or pattern (e.g., during or after jetting at speeds up to 1,080,000 dots/hour, or ~300 samples/second). Statistical metrics like hypothesis testing (e.g., t-values for volume means) are computed in batches post-production for anomaly review.

### Other Machine Types
- **Conveyor**
- **Pick-and-Place**
- **Convection Oven**
- **Vapor Phase Oven**
- **Automated Optical Inspection**
- **Auto Loader**