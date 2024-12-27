# Inspired by https://huggingface.co/docs/transformers/v4.46.2/en/internal/generation_utils#transformers.TextStreamer
# Details: https://github.com/huggingface/transformers/blob/v4.46.2/src/transformers/generation/streamers.py#L82
class LLMResponseStreamer:
  def __init__(self, socket_client=None, message_terminator=None, stream_responses=True, skip_prompt=True):
    self.responses = []
    self.socket_client = socket_client
    self.message_terminator = message_terminator
    self.stream_responses = stream_responses
    self.token_cache = []
    self.print_len = 0
    self.ended = False
    self.skip_prompt = skip_prompt
    self.next_tokens_are_prompt = True

  def set_tokenizer(self, tokenizer):
    self.tokenizer = tokenizer

  def put(self, value):
    text = self.digest_tokens(value)
    sendable_text = None

    if self.skip_prompt and self.next_tokens_are_prompt:
      self.next_tokens_are_prompt = False
      return

    print("Decoded text", text)
    # Get either the last complete sentence or the last word
    if text.endswith("\n"):
      print("Ends in newline")
      self.responses.append(text)
      sendable_text = text[self.print_len :]
      self.token_cache = []
    else:
      sendable_text = text[self.print_len : text.rfind(" ") + 1]

    self.print_len += len(sendable_text)
    self.responses.append(sendable_text)

    # Send response to client if streaming is enabled
    print ("Sendable text", sendable_text)
    if self.stream_responses and sendable_text != None:
      print("Sending response to client", sendable_text)
      self.socket_client.sendall(sendable_text.encode())
  
  def digest_tokens(self, tokens):
    if len(tokens.shape) > 1:
      tokens = tokens[0]

    self.token_cache.extend(tokens.tolist()) 

    return self.tokenizer.decode(self.token_cache)


  def end(self):
    # Flush anything left in the cache
    if len(self.token_cache) > 0:
      text = self.tokenizer.decode(self.token_cache)
      sendable_text = text[self.print_len :]
      if self.stream_responses:
        self.socket_client.sendall(sendable_text.encode())
      self.responses.append(sendable_text)

    # Add message terminator
    self.reponses.append(self.message_terminator)


    # Send final response unless we've been streaming responses
    if self.stream_responses:
      self.socket_client.sendall(self.message_terminator.encode())
    else:
      self.socket_client.sendall("".join(self.responses).encode())
    self.socket_client.close()

    # Reset state
    self.ended = True
    self.token_cache = []
    self.print_len = 0
    self.responses = []
    self.next_tokens_are_prompt = True
