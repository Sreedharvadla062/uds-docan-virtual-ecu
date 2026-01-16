"""Tests for UDS Protocol implementation"""

import pytest
from src.uds_protocol import UDSProtocol


class TestUDSProtocol:
    """Test suite for UDS Protocol"""
    
    @pytest.fixture
    def uds(self):
        """Create UDS Protocol instance"""
        return UDSProtocol()
    
    def test_uds_initialization(self, uds):
        """Test UDS initialization"""
        assert uds.session_active is False
        assert uds.security_unlocked is False
    
    def test_parse_tester_present_request(self, uds):
        """Test parsing Tester Present request"""
        request = bytes([0x3E])
        result = uds.parse_request(request)
        
        assert result["service_id"] == 0x3E
        assert result["service_name"] == "TesterPresent"
        assert result["payload"] == b""
    
    def test_parse_diagnostic_session_control(self, uds):
        """Test parsing Diagnostic Session Control request"""
        request = bytes([0x10, 0x01])  # Extended session
        result = uds.parse_request(request)
        
        assert result["service_id"] == 0x10
        assert result["service_name"] == "DiagnosticSessionControl"
        assert result["payload"] == bytes([0x01])
    
    def test_parse_read_data_by_identifier(self, uds):
        """Test parsing Read Data By Identifier request"""
        request = bytes([0x22, 0x01, 0x02])  # DID 0x0102
        result = uds.parse_request(request)
        
        assert result["service_id"] == 0x22
        assert result["service_name"] == "ReadDataByIdentifier"
        assert result["payload"] == bytes([0x01, 0x02])
    
    def test_parse_invalid_request(self, uds):
        """Test parsing invalid request"""
        request = b""
        result = uds.parse_request(request)
        
        assert "error" in result
    
    def test_get_service_name_unknown(self, uds):
        """Test getting unknown service name"""
        name = uds._get_service_name(0xFF)
        assert name == "Unknown"
    
    def test_service_code_constants(self, uds):
        """Test UDS service code constants"""
        assert uds.TESTER_PRESENT == 0x3E
        assert uds.DIAGNOSTIC_SESSION_CONTROL == 0x10
        assert uds.READ_DATA_BY_IDENTIFIER == 0x22
        assert uds.READ_DTC_INFORMATION == 0x19
