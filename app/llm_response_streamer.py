class LLMResponseStreamer:

  # Nostream is used to determine if the response should be sent in chunks as they are made available or all at once
  def __init__(self, tokenizer, socket_client, nostream=False):
    self.responses = []
    self.tokenizer = tokenizer
    self.socket_client = socket_client
    self.nostream = nostream
    self.ended = False

  def put(self, response):
    detokenized_response = self.tokenizer.decode(response)
    self.responses.append(detokenized_response)
    if not self.nostream:
      self.socket_client.sendall(detokenized_response.encode())

  def end(self):
    self.ended = True
    if self.nostream:
      self.socket_client.sendall("".join(self.responses).encode())
    self.socket_client.close()