class Request:

    def __init__(self, data=None):
        if data is None:
            return
        message = data.decode()
        lines = message.split('\n')
        request_line = lines[0].split()
        self.method = request_line[0]
        self.path = request_line[1]
        self.protocol = request_line[2]
        self.headers = {}
        for line in lines[1:]:
            if ':' in line:
                name, value = line.split(':', 1)
                self.headers[name.strip()] = value.strip()
