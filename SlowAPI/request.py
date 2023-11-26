import json

class Request:
    def __init__(self, data=None):
        if data is None:
            return
        message = data.decode()
        lines = message.split("\n")
        request_line = lines[0].split()
        self.method = request_line[0]
        self.path = request_line[1]
        self.protocol = request_line[2]
        self.headers = {}
        self.query_params = {}
        self.body_params = {}

        if "?" in self.path:
            path, query_string = self.path.split("?", 1)
            self.path = path
            self.parse_query_params(query_string)

        for line in lines[1:]:
            if ":" in line:
                name, value = line.split(":", 1)
                self.headers[name.strip()] = value.strip()

        if self.method == "POST":
            content_type = self.headers.get("Content-Type", "")
            if "application/json" in content_type:
                body_start = message.index("\r\n\r\n") + 4
                body = message[body_start:]
                self.parse_json_body(body)

    def parse_query_params(self, query_string):
        pairs = query_string.split("&")
        for pair in pairs:
            key, value = pair.split("=")
            self.query_params[key] = value

    def parse_json_body(self, body):
        try:
            self.body_params = json.loads(body)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON body: {e}")
            self.body_params = {}