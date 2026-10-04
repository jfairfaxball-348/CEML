# Configuration

No scientific or local machine configuration is frozen at bootstrap.

Future versioned configuration may include:

- frozen scientific protocol identifiers;
- non-secret generator/rung settings after R3;
- `local_machine_profile.toml` or equivalent after C1;
- build/profile identifiers;
- validation ceilings/cadence where appropriate.

Do not place secrets, raw host identifiers, or mutable ad-hoc overrides here.

Once a scientific rung starts, material configuration changes require a new protocol/build/profile version; silent recalibration is prohibited.
