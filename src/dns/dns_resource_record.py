class DNSResourceRecord:
    def __init__(self):
        self.name = None
        self.ttl = None
        self.record_class = None
        self.record_type = None
        self.record_data = None


class DNSHeader:

    def __init__(self, request):
        # 2 Byte identifier for this message
        self.ID = request[0:2]
        self.flags = request[2:4]
