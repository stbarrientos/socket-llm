import socket
from local_llm import LocalLLM
from llm_response_streamer import LLMResponseStreamer

MESSAGE_TERMINATOR = "__close__"

def start_server():
  local_llm = LocalLLM()
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind(('0.0.0.0', 65432))
  server_socket.listen(1)
  print("Server is listening on port 65432")

  while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    chunks = []
    while True:
      chunk = client_socket.recv(1024).decode()
      # If the current chunk contains the message terminator, remove the terminator,
      # store the chunk, and break the loop
      if chunk.endswith(MESSAGE_TERMINATOR):
        chunks.append(chunk[:-(len(MESSAGE_TERMINATOR))] )
        break

      # Store the chunk
      chunks.append(chunk)
      print(f"Received chunk: {chunk}")
    # Combine the chunks into the full message
    message = ''.join(chunks)
    print(f"Received message: {message}")

    streamer = LLMResponseStreamer(client_socket, stream_responses = True)
    local_llm.respond_to_prompt(message, streamer)
    client_socket.close()

if __name__ == "__main__":
  start_server()
