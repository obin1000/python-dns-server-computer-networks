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
        self.TransactionID = request[0:2]
        # 2 Byte flags
        self.flags = request[2:4]
        # 2 Byte
        self.Questions = request[4:6]
        # 2 Byte
        self.AnswerRRs = request[6:8]
        # 2 Bytes
        self.AuthorityRRs = request[8:10]
        # 2 Bytes
        self.AdditionalRRs = request[10:12]
        # Variable bytes for name
        self.QueryName = request[12:-4]
        # 2 Bytes second last
        self.QueryType = request[-4:-2]
        # 2 Bytes from end
        self.QueryClass = request[-2:]

        print(self)

    def __str__(self):
        return '{} {} {}'.format(self.TransactionID, self.flags, self.QueryName)


