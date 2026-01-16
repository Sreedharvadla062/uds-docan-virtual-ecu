# uds-docan-virtual-ecu

UDS (ISO 14229) client/server diagnostics over DoCAN (ISO 15765-2) using SocketCAN

## Overview

This project implements a Virtual ECU (Electronic Control Unit) with support for UDS (Unified Diagnostic Services) protocol over DoCAN (Diagnostic Communication over CAN) bus. It's designed for automotive diagnostics simulation, testing, and development.

### Features

- **UDS Protocol Support**: Full implementation of ISO 14229 UDS services
- **DoCAN Bus**: ISO 15765-2 compliant transport layer
- **Virtual ECU**: Simulated ECU with diagnostic capabilities
- **Multi-frame Support**: Handling of single and multi-frame CAN messages
- **Service Support**: 
  - Diagnostic Session Control
  - ECU Reset
  - Security Access
  - Read/Write Data by Identifier
  - Read DTC Information
  - Tester Present
  - And more...

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Sreedharvadla062/uds-docan-virtual-ecu.git
cd uds-docan-virtual-ecu
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package (optional):
```bash
pip install -e .
```

## Project Structure

```
uds-docan-virtual-ecu/
├── src/
│   ├── __init__.py
│   ├── uds_protocol.py      # UDS protocol implementation
│   ├── docan_bus.py         # DoCAN bus implementation
│   └── virtual_ecu.py       # Virtual ECU implementation
├── tests/                    # Unit tests
├── docs/                     # Documentation
├── examples/                 # Example usage
├── setup.py                  # Package setup
├── requirements.txt          # Dependencies
└── README.md
```

## Quick Start

### Basic Virtual ECU Usage

```python
from src.virtual_ecu import VirtualECU

# Create a virtual ECU
ecu = VirtualECU("ECU_001")

# Set data identifiers
ecu.set_data_identifier(0x0102, b"\x12\x34\x56\x78")

# Process a UDS request
request = b"\x3E"  # Tester Present
response = ecu.process_request(request)
print(f"Response: {response.hex()}")
```

## UDS Services

Supported UDS Services (SID):

| Service | Code | Description |
|---------|------|-------------|
| Diagnostic Session Control | 0x10 | Control diagnostic sessions |
| ECU Reset | 0x11 | Reset the ECU |
| Security Access | 0x27 | Unlock security levels |
| Read Data By Identifier | 0x22 | Read DIDs |
| Write Data By Identifier | 0x2E | Write DIDs |
| Routine Control | 0x31 | Control routines |
| Request Download | 0x34 | Initiate download |
| Request Upload | 0x35 | Initiate upload |
| Transfer Data | 0x36 | Transfer data |
| Tester Present | 0x3E | Keep-alive signal |
| Read DTC Information | 0x19 | Read DTCs |
| Clear Diagnostic Information | 0x14 | Clear DTCs |

## Development

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type checking
mypy src/
```

## DoCAN Frame Format

### Single Frame
```
Byte 0: [Frame Type (4 bits) | Length (4 bits)]
Bytes 1-7: Data (up to 7 bytes)
```

### First Frame
```
Bytes 0-1: [Frame Type (4 bits) | Length MSB (4 bits) | Length LSB]
Bytes 2-7: Data (6 bytes)
```

### Consecutive Frame
```
Byte 0: [Frame Type (4 bits) | Sequence Number (4 bits)]
Bytes 1-7: Data (up to 7 bytes)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- ISO 14229-1: Road vehicles - Unified diagnostic services (UDS)
- ISO 15765-2: Road vehicles - Diagnostic communication over Controller Area Network (DoCAN)
- CAN Bus (Controller Area Network) Specifications
