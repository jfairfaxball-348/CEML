# Local Environment Plan

Status: **Planning only**

CEML is designed for eventual sustained execution on one dedicated laptop or workstation without requiring internet connectivity during a scientific run.

## C1 responsibilities

The local implementation phase must determine, from actual inspection and bounded testing:

- suitable mains-power configuration;
- sleep/hibernation settings that prevent accidental suspension;
- thermal-management practices;
- safe RAM utilization;
- whether swap should be disabled, limited, or tolerated;
- minimum SSD free-space reserve;
- local log rotation;
- checkpoint retention/rotation;
- graceful shutdown procedure;
- resume procedure after planned or unplanned interruption.

## Offline requirement

Scientific execution must not depend on cloud services, remote APIs, package downloads, telemetry, or a network connection. All dependencies and validation assets required for a run must be present locally before E1.

## Sensitive state

Large exact states, checkpoints, raw hardware reports before sanitization, and detailed runtime logs live under ignored local paths. Only compact approved artifacts, sanitized profiles, hashes, schemas, source, and reports are committed.

## Reproducibility

The machine profile must record enough non-sensitive information to explain performance and reproduce the build configuration. It must not attempt to fingerprint the owner or machine beyond scientific necessity.
