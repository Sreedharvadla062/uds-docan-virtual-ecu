"""DoCAN (ISO 15765-2) Bus Implementation"""

import struct

class DoCAN:
    """DoCAN (ISO 15765-2) Protocol Implementation"""
    
    # Frame types
    SINGLE_FRAME = 0x0
    FIRST_FRAME = 0x1
    CONSECUTIVE_FRAME = 0x2
    FLOW_CONTROL_FRAME = 0x3
    
    # DoCAN header format
    DOCAN_HEADER_SIZE = 8  # PCI bytes
    DOCAN_MAX_DATA_LENGTH = 4095  # 12-bit length field
    
    def __init__(self):
        """Initialize DoCAN handler"""
        self.buffer = bytearray()
        self.expected_length = 0
        self.sequence_number = 0
        
    def create_single_frame(self, data: bytes) -> bytes:
        """Create a DoCAN single frame"""
        if len(data) > 7:
            raise ValueError("Single frame data must be <= 7 bytes")
        
        pci = self.SINGLE_FRAME << 4 | len(data)
        return bytes([pci]) + data
    
    def create_first_frame(self, data: bytes, length: int) -> bytes:
        """Create a DoCAN first frame"""
        pci_byte1 = (self.FIRST_FRAME << 4) | ((length >> 8) & 0x0F)
        pci_byte2 = length & 0xFF
        payload = data[:6]
        return bytes([pci_byte1, pci_byte2]) + payload
    
    def create_consecutive_frame(self, data: bytes, seq_num: int) -> bytes:
        """Create a DoCAN consecutive frame"""
        pci = (self.CONSECUTIVE_FRAME << 4) | (seq_num & 0x0F)
        payload = data[:7]
        return bytes([pci]) + payload
    
    def parse_frame(self, frame: bytes) -> dict:
        """Parse a DoCAN frame"""
        if len(frame) < 1:
            return {"error": "Invalid frame"}
        
        pci_byte = frame[0]
        frame_type = (pci_byte >> 4) & 0x0F
        
        if frame_type == self.SINGLE_FRAME:
            length = pci_byte & 0x0F
            data = frame[1:1+length]
            return {"type": "SingleFrame", "length": length, "data": data}
        
        elif frame_type == self.FIRST_FRAME:
            length = ((pci_byte & 0x0F) << 8) | frame[1]
            data = frame[2:8]
            return {"type": "FirstFrame", "length": length, "data": data}
        
        elif frame_type == self.CONSECUTIVE_FRAME:
            seq_num = pci_byte & 0x0F
            data = frame[1:]
            return {"type": "ConsecutiveFrame", "seq_num": seq_num, "data": data}
        
        else:
            return {"error": "Unknown frame type"}
