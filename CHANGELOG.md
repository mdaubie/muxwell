## v0.9.1 (2026-05-04)

### Bug Fixes

- escape file paths to render potential brackets (#127)
- **mkv**: include track filepath in change detection (#121)

## v0.9.0 (2026-05-03)

### Features

- **apply**: ignore case when matching subs (#69)

### Bug Fixes

- **operations**: move operations ordering to engine (#64)

### Tests

- **operations**: cover existing ops (#93)

## v0.8.0 (2026-03-02)

### Features

- **subtitles**: add command with shift subcommand (#59)
- **apply**: add auto match subs option (#30)

### Bug Fixes

- **apply**: properly handle errors/warnings (#31)

### Tests

- cover mkv wrapper (#32)
- add coverage (#29)

## v0.7.0 (2026-02-08)

### Features

- **apply**: add infer title option (#28)
- add Python 3.10 and 3.11 support (#26)

## v0.6.0 (2026-02-06)

### Features

- add Python 3.12 support (#25)
- **apply**: add set/unset default options (#21)

### Tests

- **info**: add info command tests (#24)
- **apply**: add apply command tests (#23)
- **core**: setup tests (#22)

## v0.5.0 (2026-02-05)

### Features

- **core**: add recursive mode (#17)
- **apply**: add remove track option (#15)

## v0.4.0 (2026-02-05)

### Features

- **apply**: implement set track language operation (#8)
- **apply**: implement add subtitle operation (#7)

### Bug Fixes

- **apply**: validate extension when adding subs (#9)

## v0.3.0 (2026-02-04)

### Performance Improvements

- **engine**: Mux only modified videos (#2)

## v0.3.0b1 (2026-02-04)

### Bug Fixes

- **core**: ensure single video files are properly collected (#6)

## v0.3.0b0 (2026-02-03)

### Features

- **apply**: add apply command with set title action
- **core**: add engine, setup actions and operations

## v0.2.0 (2026-02-03)

### Features

- **info**: add info command
- **core**: Setup cli

## v0.1.0 (2026-01-30)
