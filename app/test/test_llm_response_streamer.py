import unittest
from unittest.mock import Mock
from llm_response_streamer import LLMResponseStreamer

class TestLLMResponseStreamer(unittest.TestCase):

  def setUp(self):
    self.mock_socket_client = Mock()
    self.mock_tokenizer = Mock()
    self.streamer = LLMResponseStreamer(self.mock_socket_client, stream_responses=True)
    self.streamer.set_tokenizer(self.mock_tokenizer)

  def test_put_stream_responses(self):
    self.mock_tokenizer.decode.return_value = "decoded_response"
    self.streamer.put("response")
    self.mock_tokenizer.decode.assert_called_once_with("response")
    self.mock_socket_client.sendall.assert_called_once_with(b"decoded_response")
    self.assertEqual(self.streamer.responses, ["decoded_response"])

  def test_put_no_stream_responses(self):
    self.streamer.stream_responses = False
    self.mock_tokenizer.decode.return_value = "decoded_response"
    self.streamer.put("response")
    self.mock_tokenizer.decode.assert_called_once_with("response")
    self.mock_socket_client.sendall.assert_not_called()
    self.assertEqual(self.streamer.responses, ["decoded_response"])

  def test_end_stream_responses(self):
    self.streamer.responses = ["response1", "response2"]
    self.streamer.end()
    self.mock_socket_client.sendall.assert_not_called()
    self.mock_socket_client.close.assert_called_once()
    self.assertTrue(self.streamer.ended)

  def test_end_no_stream_responses(self):
    self.streamer.stream_responses = False
    self.streamer.responses = ["response1", "response2"]
    self.streamer.end()
    self.mock_socket_client.sendall.assert_called_once_with(b"response1response2")
    self.mock_socket_client.close.assert_called_once()
    self.assertTrue(self.streamer.ended)

if __name__ == '__main__':
  unittest.main()