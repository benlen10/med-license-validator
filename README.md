# med-license-validator

## Overview

Automatically validate medical licenses (EMT, RN, CPR/BLS, etc.) from a variety of sources

## Supported Licenses

- ESMA (California Emergency Medical Services Agency) EMT/A-EMT/Paramedic licenses
- AHA (American Heart Association) - BLS/CPR Certs
- ARC (American Red Cross) - BLS/CPR Certs
- DCA (California Department of Consumer Affairs) - RN, PT, etc.

## Usage Examples

- python3 validate.py EMT E142304
- python3 validate.py AHA 195506016954
- python3 validate.py ARC 10FMU9
- python3 validate.py DCA "G 50925" last_name DOEMENY
