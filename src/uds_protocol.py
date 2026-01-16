"""UDS (ISO 14229) Protocol Implementation"""

class UDSProtocol:
    """UDS Protocol handler for diagnostics communication"""
    
    # UDS Services (SID)
    DIAGNOSTIC_SESSION_CONTROL = 0x10
    ECU_RESET = 0x11
    SECURITY_ACCESS = 0x27
    COMMUNICATION_CONTROL = 0x28
    READ_DATA_BY_IDENTIFIER = 0x22
    WRITE_DATA_BY_IDENTIFIER = 0x2E
    ROUTINE_CONTROL = 0x31
    REQUEST_DOWNLOAD = 0x34
    REQUEST_UPLOAD = 0x35
    TRANSFER_DATA = 0x36
    REQUEST_TRANSFER_EXIT = 0x37
    TESTER_PRESENT = 0x3E
    READ_DTC_INFORMATION = 0x19
    CLEAR_DIAGNOSTIC_INFORMATION = 0x14
    
    def __init__(self):
        """Initialize UDS Protocol handler"""
        self.session_active = False
        self.security_unlocked = False
        
    def parse_request(self, data: bytes) -> dict:
        """Parse UDS request"""
        if len(data) < 1:
            return {"error": "Invalid request"}
        
        sid = data[0]
        payload = data[1:]
        
        return {
            "service_id": sid,
            "payload": payload,
            "service_name": self._get_service_name(sid)
        }
    
    def _get_service_name(self, sid: int) -> str:
        """Get service name from SID"""
        services = {
            0x10: "DiagnosticSessionControl",
            0x11: "ECUReset",
            0x27: "SecurityAccess",
            0x22: "ReadDataByIdentifier",
            0x2E: "WriteDataByIdentifier",
            0x3E: "TesterPresent",
        }
        return services.get(sid, "Unknown")
