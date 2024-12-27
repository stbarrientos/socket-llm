# Import necessary modules
from transformers import AutoTokenizer, AutoModelForCausalLM

class LocalLLM:
  def __init__(self):
    # Load the pre-trained tokenizer and model
    print("Loading tokenizer")
    self.tokenizer = AutoTokenizer.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
    print("Loaded tokenizer")
    print("Loading model")
    self.model = AutoModelForCausalLM.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
    print("Loaded model")

  def respond_to_prompt(self, prompt, streamer):
    # Encode the input text
    input_ids = self.tokenizer([prompt], return_tensors='pt').input_ids

    streamer.set_tokenizer(self.tokenizer)

    kwargs = {
      "streamer": streamer,
      "max_length": 100,
      "pad_token_id": self.tokenizer.eos_token_id,
      "eos_token_id": self.tokenizer.eos_token_id
    }

    # Generate text
    self.model.generate(input_ids, **kwargs)
