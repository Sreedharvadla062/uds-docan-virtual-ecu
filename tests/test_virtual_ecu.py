"""Tests for Virtual ECU implementation"""

import pytest
from src.virtual_ecu import VirtualECU


class TestVirtualECU:
    """Test suite for Virtual ECU"""
    
    @pytest.fixture
    def ecu(self):
        """Create Virtual ECU instance"""
        return VirtualECU("TEST_ECU")
    
    def test_ecu_initialization(self, ecu):
        """Test ECU initialization"""
        assert ecu.ecu_id == "TEST_ECU"
        assert ecu.is_running is True
        assert len(ecu.dtc_codes) == 0
        assert len(ecu.data_identifiers) == 0
    
    def test_set_data_identifier(self, ecu):
        """Test setting data identifier"""
        did = 0x0102
        value = b"\x12\x34\x56\x78"
        ecu.set_data_identifier(did, value)
        
        assert ecu.data_identifiers[did] == value
    
    def test_add_dtc(self, ecu):
        """Test adding DTC code"""
        dtc = 0x123456
        ecu.add_dtc(dtc)
        
        assert dtc in ecu.dtc_codes
        assert len(ecu.dtc_codes) == 1
    
    def test_clear_dtcs(self, ecu):
        """Test clearing DTCs"""
        ecu.add_dtc(0x123456)
        ecu.add_dtc(0x234567)
        
        assert len(ecu.dtc_codes) == 2
        
        ecu.clear_dtcs()
        assert len(ecu.dtc_codes) == 0
    
    def test_tester_present_response(self, ecu):
        """Test Tester Present service response"""
        # Create single frame with Tester Present (0x3E)
        request = bytes([0x01, 0x3E])
        response = ecu.process_request(request)
        
        assert response[0] == 0x01  # Single frame, length 1
        assert response[1] == 0x7E  # Positive response (0x3E + 0x40)
    
    def test_diagnostic_session_control_response(self, ecu):
        """Test Diagnostic Session Control response"""
        # Extended session
        request = bytes([0x02, 0x10, 0x03])
        response = ecu.process_request(request)
        
        assert response[1] == 0x50  # Positive response
        assert ecu.uds.session_active is True
    
    def test_read_data_identifier_response(self, ecu):
        """Test Read Data By Identifier response"""
        did = 0x0102
        value = b"\x12\x34\x56\x78"
        ecu.set_data_identifier(did, value)
        
        # Read DID request
        request = bytes([0x03, 0x22, 0x01, 0x02])
        response = ecu.process_request(request)
        
        assert response[1] == 0x62  # Positive response
        assert response[2:4] == bytes([0x01, 0x02])  # DID
    
    def test_read_dtc_response(self, ecu):
        """Test Read DTC Information response"""
        ecu.add_dtc(0x123456)
        ecu.add_dtc(0x234567)
        
        # Read number of DTCs
        request = bytes([0x02, 0x19, 0x01])
        response = ecu.process_request(request)
        
        assert response[1] == 0x59  # Positive response
        # Response format: [SF_header, SID+0x40, sub_func, status, count_high, count_low]
        assert response[4] == 0x02  # Number of DTCs (at index 4 for SF format)
    
    def test_unsupported_service(self, ecu):
        """Test unsupported service response"""
        # Invalid service
        request = bytes([0x01, 0xFF])
        response = ecu.process_request(request)
        
        assert response[1] == 0x7F  # Negative response
        assert response[3] == 0x12  # Service not supported NRC
