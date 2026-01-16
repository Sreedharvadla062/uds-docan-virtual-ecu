# Project Documentation

## Architecture Overview

```
┌─────────────────────────────────────────┐
│       Diagnostic Client/Scanner         │
└─────────────────────┬───────────────────┘
                      │ UDS Requests
                      ▼
┌─────────────────────────────────────────┐
│      Virtual ECU (Main Controller)      │
│  ┌───────────────────────────────────┐  │
│  │   UDS Protocol Handler (0x10-0x3E)   │
│  ├───────────────────────────────────┤  │
│  │  - Session Control               │  │
│  │  - Security Access               │  │
│  │  - DTC Management                │  │
│  │  - Data Identifier R/W           │  │
│  └───────────────────────────────────┘  │
└─────────────────────┬───────────────────┘
                      │ UDS/DoCAN Frames
                      ▼
┌─────────────────────────────────────────┐
│      DoCAN Bus (ISO 15765-2 Layer)      │
│  ┌───────────────────────────────────┐  │
│  │  Frame Formatting & Fragmentation │  │
│  │  - Single Frame (SF)              │  │
│  │  - First Frame (FF)               │  │
│  │  - Consecutive Frame (CF)         │  │
│  │  - Flow Control (FC)              │  │
│  └───────────────────────────────────┘  │
└─────────────────────┬───────────────────┘
                      │ CAN Messages
                      ▼
                    CAN Bus
```

## Module Description

### UDS Protocol (`uds_protocol.py`)

Implements ISO 14229-1 Unified Diagnostic Services protocol.

**Key Classes:**
- `UDSProtocol`: Main protocol handler

**Supported Services:**
- Diagnostic Session Control (0x10)
- ECU Reset (0x11)
- Security Access (0x27)
- Read/Write Data By Identifier (0x22, 0x2E)
- Read DTC Information (0x19)
- Tester Present (0x3E)

### DoCAN Bus (`docan_bus.py`)

Implements ISO 15765-2 transport layer.

**Key Classes:**
- `DoCAN`: Frame formatting and parsing

**Supported Frames:**
- Single Frame: Up to 7 bytes
- First Frame: Initiates multi-frame transfer
- Consecutive Frame: Continuation frames
- Flow Control: Manages frame transfers

### Virtual ECU (`virtual_ecu.py`)

Simulates an ECU with full diagnostics capabilities.

**Key Classes:**
- `VirtualECU`: Main ECU simulator

**Features:**
- Data identifier management
- DTC storage and retrieval
- Session management
- Request/response handling

## Getting Started

### Installation

```bash
git clone https://github.com/Sreedharvadla062/uds-docan-virtual-ecu.git
cd uds-docan-virtual-ecu
pip install -r requirements.txt
```

### Basic Usage

```python
from src.virtual_ecu import VirtualECU

# Create ECU
ecu = VirtualECU("ECU_001")

# Configure
ecu.set_data_identifier(0x0102, b"v1.0.0")

# Process request
request = bytes([0x01, 0x3E])  # Tester Present
response = ecu.process_request(request)
```

### Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v --cov=src
```

## Protocol Flow

### Diagnostic Session

1. **Initiate Session**: Client sends Diagnostic Session Control (0x10)
2. **Keep Alive**: Regular Tester Present (0x3E) messages
3. **Read Data**: Client reads data identifiers (0x22)
4. **Read DTCs**: Client retrieves diagnostic codes (0x19)
5. **Exit Session**: Client disconnects

### Multi-Frame Transfer

For data > 7 bytes:

1. **FF (First Frame)**: Header + first 6 bytes
2. **CF (Consecutive Frames)**: Sequence numbers + 7 bytes each
3. **FC (Flow Control)**: Controls transfer speed

## Common Responses

| Response | Meaning |
|----------|---------|
| `0x7E` | Positive Tester Present |
| `0x50` | Positive Session Control |
| `0x62` | Positive Read DID |
| `0x7F` | Negative Response |
| `0x7F 0x12` | Service Not Supported |
| `0x7F 0x13` | Incorrect Message Length |

## Roadmap

- [ ] Add CAN bus integration (python-can)
- [ ] Implement security access algorithms
- [ ] Add routine control services
- [ ] Support file transfer (download/upload)
- [ ] Add performance metrics
- [ ] Create GUI interface
- [ ] Add real-time logging

## References

- ISO 14229-1: Road vehicles - Unified diagnostic services (UDS)
- ISO 15765-2: Road vehicles - Diagnostic communication over CAN
- SAE J2534: Recommended Practice for Pass-Thru Device Programming
