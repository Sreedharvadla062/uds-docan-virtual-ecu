# Troubleshooting Guide

## UDS DoCAN Virtual ECU - Common Issues & Solutions

### Table of Contents
1. [Installation Issues](#installation-issues)
2. [Import & Runtime Errors](#import--runtime-errors)
3. [Test Failures](#test-failures)
4. [Performance Issues](#performance-issues)
5. [Data & State Issues](#data--state-issues)
6. [Debugging Tips](#debugging-tips)

---

## Installation Issues

### ❌ Error: `ModuleNotFoundError: No module named 'pip'`

**Symptoms:** Cannot install packages

**Solutions:**
```bash
# Windows
python -m ensurepip --default-pip

# Linux/macOS
python3 -m pip install --upgrade pip
```

---

### ❌ Error: `No such file or directory: 'python'`

**Symptoms:** Python command not found

**Solutions:**
```bash
# Check Python installation
python --version
# or
python3 --version

# Windows: Add Python to PATH
set PATH=%PATH%;C:\Python311\

# Linux/macOS: Create alias
alias python=python3
```

---

### ❌ Error: `Permission denied` on Linux/macOS

**Symptoms:** Cannot access files or run scripts

**Solutions:**
```bash
# Fix permissions
chmod +x *.py
chmod 755 -R src/

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

---

## Import & Runtime Errors

### ❌ Error: `ModuleNotFoundError: No module named 'src'`

**Symptoms:**
```
ModuleNotFoundError: No module named 'src'
  File "examples/basic_example.py", line 3, in <module>
    from src.virtual_ecu import VirtualECU
```

**Solutions:**

**Option 1: Install as development package**
```bash
pip install -e .
```

**Option 2: Run from project root**
```bash
cd /path/to/uds-docan-virtual-ecu
python examples/basic_example.py
```

**Option 3: Set PYTHONPATH**
```bash
# Windows
set PYTHONPATH=%PYTHONPATH%;C:\path\to\project

# Linux/macOS
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

---

### ❌ Error: `ValueError: Single frame data must be <= 7 bytes`

**Symptoms:**
```python
ValueError: Single frame data must be <= 7 bytes
  File "src/docan_bus.py", line 27, in create_single_frame
    raise ValueError("Single frame data must be <= 7 bytes")
```

**Causes:**
- DoCAN Single Frames can only contain up to 7 bytes of data
- Single frame format: [PCI byte (1) + Data (≤7)]

**Solutions:**

**Option 1: Reduce data size**
```python
# Wrong
data = b"\x01\x02\x03\x04\x05\x06\x07\x08"  # 8 bytes
frame = handler.create_single_frame(data)  # ❌ ERROR

# Correct
data = b"\x01\x02\x03\x04\x05\x06\x07"  # 7 bytes
frame = handler.create_single_frame(data)  # ✅ OK
```

**Option 2: Use multi-frame for larger data**
```python
# For data > 7 bytes, use First Frame + Consecutive Frames
total_data = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A"
length = len(total_data)

# Send as multi-frame
ff = handler.create_first_frame(total_data[:6], length)  # First 6 bytes
cf = handler.create_consecutive_frame(total_data[6:], 1)  # Rest
```

---

### ❌ Error: `AttributeError: 'bytes' object has no attribute 'encode'`

**Symptoms:**
```python
AttributeError: 'bytes' object has no attribute 'encode'
```

**Causes:**
- Attempting to encode bytes (already bytes)
- String/bytes mismatch

**Solutions:**
```python
# Wrong
data = b"\x3E".encode()  # ❌ bytes don't have encode()

# Correct
data = b"\x3E"  # ✅ Already bytes

# Or if starting with string
data = "\x3E".encode()  # ✅ Convert string to bytes
data = bytes([0x3E])    # ✅ Alternative syntax
```

---

## Test Failures

### ❌ Error: `pytest: command not found`

**Symptoms:**
```
pytest: command not found
```

**Solutions:**
```bash
# Install pytest
pip install -r requirements-dev.txt

# Or install directly
pip install pytest pytest-cov
```

---

### ❌ Error: `FAILED tests/test_virtual_ecu.py::TestVirtualECU::test_XXX`

**Symptoms:** Test fails with assertion error

**Solutions:**

**Step 1: Run with verbose output**
```bash
pytest tests/test_virtual_ecu.py::TestVirtualECU::test_XXX -v
```

**Step 2: Check assertion**
```bash
pytest tests/ -v --tb=long  # Show full traceback
```

**Step 3: Debug with print**
```python
# Add print statements to code
print(f"Value: {result}")
pytest tests/ -v -s  # -s shows print output
```

---

### ❌ Error: `ModuleNotFoundError` in tests

**Symptoms:**
```
ModuleNotFoundError: No module named 'src' (in test file)
```

**Solutions:**
```bash
# Ensure you're in the project root
cd /path/to/uds-docan-virtual-ecu

# Run pytest from root
pytest tests/

# Not from tests directory
cd tests && pytest  # ❌ WRONG
```

---

## Performance Issues

### ❌ Slow test execution

**Symptoms:** Tests take >5 seconds

**Solutions:**
```bash
# Run tests in parallel
pip install pytest-xdist
pytest tests/ -n auto

# Skip slow tests
pytest tests/ -m "not slow"

# Profile tests
pytest tests/ --durations=10  # Show 10 slowest tests
```

---

### ❌ High memory usage

**Symptoms:** Application uses >500 MB RAM

**Solutions:**
```python
# Clear large objects
ecu.dtc_codes.clear()
ecu.data_identifiers.clear()

# Check for memory leaks
import tracemalloc
tracemalloc.start()
# ... run code ...
tracemalloc.print_top(10)
```

---

## Data & State Issues

### ❌ DTC not stored

**Symptoms:** Added DTC doesn't appear in read

**Solutions:**
```python
# Verify DTC was added
ecu.add_dtc(0xC0FF01)
print(ecu.dtc_codes)  # Should contain code

# Check read logic
dtc_request = bytes([0x02, 0x19, 0x01])
response = ecu.process_request(dtc_request)
print(f"DTCs in response: {response.hex()}")
```

---

### ❌ Data identifier returns wrong value

**Symptoms:** Wrong data returned for DID

**Solutions:**
```python
# Verify data was set correctly
ecu.set_data_identifier(0x0102, b"test")
print(ecu.data_identifiers)  # Check stored value

# Verify DID format
did = 0x0102
print(f"DID: 0x{did:04X}")  # Should be 0x0102

# Check response format
request = bytes([0x03, 0x22, 0x01, 0x02])
response = ecu.process_request(request)
print(f"Response: {response.hex()}")
```

---

### ❌ Session not staying active

**Symptoms:** Session closes unexpectedly

**Solutions:**
```python
# Verify session after each request
ecu.uds.session_active = False
request = bytes([0x02, 0x10, 0x03])  # Start session
ecu.process_request(request)
print(ecu.uds.session_active)  # Should be True

# Send Tester Present to keep alive
tp = bytes([0x01, 0x3E])
ecu.process_request(tp)  # Keeps session active
```

---

## Debugging Tips

### 📍 Enable Detailed Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add to your code
logger.debug(f"Processing request: {request.hex()}")
logger.info(f"ECU response: {response.hex()}")
logger.warning(f"Unexpected state: {state}")
logger.error(f"Critical error: {error}")
```

### 🔍 Inspect Objects

```python
from pprint import pprint

# Pretty print ECU state
print("=== ECU State ===")
print(f"ID: {ecu.ecu_id}")
print(f"Running: {ecu.is_running}")
print(f"DTCs: {len(ecu.dtc_codes)} codes")
pprint(ecu.data_identifiers)

# Inspect request/response
request = bytes([0x01, 0x3E])
print(f"Request hex: {request.hex()}")
print(f"Request bytes: {list(request)}")
print(f"Request repr: {repr(request)}")
```

### 🐛 Use Python Debugger

```python
import pdb

# Add breakpoint
pdb.set_trace()

# Or in Python 3.7+
breakpoint()  # Equivalent to pdb.set_trace()

# Debugger commands:
# n - next line
# s - step into function
# c - continue
# p variable - print variable
# l - list code
# h - help
```

### 📊 Profile Code

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
for i in range(100):
    response = ecu.process_request(request)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest functions
```

### 🧪 Test Individual Components

```python
# Test DoCAN independently
from src.docan_bus import DoCAN

handler = DoCAN()
frame = handler.create_single_frame(b"\x3E")
parsed = handler.parse_frame(frame)
assert parsed['data'] == b"\x3E"
print("✓ DoCAN OK")

# Test UDS independently
from src.uds_protocol import UDSProtocol

uds = UDSProtocol()
result = uds.parse_request(bytes([0x3E]))
assert result['service_id'] == 0x3E
print("✓ UDS OK")

# Test Virtual ECU
from src.virtual_ecu import VirtualECU

ecu = VirtualECU()
response = ecu.process_request(bytes([0x01, 0x3E]))
assert response[1] == 0x7E
print("✓ Virtual ECU OK")
```

---

## Still Having Issues?

### 📋 Diagnostic Checklist

- [ ] Python version is 3.8+ (`python --version`)
- [ ] All dependencies installed (`pip list | grep -i pytest`)
- [ ] Running from project root directory
- [ ] Virtual environment activated (if using one)
- [ ] PYTHONPATH set correctly (if needed)
- [ ] File permissions are correct (Linux/macOS)
- [ ] No syntax errors in modified code
- [ ] All tests pass locally (`pytest tests/`)

### 📞 Getting Help

1. **Check existing issues:** [GitHub Issues](https://github.com/Sreedharvadla062/uds-docan-virtual-ecu/issues)

2. **Create new issue with:**
   - Python version (`python --version`)
   - OS and version
   - Complete error message
   - Steps to reproduce
   - Actual vs expected behavior
   - Relevant code snippet

3. **Email support:** sreedharvadla062@gmail.com

---

## Quick Reference

| Issue | Command |
|-------|---------|
| Missing dependencies | `pip install -r requirements.txt` |
| Run tests | `pytest tests/ -v` |
| Check coverage | `pytest tests/ --cov=src` |
| Format code | `black src/ tests/` |
| Lint code | `flake8 src/` |
| Type check | `mypy src/` |
| Install development | `pip install -e ".[dev]"` |

---

**Last Updated:** January 16, 2026  
**Version:** 1.0.0
