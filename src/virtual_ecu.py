"""Virtual ECU Implementation"""

from uds_protocol import UDSProtocol
from docan_bus import DoCAN

class VirtualECU:
    """Virtual ECU with UDS and DoCAN support"""
    
    def __init__(self, ecu_id: str = "ECU_001"):
        """Initialize Virtual ECU"""
        self.ecu_id = ecu_id
        self.uds = UDSProtocol()
        self.docan = DoCAN()
        self.dtc_codes = []
        self.data_identifiers = {}
        self.is_running = True
        
    def process_request(self, request_data: bytes) -> bytes:
        """Process incoming request and generate response"""
        # Parse DoCAN frame
        docan_frame = self.docan.parse_frame(request_data)
        if "error" in docan_frame:
            return self._create_error_response(0x12)  # NRC: Service not supported
        
        # Extract UDS data from DoCAN frame
        if docan_frame["type"] == "SingleFrame":
            uds_data = docan_frame["data"]
        else:
            # Handle multi-frame (simplified)
            return self._create_error_response(0x31)  # NRC: Request out of range
        
        # Parse UDS request
        uds_request = self.uds.parse_request(uds_data)
        if "error" in uds_request:
            return self._create_error_response(0x12)
        
        # Handle UDS service
        service_id = uds_request["service_id"]
        response = self._handle_uds_service(service_id, uds_request["payload"])
        
        # Wrap response in DoCAN single frame
        docan_response = self.docan.create_single_frame(response)
        return docan_response
    
    def _handle_uds_service(self, service_id: int, payload: bytes) -> bytes:
        """Handle UDS service request"""
        
        if service_id == 0x3E:  # Tester Present
            return bytes([service_id + 0x40])  # Positive response
        
        elif service_id == 0x10:  # Diagnostic Session Control
            session_type = payload[0] if payload else 0
            self.uds.session_active = True
            return bytes([service_id + 0x40, session_type])
        
        elif service_id == 0x22:  # Read Data By Identifier
            return self._handle_read_data_identifier(payload)
        
        elif service_id == 0x19:  # Read DTC Information
            return self._handle_read_dtc(payload)
        
        else:
            return self._create_error_response(0x12)  # Service not supported
    
    def _handle_read_data_identifier(self, payload: bytes) -> bytes:
        """Handle Read Data By Identifier request"""
        if len(payload) < 2:
            return self._create_error_response(0x13)  # Incorrect length
        
        did = int.from_bytes(payload[:2], "big")
        response_data = self.data_identifiers.get(did, b"\x00")
        
        return bytes([0x62]) + payload[:2] + response_data
    
    def _handle_read_dtc(self, payload: bytes) -> bytes:
        """Handle Read DTC Information request"""
        subfunction = payload[0] if payload else 0
        
        if subfunction == 0x01:  # Read number of DTCs
            num_dtcs = len(self.dtc_codes)
            return bytes([0x59, 0x01, 0x00, num_dtcs, 0x00])
        
        elif subfunction == 0x02:  # Read all DTCs
            response = bytes([0x59, 0x02])
            for dtc in self.dtc_codes:
                response += dtc.to_bytes(3, "big") + b"\x00"
            return response
        
        return self._create_error_response(0x12)
    
    def _create_error_response(self, nrc: int) -> bytes:
        """Create negative response"""
        return bytes([0x7F, 0x00, nrc])
    
    def set_data_identifier(self, did: int, value: bytes):
        """Set a data identifier value"""
        self.data_identifiers[did] = value
    
    def add_dtc(self, dtc_code: int):
        """Add a DTC code"""
        self.dtc_codes.append(dtc_code)
    
    def clear_dtcs(self):
        """Clear all DTCs"""
        self.dtc_codes.clear()
