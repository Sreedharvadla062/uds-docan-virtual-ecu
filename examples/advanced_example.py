"""Example: Advanced Virtual ECU with Multi-Client Support"""

import sys
from pathlib import Path
import time

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.virtual_ecu import VirtualECU


class DiagnosticClient:
    """Simulated diagnostic client"""
    
    def __init__(self, name: str):
        self.name = name
    
    def send_request(self, ecu: VirtualECU, request: bytes) -> bytes:
        """Send request to ECU"""
        return ecu.process_request(request)
    
    def test_session(self, ecu: VirtualECU):
        """Test diagnostic session"""
        print(f"\n[{self.name}] Starting diagnostic session...")
        
        # Enter extended diagnostic session
        session_request = bytes([0x02, 0x10, 0x03])
        response = self.send_request(ecu, session_request)
        print(f"    → Entered Extended Session: {response.hex().upper()}")
        
        # Keep session alive with Tester Present
        for i in range(3):
            time.sleep(0.1)
            tp_request = bytes([0x01, 0x3E])
            response = self.send_request(ecu, tp_request)
            print(f"    → Tester Present #{i+1}: {response.hex().upper()}")
    
    def read_vehicle_data(self, ecu: VirtualECU):
        """Read vehicle data"""
        print(f"\n[{self.name}] Reading vehicle data...")
        
        dids_to_read = [
            (0x0102, "Software Version"),
            (0x0103, "Serial Number"),
        ]
        
        for did, name in dids_to_read:
            request = bytes([0x03, 0x22, (did >> 8) & 0xFF, did & 0xFF])
            response = self.send_request(ecu, request)
            data = response[4:] if len(response) > 4 else b""
            print(f"    → {name} (0x{did:04X}): {data.hex().upper()}")
    
    def read_dtcs(self, ecu: VirtualECU):
        """Read diagnostic trouble codes"""
        print(f"\n[{self.name}] Reading DTCs...")
        
        request = bytes([0x02, 0x19, 0x01])
        response = self.send_request(ecu, request)
        num_dtcs = response[3] if len(response) > 3 else 0
        print(f"    → Total DTCs: {num_dtcs}")
        
        if num_dtcs > 0:
            request = bytes([0x02, 0x19, 0x02])
            response = self.send_request(ecu, request)
            print(f"    → DTC Data: {response.hex().upper()}")


def main():
    """Advanced example with multiple clients"""
    
    print("\n" + "=" * 70)
    print("Advanced Virtual ECU - Multi-Client Diagnostic Session")
    print("=" * 70)
    
    # Create ECU
    ecu = VirtualECU("VEHICLE_ECU_2024")
    print(f"\n✓ Created Virtual ECU: {ecu.ecu_id}")
    
    # Configure vehicle data
    ecu.set_data_identifier(0x0102, b"SW_v2.5.1")
    ecu.set_data_identifier(0x0103, b"VIN123456")
    print("✓ Loaded vehicle configuration")
    
    # Add DTCs
    ecu.add_dtc(0xC0FF01)
    print("✓ Added diagnostic codes")
    
    # Create diagnostic clients
    clients = [
        DiagnosticClient("Scanner_1"),
        DiagnosticClient("Programmer"),
    ]
    
    # Run diagnostics
    for client in clients:
        client.test_session(ecu)
        client.read_vehicle_data(ecu)
        client.read_dtcs(ecu)
    
    print("\n" + "=" * 70)
    print("Diagnostic session completed successfully!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
