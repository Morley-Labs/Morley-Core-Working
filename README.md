
# Morley-Core-Working

This repository contains working compiler components for the Morley Ladder Logic to Plutus Compiler. 

## Overview
Morley is a Ladder Logic-based smart contract language designed for Cardano. This repo includes:
- Ladder Logic Parser
- Intermediate Representation (IR) Generator
- IR Validator
- IR to Plutus Compiler
- Plutus Mappings

## Current Status
All components in this repository are functional and have passed validation tests. Broken or in-progress components are stored in a separate repository.

## Directory Structure
```
morley_core_working/
│
├── mappings/
│   ├── ladder_logic.json
│   ├── instruction_set.json
│   ├── structured_text.json
│   └── ir_to_plutus/
│       ├── ir_to_plutus_arithmetic.json
│       ├── ir_to_plutus_logical.json
│       ├── ir_to_plutus_timers.json
│       └── ir_to_plutus_counters.json
│
├── ladder_logic_parser.py
├── ir_validator.py
├── ir_to_plutus_compiler.py
└── __init__.py
```

## Usage
```bash
# Run the full compilation flow
python -m morley_compiler.ir_to_plutus_compiler
```

## Contributing
Pull requests and issues are welcome. This project is actively maintained by Morley-Labs.

## License
Apache 2.0
