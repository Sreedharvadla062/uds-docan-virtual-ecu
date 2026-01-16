"""Tests for DoCAN Bus implementation"""

import pytest
from src.docan_bus import DoCAN


class TestDoCAN:
    """Test suite for DoCAN Bus"""
    
    @pytest.fixture
    def docan(self):
        """Create DoCAN instance"""
        return DoCAN()
    
    def test_docan_initialization(self, docan):
        """Test DoCAN initialization"""
        assert docan.buffer == bytearray()
        assert docan.expected_length == 0
        assert docan.sequence_number == 0
    
    def test_create_single_frame_short(self, docan):
        """Test creating single frame with short data"""
        data = b"\x3E"  # Tester Present
        frame = docan.create_single_frame(data)
        
        assert frame[0] == 0x01  # Frame type 0, length 1
        assert frame[1:] == data
    
    def test_create_single_frame_max_length(self, docan):
        """Test creating single frame with max length"""
        data = b"\x01\x02\x03\x04\x05\x06\x07"
        frame = docan.create_single_frame(data)
        
        assert frame[0] == 0x07  # Frame type 0, length 7
        assert frame[1:] == data
    
    def test_create_single_frame_exceeds_length(self, docan):
        """Test single frame with data exceeding max length"""
        data = b"\x01\x02\x03\x04\x05\x06\x07\x08"
        
        with pytest.raises(ValueError):
            docan.create_single_frame(data)
    
    def test_create_first_frame(self, docan):
        """Test creating first frame"""
        data = b"\x01\x02\x03\x04\x05\x06"
        total_length = 20
        frame = docan.create_first_frame(data, total_length)
        
        assert frame[0] & 0xF0 == 0x10  # Frame type 1
        assert frame[1:8] == bytes([0x14]) + data
    
    def test_create_consecutive_frame(self, docan):
        """Test creating consecutive frame"""
        data = b"\x07\x08\x09\x0A\x0B\x0C\x0D"
        seq_num = 1
        frame = docan.create_consecutive_frame(data, seq_num)
        
        assert frame[0] & 0xF0 == 0x20  # Frame type 2
        assert frame[0] & 0x0F == seq_num
        assert frame[1:] == data
    
    def test_parse_single_frame(self, docan):
        """Test parsing single frame"""
        frame = bytes([0x01, 0x3E])
        result = docan.parse_frame(frame)
        
        assert result["type"] == "SingleFrame"
        assert result["length"] == 1
        assert result["data"] == b"\x3E"
    
    def test_parse_first_frame(self, docan):
        """Test parsing first frame"""
        frame = bytes([0x10, 0x14, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06])
        result = docan.parse_frame(frame)
        
        assert result["type"] == "FirstFrame"
        assert result["length"] == 20
        assert result["data"] == b"\x01\x02\x03\x04\x05\x06"
    
    def test_parse_consecutive_frame(self, docan):
        """Test parsing consecutive frame"""
        frame = bytes([0x21, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D])
        result = docan.parse_frame(frame)
        
        assert result["type"] == "ConsecutiveFrame"
        assert result["seq_num"] == 1
        assert result["data"] == b"\x07\x08\x09\x0A\x0B\x0C\x0D"
    
    def test_parse_invalid_frame(self, docan):
        """Test parsing invalid frame"""
        frame = b""
        result = docan.parse_frame(frame)
        
        assert "error" in result
    
    def test_frame_type_constants(self, docan):
        """Test frame type constants"""
        assert docan.SINGLE_FRAME == 0x0
        assert docan.FIRST_FRAME == 0x1
        assert docan.CONSECUTIVE_FRAME == 0x2
        assert docan.FLOW_CONTROL_FRAME == 0x3
