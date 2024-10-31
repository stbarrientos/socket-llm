import socket
from local_llm import respond_to_prompt, init_local_llm
from llm_response_streamer import LLMResponseStreamer

def start_server():
    init_local_llm()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))
    server_socket.listen(1)
    print("Server is listening on port 65432")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        chunks = []
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            chunks.append(chunk)
        message = b''.join(chunks).decode()
        print(f"Received message: {message}")

        response = respond_to_prompt(message, client_socket)
        client_socket.sendall(response.encode())

        client_socket.close()

if __name__ == "__main__":
    start_server()
