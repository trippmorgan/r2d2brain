def build_packet(cmd_bytes, seq=0x00):
    SOP = 0x8D
    EOP = 0xD8
    body = bytes(cmd_bytes) + bytes([seq])
    checksum = (~sum(body)) & 0xFF
    return bytes([SOP]) + body + bytes([checksum]) + bytes([EOP])
