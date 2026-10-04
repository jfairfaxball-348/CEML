# Configuration

CEML-I1 freezes configuration formats, not machine values.

- `calibration_suite_v1.json` is the public, non-scientific CEML-CAL-1 bounded calibration definition.
- `local_machine_profile.json` is created only during an authorized C1 after local audit, bounded calibration, engineering decisions and build provenance exist. Its schema is `schemas/hardware_profile.schema.json`.
- Ecosystem-native lock files and the selected dependency pin/digest manifest are added by C1 for the chosen implementation family.

Do not place secrets, usernames, hostnames, device identifiers, raw inventories or mutable ad-hoc overrides here.

The scientific seed, scientific starts and final ladder are not configuration inputs to C1. Material changes to a frozen C1 build/profile create a new build/profile identity and require affected calibration and later V1 evidence to be regenerated.
