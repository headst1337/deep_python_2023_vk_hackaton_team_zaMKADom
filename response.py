class Response:
    ...
    def __init__(self, data, writer) -> None:
        response_text = f"HTTP/1.1 {200}\r\n\r\n<html>{data}</html"
        writer.write(response_text.encode())
        writer.close()
        
        
