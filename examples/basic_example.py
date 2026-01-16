"""Example: Basic Virtual ECU Usage"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.virtual_ecu import VirtualECU


def main():
    """Demonstrate basic Virtual ECU usage"""
    
    print("=" * 60)
    print("UDS DoCAN Virtual ECU - Basic Example")
    print("=" * 60)
    
    # Create a Virtual ECU instance
    ecu = VirtualECU("DEMO_ECU_001")
    print(f"\n✓ Created Virtual ECU: {ecu.ecu_id}")
    
    # Set some data identifiers
    ecu.set_data_identifier(0x0102, b"v1.2.3")  # Software version
    ecu.set_data_identifier(0x0103, b"ABC123")  # Serial number
    print("✓ Configured data identifiers")
    
    # Add some diagnostic trouble codes
    ecu.add_dtc(0xC0FF01)
    ecu.add_dtc(0xC0FF02)
    print("✓ Added DTC codes for testing")
    
    print("\n" + "=" * 60)
    print("Testing UDS Services")
    print("=" * 60)
    
    # Test 1: Tester Present
    print("\n[1] Tester Present Service (0x3E)")
    request = bytes([0x01, 0x3E])
    response = ecu.process_request(request)
    print(f"    Request:  {request.hex().upper()}")
    print(f"    Response: {response.hex().upper()}")
    
    # Test 2: Diagnostic Session Control
    print("\n[2] Diagnostic Session Control (0x10)")
    request = bytes([0x02, 0x10, 0x03])  # Extended session
    response = ecu.process_request(request)
    print(f"    Request:  {request.hex().upper()}")
    print(f"    Response: {response.hex().upper()}")
    print(f"    Session Active: {ecu.uds.session_active}")
    
    # Test 3: Read Data By Identifier
    print("\n[3] Read Data By Identifier (0x22)")
    request = bytes([0x03, 0x22, 0x01, 0x02])  # Read DID 0x0102
    response = ecu.process_request(request)
    print(f"    Request:  {request.hex().upper()}")
    print(f"    Response: {response.hex().upper()}")
    print(f"    Data: {response[4:].decode('ascii', errors='ignore')}")
    
    # Test 4: Read DTC Information
    print("\n[4] Read DTC Information (0x19)")
    request = bytes([0x02, 0x19, 0x01])  # Read number of DTCs
    response = ecu.process_request(request)
    print(f"    Request:  {request.hex().upper()}")
    print(f"    Response: {response.hex().upper()}")
    num_dtcs = response[3]
    print(f"    DTCs Available: {num_dtcs}")
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"✓ Virtual ECU is operational")
    print(f"✓ Total DTCs: {len(ecu.dtc_codes)}")
    print(f"✓ DIDs configured: {len(ecu.data_identifiers)}")
    print("\nThe Virtual ECU is ready for diagnostics communication!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
