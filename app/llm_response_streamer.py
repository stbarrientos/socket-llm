# Inspired by https://huggingface.co/docs/transformers/v4.46.2/en/internal/generation_utils#transformers.TextStreamer
# Details: https://github.com/huggingface/transformers/blob/v4.46.2/src/transformers/generation/streamers.py#L82
class LLMResponseStreamer:
  def __init__(self, socket_client, stream_responses=True):
    self.responses = []
    self.socket_client = socket_client
    self.stream_responses = stream_responses
    self.token_cache = []
    self.print_len = 0
    self.ended = False


  def set_tokenizer(self, tokenizer):
    self.tokenizer = tokenizer

  def put(self, value):
    if len(value.shape) > 1:
      value = value[0]

    self.token_cache.extend(value.tolist()) 

    text = self.tokenizer.decode(self.token_cache)

    # Get either the last complete sentence or the last word
    if text.endswith("\n"):
      self.responses.append(text)
      sendable_text = text[self.print_len :]
      self.token_cache = []
      self.print_len = 0
    else:
      sendable_text = text[self.print_len : text.rfind(" ") + 1]
      self.print_len += len(text)

    # Send response to client if streaming is enabled
    if self.stream_responses:
      print("Sending response to client", sendable_text)
      self.socket_client.sendall(sendable_text.encode())
    self.responses.append(sendable_text)

  def end(self):
    # Flush anything left in the cache
    if len(self.token_cache) > 0:
      text = self.tokenizer.decode(self.token_cache)
      sendable_text = text[self.print_len :]
      self.response.append(sendable_text)

    # Reset state
    self.ended = True
    self.token_cache = []
    self.print_len = 0

    # Send final response unless we've been streaming responses
    if not self.stream_responses:
      self.socket_client.sendall("".join(self.responses).encode())
    self.socket_client.close()
